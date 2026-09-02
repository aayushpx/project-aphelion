# Weekly Log -2026-02-07 22:00

## Tasks Completed
- [x] Initialised I2C Bus: COnfigured ESP32 SDA (GPIO 21) and SCL (GPIO 22) using IDF v5.2 `i2c_master` driver.
- [x] Created MPU6050 Driver Class
- [x] Handshake Verification: `i2c_master_transmit_receive` to `WHO_AM_I` register.
## Challenges / Roadblocks
- Unsoldered Header pins: MPU6050 not bonded to pins leading to floating connections. Handshake semi-works when physical pressure is applied.
- Watchdog Timeouts
## Learnings / Notes
- I2C Addressing: MPU6050 expects 0x68. Receiving 0x70 is a symptom of noise on the lines due to the lack of solder. Bits are being flipped because the signal isn't clean.
- Master/Slave Relationship: The ESP32 (master) control sthe clock (SCL), while the MPU6050 (Slave) only speaks when addressed by its ID.
- I2C lines are pulled up to 3.3V and devices communicate by pulling those lines to GND.

## Code Snippets / Commands
```cpp
// The "Probe" logic that proved the hardware was alive (barely)
uint8_t reg = 0x75; // WHO_AM_I register
uint8_t data = 0;
esp_err_t err = i2c_master_transmit_receive(dev_handle, &reg, 1, &data, 1, 100);

if (err == ESP_OK && data == 0x68) {
    ESP_LOGI("IMU", "Success. Found MPU6050");
} else {
    ESP_LOGE("IMU", "Found ID 0x%02X - Check connections.", data);
}
```
## Performance Metrics (sampling rates, power consumption):
- **Sampling Rate:** Currently polling at ~1Hz for debugging; plan to move to 100Hz+ after soldering.
- **I2C Clock Speed:** Configured at 100kHz (Standard Mode).


