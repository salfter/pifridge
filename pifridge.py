#!/usr/bin/env python

from core import core
import time
from flask import Flask, Response, render_template, send_file
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import StringIO
import simplejson as json

f=core()
f.setpoint=90.0
f.gotopoint=f.setpoint

w=Flask(__name__)

@w.route("/chart.png")
def get_chart():
  imgdata=StringIO.StringIO()
  plt.plot(f.history, color="blue")
  plt.axis([0, 239, 30, 90])
  plt.gca().axes.get_xaxis().set_visible(False)
  plt.gcf().set_size_inches(6, 2)
  plt.savefig(imgdata, dpi=50, frameon=None, pad_inches=0, format="png")
  imgdata.seek(0)
  return send_file(imgdata, mimetype="image/png", cache_timeout=0)

@w.route("/history.json")
def get_history():
  return Response(json.dumps(list(f.history)), mimetype="application/json")

@w.route("/curr_temp")
def get_curr_temp():
  return Response(str(f.read_temp()), mimetype="text/plain")
  
@w.route("/setpoint")
def get_setpoint():
  return Response(str(f.setpoint), mimetype="text/plain")

@w.route("/setpointdown")
def setpoint_down():
  return Response(str(f.setpoint_down()), mimetype="text/plain")

@w.route("/setpointup")
def setpoint_up():
  return Response(str(f.setpoint_up()), mimetype="text/plain")

@w.route("/gotopoint")
def get_gotopoint():
  return Response(str(f.gotopoint), mimetype="text/plain")

@w.route("/gotopointdown")
def gotopoint_down():
  return Response(str(f.gotopoint_down()), mimetype="text/plain")

@w.route("/gotopointup")
def gotopoint_up():
  return Response(str(f.gotopoint_up()), mimetype="text/plain")

@w.route("/switch")
def get_switch():
  return Response(str(f.read_switch()), mimetype="text/plain")

@w.route("/date")
def get_date():
  return Response(time.strftime("%d %b %y"), mimetype="text/plain")

@w.route("/time")
def get_time():
  return Response(time.strftime("%H:%M"), mimetype="text/plain")
  
@w.route("/settings.html")
def get_settings():
  data={}
  return render_template("settings.html", **data)  
  
@w.route("/")
def get_index():
  data={}
  return render_template("index.html", **data)

if __name__ == "__main__":
  w.run(host="0.0.0.0", port=80, debug=True)
