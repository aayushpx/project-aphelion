# Weekly Log -2025-11-06 22:19

## Tasks Completed
- [x] Blinked LED on hardware

## Challenges / Roadblocks
- ESP32 not fully seated in breadboard, couldn't make solid contact.
- Confusion about which pins to use, got there in the end. GPIO2 for LED and GND for ground.
- LED only blinked when wires were held directly on the pins.
- Terminal adapter usage - didn't initially understand how to use ESP32 with it.
- idf.py commands not found initially, needed to source the environment.
- Invalid heater serial monitor output when running code through adapter.
- Flashing errors:
	- Serial data stream stopped / packet transfer stopped.
	- Checksum mismatch.
	- Failed to flash erase due to wiring.
	- All fixed with holding BOOT when flashing.
- Crystal frequency warning: ESP32 reported unusual values (~15-16 MHz) most likely due to noisy connections.
- LED blinking without running code: this caused me confusion; turned out to be because the last flashed program remained in flash memory.

## Learnings / Notes
- GPIO (General-Purpose Input-Output)
- GPIO 2: RTC Power Domain, Analog to Digital converter, Touch sensor input channel, Boot (strapping pin functions), OD/IE/WPU serial debugging/programming.
- ESP32 needs **solid contact** in the breadboard for GPIO pins to work.
- Pin voltage was measured with multi-meter for debugging connection issues.
- ESP32 retains flashed programs, code runs immediately on power up.
- Need to source ESP-IDF environment for idf.py commands.
- Debugging skills:
	- Learned to interpret serial monitor output
	- Learned to use trial and error - testing by touching pins, checking voltage, flashing without peripherals.
	- Crystals frequency warnings can appear but won't prevent flashing.
- Takeaway:
	1. Ensure power and wiring are solid
	2. Flash code to ESP32
	3. Connect peripherals
	4. Use monitor to verify execution


## Code Snippets / Commands
Same code, changed `#define` header properties to `GPIO_NUM_2`
```cpp
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "soc/gpio_num.h"

#define BLINK_GPIO GPIO_NUM_2
static const char *TAG = "BLINK";

extern "C" void app_main(void)
{
    gpio_reset_pin(BLINK_GPIO);
    gpio_set_direction(BLINK_GPIO, GPIO_MODE_OUTPUT);
    while (true)
    {
        gpio_set_level(BLINK_GPIO, 1);
        ESP_LOGI(TAG, "LED ON");
        vTaskDelay(500 / portTICK_PERIOD_MS);
        gpio_set_level(BLINK_GPIO, 0);
        ESP_LOGI(TAG, "LED OFF");
        vTaskDelay(500 / portTICK_PERIOD_MS);
    }
}
```


## Performance Metrics (sampling rates, power consumption):
- `vTaskDelay(500 / portTICK_PERIOD_MS);`
## - Screenshots / media links:
![[IMG_E0037.mov]]
