#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--url", help="The URL to manipulate ReST API",
                    type=str)
parser.add_argument("--records", help="The number of records to insert into the ReST API",
                    type=str)
args = parser.parse_args()
print(args.url)

if args.records:
   print("records = %s" % args.records)
