#!/usr/bin/env python3
import re
import parser
from pprint import pprint
import sys

out = parser.line_history_parse(sys.argv[1])

pprint(out)

#ith open("test.csv", "w", encoding="utf-8") as f:
#   f.write(outputs_csv)
