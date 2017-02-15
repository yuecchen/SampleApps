#!/usr/bin/env python3

import psutil

logical_cpu_count = psutil.cpu_count(logical=True)
print("logical cpu count is ", logical_cpu_count)
physical_cpu_count = psutil.cpu_count(logical=False)
print("physical cpu count is ", physical_cpu_count)

print("\n")

usage_per_logical = psutil.cpu_percent(interval=5, percpu=True)

index = 0
usage = ""
for item in usage_per_logical:
   newline = "Usage on cpu"+str(index)+" is "+str(item)+"%\n"
   usage = usage + newline
   index += 1
print(usage)
