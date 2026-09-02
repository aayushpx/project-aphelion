# Weekly Log -2025-11-22 15:02

## Tasks Completed
- [x] Find Photoresistor (LDR) and 10k Ohm resistor
- [x] Blink LED every 1 second
- [x] Blink LED in SOS pattern
- [x] Fade LED using PWM

## Challenges / Roadblocks
- Using fields like `.sleep_mode` in the `ledc_timer_config_t` structure - not suitable for ESP-IDF v5.2.1 as it caused build errors. Removed invalid field which allowed the code to compile, reflecting API version incompatibility.
- Lower baud rate to 115200, slowing the data transfer but making it reliable.
- Code was logically correct in order to fade LED using PWM but it was not reflecting physically - this was due to attempting the management of fading manually in software, which can sometimes skip updates as well as continuous changes not registering correctly in the hardware registers, ultimately leading to the pin getting stuck at a constant high state.
	- **Fixed** - Switched to hardware-assisted fading API: 
		- `ledc_fade_func_install(0)` initialises necessary internal service.
		- `ledc_set_fade_with_time(...)` tells hardware to calculate and schedule duty cycle changes over a specified time.
		- `ledc_fade_start(...)` triggers the hardware to begin the fade sequence, running autonomously while main task waits or performs other duties.

## Learnings / Notes
- Ticks, RTOS, 1 tick = 1ms for ESP32 default. 

## Code Snippets / Commands
```cpp
// Example C++ snippet

```


## Performance Metrics (sampling rates, power consumption):
- 

## - Screenshots / media links:
