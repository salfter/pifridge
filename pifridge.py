#!/usr/bin/env python

from core import core
import time
from functools import wraps
from flask import Flask, Response, render_template, send_file, request
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import StringIO
import simplejson as json
import ConfigParser

f=core()
f.setpoint=90.0
f.gotopoint=f.setpoint

w=Flask(__name__)

cfg=ConfigParser.ConfigParser()
cfg.read("pifridge.conf")

def check_auth(username, password):
  return (username==cfg.get("Authentication", "username") and password==cfg.get("Authentication", "password"))
  
def authenticate():
  return Response(
  "Valid username and password required.", 401,
  {"WWW-Authenticate": 'Basic realm="Login Required"'})
  
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if (request.remote_addr!="127.0.0.1"):
      auth=request.authorization
      if (not auth or not check_auth(auth.username, auth.password)):
        return authenticate()
      return f(*args, **kwargs)
    else:
      return f(*args, **kwargs)
  return decorated

@w.route("/chart.png")
def get_chart():
  imgdata=StringIO.StringIO()
  plt.plot(f.history, color="blue")
  plt.axis([0, 239, 30, 90])
  plt.gca().axes.get_xaxis().set_visible(False)
  plt.gcf().set_size_inches(6, 2)
  plt.savefig(imgdata, dpi=50, frameon=None, pad_inches=0, format="png")
  plt.close()
  imgdata.seek(0)
  return send_file(imgdata, mimetype="image/png", cache_timeout=0)

@w.route("/chart.html")
def get_chart_page():
  data={}
  return render_template("chart.html", **data)  

@w.route("/chart_l.png")
def get_large_chart():
  imgdata=StringIO.StringIO()
  plt.plot(f.history, color="blue")
  plt.axis([0, 239, 30, 90])
  plt.gca().axes.get_xaxis().set_visible(False)
  plt.gcf().set_size_inches(6, 4.5)
  plt.savefig(imgdata, dpi=50, frameon=None, pad_inches=0, format="png")
  plt.close()
  imgdata.seek(0)
  return send_file(imgdata, mimetype="image/png", cache_timeout=0)

@w.route("/history.json")
def get_history():
  return Response(json.dumps(list(f.history)), mimetype="application/json")

@w.route("/info.json")
def get_info_json():
  return Response(json.dumps({"curr_temp": f.read_temp(), "setpoint": f.setpoint, "gotopoint": f.gotopoint, "switch_status": f.read_switch()}), mimetype="application/json")

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
@requires_auth
def get_settings():
  data={}
  return render_template("settings.html", **data)  
  
@w.route("/")
def get_index():
  data={}
  return render_template("index.html", **data)

if __name__ == "__main__":
  w.run(host="0.0.0.0", port=80, debug=True)
