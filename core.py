#!/usr/bin/env python

import os
import glob
import thread
import time
from collections import deque

class core:

  def __init__(self):
    self.setpoint=55.0
    self.gotopoint=self.setpoint
    self.bus_lock=thread.allocate_lock()
    self.settings_lock=thread.allocate_lock()
    self.temp_device=glob.glob("/sys/bus/w1/devices/28*")[0]+"/w1_slave"
    self.switch_device=glob.glob("/sys/bus/w1/devices/12*")[0]+"/output"
    self.switch_status=glob.glob("/sys/bus/w1/devices/12*")[0]+"/state"
    self.history=deque()
    for i in range(0, 240):
      self.history.append(self.setpoint)
    self.switch_state=self.read_switch()
    thread.start_new_thread(self.core_loop, ("core_loop",))      
    return

  def read_switch(self, switchsel=0):
    with self.bus_lock:
      done=False
      while (not done):
        try:
          f=open(self.switch_status, "r")
          st=int(f.read())
          f.close()
          done=True
        except:
          pass
    return st&(1<<switchsel)==0
    
  def set_switch(self, new_state, switchsel=0):
    with self.bus_lock:
      done=False
      while (not done):
        try:
          f=open(self.switch_status, "r")
          st=int(f.read())&(2-switchsel)
          f.close()
          done=True
        except:
          pass
      if (not new_state):
        st=st|(1<<switchsel)
      done=False
      while (not done):
        try:
          f=open(self.switch_device, "w")
          f.write(str(st))
          f.close()
          self.switch_state=new_state
          done=True
        except:
          pass
    
  def read_temp_raw(self):
    with self.bus_lock:
      done=False
      while (not done):
        try:
          f=open(self.temp_device, "r")
          lines=f.readlines()
          f.close()
          done=True
        except:
          pass
    return lines
    
  def read_temp(self, fahrenheit=True):
    lines=self.read_temp_raw()
    while (lines[0].strip()[-3:]!="YES"):
      time.sleep(0.25)
      lines=self.read_temp_raw()
    temp_s=lines[1][lines[1].find("t=")+2:]
    temp=float(temp_s)/1000.0
    if (fahrenheit):
      temp=temp/5.0*9.0+32
    return temp

  def setpoint_down(self):
    sp=0
    with self.settings_lock:
      self.setpoint-=1
      self.gotopoint=self.setpoint
      sp=self.setpoint
    return sp

  def setpoint_up(self):
    sp=0
    with self.settings_lock:
      self.setpoint+=1
      self.gotopoint=self.setpoint
      sp=self.setpoint
    return sp
      
  def gotopoint_down(self):
    gp=0
    with self.settings_lock:
      self.gotopoint-=1
      gp=self.gotopoint
    return gp

  def gotopoint_up(self):
    gp=0
    with self.settings_lock:
      self.gotopoint+=1
      gp=self.gotopoint
    return gp

  def core_loop(self, thread_name):
    wait=0
    gotocount=60
    while True:
      with self.settings_lock:
        t=self.read_temp()
        s=self.switch_state
        self.history.popleft()
        self.history.append(t)
        if (t>self.setpoint+1 and s==False and wait==0):
          self.set_switch(True)
        if (t<self.setpoint-1 and s==True):
          self.set_switch(False)
          wait=6
        if (wait>0):
          wait-=1
        if (self.gotopoint!=self.setpoint):
          if (gotocount==0):
            if (self.gotopoint<self.setpoint):
              self.setpoint-=1
            else:
              self.setpoint+=1
            gotocount=60
          else:
            gotocount-=1
      time.sleep(60)
      