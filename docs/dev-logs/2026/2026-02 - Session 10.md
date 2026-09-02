# Weekly Log -2026-02-20 00:06

## Tasks Completed
- [ ] First-ever physical soldering: Successfully joined header pins to the MPU6050 IMU using a T12-942 station.
- [ ] Developed a custom C++ class using `i2c_master` to wake the sensor and stream raw data.
- [ ] Verified real-time communication with the flight computer, confirming the IMU is alive and responding!

## Challenges / Roadblocks
- Bit-Shifting (0x70 Error): The device reports a WHO_AM_I of 0x70 instead of 0x68. This indicates signal noise or weak pull-ups causing a 1-bit shift in the I2C stream.
- Sleep Mode: The MPU6050 defaults to sleep; initial code failed because it didn't write to the PWR_MGMT_1 register.

## Learnings / Notes
- Flux is essential. Used Mechanic Nano Flux to ensure clean solder joints and prevent bridges.
- Strict ID checking prevents a functional sensor from starting if the signal is slightly noisy.
- Disconnecting AD0 defaults to 0x68 via internal pull-down, but grounding it manually provides a more stable reference.

## Code Snippets / Commands
```cpp
// Wake up command to register 0x6B (PWR_MGMT_1)
esp_err_t MPU6050::wake_up() {
    uint8_t data[] = {0x6B, 0x00};
    return i2c_master_transmit(_dev_handle, data, sizeof(data), -1);
}

// Reading 6 bytes of raw accelerometer data (X, Y, Z)
uint8_t start_reg = 0x3B;
uint8_t data[6];
i2c_master_transmit_receive(_dev_handle, &start_reg, 1, data, 6, -1);
```

### Output
```bash
I (110853) ROCKET_IMU: ACCEL -> X: -1336 | Y: 288 | Z: 16840
I (111353) ROCKET_IMU: ACCEL -> X: -1216 | Y: 284 | Z: 16768
I (111853) ROCKET_IMU: ACCEL -> X: -1316 | Y: 240 | Z: 16616
I (112353) ROCKET_IMU: ACCEL -> X: -1240 | Y: 268 | Z: 16764
I (112853) ROCKET_IMU: ACCEL -> X: -1192 | Y: 184 | Z: 16860
I (113353) ROCKET_IMU: ACCEL -> X: -1244 | Y: 232 | Z: 16764
I (113853) ROCKET_IMU: ACCEL -> X: -1300 | Y: 284 | Z: 16812

~/Pr/rocket-telemetry-system/f/f/I2C-lrn main >1 ?27 >     
```
## Performance Metrics (sampling rates, power consumption):
- Z-Axis Baseline: ~16700 LSB (matches expected 1g gravity at ±2g sensitivity).
