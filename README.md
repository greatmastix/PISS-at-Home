# PISS@Home 🚽🛰️

> **Yes, this project is AI-generated.**  
> **No, I am not taking feature requests, complaints, or philosophy debates about that.**

PISS@Home is a Home Assistant integration that exposes the **ISS Urine Tank fill level (%)** using publicly available ISS telemetry (via Lightstreamer).

It does exactly one dumb, beautiful thing:
👉 tells you how full the International Space Station’s piss tank is.

---

## ⚠️ IMPORTANT DISCLAIMER (READ THIS FIRST)

This project was **generated with the help of AI**.

That means:
- I didn’t hand-craft every line like a Victorian watchmaker
- I’m not emotionally invested in edge cases
- I’m not interested in arguments about “AI code quality”
- I am **especially** not interested in being @’d, pinged, tagged, or summoned about it

If you don’t like AI-generated projects:
- Close the tab
- Touch grass
- Write your own piss telemetry integration

If it works for you: great.  
If it doesn’t: forks are free.

---

## Features

- 🚀 Real-time ISS telemetry
- 🚽 Urine tank fill level (0–100%)
- 🧠 Zero configuration (Config Flow)
- 📦 HACS compatible
- 📉 Absolutely no opinions about your YAML style

---

## Installation (HACS)

1. Put this repo on GitHub
2. In Home Assistant:
   - **HACS → Integrations → ⋮ → Custom repositories**
   - Add the repo as **Integration**
3. Install **PISS@Home**
4. Restart Home Assistant
5. Go to **Settings → Devices & Services → Add Integration**
6. Search for **PISS@Home**
7. Enjoy knowing things you didn’t need to know

---

## Entities

- `sensor.iss_urine_tank`  
  → Percentage full of the ISS urine tank

Yes, it’s real.  
Yes, NASA publishes this.  
No, I didn’t make that decision.

---

## Support / Issues / Complaints

- Bugs: open an issue (preferably with logs)
- Feature requests: maybe
- Complaints about AI: **don’t**
- “Why did you make this?”: because it’s funny

---

## License

MIT.  
Do whatever you want.  
Just don’t @ me about how it was made.
