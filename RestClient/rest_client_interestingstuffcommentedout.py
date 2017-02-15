#!/usr/bin/env python3

import requests
import pprint
import json
import time

MAXRECORDS = 10
RETRIES = 3

BASEURL = "http://localhost:8080/todo/api/tasks"

def get_http_status_code(r):
  return(r.status_code)
 
def send_http_command(command, payload, url, expected_code):

    attempts = 1
    while (attempts <= RETRIES):
       if command == 'POST':
          r = requests.post(url, json=payload)
          status = get_http_status_code(r)
          if status == 201:
             attempts = RETRIES + 1
             print("Post was successful")
          else:
             attempt += 1      
             print("Post was unsuccessful - will wait and retry")
             sleep(1)
       elif command == 'PUT':
          r = requests.put(url, json=payload)
          status = get_http_status_code(r)
          if status == 200:
             attempts = RETRIES + 1
             print("Put was successful")
          else:
             attempt += 1      
             print("Put was unsuccessful - will wait and retry")
             sleep(1)
       elif command == 'DELETE':
          r = requests.delete(url, json=payload) 
          status = get_http_status_code(r)
          if status == 200:
             attempts = RETRIES + 1
             print("Delete was successful")
          else:
             attempt += 1      
             print("Delete was unsuccessful - will wait and retry")
             sleep(1)
       elif command == 'GET':
          r = requests.get(url) 
          status = get_http_status_code(r)
          if status == 200:
             attempts = RETRIES + 1
             print("Get was successful")
          else:
             attempt += 1      
             print("Get was unsuccessful - will wait and retry")
             sleep(1)
       else:
           print("Tragedy has occurred.  Exiting")
           exit(99)
    return(r)

print("                                 << Dumping records >>                             ")
print("===================================================================================")
#r = requests.get(BASEURL)
r = send_http_command("GET", "", BASEURL, 200)
#print("Status Code %s" % get_http_status_code(r))
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(r.json())
print("===================================================================================\n")
time.sleep(3)

print("                                 << Inserting records >>                           ")
print("===================================================================================")
for i in range(2,MAXRECORDS+1):
   title_str = "One: task#"+str(i)
   desc_str = "Actions to take for task #"+str(i)
   payload = {'title':title_str, 'description':desc_str}
   print("Inserting ->", payload)
   #r = requests.post(BASEURL, json=payload)
   r = send_http_command("POST", payload, BASEURL, 201)
   #print(r.headers)
   #print(r.text)
   #print(r.status_code)
   print("-----------------------------------------------------------------------------------")
   time.sleep(1)

print("\n")
print("                                 << Dumping records >>                             ")
print("===================================================================================\n")
r = requests.get(BASEURL)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(r.json())
print("===================================================================================\n")
#record_count = r.text.count("id")
#print("There are %s records" % record_count)
time.sleep(3)


print("                                 << Updating records >>                           ")
print("===================================================================================")
for i in range(1,MAXRECORDS+1):
   NEWURL = BASEURL + "/" + str(i) 
   payload = {'done':True}
   print("setting %s on %s" % (payload, NEWURL))
   r = send_http_command("PUT", payload, NEWURL, 200)
   #print(r.status_code)
   #print(r.headers)
   #print(r.text)
   print("-----------------------------------------------------------------------------------")
   time.sleep(1)

print("\n")
print("                                 << Dumping records >>                             ")
print("===================================================================================\n")
r = requests.get(BASEURL)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(r.json())
print("===================================================================================\n")
time.sleep(3)



print("                                  << Purging  records >>                           ")
print("===================================================================================")
for i in range(2,MAXRECORDS+1):
   NEWURL = BASEURL + "/" + str(i)
   payload = {'id':i}
   print("Deleting record %s on %s" % (payload, NEWURL))
   #r = requests.delete(NEWURL, json=payload) 
   r = send_http_command("DELETE", payload, NEWURL, 200)
   #print(r.headers)
   #print(r.text)
   print("-----------------------------------------------------------------------------------")
   time.sleep(1)


print("\n")
print("                                 << Dumping records >>                             ")
print("===================================================================================\n")
r = requests.get(BASEURL)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(r.json())
#print(r.headers)
#print("___________________________________")
#print(r.text)
print("===================================================================================\n")
time.sleep(3)

print("\n")
print("                              << Updating base record >>                             ")
print("===================================================================================\n")
NEWURL = BASEURL + "/" + str(1) 
payload = {'done':False}
print("Updating record %s with %s" % (NEWURL, payload))
r = requests.put(NEWURL, json=payload)
#print(r.headers)
#print(r.text)

print("\n")
print("                                 << Dumping records >>                             ")
print("===================================================================================\n")
r = requests.get(BASEURL)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(r.json())
print("===================================================================================\n")
