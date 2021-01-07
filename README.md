## What is a Mouth Mouse / Mundmaus
The mouth mouse is intended for handicapped people, which suffer for instance tetraplegia. Instead of using their extremities, they use their mouth and tounge inlcuding puffing to control the mouse motion and clicking.
## What is tetraplegia
These people for instance cannot move any of their extermities up to very severe cases, where they can neither move nor hold their head, which means their available movements are very limited.
The extreme case, where people cannot move or hold their head, their head needs to be fixed with a strap band. They are only able to do facials, use their mouth, their tounge.
These people are also artificially respirated, which means they cannot puff air, but are limited to use the available air in their mouth and contract their cheeks to simulate puffing.
## What is the intention of this project
Such commercial mice can be very expensive up to 2.200 EUR (what I have seen). Not all insurance pay for this. They pay in Germany for instance but not in Austria.
This mouse is approx. 22 EUR (ESP32 chip [10 EUR], joystick [2 EUR], water flow sensor [10 EUR]). The code to make this work is for free and will be kept freely available forever.
It is intended to make this available at no cost, but the parts one needs to buy. It is kept very simplistic in terms of required parts, which are available everywhere to make sure everyone has access and is able to build this.
## What are the features of the mouse
* Bluetooth connectivity, no cables to the PC, hence you can use distant large screens, like the TV with a Raspberry for instance, which has bluetooth build in.
* Puffing is clicking in click mode. In Drag'n'Drop mode one puff picks the object, like a window or a card in a card game for instance. A second puff will release it where the pointer was moved to.
* The joystick is used to move the mouse pointer.
## Why bluetooth?
Simply because the ESP32 cannot be run as a USB device like the pyboard, hence I had to find an alternative. Eventually this is more practical, since less cabling and longer USB cables may result into problems with a Microcomputer like this.
## How did I use it?
I used a Raspberry PI 3B running Raspbian as the computer connected to the TV. The mouse you will build is then connected via Bluetooth to the Raspberry. It will always automatically reconnect, hence super simple to use. If you opt for the Display you will see status messages.
## Can I contribute?
Absolutely. I am not a professionial developer and appreciate coding feedback, input and suggestions as well as contributions. If there are other ideas or better ideas, let's collaborate and improve life of severly impacted humand beings instead of looking for their money!
## Technologies
Everything is based on an ESP32 (think of it as a Microcomputer) and Micropython.
You will need to get the following:
* [ESP32](https://smile.amazon.de/AZDelivery-ESP32-NodeMCU-gratis-eBook/dp/B07Z83MF5W/ref=sr_1_4?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=esp32+azdelivery&qid=1610048309&sr=8-4) - 10 EUR
* [Joystick](https://smile.amazon.de/gp/product/B07CKCBHF4/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1) - 2 EUR
* [Water Flow Sensor](https://smile.amazon.de/gp/product/B073VJQMJJ/ref=ppx_yo_dt_b_asin_title_o05_s00?ie=UTF8&psc=1) - 10 EUR
* Optional: [Display](https://smile.amazon.de/gp/product/B078J5TS2G/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) - 7.50 EUR
* Optional: [Microphone Stand](https://smile.amazon.de/Adam-Stands-S5B-Mikrofonst%C3%A4nder-Schwenkarm/dp/B001W6WDNI/ref=psdc_5759560031_t1_B019NY2PKG) - 15 EUR
* Optional: [Raspberry PI 4 with 4GB](https://smile.amazon.de/Raspberry-Pi-ARM-Cortex-A72-Bluetooth-Micro-HDMI/dp/B07TC2BK1X/ref=sr_1_3?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=10TENZVLWRRGR&dchild=1&keywords=raspberry+pi+4&qid=1610051320&quartzVehicle=812-409&replacementKeywords=raspberry+pi&sprefix=raspberry+%2Caps%2C195&sr=8-3) at approx 60 EUR - no case, power supply, neither HDMI cable included. Sets vary between 100-120 EUR.
* Optional: [Battery for ESP32 instead of USB cable](https://smile.amazon.de/gp/product/B0822Q4VS4/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1) - 10.50 EUR, alternative with [4 Batteries](https://smile.amazon.de/gp/product/B082MFWC7H/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1) at 14.90 EUR
* Optional: [Bluetooth USB Stick for PC](https://smile.amazon.de/gp/product/B009ZIILLI/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1) - 12 EUR
## Credits
* the ST7735.py file is orignally from boochow's [repo](https://github.com/boochow/MicroPython-ST7735). I made no changes.
* the sysfont.py is from GuyCarver's [repo](https://github.com/GuyCarver/MicroPython/blob/master/lib/sysfont.py)
* the bluetooth code I assembled from samples from MicroPython. Thank you very much for this!!!
## Setup
* Follow the fritzing for cabling the different pieces
Ideally run Linux for the next steps - use the Raspberry for instance
* Download all .py files from this repo into a folder
* Download the MicroPython [firmware](http://micropython.org/download/esp32/) - I used the IDF4 latest unstable version, which ran just and has all features used in this project per 7th January 2021.
* Run following commands to install necessary software
```
sudo apt install screen
sudo pip3 install rshell
sudo pip3 install esptool
```
Next you need to flash the ESP32 chip. Any commands you run wrong can damage or destroy your ESP32. Running it per below is your own risk. MicroPython may have changed the instructions during me writing this up to now, hence please double check on their [webpage](http://micropython.org/download/esp32/).
Connect the ESP32 via a Micro USB cable to the Raspberry or any other PC running Linux. If this is the first time you put MicroPython on the ESP32, you need to erase the flash as per below. If you have multiple USB to Serial devices connected your ttyUSB[n] may have a different number!
You may need to press the "boot" button the the ESP32 chip in case the esptool fails with reading errors.
```
sudo esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
```
After that you can upload the MicroPython firmware you previously downloaded. Make sure to adjust the directory if necessary.
```
sudo esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-idf3-20210107-unstable-v1.13-268-gf7aafc062.bin
```
Now since the "operating system" is successfully uploaded, you need to copy all .py files to the chip, which is only one command, which mirrors the folder you downloaded the files to. You need to be in the folder or replace the "." after -m with the correct path.
```
sudo rshell --buffer-size=30 -p /dev/ttyUSB0 rsync -m . /pyboard
```
If you cabled everything correctly you can follow your mouse booting using screen:
```
sudo screen /dev/ttyUSB0 115200
```
To exit screen and release the block on the tty for an additional file sync, simple press `CTRL-A` followed by `k` and confirm with `y`
Last not least we need to connect the mouse to the Raspberry. You need at least kernel 5.10. Version 5.4 is buggy. You can upgrade from 5.4 to 5.10 using `rpi-update`. There will be warnings you will need to accept. To connect the mouse we need bluetoothctl which we first need to install.
```
sudo apt install bluetoothctl
```
After that we need to trust and connect to the mouse after scanning for it. You will need to replace "mac" with the MAC address. Once bluetoothctl start the next commands are part of this extra command "shell".
```
bluetoothctl
scan on
trust "mac"
connect "mac"
exit
```
That's it. You should see the pointer moving now. You will however not see the mouse as "paired" in the bluetooth icon on the taskbar. If you pair it will not reconnect successfully after rebooting either the Raspberry or the mouse. Pairing is also not necessary for this to work.
## Problems with flashing
If the flashing times out you may need to keep the "boot" button pressed until the connection is successfully established. Also never use Pin 0 - any connection to Pin 0 can cause issues with uploading or updating your py files later. 

