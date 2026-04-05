# Weekly Log -2025-11-04 21:52

## Tasks Completed
- [x] Flashed board
- [x] Ran light program

## Challenges / Roadblocks
- Simulation light flash in CLI

## Learnings / Notes
- Whenever I edit source files, I have to rebuild the project with `idf.py build` and then flash the updated firmware with `idf.py -p`.

## Code Snippets / Commands
First code
```cpp
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"

#define BLINK_GPIO (gpio_num_t)2
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

CLI
```shell
~/Pr/rocket-telemetry-system/f/esp32-blink main ?1 > idf.py -p /dev/ttyUSB0 monitor                   5s
Executing action: monitor
Running idf_monitor in directory /home/neo/Projects/rocket-telemetry-system/firmware/esp32-blink
Executing "/home/neo/.espressif/python_env/idf6.0_py3.12_env/bin/python /home/neo/esp/esp-idf/tools/idf_monitor.py -p /dev/ttyUSB0 -b 115200 --toolchain-prefix xtensa-esp32-elf- --target esp32 --revision 0 /home/neo/Projects/rocket-telemetry-system/firmware/esp32-blink/build/esp32-blink.elf /home/neo/Projects/rocket-telemetry-system/firmware/esp32-blink/build/bootloader/bootloader.elf -m '/home/neo/.espressif/python_env/idf6.0_py3.12_env/bin/python' '/home/neo/esp/esp-idf/tools/idf.py' '-p' '/dev/ttyUSB0'"...
--- esp-idf-monitor 1.8.0 on /dev/ttyUSB0 115200
--- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H

rst:ets Jul 29 2019 12:21:46

rst:ets Jul 29 201ESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0040,len:6376
load:0x40078000,len:15900
ho 0 tail 12 room 4
load:0x40080400,len:3920
--- 0x40080400: _invalid_pc_placeholder at /home/neo/esp/esp-idf/components/xtensa/xtensa_vectors.S:2235
entry 0x40080644
--- 0x40080644: call_start_cpu0 at /home/neo/esp/esp-idf/components/bootloader/subproject/main/bootloader_start.c:25
I (29) boot: ESP-IDF v6.0-dev-2980-gab149384e1 2nd stage bootloader
I (29) boot: compile time Nov  4 2025 21:48:56
I (29) boot: Multicore bootloader
I (32) boot: chip revision: v3.1
I (35) boot.esp32: SPI Speed      : 40MHz
I (39) boot.esp32: SPI Mode       : DIO
I (42) boot.esp32: SPI Flash Size : 2MB
I (46) boot: Enabling RNG early entropy source...
I (50) boot: Partition Table:
I (53) boot: ## Label            Usage          Type ST Offset   Length
I (59) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (66) boot:  1 phy_init         RF data          01 01 0000f000 00001000
I (72) boot:  2 factory          factory app      00 00 00010000 00100000
I (79) boot: End of partition table
I (82) esp_image: segment 0: paddr=00010020 vaddr=3f400020 size=09c00h ( 39936) map
I (104) esp_image: segment 1: paddr=00019c28 vaddr=3ffb0000 size=02630h (  9776) load
I (108) esp_image: segment 2: paddr=0001c260 vaddr=40080000 size=03db8h ( 15800) load
I (115) esp_image: segment 3: paddr=00020020 vaddr=400d0020 size=11ae4h ( 72420) map
I (141) esp_image: segment 4: paddr=00031b0c vaddr=40083db8 size=07160h ( 29024) load
I (153) esp_image: segment 5: paddr=00038c74 vaddr=50000000 size=00024h (    36) load
I (159) boot: Loaded app from partition at offset 0x10000
I (159) boot: Disabling RNG early entropy source...
I (171) cpu_start: Multicore app
I (179) cpu_start: GPIO 3 and 1 are used as console UART I/O pins
I (180) cpu_start: Pro cpu start user code
I (180) cpu_start: cpu freq: 160000000 Hz
I (182) app_init: Application information:
I (185) app_init: Project name:     esp32-blink
I (190) app_init: App version:      c595741
I (194) app_init: Compile time:     Nov  4 2025 21:48:57
I (199) app_init: ELF file SHA256:  793592dc0...
I (203) app_init: ESP-IDF:          v6.0-dev-2980-gab149384e1
I (208) efuse_init: Min chip rev:     v0.0
I (212) efuse_init: Max chip rev:     v3.99 
I (216) efuse_init: Chip rev:         v3.1
I (220) heap_init: Initializing. RAM available for dynamic allocation:
I (226) heap_init: At 3FFAE6E0 len 00001920 (6 KiB): DRAM
I (231) heap_init: At 3FFB2EF8 len 0002D108 (180 KiB): DRAM
I (237) heap_init: At 3FFE0440 len 00003AE0 (14 KiB): D/IRAM
I (242) heap_init: At 3FFE4350 len 0001BCB0 (111 KiB): D/IRAM
I (248) heap_init: At 4008AF18 len 000150E8 (84 KiB): IRAM
W (254) spi_flash: Detected boya flash chip but using generic driver. For optimal functionality, enable `SPI_FLASH_SUPPORT_BOYA_CHIP` in menuconfig
I (266) spi_flash: detected chip: generic
I (269) spi_flash: flash io: dio
W (272) spi_flash: Detected size(4096k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (286) main_task: Started on CPU0
I (296) main_task: Calling app_main()
I (296) BLINK: LED ON
I (796) BLINK: LED OFF
I (1296) BLINK: LED ON
I (1796) BLINK: LED OFF
I (2296) BLINK: LED ON
I (2796) BLINK: LED OFF
```

## TODO next
- Wire LED and blink hardware
- Use GPIO2 and 220 Ohm resistor.
