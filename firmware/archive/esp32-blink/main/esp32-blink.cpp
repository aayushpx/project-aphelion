#include "freertos/FreeRTOS.h" jj
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "portmacro.h"
#include "soc/gpio_num.h"

#define BLINK_GPIO GPIO_NUM_2 // define LED pin
static const char *TAG = "BLINK"; // label for debugging
// brah
extern "C" void app_main(void)
{
    gpio_reset_pin(BLINK_GPIO); // makes sure pin is in default state
    gpio_set_direction(BLINK_GPIO, GPIO_MODE_OUTPUT); // set pin to output
    while (true)
    {
      for (int i = 0; i < 3; i++) {
        gpio_set_level(BLINK_GPIO, 1); // set output voltage HIGH
        ESP_LOGI(TAG, "LED ON - fast"); // log for on state
        vTaskDelay(200 / portTICK_PERIOD_MS); // wait 5000ms=5state 
                        // portTICK converts ms into ticks 
        gpio_set_level(BLINK_GPIO, 0); // set output volt OFF
        ESP_LOGI(TAG, "LED OFF - fast");
        vTaskDelay(300 / portTICK_PERIOD_MS); // wait 5set
      }

      for (int i = 0; i < 3; i++) {
        gpio_set_level(BLINK_GPIO, 1);
        ESP_LOGI(TAG, "LED ON - slow");
        vTaskDelay(1000 / portTICK_PERIOD_MS);

        gpio_set_level(BLINK_GPIO, 0);
        ESP_LOGI(TAG, "LED OFF - slow");
        vTaskDelay(100 / portTICK_PERIOD_MS);
      }
    }
}
