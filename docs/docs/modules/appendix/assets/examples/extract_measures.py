#!/usr/bin/env python

from __future__ import unicode_literals

import pandas as pd

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input", help="input cvs file (ex. thermo-electric.electric.measures.csv)")
parser.add_argument("--keys", help="output key(s)")
parser.add_argument("--list", help="display available keys", action='store_true')
args = parser.parse_args()

input_file = args.input

# Import Dataset
df = pd.read_csv(input_file, sep=',\s+', engine='python')

# Get Name of columns
keys = df.columns.values.tolist()
if args.list:
    print "Valid keys are: ", keys

if args.keys:
    ukeys = args.keys.split(";")
    for ukey in ukeys:
        if ukey in keys:
            print df[ukey].values.tolist()
        else:
            print "Unknow key: %s" % ukey
            print "Valid keys are: ", keys
            exit(1)

