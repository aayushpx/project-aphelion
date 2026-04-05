## Mission Control Suite  `/mission-control`

| Module | Status | Description |
|---|---|---|
| `propagator/` | In Progress | 3DOF RK4 trajectory propagator with drag and gravity models |
| `state-estimator/` | Planned | Extended Kalman Filter for 6-DOF state estimation |
| `monte-carlo/` | Planned | Dispersion analysis — 1000+ runs, landing footprint scatter plots |
| `ground-station/` | Planned | Flask dashboard, MQTT telemetry receiver, real-time visualisation |

## Flight Computer Firmware  `/firmware`

**Active development:** `firmware/flight-computer/`
- Custom MPU6050 driver (ESP-IDF v5.2 Master Bus API, I2C at 400kHz)
- I2C integrity validation via WHO_AM_I handshake (`0x68` signature)
- Voltage divider ($1k\Omega / 2.2k\Omega$) for 5V→3.3V HC-SR04 logic level protection
- StateMachine: `IDLE → PRE_FLIGHT → ACTIVE → DESCENT → LANDED`

**Archived experiments:** `firmware/archive/` — early drivers and learning exercises

## Tech Stack

**Flight Computer:** Embedded C++ · ESP-IDF v5.2 · FreeRTOS · ESP32-WROOM  
**Mission Control:** Python · NumPy/SciPy · Matplotlib · Paho MQTT · Flask  
**Hardware:** ESP32-WROOM · MPU6050 · BMP280 · HC-SR04 · Raspberry Pi 5

## Dev Logs

Session notes in `/docs/dev-logs/` — tracking progress, debugging decisions, 
and physics derivations as the project grows.

---
