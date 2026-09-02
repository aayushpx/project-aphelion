# Weekly Log -2026-02-04 11:35

## Tasks Completed
- [x] Create wiring diagram
- [x] Equipment Check: Power module, Ultrasonic sensor, active buzzer
- [x] Successfully implemented C++ class-based Radar System in ESP-IDF
- [x] Verified hardware configuration

## Challenges / Roadblocks
- **Voltage Mismatch**: HC-SR04 Echo pin outputs 5V, which is unsafe for ESP32 (3.3V). Solved using $1k\ohm$ and $2.2k\ohm$ resistor voltage divider.
- Initialisation error: LED was stuck because GPIO direction was incorrectly set to the Buzzer pin instead of the LED pin.

## Learnings / Notes
- **Goal: If the Ultrasonic sensor detects the ground is closer than 1 meter, the Active Buzzer should start beeping quickly.**
- A voltage divider uses two resistors to 'tap off' some of that pressure to GND, leaving exactly 3.3V for esp32.
- All components must share a GND rail so they have the same reference point for signals.

## Code Snippets / Commands
```cpp
float duration = (float)(t_end - t_start); 
float distance = (duration * 0.0343f) / 2.0f;

```
## Performance Metrics (sampling rates, power consumption):
- Sampling rate set to ~5Hz (every 200ms).
- Radar Accuracy: Reliable down to ~2cm; timeouts occur if sensor is obstructed or ''touching" the target.

## - Screenshots / media links:

### Wiring Diagram
![[Screenshot from 2026-02-04 17-36-19.png | 600]]

### Photo of Breadboard
![[radar-detector-brd.jpg | 600]]