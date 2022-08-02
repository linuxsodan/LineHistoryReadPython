#!/usr/bin/env python3
from pprint import pprint
import pickle
import sys
if len(sys.argv) != 2:
    print("usage: "+sys.argv[0]+" [PICKLE FILE]")
    sys.exit(1)

talks ={}
with open(sys.argv[1],mode="rb") as f:
    talks = pickle.load(f)

# pprint(talks)

for talk in talks:
    print("================================================")
    print("NAME = "+talk['name'])
    print("DATE = "+str(talk['date']))
    print("WHAT = "+talk['comm'])

