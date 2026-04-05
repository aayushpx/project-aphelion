#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "rom/ets_sys.h" 

class DHT11 {
public:
  DHT11(gpio_num_t pin) {
    _pin = pin;
  }
  void init() {
    gpio_reset_pin(_pin);
  }
  float readTemperature() {
    uint8_t data[5] = {0, 0, 0, 0, 0}; // 5 bytes = 40 bits
    
    gpio_set_direction(_pin, GPIO_MODE_OUTPUT);
    gpio_set_level(_pin, 0);
    vTaskDelay(pdMS_TO_TICKS(20));
    gpio_set_level(_pin, 1);
    ets_delay_us(40);
    gpio_set_direction(_pin, GPIO_MODE_INPUT);
    
    if (wait_for_level(0, 80) == -1) return -1.0;
    if (wait_for_level(1, 80) == -1) return -1.0;
    if (wait_for_level(0, 80) == -1) return -1.0;

    for (int i = 0; i < 40; i++) {
      if (wait_for_level(1, 60) == -1) return -1.1;

      int duration = wait_for_level(0, 80);
      if (duration == -1) return -1.2;

      if (duration > 35) {
        data[i/8] <<= 1;
        data[i/8] |= 1;
      } else {
        data[i/8] <<= 1;
      }
    }

    return (float)data[2];
  }
 
private:
  gpio_num_t _pin;

  int wait_for_level(int level, int timeout_us) {
    int timer = 0;
    while(gpio_get_level(_pin) != level) {
      if (timer > timeout_us) return -1;
      ets_delay_us(1);
      timer++;
    }
    return timer;
  }
};

extern "C" void app_main(void) {
  DHT11 cabin_sensor(GPIO_NUM_32);
  cabin_sensor.init();
  while(1) {
    float t = cabin_sensor.readTemperature();
    ESP_LOGI("TELEMETRY", "Temp: %.1f", t);
    vTaskDelay(pdMS_TO_TICKS(2000));
  }
}

