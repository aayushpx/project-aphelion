# Hardware

This document describes the hardware interfaces and integration targets for Project Aphelion.

## Supported Hardware

### ESP32-WROOM-32D (Flight Computer)

The primary embedded platform for the flight computer subsystem.

- **MCU:** Xtensa LX6 dual-core, 240 MHz
- **RAM:** 520 KB SRAM + 4 MB PSRAM (ESP32-WROOM-32D)
- **Flash:** 4 MB
- **Connectivity:** Wi-Fi 802.11 b/g/n, Bluetooth 4.2 + BLE
- **GPIO:** 34 programmable pins (ADC, I2C, SPI, UART, PWM)
- **Voltage:** 3.0–3.6V (typical 3.3V)
- **Framework:** ESP-IDF v6.0+

**I2C Bus Configuration (MPU6050 driver):**
- SDA: GPIO 21
- SCL: GPIO 22
- Clock: 100 kHz (standard mode)
- Pullups: Internal (7-cycle glitch filter)

### MPU6050 IMU

Six-axis inertial measurement unit connected to the ESP32 via I2C.

- **Registers:** 0x3B–0x48 (14 bytes: accel + temp + gyro)
- **Address:** 0x68 (AD0 = LOW)
- **WHO_AM_I:** 0x68 (some units report 0x70)
- **Sample rate:** 200 Hz (5 ms period, implemented)
- **Axes:** Accelerometer X/Y/Z, Gyroscope X/Y/Z, Temperature
- **Protocol:** I2C (100 kHz)

**Current status:** ✅ Working; see `firmware/flight-computer/mpu6050-driver/`

---

## Integration Targets (Planned)

### Telemetry Radio

- **Interface:** UART (115200 baud)
- **Protocol:** Custom binary framing (Level 5+)
- **Purpose:** Real-time telemetry downlink to ground station

### SD Card Logger

- **Interface:** SPI
- **Purpose:** Flight data recording for post-flight analysis
- **Format:** Binary or CSV (TBD)

### Servo Actuators

- **Interface:** PWM (via PCA9685 or ESP32 native PWM)
- **Purpose:** Thrust vector control, gimbal, or deployment mechanisms
- **Voltage:** 4.8–6V (typical SG90 servo)

---

## Hardware Compatibility Matrix

| Component | Interface | Status | Level |
|---|---|---|---|
| ESP32-WROOM-32D | N/A | ✅ Working | 0+ |
| MPU6050 IMU | I2C | ✅ Working | 0+ |
| Telemetry Radio | UART | 📋 Planned | 5+ |
| SD Card Logger | SPI | 📋 Planned | 5+ |
| Servo Actuators | PWM | 📋 Planned | 6+ |
| Raspberry Pi (Ground Station) | Wi-Fi/Ethernet | 📋 Planned | 5+ |

---

## Electrical Notes

- **Logic level:** 3.3V (ESP32 native). Do NOT connect 5V signals directly to GPIO.
- **I2C pullups:** Internal pullups are enabled on the MPU6050 bus. External 4.7kΩ pullups recommended for longer wires or higher bus speeds.
- **Power:** ESP32 dev boards typically accept USB (5V) or VIN (5–12V). Regulated 3.3V rail available on board.
- **Current draw:** ~80 mA active (Wi-Fi on), ~5 mA light sleep, ~150 µA deep sleep.

---

## References

- [ESP32-WROOM-32D Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32d_datasheet.pdf)
- [MPU6050 Register Map](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map2.pdf)
- [ESP-IDF I2C Master Driver](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/i2c_master.html)
