#!/usr/bin/env python

from core import core
import time

f=core()
f.setpoint=82.0
f.gotopoint=78.0

while True:
  print time.strftime("%X")+" "+str(f.read_temp())+" "+str(f.read_switch())+" "+str(f.setpoint)+" "+str(f.gotopoint)
  time.sleep(5)
