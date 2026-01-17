DOMAIN = "piss_at_home"

# Public Lightstreamer endpoint used for ISS telemetry (as surfaced by ISS Mimic).
LS_SERVER = "https://push.lightstreamer.com"
LS_ADAPTER_SET = "ISSLIVE"

# ISS Node 3 telemetry item for "Urine Tank [%]"
ISS_URINE_TANK_ITEM = "NODE3000005"
ISS_WASTE_WATER_TANK_ITEM = "NODE3000006"
ISS_FRESH_WATER_TANK_ITEM = "NODE3000007"
ISS_TANK_FIELDS = ["Value"]

OPTION_INCLUDE_URINE_TANK = "include_urine_tank"
OPTION_INCLUDE_WASTE_WATER_TANK = "include_waste_water_tank"
OPTION_INCLUDE_FRESH_WATER_TANK = "include_fresh_water_tank"

DEFAULT_OPTIONS = {
    OPTION_INCLUDE_URINE_TANK: True,
    OPTION_INCLUDE_WASTE_WATER_TANK: False,
    OPTION_INCLUDE_FRESH_WATER_TANK: False,
}
