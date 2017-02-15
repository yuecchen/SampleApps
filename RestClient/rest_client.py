#!/usr/bin/env python3

import requests
import pprint
import json
import time
import argparse


MAXRECORDS = 10
RETRIES = 3

BASEURL = "http://localhost:8080/todo/api/tasks"

parser = argparse.ArgumentParser()
parser.add_argument("--url", help="The URL to manipulate ReST API",
                    type=str)
parser.add_argument("--records", help="The number of records to insert into the ReST API",
                    type=int)
args = parser.parse_args()

if args.url:
   BASEURL = args.url
#else:
#   print("You most enter a URL")

if args.records:
   MAXRECORDS = args.records


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

while True:
   print("                                 << Dumping records >>                             ")
   print("===================================================================================")
   r = send_http_command("GET", "", BASEURL, 200)
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
      r = send_http_command("POST", payload, BASEURL, 201)
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


   print("                                 << Updating records >>                           ")
   print("===================================================================================")
   for i in range(1,MAXRECORDS+1):
      NEWURL = BASEURL + "/" + str(i) 
      payload = {'done':True}
      print("setting %s on %s" % (payload, NEWURL))
      r = send_http_command("PUT", payload, NEWURL, 200)
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
      r = send_http_command("DELETE", payload, NEWURL, 200)
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

   print("\n")
   print("                              << Updating base record >>                             ")
   print("===================================================================================\n")
   NEWURL = BASEURL + "/" + str(1) 
   payload = {'done':False}
   print("Updating record %s with %s" % (NEWURL, payload))
   r = requests.put(NEWURL, json=payload)

   print("\n")
   print("                                 << Dumping records >>                             ")
   print("===================================================================================\n")
   r = requests.get(BASEURL)
   pp = pprint.PrettyPrinter(indent=4)
   pp.pprint(r.json())
   print("===================================================================================\n")
