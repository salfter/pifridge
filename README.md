pifridge
========

This is a simple temperature controller, aimed at overriding the thermostat
in a refrigerator or freezer to allow warmer temperatures for the
fermentation of beer (though it could be used for other purposes).  It works
with 1-Wire devices: a DS18B20 temperature sensor and a DS2406 addressable
switch.  The latter device controls a solid-state relay, which in turn
controls power to the refrigerator.  A web interface is included for remote
monitoring, or for use with a local display.

I'm writing this to work with a Raspberry Pi, equipped with an Adafruit
PiTFT touchscreen and a 1-Wire/I2C adapter board of my own design.  The
adapter board design files are at Upverter:

https://upverter.com/salfter/b0ef63c2cd7a37c7/rpi_i2c_1w/

Check the comments for links to order bare boards and parts to assemble your
own.  It uses the w1_gpio bit-bang driver.  Other supported 1-Wire
interfaces should also work, as this code works with the /sys/bus/w1 file
hierarchy.

Dependencies
------------

Note that current releases of Linux don't include support for the DS2406. 
I've written a driver for it; a patch that should apply to reasonably
current kernel releases is available:

https://dl.dropboxusercontent.com/u/57535575/w1_ds2406.patch

Apply the patch to your kernel source tree, make sure CONFIG_W1_SLAVE_DS2406
is enabled in your config, rebuild, and install.

The web interface uses Flask, simplejson, and matplotlib, so those need to
be installed:

```
sudo apt-get install python-pip python-simplejson python-matplotlib
sudo pip install flask 
```


Writing to the DS2406 (to switch it on and off) needs root access.  For that
matter, so does Flask if you want it to run on port 80.  Therefore, pifridge
will need to run as root.

