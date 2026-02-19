#include <cstdint>
#include <stdio.h>
#include "driver/i2c_master.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

static const char *TAG = "ROCKET_IMU";

class MPU6050 {
private:
    i2c_master_bus_handle_t _bus_handle;
    i2c_master_dev_handle_t _dev_handle;
    uint8_t _address;

public:
    MPU6050(uint8_t addr) : _address(addr) {};
    
    esp_err_t init();
    uint8_t who_am_i();
    esp_err_t wake_up();
    esp_err_t read_accel();
};

extern "C" void app_main() {
    MPU6050 imu(0x68);
    
    if (imu.init() != ESP_OK) {
        ESP_LOGE(TAG, "I2C Initialization failed");
        return;
    }

    uint8_t id = imu.who_am_i();
    ESP_LOGI(TAG, "WHO_AM_I reported: 0x%02X", id);

    // Proceed if ID is correct (0x68) or slightly corrupted (0x70)
    if (id == 0x68 || id == 0x70) {
        if (imu.wake_up() == ESP_OK) {
            ESP_LOGI(TAG, "Sensor woken up successfully");
            
            while (1) {
                imu.read_accel();
                vTaskDelay(pdMS_TO_TICKS(500));
            }
        } else {
            ESP_LOGE(TAG, "Failed to wake up sensor");
        }
    } else {
        ESP_LOGE(TAG, "Unexpected Device ID. Check wiring.");
    }
}

esp_err_t MPU6050::init() {
    i2c_master_bus_config_t bus_cfg = {
        .i2c_port = I2C_NUM_0,
        .sda_io_num = GPIO_NUM_21,
        .scl_io_num = GPIO_NUM_22,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags = {.enable_internal_pullup = true}
    };
    ESP_ERROR_CHECK(i2c_new_master_bus(&bus_cfg, &_bus_handle));

    i2c_device_config_t dev_cfg = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = _address,
        .scl_speed_hz = 100000,
    };
    return i2c_master_bus_add_device(_bus_handle, &dev_cfg, &_dev_handle);
}

uint8_t MPU6050::who_am_i() {
    uint8_t reg = 0x75;
    uint8_t data = 0;
    i2c_master_transmit_receive(_dev_handle, &reg, 1, &data, 1, -1);
    return data;
}

esp_err_t MPU6050::wake_up() {
    // Write 0 to PWR_MGMT_1 (0x6B) to wake the sensor
    uint8_t data[] = {0x6B, 0x00};
    return i2c_master_transmit(_dev_handle, data, sizeof(data), -1);
}

esp_err_t MPU6050::read_accel() {
    uint8_t start_reg = 0x3B; // Accel X High register
    uint8_t data[6];          // Buffers for X, Y, Z (High/Low bytes)
    
    // Read 6 bytes starting from 0x3B
    esp_err_t ret = i2c_master_transmit_receive(_dev_handle, &start_reg, 1, data, 6, -1);
    
    if (ret == ESP_OK) {
        // Shift and combine high/low bytes into signed 16-bit integers
        int16_t ax = (data[0] << 8) | data[1];
        int16_t ay = (data[2] << 8) | data[3];
        int16_t az = (data[4] << 8) | data[5];
        
        ESP_LOGI(TAG, "ACCEL -> X: %d | Y: %d | Z: %d", ax, ay, az);
    }
    return ret;
}
