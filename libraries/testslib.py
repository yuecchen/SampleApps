from collections import OrderedDict
import platform
import multiprocessing
import sys
import os
import psutil 
import re
import subprocess
import signal
import datetime
import time
import random
import json
from  ctypes import *

def random_alphanum():
   return ''.join(random.choice('0123456789abcded') for i in range(6))

def sentence_maker():
   s_nouns = ["A dude", "My mother", "The king", "Some guy", "A cat with rabies", "A sloth", "Your homie", "This cool guy my gardener met yesterday", "Superman", "The host, a guy they call Ghost", "Henry Ford", "Al Kaline", "Gordie Howe", "The cross species Chimera", "Babe Ruth", "Loni Anderson", "The incredible hulk", "Digital Pig Snuggler"]
   p_nouns = ["These dudes", "Both of my moms", "All the kings of the world", "Some guys", "All of a cattery's cats", "The multitude of sloths living under your bed", "Your homies", "Like, these, like, all these people", "Supermen", "Pack of dudes", "Drunken mob", "Crew of the USS Enterprise", "1968 Detroit Tigers"]
   s_verbs = ["eats", "rants", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures", "spies on", "diminishes", "meows on", "flees from", "tries to automate", "explodes", "spreads it around like wildfire", "hands", "deletes", "flies", "lopes"]
   p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack", "configure", "spy on", "diminish", "meow on", "flee from", "try to automate", "explode", "devastate"]
   infinitives = ["to wash the car", "to make a pie", "for no apparent reason", "because the sky is green", "for a disease", "to be able to make toast explode", "to know more about archeology", "as the Whole World Wonders", "because she said so", "to swab the deck", "for a view"]
   sentence_list = random.choice(s_nouns), random.choice(s_verbs), random.choice(s_nouns).lower() or random.choice(p_nouns).lower(), random.choice(infinitives)
   sentence = ' '.join(sentence_list)
   return sentence

def generate_json_data(MAX_ALBUMID, MAX_ID):

   album_count = 1
   album_id = 1
   data = {}
   content = []
   for x in range(1, MAX_ID):
      if album_count < MAX_ALBUMID:
         album_count += 1
      else:
         album_count = 1
         album_id += 1
      url_value = "http://placeholder.org/"+str(album_id)+"00/"+random_alphanum()
      thumb_value = "http://placeholder.org/"+str(album_id)+"00/"+random_alphanum()+".jpg"
      data = {
         'albumId': album_id,
         'Id': x,
         'title': sentence_maker(),
         'url': url_value,
         'thumbnailUrl': thumb_value
      }
      content.append(data)
   return content

def kill_process_by_name(name):
   p = subprocess.Popen(['ps', '-eaf'], stdout=subprocess.PIPE)
   out, err = p.communicate()

   for line in out.splitlines():
      if name in line:
         pid = int(line.split(None, 2)[1])
         print("killing pid = %d" % pid)
         os.kill(pid, signal.SIGKILL)
   return

def process_running_by_name(process_name):

    s = subprocess.Popen(['ps', 'axw'],stdout=subprocess.PIPE)
    print("Process Name in check")
    print(process_name)
    for x in s.stdout:
       print(x)
       if re.search(process_name, str(x)):
         return True
    return False

def is_cputest_running():
    cwd = os.getcwd()
    print(cwd)
    worker_path=cwd+'/'+'workers'+'/'
    print(worker_path)
    runcpu_process_string = 'python3'+' '+worker_path+'runcpu.py'
    print(runcpu_process_string)
    is_runcpu_running = process_running_by_name(runcpu_process_string)
    return is_runcpu_running

def launch_cpu_tests():
    print("Launch Me")

    cwd = os.getcwd()
    print(cwd)
    worker_path=cwd+'/'+'workers'+'/'
    print(worker_path)
    print()
    runcpu_process_string = 'python3'+' '+worker_path+'runcpu.py'
    print(runcpu_process_string)
    is_runcpu_running = process_running_by_name(runcpu_process_string)

    if is_runcpu_running:
       print("CPU Test is active")
    else:
       print("CPU Test is *not* active")
       subprocess.Popen(['python3', (worker_path+'runcpu.py')])
    return 

def is_timebomb_running():
    cwd = os.getcwd()
    print(cwd)
    worker_path=cwd+'/'+'workers'+'/'
    print(worker_path)
    timebomb_process_string = 'python3'+' '+worker_path+'timebomb.py'
    print(timebomb_process_string)
    timebomb_status = process_running_by_name(timebomb_process_string)
    return timebomb_status 

def launch_timebomb(target_seconds):
    print("Launch Me")

    cwd = os.getcwd()
    print(cwd)
    worker_path=cwd+'/'+'workers'+'/'
    print(worker_path)
    print()
    timebomb_string = 'python3'+' '+worker_path+'timebomb.py'
    print(timebomb_string)
    is_timebomb_running = process_running_by_name(timebomb_string)

    if is_timebomb_running:
       print("Timebomb is active")
    else:
       print("Timebomb is *NOT* active")

       subprocess.Popen(['python3', (worker_path+'timebomb.py'), str(target_seconds)])
    return 

def force_ise():
    x = 9
    y = x / 0
    return


def force_crash():
   i = c_char(b'a')
   j = pointer(i)
   c = 0

   while True:
      j[c] = b'a'
      c += 1
   j
   return

def set_target_time(button_setting):
    current_time = time.time()
    target_time = 0
    secsperhour = 60
    minsperhour = 60
    if button_setting == "1hour":
       target_hours = 1 
       print("Blow in one huor")
    elif button_setting == "2hour":  
       print("Blow in two huor")
       target_hours = 2 
    elif button_setting == "4hour":  
       print("Blow in four hour")
       target_hours = 4 
    elif button_setting == "8hour":  
       print("Blow in eight hour")
       target_hours = 8 
    elif button_setting == "12hour":  
       print("Blow in twelve hour")
       target_hours = 12 
    elif button_setting == "24hour":  
       print("Blow in twentyfour hour")
       target_hours = 24 
    elif button_setting == "randomhour":  
       print("Blow in random hour")
       target_hours = random.randrange(1, 24)
    else:
       print("Blow my mind")

    print(target_hours)
    target_time = current_time + (target_hours * (secsperhour * minsperhour))
    return target_time 
