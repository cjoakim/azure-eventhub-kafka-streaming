
# Ad-hoc program to validate JSON file content.
# Chris Joakim, Microsoft, 2020/06/29

import copy
import json

import os
import random
import sys
import time
import traceback

def read_json(infile):
    with open(infile, 'rt') as f:
        return json.loads(f.read())

# python json_check.py tmp/f2.json

if __name__ == '__main__':
    infile = sys.argv[1]
    print('infile: {}'.format(infile))

    obj = read_json(infile)
    print(obj)
