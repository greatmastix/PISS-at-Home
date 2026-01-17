from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DEFAULT_OPTIONS,
    ISS_FRESH_WATER_TANK_ITEM,
    ISS_TANK_FIELDS,
    ISS_URINE_TANK_ITEM,
    ISS_WASTE_WATER_TANK_ITEM,
    LS_ADAPTER_SET,
    LS_SERVER,
    OPTION_INCLUDE_FRESH_WATER_TANK,
    OPTION_INCLUDE_URINE_TANK,
    OPTION_INCLUDE_WASTE_WATER_TANK,
)

_LOGGER = logging.getLogger(__name__)

# Lightstreamer Python Client SDK (installed via manifest "requirements")
from lightstreamer.client import LightstreamerClient, Subscription  # type: ignore


@dataclass(frozen=True)
class TankDefinition:
    name: str
    unique_id: str
    item: str
    icon: str


TANK_DEFINITIONS = {
    OPTION_INCLUDE_URINE_TANK: TankDefinition(
        name="ISS Urine Tank",
        unique_id="piss_at_home_iss_urine_tank_node3000005",
        item=ISS_URINE_TANK_ITEM,
        icon="mdi:toilet",
    ),
    OPTION_INCLUDE_WASTE_WATER_TANK: TankDefinition(
        name="ISS Waste Water Tank",
        unique_id="piss_at_home_iss_waste_water_tank_node3000006",
        item=ISS_WASTE_WATER_TANK_ITEM,
        icon="mdi:water-alert",
    ),
    OPTION_INCLUDE_FRESH_WATER_TANK: TankDefinition(
        name="ISS Fresh Water Tank",
        unique_id="piss_at_home_iss_fresh_water_tank_node3000007",
        item=ISS_FRESH_WATER_TANK_ITEM,
        icon="mdi:water",
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities for the config entry."""
    options = {**DEFAULT_OPTIONS, **entry.options}
    sensors = [
        PissatHomeTankSensor(hass, definition)
        for option_key, definition in TANK_DEFINITIONS.items()
        if options.get(option_key, False)
    ]
    if sensors:
        async_add_entities(sensors)


class PissatHomeTankSensor(SensorEntity):
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_should_poll = False  # push updates

    def __init__(self, hass: HomeAssistant, definition: TankDefinition) -> None:
        self.hass = hass
        self._definition = definition
        self._attr_name = definition.name
        self._attr_unique_id = definition.unique_id
        self._attr_icon = definition.icon
        self._attr_native_value: Optional[float] = None
        self._task: Optional[asyncio.Task] = None
        self._client: Optional[LightstreamerClient] = None
        self._connected: bool = False

    @property
    def extra_state_attributes(self):
        return {
            "source": "ISS telemetry via Lightstreamer",
            "item": self._definition.item,
            "connected": self._connected,
        }

    async def async_added_to_hass(self) -> None:
        self._task = self.hass.async_create_task(self._run_lightstreamer())

    async def async_will_remove_from_hass(self) -> None:
        if self._task:
            self._task.cancel()
            self._task = None
        await self._disconnect()

    async def _disconnect(self) -> None:
        client = self._client
        self._client = None
        if client is None:
            return
        try:
            await asyncio.to_thread(client.disconnect)
        except Exception as err:
            _LOGGER.debug("Disconnect error: %s", err)

    async def _run_lightstreamer(self) -> None:
        """Connect, subscribe, and keep receiving updates with a reconnect loop."""
        while True:
            try:
                await self._connect_and_subscribe()
            except asyncio.CancelledError:
                raise
            except Exception as err:
                self._connected = False
                self.async_write_ha_state()
                _LOGGER.warning("ISS stream error, retrying: %s", err)

            # backoff before reconnect
            await asyncio.sleep(10)

    async def _connect_and_subscribe(self) -> None:
        client = LightstreamerClient(LS_SERVER, LS_ADAPTER_SET)
        self._client = client

        sub = Subscription("MERGE", [self._definition.item], ISS_TANK_FIELDS)

        def on_update(item_update):
            try:
                raw = item_update.getValue("Value")
                if raw is None:
                    return
                val = float(raw)
            except Exception:
                return

            def _set():
                self._connected = True
                self._attr_native_value = val
                self.async_write_ha_state()

            self.hass.loop.call_soon_threadsafe(_set)

        def on_subscription():
            self.hass.loop.call_soon_threadsafe(self._set_connected, True)

        def on_unsubscription():
            self.hass.loop.call_soon_threadsafe(self._set_connected, False)

        listener = type(
            "Listener",
            (),
            {
                "onItemUpdate": staticmethod(on_update),
                "onSubscription": staticmethod(on_subscription),
                "onUnsubscription": staticmethod(on_unsubscription),
            },
        )()
        sub.addListener(listener)

        await asyncio.to_thread(client.connect)
        await asyncio.to_thread(client.subscribe, sub)

        self._set_connected(True)

        # Keep task alive; the SDK drives updates in background threads.
        while True:
            await asyncio.sleep(60)

    def _set_connected(self, connected: bool) -> None:
        self._connected = connected
        self.async_write_ha_state()
