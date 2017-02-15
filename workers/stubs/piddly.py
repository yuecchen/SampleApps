#!/usr/bin/env python3
#from subprocess import check_output
#def get_pid(name):
#    return map(int,check_output(["pidof",name]).split())



#piddy = get_pid("midori")

#print(piddy)

import subprocess, signal, os

def kill_process_by_name(name):
   p = subprocess.Popen(['ps', '-eaf'], stdout=subprocess.PIPE)
   out, err = p.communicate()

   for line in out.splitlines():
      if name in line:
         pid = int(line.split(None, 2)[1])
         print("killing pid = %d" % pid)
         os.kill(pid, signal.SIGKILL)

kill_process_by_name(b'runcpu')
