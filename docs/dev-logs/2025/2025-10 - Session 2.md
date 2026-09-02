# Weekly Log -2025-10-26 19:56

## Tasks Completed
- [x] Label ESP32-DevKitC V4 Board
- [ ] ESP-IDF configuration

## Challenges / Roadblocks
- 

## Learnings / Notes
- Port: /dev/ttyUSB0

## Code Snippets / Commands
Creating project folder with ESP-IDF
```bash
idf.py create-project .
```

Detecting serial port
```bash
~ > sudo dmesg | tail -n 20
[48960.280998] usb 1-5.3: new full-speed USB device number 12 using xhci_hcd
[48960.354959] usb 1-5.3: New USB device found, idVendor=10c4, idProduct=ea60, bcdDevice= 1.00
[48960.354974] usb 1-5.3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[48960.354979] usb 1-5.3: Product: CP2102 USB to UART Bridge Controller
[48960.354983] usb 1-5.3: Manufacturer: Silicon Labs
[48960.354987] usb 1-5.3: SerialNumber: 0001
[48960.361065] cp210x 1-5.3:1.0: cp210x converter detected
[48960.361536] usb 1-5.3: cp210x converter now attached to ttyUSB0
~ > ls -l /dev/ttyUSB0
crw-rw---- 1 root dialout 188, 0 Oct 26 22:26 /dev/ttyUSB0
~ > 
```

Created new `sdkconfig`  file for ESP32 target
```bash
idf.py set-target esp32
```

Configure project options
```bash

```

