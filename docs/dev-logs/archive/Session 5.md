# Weekly Log -2025-11-15 21:16

## Tasks Completed
- [ ] Get terminal adapter working
- [ ] Wire it up and blink LED

## Challenges / Roadblocks
- Crystal frequency warning - board contains a crystal oscillator. Expected frequency: 26 MHz. Detected frequency: 15.6 MHz. ESP32 not reliably reading its own clock.
- Fixed - debugged with multi-meter and found that four pins were not making contact. Originally bent the pins for more friction inside joints but then tightened the Flathead screws on the adapter. Tightening worked
- New error: 
```bash
Writing at 0x000076b0 [==============================] 100.0% 16626/16626 bytes... 

A fatal error occurred: Serial data stream stopped: Possible serial noise or corruption.
```
-  Attempted to flash with baud rate 115200 - did not work
- **Pin Tested for continuity**
	- 3V3: Successful
	- GND: Successful
	- EN: Successful
	- IO0: Unsuccessful - Required for flashing (BOOT pin)
	- IO6: Successful
	- IO7: Successful
	- IO8: Successful
	- IO9: Successful
	- IO10: Unsuccessful - SPI flash pin, causes crystal errors
	- IO11: Unsuccessful - SPI flash pin, causes crystal errors
	- U0TXD: Unsuccessful - Serial output fail
	- U0RXD: Successful
- Fixed - all successful continuity
- Continuity confusion, everything beeped until the LED's anode.
- Voltage confusion.
- Fighting the terminal adapter to work.
- Plugged Dupont wires into the top female header of the adapter and not the screw terminals.
## Learnings / Notes
- Bad connections are the number one cause of trouble!
	- ESP32 worked when not in adapter
	- ESP32 worked when forced into breadboard
	- Adapter was the point of failure
- ESP32 GPIO outputs 3.3V and LED drops ~1.7V
	- Forward voltage: 3.3V
	- Voltage drop: 3.3V to 1.7V
	- Series circuit behaviour
- Adapters are not universal
## Code Snippets / Commands
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
## Code Study (since hardware is finally working)
- Header files give FreeRTOS timing,  GPIO control, Logging, Access to GPIO pin numbers
- `#define BLINK_GPIO_NUM_2` - tells the compiler to replace `BLINK_GPIO` to `GPIO_NUM_2`
- `static const char *TAG = "BLINK";` -  tag for logging in monitor
- `extern "C" void app_main(void)` - entry point of program (like int main()). extern "C" is required as ESP-IDF is C-based and this prevents C++ from name-mangling so that runtime can find the  symbol.
- `gpio_reset_pin(BLINK_GPIO);` - resets and returns the pin to its default state, essentially cleaning it.
- `gpio_set_direction(BLINK_GPIO, GPIO_MODE_OUTPUT);` - GPIO2 is set as an output, so we can drive it HIGH/LOW.
---
