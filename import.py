#!/usr/bin/env python3
import lineOC
import pickle
import sys

if len(sys.argv) != 3:
    print("usage: "+sys.argv[0]+" [LOGFILE] [OUTPUT_NAME]")
    sys.exit(1)

f = open(sys.argv[1], encoding="utf-8")
talks = lineOC.parser(f.read())
f.close()

with open(sys.argv[2]+".pickle",mode="wb") as f:
    pickle.dump(talks,f)