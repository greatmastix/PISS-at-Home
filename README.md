# PISS@Home (Home Assistant integration)

A Home Assistant custom integration that exposes the ISS **Urine Tank [%]** as a sensor using public ISS telemetry (Lightstreamer).

## Install (HACS)

1. Put this repo on GitHub.
2. In Home Assistant: **HACS → Integrations → ⋮ → Custom repositories**
   - Repository: your GitHub URL
   - Category: **Integration**
3. Install **PISS@Home** from HACS and restart Home Assistant.
4. Add it via **Settings → Devices & Services → Add Integration → PISS@Home**.

## Entity

- `sensor.iss_urine_tank` — percentage full (0–100)

## Notes

- Domain (folder name): `piss_at_home`
- UI setup: yes (Config Flow; no YAML needed)
