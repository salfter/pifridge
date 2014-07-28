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

Interface
---------

You could run this headless, using a web browser on the device of your
choice to control your fridge.  However, the interface is designed to fit
within the constraints of the PiTFT touchscreen.  I have my Raspberry Pi set
to auto-login the "pi" user; scripts in /home/pi fire up X, Ratpoison, and
Chromium (in kiosk mode).  The setup looks something like this:

 * packages that need to be installed
```
sudo apt-get install ratpoison unclutter chromium nmap
```

 * /etc/inittab 
```
...
#1:2345:respawn:/sbin/getty --noclear 38400 tty1
1:2345:respawn:/bin/login -f pi tty1 /dev/tty1 2>&1
2:23:respawn:/sbin/getty 38400 tty2
3:23:respawn:/sbin/getty 38400 tty3
...
```

 * /home/pi/.bash_profile
```
if [ -z "$DISPLAY" ] && [ $(tty) == /dev/console ]; then
  startx
fi
```

 * /home/pi/.xinitrc
```
exec ratpoison
```

 * /home/pi/.ratpoisonrc
```
banish
exec xset s off
exec xset -dpms
exec unclutter -idle 0
exec /home/pi/start-pifridge.sh
```

 * /home/pi/start-pifridge.sh
```
#!/bin/bash
if [ "`nmap -oG - -p 80 localhost | grep open`" == "" ]
then
  sudo nohup /root/pifridge/pifridge.py 2>&1 >/dev/null &
fi
while [ "`nmap -oG - -p 80 localhost | grep open`" == "" ]
do
  sleep 1
done
exec /usr/bin/chromium --incognito --kiosk http://localhost/
```

unclutter keeps the mouse pointer hidden most of the time...it only comes up
when you touch the screen, and then goes away.

nmap is used to verify that pifridge is running before Chromium starts.

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

