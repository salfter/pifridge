#!/usr/bin/env python

from core import core
import time
from flask import Flask, Response, render_template

f=core()
f.setpoint=70.0
f.gotopoint=f.setpoint

w=Flask(__name__)

@w.route("/curr_temp")
def get_curr_temp():
  return Response(str(f.read_temp()), mimetype="text/plain")
  
@w.route("/setpoint")
def get_setpoint():
  return Response(str(f.setpoint), mimetype="text/plain")

@w.route("/gotopoint")
def get_gotopoint():
  return Response(str(f.gotopoint), mimetype="text/plain")

@w.route("/switch")
def get_switch():
  return Response(str(f.read_switch()), mimetype="text/plain")

@w.route("/date")
def get_date():
  return Response(time.strftime("%d %b %y"), mimetype="text/plain")

@w.route("/time")
def get_time():
  return Response(time.strftime("%H:%M"), mimetype="text/plain")
  
@w.route("/")
def get_index():
  data={}
  return render_template("index.html", **data)

if __name__ == "__main__":
  w.run(host="0.0.0.0", port=80, debug=True)