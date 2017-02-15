from collections import OrderedDict
import platform
import multiprocessing
import sys
import psutil 

def gather_cpu_info():
    with open('/proc/cpuinfo') as f:
       for line in f:
          if line.strip():
             if line.rstrip('\n').startswith('model name'):
                model_name = line.rstrip('\n').split(':')[1]
    return model_name

def determine_mem_info():
    meminfo=OrderedDict()

    with open('/proc/meminfo') as f:
      for line in f:
         meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

#total_memory = mem_info_wrapper("MemTotal")
#free_memory = mem_info_wrapper('MemFree')
#avail_memory = mem_info_wrapper('MemAvailable')
#total_swap = mem_info_wrapper('SwapTotal')
#free_swap = mem_info_wrapper('SwapFree')

def gather_mem_info(target):
    meminfo = determine_mem_info()
    return format(meminfo[target])

def gather_network_info():
    network_data=""

    with open('/proc/net/dev') as f:
      for line in f:
         network_data += str(line)
      print(network_data)
    return network_data

def gather_python_info():
    pyth_ver = sys.version
    return(pyth_ver)

# OS type is flavor - linux, windows, etc
def gather_os_type():
    os_type = sys.platform
    return(os_type)

def gather_platform_info():
    plat = platform.platform() 
    return(plat)

def gather_arch_info():
    arch = platform.processor()
    return(arch)

def gather_kernel_info():
    kernel = platform.uname().release
    return(kernel)

def gather_distro_info():
    distro1 = platform.linux_distribution()[0]
    distro2 = platform.linux_distribution()[1]
    distro3 = platform.linux_distribution()[2]
    distro = distro1+" "+distro2+" "+distro3 
    return(distro)

def gather_endianess_info():
    endianess = sys.byteorder
    return(endianess)

def gather_logical_cores():
    logical_cores = psutil.cpu_count(logical=True)
    return(logical_cores)

def gather_physical_cores():
    physical_cores = psutil.cpu_count(logical=False)
    return(physical_cores)

def cpu_usage_per_logical(interval_time):
    usage_per_logical = psutil.cpu_percent(interval=5, percpu=True)

    index = 0
    usage = ""

    for item in usage_per_logical:
       newline = "Usage on cpu"+str(index)+" is "+str(item)+"%\n"
       usage = usage + newline
       index += 1
    return(usage) 
