#include "driver/ledc.h"
#include "esp_err.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

// Define LEDC params
#define LEDC_TIMER      LEDC_TIMER_0
#define LEDC_CHANNEL    LEDC_CHANNEL_0
#define LEDC_SPEED_MODE LEDC_HIGH_SPEED_MODE
#define LEDC_DUTY_RESOLUTION LEDC_TIMER_8_BIT
#define LEDC_OUTPUT_IO  18
#define FADE_TIME_MS    2000 // 2 seconds for a full fade

// MAX_DUTY is 255 for 8-bit resolution
#define MAX_DUTY        (1 << LEDC_DUTY_RESOLUTION) - 1 


void setup_pwm() {
    // --- Timer config ---
    ledc_timer_config_t timer_config = {
        .speed_mode      = LEDC_SPEED_MODE,
        .duty_resolution = LEDC_DUTY_RESOLUTION,
        .timer_num       = LEDC_TIMER,
        .freq_hz         = 5000,
        .clk_cfg         = LEDC_AUTO_CLK
    };
    ESP_ERROR_CHECK(ledc_timer_config(&timer_config));

    // --- Channel config ---
    ledc_channel_config_t channel_config = {
        .gpio_num  = LEDC_OUTPUT_IO,
        .speed_mode = LEDC_SPEED_MODE,
        .channel   = LEDC_CHANNEL,
        .intr_type = LEDC_INTR_DISABLE,
        .timer_sel = LEDC_TIMER,
        .duty      = 0,
        .hpoint    = 0
    };
    ESP_ERROR_CHECK(ledc_channel_config(&channel_config));

    ledc_fade_func_install(0);
    
    // Set initial duty to 0 and update to activate the channel, as before
    ESP_ERROR_CHECK(ledc_set_duty(LEDC_SPEED_MODE, LEDC_CHANNEL, 0));
    ESP_ERROR_CHECK(ledc_update_duty(LEDC_SPEED_MODE, LEDC_CHANNEL));
}

extern "C" void app_main(void) {
    setup_pwm();

    while (1) { 

        // Fade Up (to MAX_DUTY / 255)
        ESP_ERROR_CHECK(ledc_set_fade_with_time(LEDC_SPEED_MODE, LEDC_CHANNEL, MAX_DUTY, FADE_TIME_MS));
        ESP_ERROR_CHECK(ledc_fade_start(LEDC_SPEED_MODE, LEDC_CHANNEL, LEDC_FADE_NO_WAIT));
        
        // Wait for the fade up to complete before starting the fade down
        vTaskDelay(pdMS_TO_TICKS(FADE_TIME_MS + 100)); // +100ms buffer

        // Fade Down (to 0)
        ESP_ERROR_CHECK(ledc_set_fade_with_time(LEDC_SPEED_MODE, LEDC_CHANNEL, 0, FADE_TIME_MS));
        ESP_ERROR_CHECK(ledc_fade_start(LEDC_SPEED_MODE, LEDC_CHANNEL, LEDC_FADE_NO_WAIT));

        // Wait for the fade down to complete
        vTaskDelay(pdMS_TO_TICKS(FADE_TIME_MS + 100)); // +100ms buffer
    }
}
