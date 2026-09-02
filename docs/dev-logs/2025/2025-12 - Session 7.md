# Weekly Log -2025-12-20 19:16

## Tasks Completed
- [x] Fixed ESP-IDF Python Virtual Environment issues.
- [x] Implemented custom C++ `DHT11` Class (Object-Oriented approach).
- [x] Successfully decoded 40-bit Pulse Width Protocol.
- [x] Verified hardware-to-software link via Serial Monitor (Temperature increase confirmed).

## Challenges / Roadblocks
- Linker Error: `undefined reference to app_main` (Resolved using `extern "C"` to prevent C++ name mangling).
- Bitwise Logic: Initially confusing, but understood through "Shift and OR" logic.

## Learnings / Notes
- **Timing Protocol:** DHT11 uses Pulse Width; Binary 0 is ~26µs HIGH, Binary 1 is ~70µs HIGH.
- **Polling & Timeouts:** Implemented a `wait_for_level` method with a microsecond timer and safety timeout to prevent CPU deadlocks on hardware failure.
- **Memory/Bitwise:** Used integer division (`i/8`) to map 40 bits into a 5-byte array.

- DHT11:
	- 's' - Data
	- middle - VCC
	- '-' is GND


## Code Snippets / Commands
```bash 
# Repair the environment 
./install.sh esp32 . $HOME/esp/esp-idf/export.sh 
# Build and Flash
idf.py build flash monitor
```
## Performance Metrics (sampling rates, power consumption):
- 0.33 Hz
- 1-microsecond sampling increments using `ets_delay_us(1)`

## - Screenshots / media links:
