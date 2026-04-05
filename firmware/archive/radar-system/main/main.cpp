#include <cstdint>
#include <cstdio>
#include "freertos/FreeRTOS.h"
#include "freertos/projdefs.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_timer.h"
#include "esp_rom_sys.h"
#include "hal/gpio_types.h"
#include "soc/gpio_num.h"

#define TRIG_PIN GPIO_NUM_32
#define ECHO_PIN GPIO_NUM_33
#define BUZZ_PIN GPIO_NUM_25
#define LED_PIN GPIO_NUM_26

class LandingRadar {
private:
  gpio_num_t _trig, _echo;

public:
  LandingRadar(gpio_num_t t, gpio_num_t e) : _trig(t), _echo(e) {};

  void begin();
  float readDistance();
};

extern "C" void app_main(void) {
  LandingRadar radar(GPIO_NUM_32, GPIO_NUM_33);
  radar.begin();

  gpio_reset_pin(BUZZ_PIN);
  gpio_set_direction(BUZZ_PIN, GPIO_MODE_OUTPUT);
  gpio_reset_pin(LED_PIN);
  gpio_set_direction(LED_PIN, GPIO_MODE_OUTPUT);

  printf("Rocket Telemetry System: ONLINE\n");

  while(true) {
    float dist = radar.readDistance();

    if (dist < 0) {
      printf("Radar Error: Timeout\n");
    } else {
      printf("Current Altitude: %.2f cm\n", dist);

      if (dist < 30.0f && dist > 2.0f) {
        gpio_set_level(BUZZ_PIN, 1);
        gpio_set_level(GPIO_NUM_26, 1);
        vTaskDelay(pdMS_TO_TICKS(50));
        gpio_set_level(GPIO_NUM_26, 0);
        gpio_set_level(BUZZ_PIN, 0);
      }
    }
    vTaskDelay(pdMS_TO_TICKS(200));
  }
}

void LandingRadar::begin() {
  gpio_reset_pin(_trig);
  gpio_reset_pin(_echo);
  gpio_set_direction(_trig, GPIO_MODE_OUTPUT);
  gpio_set_direction(_echo, GPIO_MODE_INPUT);
  gpio_set_level(_trig, 0);
}

float LandingRadar::readDistance() {
  // Send trigger pulse
  gpio_set_level(_trig, 1);
  esp_rom_delay_us(10);
  gpio_set_level(_trig, 0);

  // Wait for Echo to go HIGH
  uint64_t start_wait = esp_timer_get_time();
  while (gpio_get_level(_echo) == 0) {
    if (esp_timer_get_time() - start_wait > 30000) return -1.0f;
  }
  uint64_t t_start = esp_timer_get_time();

  // Wait for Echo to go LOW
  while (gpio_get_level(_echo) == 1) {
    if (esp_timer_get_time() - t_start > 30000) return -1.0f;
  }
  uint64_t t_end = esp_timer_get_time();

  // Calculate distance 
  // Duration is in us, speed of sound is ~0.0343 cm/us
  // Divide by 2 since sound travelled to floor and back
  float duration = (float)(t_end - t_start);
  return (duration * 0.0343f) / 2.0f;
}
