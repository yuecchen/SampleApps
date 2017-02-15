#!/usr/bin/env python3


import datetime
import time
import subprocess
import signal
import os
import argparse

SECONDS = 60
MINUTES = 60
HOURS = 8
FUDGE = 45

def kill_process_by_name(name):
   p = subprocess.Popen(['ps', '-eaf'], stdout=subprocess.PIPE)
   out, err = p.communicate()
   for line in out.splitlines():
      print(line)
      if name in line:
         pid = int(line.split(None, 2)[1])
         print("killing pid = %d" % pid)
         os.kill(pid, signal.SIGKILL)
   return

parser = argparse.ArgumentParser()
parser.add_argument("seconds2wait", help="Number of seconds to wait until kill all python3 processes", type=int)
args = parser.parse_args()
FUDGE = args.seconds2wait
ts = time.time()
print(ts)
current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
print(current_time)

#target_time = (HOURS*MINUTES*SECONDS) + ts
target_time = (FUDGE) + ts
print(target_time)
future_time = datetime.datetime.fromtimestamp(target_time).strftime('%m-%d-%Y %H:%M:%S')
print(future_time)

while True:
   #sleep(1)
   ts = time.time()
   current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
   if ts >= target_time:
     print("Bombs away!!!!!!!!!!!!!!!!!!!!!")
     nuke = b"python3"
     kill_process_by_name(nuke)
     break
   
