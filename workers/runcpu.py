#!/usr/bin/env python3
import datetime
import time
import sys
from multiprocessing import Pool
from multiprocessing import cpu_count

def busybee(x):
   while True:
     x * x

def cpu_worker():
	filer = open("cpu_output.txt", "a")
	ts = time.time()
	current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
	output = current_time + " cpu ran\n";
	filer.write(output)
	filer.close()

number_of_cpus = cpu_count()
cpu_worker()
y = Pool(processes=number_of_cpus)
y.map(busybee, range(number_of_cpus))



