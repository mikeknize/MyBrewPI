# MyBrewPI
Temperature controller for fermentation

##Parts:
- Raspberry PI A+
- Powerswitch tail 2 http://www.adafruit.com/product/268
- Waterproof DS18B20 Digital temperature sensor + extras http://www.adafruit.com/products/381
- Case for Rasberry PI, stl files provided in repo.

## Instructions
- Install rasbian on sd card for pi.
- Configure wpa_supplicant.conf if using wifi

### Hardware
- The adafruit tutorial shows PI Cobbler gpio breakout but it is not needed use F-M jumpers instead.
- On breadboard connect power, ground and data as shown here https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware
- Add one wire support  https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20
- Depending on model of PI gpio pin numbers may differ
- Connect a gpio ground to -in on power switch tail
- Connect pin 15 to +in on power switch tail.

### Software
- SSH to your pi
- Copy the files over, except for the case folder.
- Install Node.js if you want a local webpage
- Run sudo python tempcontrol.py
- Python script will output to console 
- In a browser go to the ip address you specified in index.js on line 39