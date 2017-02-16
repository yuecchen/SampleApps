#!/usr/bin/env python3
from __future__ import print_function
from flask import Flask, request, url_for, redirect, render_template, jsonify, abort, Response
from collections import OrderedDict
import multiprocessing 
import datetime
import time
import os
import platform
import sys
import logging
import psutil
import random
import math
import socket
import json
from decimal import *
from libraries.environmentlib import *
from libraries.testslib import *
from functools import wraps

FQ_HOSTNAME = socket.getfqdn()
#TODO_API = 'http://'+FQ_HOSTNAME+'/todo/api/tasks'
TODO_API = ""
API_ONE = ""
API_TWO = ""
API_THREE = ""
API_FOUR = ""
API_FIVE = ""
API_SIX = ""
API_SEVEN = "" 
API_EIGHT = ""
API_NINE = ""
API_SUBONE = ""
API_SUBNINE = ""
API_SECURE = ""
API_CODE = ""
API_GETMINI = ""
API_GETSMALL = ""
API_GETMEDIUM = ""
API_GETLARGE = ""
API_GETXL = ""
API_GETXXL = ""
API_GETXXXL = ""
API_PUTSIM = ""
API_POSTSIM = ""
API_DELETESIM = ""
API_TUNER = ""
CPU_USAGE_INTERVAL = 5
TIMEBOMB_SET = False
BOMB_TIME = datetime.datetime.fromtimestamp(0).strftime('%m-%d-%Y %H:%M:%S')
LOGIN = 'admin' 
PASSWD = 'password'
WEB_STATUS_CODE = 200
API_STATUS_CODE = 200
WEB_DELAY_TIME = 1 
API_DELAY_TIME = 1 
APP_MEM  = 0
APP_DISK = 0
APP_NAME = ""
APP_URI = ""
APP_VER = ""
APP_ID = ""
INST_ID = ""
INST_IDX = ""
APP_HOST = ""
APP_PORT = ""

#TIMEBOMB_SET = TrueG

app = Flask(__name__)

app.config.update(
    Debug = True,
    PROPOGATE_EXCEPTIONS = True
)

def build_api_urls():
    global TODO_API, APP_URI, API_CODE
    global API_ONE, API_TWO, API_THREE
    global API_FOUR, API_FIVE, API_SIX
    global API_SEVEN, API_EIGHT, API_NINE
    global API_SUBONE, API_SUBNINE, API_SECURE
    global API_GETMINI, API_GETSMALL, API_GETMEDIUM
    global API_GETLARGE, API_GETXL, API_GETXXL
    global API_GETXXXL, API_PUTSIM, API_POSTSIM
    global API_DELETESIM, API_TUNER
    global API_DELETESIMSECURED, API_POSTSIMSECURED, API_PUTSIMSECURED

    TODO_API = 'http://'+APP_URI+'/todo/api/tasks'
    API_CODE = 'http://'+APP_URI+'/code/api'
    API_ONE = 'http://'+APP_URI+'/delay/api/one'
    API_TWO = 'http://'+APP_URI+'/delay/api/two'
    API_THREE = 'http://'+APP_URI+'/delay/api/three'
    API_FOUR = 'http://'+APP_URI+'/delay/api/four'
    API_FIVE = 'http://'+APP_URI+'/delay/api/five'
    API_SIX = 'http://'+APP_URI+'/delay/api/six'
    API_SEVEN = 'http://'+APP_URI+'/delay/api/seven'
    API_EIGHT = 'http://'+APP_URI+'/delay/api/eight'
    API_NINE = 'http://'+APP_URI+'/delay/api/nine'
    API_SUBONE = 'http://'+APP_URI+'/delay/api/subone'
    API_SUBNINE = 'http://'+APP_URI+'/delay/api/subnine'
    API_SECURE = 'http://'+APP_URI+'/secure/api'
    API_GETMINI = 'http://'+APP_URI+'/method/api/get/mini'
    API_GETSMALL = 'http://'+APP_URI+'/method/api/get/small'
    API_GETMEDIUM = 'http://'+APP_URI+'/method/api/get/medium'
    API_GETLARGE = 'http://'+APP_URI+'/method/api/get/large'
    API_GETXL = 'http://'+APP_URI+'/method/api/get/xl'
    API_GETXXL = 'http://'+APP_URI+'/method/api/get/xxl'
    API_GETXXXL = 'http://'+APP_URI+'/method/api/get/xxxl'
    API_PUTSIM = 'http://'+APP_URI+'/method/api/put/sim'
    API_PUTSIMSECURED = 'http://'+APP_URI+'/method/api/put/secured/sim'
    API_POSTSIM = 'http://'+APP_URI+'/method/api/post/sim'
    API_POSTSIMSECURED = 'http://'+APP_URI+'/method/api/post/secured/sim'
    API_DELETESIM = 'http://'+APP_URI+'/method/api/delete/sim'
    API_DELETESIMSECURED = 'http://'+APP_URI+'/method/api/delete/secured/sim'
    API_TUNER = 'http://'+APP_URI+'/delay/api/tunable'
    return

def parse_vcap_application(app_info):
    global APP_MEM, APP_DISK, APP_NAME, APP_URI
    global APP_VER, APP_ID, INST_ID, INST_IDX
    global APP_HOST, APP_PORT

    start = '"mem":'
    end = ','
    APP_MEM=app_info.split(start)[1].split(end)[0]

    start = '"disk":'
    end = '},'
    APP_DISK=(app_info.split(start)[1].split(end)[0])

    start = '"application_name":"'
    end = '",'
    APP_NAME=(app_info.split(start)[1].split(end)[0])

    start = '"application_uris":["'
    end = '"],'
    APP_URI=(app_info.split(start)[1].split(end)[0])

    start = '"application_version":"'
    end = '",'
    APP_VER=(app_info.split(start)[1].split(end)[0])

    start = '"application_id":"'
    end = '",'
    APP_ID=(app_info.split(start)[1].split(end)[0])

    start = '"instance_id":"'
    end = '",'
    INST_ID=(app_info.split(start)[1].split(end)[0])

    start = '"instance_index":'
    end = ','
    INST_IDX=(app_info.split(start)[1].split(end)[0])

    start = '"host":"'
    end = '",'
    APP_HOST=(app_info.split(start)[1].split(end)[0])

    start = '"port":'
    end = ','
    APP_PORT=(app_info.split(start)[1].split(end)[0])

    return

def check_auth(username, password):
    global LOGIN
    global PASSWD
    """This function is called to check if a username /
    password combination is valid.
    """
    #return username == 'admin' and password == 'secret'
    return username == LOGIN and password == PASSWD

def authenticate():
    """Sends a 401 response that enables basic auth"""
    print("************************************************")
    print("*   << Bad credentials have been received >>   *")
    print("************************************************")
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/secure/api', methods=['GET'])
@requires_auth
def secure_api():
    return jsonify({'Secure':'Login'})


@app.route('/code/api', methods=['GET'])
def code_api():
    global API_STATUS_CODE
    return_code = API_STATUS_CODE
    return jsonify({'API Status Code':return_code}), return_code


def setup_tasks():
   tasker = [
       {
           'id': 1,
           'title': u'One: task#1',
           'description': u'Actions to take for task #1', 
           'done': False
       },
   ]
   return(tasker)

# On BlueMix, get the port number from the environment variable VCAP_APP_PORT
# when running the app locally, default the port to 8080
port = int(os.getenv('VCAP_APP_PORT', 8080))

# Pull the VCAP_APPLICATION info from BlueMix/CF 
# When running locally for testing comment out the getenv and go with the mocked up
# data.  Also vice versa
app_info = os.getenv('VCAP_APPLICATION', "")
#app_info = '{"limits":{"fds":16384,"mem":512,"disk":1024},"application_name":"WinkPatTry","application_uris":["winkpattry.stage1.mybluemix.net"],"name":"WinkPatTry","space_name":"dev","space_id":"21ee0aba-918c-408b-b7a2-5639c2b6f5dd","uris":["winkpattry.stage1.mybluemix.net"],"users":null,"version":"26da2ea9-f922-4993-b0a8-b53a86e3b23b","application_version":"26da2ea9-f922-4993-b0a8-b53a86e3b23b","application_id":"af164696-f8c5-457d-8f81-dd61f2645e13","instance_id":"c2bcb11fa49a4935a296c812aa27f8a3","instance_index":0,"host":"0.0.0.0","port":64602,"started_at":"2016-07-10 16:53:00 +0000","started_at_timestamp":1468169580,"start":"2016-07-10 16:53:00 +0000","state_timestamp":1468169580}'


tasks = setup_tasks()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/method/api/get/mini', methods=['GET'])
def get_api_mini():
    mini_data = generate_json_data(int(10),int(101))
    return Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')

@app.route('/method/api/get/small', methods=['GET'])
def get_api_small():
    mini_data = generate_json_data(int(50),int(1001))
    return Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')

@app.route('/method/api/get/medium', methods=['GET'])
def get_api_medium():
    mini_data = generate_json_data(int(100),int(5001))
    return Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')

@app.route('/method/api/get/large', methods=['GET'])
def get_api_large():
    mini_data = generate_json_data(int(100),int(10001))
    return Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')

@app.route('/method/api/get/xl', methods=['GET'])
def get_api_xl():
    mini_data = generate_json_data(int(500),int(100001))
    return Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')

@app.route('/method/api/get/xxl', methods=['GET'])
def get_api_xxl():
    mini_data = generate_json_data(int(750),int(500001))
    return Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')

@app.route('/method/api/get/xxxl', methods=['GET'])
def get_api_xxxl():
    mini_data = generate_json_data(int(1000),int(1000001))
    return Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')

@app.route('/method/api/delete/sim', methods=['DELETE','GET'])
def simulated_delete():

    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    print("************************************************")
    print("*        << DELETE has been received >>        *")
    print("************************************************")
    print("*           %s                *" % current_time)
    print("************************************************")
    return jsonify({'DELETE Simulation': 'Done'})

@app.route('/method/api/delete/secured/sim', methods=['DELETE','GET'])
@requires_auth
def simulated_delete_secured():
    global LOGIN, PASSWD

    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    print("************************************************")
    print("*   << Secured DELETE has been received >>     *")
    print("************************************************")
    print("*           %s                *" % current_time)
    print("* Username:           %s                *" % LOGIN)
    print("* Password:           %s                *" % PASSWD)
    print("************************************************")
    return jsonify({'Secured DELETE Simulation': 'Done'})

@app.route('/method/api/put/sim', methods=['PUT','GET'])
def simulated_put():

    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')

    if request.method == 'PUT':
       data = request.get_json() 
       print("************************************************")
       print("*        << PUT has been received >>           *")
       print("************************************************")
       print("*           %s                *" % current_time)
       print("************************************************")
       print("*           Received JSON Data below           *")
       print("************************************************")
       print("%s" % data)
       print("************************************************")
    return jsonify({'PUT Simulation': 'Done'})

@app.route('/method/api/put/secured/sim', methods=['PUT','GET'])
@requires_auth
def simulated_put_secured():

    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')

    if request.method == 'PUT':
       data = request.get_json() 
       print("************************************************")
       print("*   << Secured PUT has been received >>        *")
       print("************************************************")
       print("*           %s                *" % current_time)
       print("************************************************")
       print("*           Received JSON Data below           *")
       print("************************************************")
       print("%s" % data)
       print("************************************************")
       print("* Username:           %s                *" % LOGIN)
       print("* Password:           %s                *" % PASSWD)
       print("************************************************")
    return jsonify({'Secured PUT Simulation': 'Done'})

@app.route('/method/api/post/sim', methods=['POST','GET'])
def simulated_post():

    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
       data = request.get_json() 
       print("************************************************")
       print("*        << POST has been received >>          *")
       print("************************************************")
       print("*           %s                *" % current_time)
       print("************************************************")
       print("*           Received JSON Data below           *")
       print("************************************************")
       print("%s" % data)
       print("************************************************")
    return jsonify({'POST Simulation': 'Done'})

@app.route('/method/api/post/secured/sim', methods=['POST','GET'])
@requires_auth
def simulated_post_secured():
    global LOGIN, PASSWD

    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
       data = request.get_json() 
       print("************************************************")
       print("*    << Secured POST has been received >>      *")
       print("************************************************")
       print("*           %s                *" % current_time)
       print("************************************************")
       print("*           Received JSON Data below           *")
       print("************************************************")
       print("%s" % data)
       print("************************************************")
       print("* Username:           %s                *" % LOGIN)
       print("* Password:           %s                *" % PASSWD)
       print("************************************************")
    return jsonify({'Secured POST Simulation': 'Done'})

@app.route('/delay/api/subone', methods=['GET'])
def get_delay_subone():
    subone_wait_raw = random.random()
    time.sleep(subone_wait_raw)
    subone_wait_round = Decimal(subone_wait_raw).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    subone_wait = str(subone_wait_round)
    return jsonify({'Delay:': subone_wait})

@app.route('/delay/api/subnine', methods=['GET'])
def get_delay_subnine():
    subnine_wait_raw = random.uniform(0, 9)
    time.sleep(subnine_wait_raw)
    subnine_wait_round = Decimal(subnine_wait_raw).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    subnine_wait = str(subnine_wait_round)
    return jsonify({'Delay:': subnine_wait})

@app.route('/delay/api/one', methods=['GET'])
def get_delay_one():
    time.sleep(1)
    return jsonify({'Delay:': 'One second'})

@app.route('/delay/api/two', methods=['GET'])
def get_delay_two():
    time.sleep(2)
    return jsonify({'Delay:': 'Two seconds'})

@app.route('/delay/api/three', methods=['GET'])
def get_delay_three():
    time.sleep(3)
    return jsonify({'Delay:': 'Three seconds'})

@app.route('/delay/api/four', methods=['GET'])
def get_delay_four():
    time.sleep(4)
    return jsonify({'Delay:': 'Four seconds'})

@app.route('/delay/api/five', methods=['GET'])
def get_delay_five():
    time.sleep(5)
    return jsonify({'Delay:': 'Five seconds'})

@app.route('/delay/api/six', methods=['GET'])
def get_delay_six():
    time.sleep(6)
    return jsonify({'Delay:': 'Six seconds'})

@app.route('/delay/api/seven', methods=['GET'])
def get_delay_seven():
    time.sleep(7)
    return jsonify({'Delay:': 'Seven seconds'})

@app.route('/delay/api/eight', methods=['GET'])
def get_delay_eight():
    time.sleep(8)
    return jsonify({'Delay:': 'Eight seconds'})

@app.route('/delay/api/nine', methods=['GET'])
def get_delay_nine():
    time.sleep(9)
    return jsonify({'Delay:': 'Nine seconds'})

@app.route('/todo/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/todo/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]

    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/todo/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


@app.route('/todo/api/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/cpu_util_page', methods=['GET', 'POST'])
def cpu_util_page():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    logical_core_usage = cpu_usage_per_logical(CPU_USAGE_INTERVAL)
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))
 
    return render_template('cpuutilization.html', current_time=current_time, logical_core_usage=logical_core_usage)


@app.route('/under_construction_page', methods=['GET', 'POST'])
def under_construction_page():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        return redirect(url_for('index'))
 
    return render_template('under_construction_page.html')

@app.route('/secure_rest_api', methods=['GET', 'POST'])
def secure_rest_api():
    global LOGIN
    global PASSWD
    global API_SECURE
	
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        if request.form['submit'] == 'SetCredentials':
           id_button_setting = request.form.get("IdRadio")
           print(id_button_setting)
           LOGIN = id_button_setting
           pw_button_setting = request.form.get("PwRadio")
           print(pw_button_setting)
           PASSWD = pw_button_setting
           return redirect(url_for('secure_rest_api'))
        elif request.form['submit'] == 'Return':
           print("Return button clicked?")
           return redirect(url_for('index'))
        else:
           return redirect(url_for('index'))

    return render_template('secure_rest_api.html', current_time=current_time, userid=LOGIN, password=PASSWD, apisecure=API_SECURE)

@app.route('/api_method', methods=['GET', 'POST'])
def api_method():
    global API_GETMINI
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling:
        if request.form['submit'] == 'GoHome':
           print("Go Home button clicked")
           return redirect(url_for('index'))
        else:
           return redirect(url_for('index'))
    return render_template('api_method.html', current_time=current_time, getmini=API_GETMINI, getsmall=API_GETSMALL, getmedium=API_GETMEDIUM, getlarge=API_GETLARGE, getxl=API_GETXL, getxxl=API_GETXXL, getxxxl=API_GETXXXL, putsim=API_PUTSIM, putsimsecured=API_PUTSIMSECURED, postsim=API_POSTSIM, postsimsecured=API_POSTSIMSECURED, deletesim=API_DELETESIM, deletesimsecured=API_DELETESIMSECURED)

@app.route('/rest_api', methods=['GET', 'POST'])
def rest_api():
    global tasks
    global TODO_API
    global API_ONE, API_TWO, API_THREE
    global API_FOUR, API_FIVE, API_SIX
    global API_SEVEN, API_EIGHT, API_NINE
    global API_SUBONE, API_SUBNINE

    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    task_info = "\n".join(str(task) for task in tasks)

    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        if request.form['submit'] == 'TaskReset':
           print("Task Reset button clicked")
           tasks = setup_tasks()
           #tasks = None
           return redirect(url_for('rest_api'))
        elif request.form['submit'] == 'GoHome':
           print("Go Home button clicked")
           return redirect(url_for('index'))
        elif request.form['submit'] == 'Refresh':
           print("Refresh button clicked")
           return redirect(url_for('rest_api'))
        else:
           return redirect(url_for('index'))
    return render_template('rest_api.html', current_time=current_time, task_info=task_info, todoapi=TODO_API, apione=API_ONE, apitwo=API_TWO, apithree=API_THREE, apifour=API_FOUR, apifive=API_FIVE, apisix=API_SIX, apiseven=API_SEVEN, apieight=API_EIGHT, apinine=API_NINE, apisubone=API_SUBONE, apisubnine=API_SUBNINE)

@app.route('/environmental', methods=['GET', 'POST'])
def environmental():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    cpu_info = gather_cpu_info()
    #print(cpu_info)
    logical_core_count = gather_logical_cores()
    #print(logical_core_count)
    physical_core_count = gather_physical_cores()
    #print(physical_core_count)
    cpu_endianess = gather_endianess_info()
    #print(cpu_endianess)
    pyth_ver = gather_python_info()
    #print(pyth_ver)
    net_info = gather_network_info()
    #print(net_info)
    total_memory = gather_mem_info("MemTotal")
    #print(total_memory)
    free_memory = gather_mem_info('MemFree')
    #print(free_memory) 
    avail_memory = gather_mem_info('MemAvailable')
    #print(avail_memory) 
    total_swap = gather_mem_info('SwapTotal')
    #print(total_swap) 
    free_swap = gather_mem_info('SwapFree')
    #print(free_swap) 
    os_type = gather_os_type()
    #print(os_type) 
    plat = gather_platform_info()
    #print(plat) 
    os_arch = gather_arch_info()
    #print(os_arch)
    os_kernel = gather_kernel_info()
    #print(os_kernel)
    os_distro = gather_distro_info()
    #print(os_distro)

    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        if request.form['submit'] == 'CPUUsage':
           print("CPU Usage button clicked")
           return redirect(url_for('cpu_util_page'))
        elif request.form['submit'] == 'GoHome':
           print("Go Home button clicked")
           return redirect(url_for('index'))
        elif request.form['submit'] == 'Refresh':
           print("refresh button clicked")
           return redirect(url_for('environmental'))
        else:
           return redirect(url_for('index'))
          
    # show the form, it wasn't submitted
    return render_template('environmental.html', current_time=current_time, cpu_info=cpu_info, logical_core_count=logical_core_count, physical_core_count=physical_core_count, cpu_endianess=cpu_endianess, total_memory=total_memory, free_memory=free_memory, avail_memory=avail_memory, total_swap=total_swap, free_swap=free_swap, os_type=os_type, plat=plat, os_arch=os_arch, os_kernel=os_kernel, os_distro=os_distro, net_info=net_info, pyth_ver=pyth_ver, appmem=APP_MEM, appdisk=APP_DISK, appname=APP_NAME, appuri=APP_URI, appver=APP_VER, appid=APP_ID, instid=INST_ID, instidx=INST_IDX, apphost=APP_HOST, appport=APP_PORT)

@app.route('/test_termination', methods=['GET', 'POST'])
def test_termination():
    global BOMB_TIME
    global TIMEBOMB_SET 

    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        if request.form['submit'] == 'KillCPUTest':
           print("Kill CPU button clicked")
           kill_process_by_name(b'runcpu')
           time.sleep(0.5)
           return redirect(url_for('test_status'))
        elif request.form['submit'] == 'KillTimeBomb':
           kill_process_by_name(b'timebomb')
           BOMB_TIME = datetime.datetime.fromtimestamp(0).strftime('%m-%d-%Y %H:%M:%S')
           TIMEBOMB_SET = False
           time.sleep(0.5)
           print("Kill button clicked")
           return redirect(url_for('test_status'))
        elif request.form['submit'] == 'KillMemTest':
           print("Kill button clicked")
           return redirect(url_for('under_construction_page'))
        else:
           return redirect(url_for('index'))
    return render_template('test_termination.html', current_time=current_time)

@app.route('/test_selection', methods=['GET', 'POST'])
def test_selection():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        if request.form['submit'] == 'GoISE':
           print("ISE button clicked")
           force_ise()
           return redirect(url_for('index'))
        elif request.form['submit'] == 'GoKill':
           print("Kill button clicked")
           return redirect(url_for('under_construction_page'))
        elif request.form['submit'] == 'GoCrash':
           print("Crash button clicked")
           force_crash()
           return redirect(url_for('test_status'))
        elif request.form['submit'] == 'GoCPUTest':
           print("CPU Test button clicked")
           launch_cpu_tests()
           return redirect(url_for('test_status'))
        elif request.form['submit'] == 'GoMemTest':
           print("CPU Test button clicked")
           return redirect(url_for('under_construction_page'))
        else:
           return redirect(url_for('index'))
    # show the form, it wasn't submitted
    return render_template('test_selection.html', current_time=current_time)

@app.route('/test_status', methods=['GET', 'POST'])
def test_status():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if is_cputest_running():
       cpu_test_status = "CPU Test is active" 
    else:
       cpu_test_status = "CPU Test is not active" 
    
    if is_timebomb_running():
       timebomb_status = "Timebomb is active" 
    else:
       timebomb_status = "Timebomb is not active" 

    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('test_status.html', current_time=current_time, cpu_test_status=cpu_test_status, timebomb_status=timebomb_status, bombtime=BOMB_TIME)

@app.route('/web_delay_base', methods=['GET', 'POST'])
def web_delay_base():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('web_delay_base.html', current_time=current_time)

@app.route('/web_large_base', methods=['GET', 'POST'])
def web_large_base():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('web_large_base.html', current_time=current_time)


@app.route('/web_large_pull', methods=['GET', 'POST'])
def web_large_pull():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('web_large_pull.html', current_time=current_time)

@app.route('/web_delay_one', methods=['GET', 'POST'])
def web_delay_one():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    time.sleep(1) 
    if request.method == 'POST':
        return redirect(url_for('web_delay_base'))

    # show the form, it wasn't submitted
    return render_template('web_delay_one.html', current_time=current_time)

@app.route('/web_delay_subone', methods=['GET', 'POST'])
def web_delay_subone():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    subone_wait_raw = random.random()
    time.sleep(subone_wait_raw)
    subone_wait = Decimal(subone_wait_raw).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    if request.method == 'POST':
        return redirect(url_for('web_delay_base'))

    # show the form, it wasn't submitted
    return render_template('web_delay_subone.html', current_time=current_time, subone_wait=subone_wait)

@app.route('/web_delay_two', methods=['GET', 'POST'])
def web_delay_two():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    time.sleep(2) 
    if request.method == 'POST':
        return redirect(url_for('web_delay_base'))

    # show the form, it wasn't submitted
    return render_template('web_delay_two.html', current_time=current_time)

@app.route('/web_delay_three', methods=['GET', 'POST'])
def web_delay_three():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    time.sleep(3) 
    if request.method == 'POST':
        return redirect(url_for('web_delay_base'))

    # show the form, it wasn't submitted
    return render_template('web_delay_three.html', current_time=current_time)

@app.route('/web_delay_four', methods=['GET', 'POST'])
def web_delay_four():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    time.sleep(4) 
    if request.method == 'POST':
        return redirect(url_for('web_delay_base'))

    # show the form, it wasn't submitted
    return render_template('web_delay_four.html', current_time=current_time)

@app.route('/web_delay_five', methods=['GET', 'POST'])
def web_delay_five():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    time.sleep(5) 
    if request.method == 'POST':
        return redirect(url_for('web_delay_base'))

    # show the form, it wasn't submitted
    return render_template('web_delay_five.html', current_time=current_time)

@app.route('/web_delay_six', methods=['GET', 'POST'])
def web_delay_six():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    time.sleep(6) 
    if request.method == 'POST':
        return redirect(url_for('web_delay_base'))

    # show the form, it wasn't submitted
    return render_template('web_delay_six.html', current_time=current_time)

@app.route('/web_delay_seven', methods=['GET', 'POST'])
def web_delay_seven():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    time.sleep(7) 
    if request.method == 'POST':
        return redirect(url_for('web_delay_base'))

    # show the form, it wasn't submitted
    return render_template('web_delay_seven.html', current_time=current_time)

@app.route('/web_delay_eight', methods=['GET', 'POST'])
def web_delay_eight():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    time.sleep(8) 
    if request.method == 'POST':
        return redirect(url_for('web_delay_base'))

    # show the form, it wasn't submitted
    return render_template('web_delay_eight.html', current_time=current_time)

@app.route('/web_delay_nine', methods=['GET', 'POST'])
def web_delay_nine():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    time.sleep(9) 
    if request.method == 'POST':
        return redirect(url_for('web_delay_base'))

    # show the form, it wasn't submitted
    return render_template('web_delay_nine.html', current_time=current_time)

@app.route('/web_delay_subnine', methods=['GET', 'POST'])
def web_delay_subnine():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    subnine_wait_raw = random.uniform(0, 9)
    time.sleep(subnine_wait_raw)
    subnine_wait = Decimal(subnine_wait_raw).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    if request.method == 'POST':
        return redirect(url_for('web_delay_base'))

    # show the form, it wasn't submitted
    return render_template('web_delay_subnine.html', current_time=current_time, subnine_wait=subnine_wait)

@app.route('/web_mini', methods=['GET', 'POST'])
def web_mini():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        return redirect(url_for('web_large_base'))

    mini_data = generate_json_data(int(10),int(101))
    #display_data=Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')
    display_data = json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': '))
    # show the form, it wasn't submitted
    return render_template('web_mini.html', current_time=current_time, display_data=display_data)

@app.route('/web_small', methods=['GET', 'POST'])
def web_small():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        return redirect(url_for('web_large_base'))

    mini_data = generate_json_data(int(50),int(1001))
    #display_data=Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')
    display_data = json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': '))
    # show the form, it wasn't submitted
    return render_template('web_small.html', current_time=current_time, display_data=display_data)

@app.route('/web_medium', methods=['GET', 'POST'])
def web_medium():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        return redirect(url_for('web_large_base'))

    mini_data = generate_json_data(int(100),int(5001))
    #display_data=Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')
    display_data = json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': '))
    # show the form, it wasn't submitted
    return render_template('web_medium.html', current_time=current_time, display_data=display_data)

@app.route('/web_large', methods=['GET', 'POST'])
def web_large():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        return redirect(url_for('web_large_base'))

    mini_data = generate_json_data(int(100),int(10001))
    #display_data=Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')
    display_data = json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': '))
    # show the form, it wasn't submitted
    return render_template('web_large.html', current_time=current_time, display_data=display_data)

@app.route('/web_xl', methods=['GET', 'POST'])
def web_xl():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        return redirect(url_for('web_large_base'))

    mini_data = generate_json_data(int(500),int(100001))
    #display_data=Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')
    display_data = json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': '))
    # show the form, it wasn't submitted
    return render_template('web_xl.html', current_time=current_time, display_data=display_data)

@app.route('/web_xxl', methods=['GET', 'POST'])
def web_xxl():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        return redirect(url_for('web_large_base'))

    mini_data = generate_json_data(int(750),int(500001))
    #display_data=Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')
    display_data = json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': '))
    # show the form, it wasn't submitted
    return render_template('web_xxl.html', current_time=current_time, display_data=display_data)

@app.route('/web_xxxl', methods=['GET', 'POST'])
def web_xxxl():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        return redirect(url_for('web_large_base'))

    mini_data = generate_json_data(int(1000),int(1000001))
    #display_data=Response(json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': ')), mimetype='application/json')
    display_data = json.dumps(mini_data, sort_keys=True,indent=4, separators=(',',': '))
    # show the form, it wasn't submitted
    return render_template('web_xxxl.html', current_time=current_time, display_data=display_data)

@app.route('/web_pix', methods=['GET', 'POST'])
def web_pix():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        return redirect(url_for('web_large_base'))

    return render_template('web_pix.html', current_time=current_time)

@app.route('/timebomb', methods=['GET', 'POST'])
def timebomb():
    global TIMEBOMB_SET
    global BOMB_TIME
 
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')

    if TIMEBOMB_SET:
      current_state_text = "set"
    else:
      current_state_text = "not set"


    if request.method == 'POST':
        if request.form['submit'] == 'StartTimebomb':
           print("Set Time Bomb button clicked")
           TIMEBOMB_SET = True
           button_setting = request.form.get("TgtTimeRadio")
           target_time = set_target_time(button_setting)
           BOMB_TIME = datetime.datetime.fromtimestamp(target_time).strftime('%m-%d-%Y %H:%M:%S')
           print(button_setting) 
           print("Current Target time is ") 
           print(ts) 
           print("Da Target time is ") 
           print(target_time)
           target_seconds = round(target_time - ts)
           print(target_seconds)
           launch_timebomb(target_seconds)
           time.sleep(0.3) 
           return redirect(url_for('test_status'))
        elif request.form['submit'] == 'Return':
           print("Return button clicked?")
           return redirect(url_for('index'))
        else:
           return redirect(url_for('index'))

    # show te form, it wasn't submitted
    return render_template('timebomb.html', current_time=current_time, timebomb_state = TIMEBOMB_SET, timebomb_state_text=current_state_text, bombtime = BOMB_TIME)

@app.route('/web_screenshot_test', methods=['GET', 'POST'])
def web_screenshot_test():
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('web_screenshot_test.html', current_time=current_time)

@app.route('/web_tunable_delay', methods=['GET', 'POST'])
def web_tunable_delay():
    global WEB_DELAY_TIME

    time.sleep(float(WEB_DELAY_TIME))
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('web_tunable_delay.html', current_time=current_time, web_wait=WEB_DELAY_TIME)

@app.route('/web_status_code', methods=['GET', 'POST'])
def web_status_code():
    global WEB_STATUS_CODE
    return_code = WEB_STATUS_CODE
    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('web_status_code.html', current_time=current_time, http_status=return_code), return_code
    #return render_template('web_status_code.html', http_status=return_code)

@app.route('/set_status_codes', methods=['GET', 'POST'])
def set_status_codes():
    global WEB_STATUS_CODE
    global API_STATUS_CODE
    global API_CODE

    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        if request.form['submit'] == 'SetAPICodes':
           print("Set API Codes")
           button_setting = request.form.get("APIRadio")
           API_STATUS_CODE = button_setting
           return redirect(url_for('set_status_codes'))
        if request.form['submit'] == 'SetWebCodes':
           print("Set Web Codes")
           button_setting = request.form.get("WebRadio")
           WEB_STATUS_CODE = button_setting
           return redirect(url_for('set_status_codes'))
        elif request.form['submit'] == 'Return':
           print("Return button clicked?")
           return redirect(url_for('index'))
        else:
           return redirect(url_for('index'))

    return render_template('set_status_codes.html', current_time=current_time, http_status_code=WEB_STATUS_CODE, api_status_code=API_STATUS_CODE, apicode=API_CODE)

@app.route('/delay/api/tunable', methods=['GET'])
def api_delay_tunable():
    global API_DELAY_TIME
    time.sleep(float(API_DELAY_TIME))
    wait_time = str(API_DELAY_TIME)
    return jsonify({'Delay:': wait_time})

@app.route('/set_tuner_time', methods=['GET', 'POST'])
def set_tuner_time():
    global WEB_DELAY_TIME
    global API_DELAY_TIME
    global API_TUNER

    ts = time.time()
    current_time = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y %H:%M:%S')
    if request.method == 'POST':
        if request.form['submit'] == 'SetAPITime':
           print("Set API Tunable Time")
           button_setting = request.form.get("APIRadio")
           API_DELAY_TIME = button_setting
           return redirect(url_for('set_tuner_time'))
        if request.form['submit'] == 'SetWebTime':
           print("Set Web Tunable Time")
           button_setting = request.form.get("WebRadio")
           WEB_DELAY_TIME = button_setting
           return redirect(url_for('set_tuner_time'))
        elif request.form['submit'] == 'Return':
           print("Return button clicked?")
           return redirect(url_for('index'))
        else:
           return redirect(url_for('index'))

    return render_template('set_tuner_time.html', current_time=current_time, web_tunable_delay=WEB_DELAY_TIME, api_tunable_delay=API_DELAY_TIME, apituner=API_TUNER)

@app.route('/info', methods=['GET', 'POST'])
def info():
    
    if request.method == 'POST':
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('info.html')

if __name__ == "__main__":
     #print(FQ_HOSTNAME)
     #print(TODO_API)
     parse_vcap_application(app_info)
     build_api_urls()
     app.run(host='0.0.0.0', port=port, debug=True)
#    app.run(host='0.0.0.0', port=port)
