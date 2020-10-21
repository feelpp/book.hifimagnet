from __future__ import unicode_literals
import os
import sys
import glob
import argparse
import pandas as pd
import numpy as np
import matplotlib
# print("matplotlib=", matplotlib.rcParams.keys())
# matplotlib.rcParams['text.latex.unicode'] = True key not available
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", help="input txt file (ex. HL31_2018.04.13.txt)")
args = parser.parse_args()

skiprows=0
input_file = args.input_file
print("input_file=", input_file )

ax = plt.gca()

if input_file.endswith(".csv"):
    skiprows=2

if '*' in input_file:
    pwdpath = os.getcwd()
    path = os.path.join( pwdpath, input_file)
    for file in glob.glob(path):
        with open(file, 'r') as f:
            df = pd.read_csv(f, skiprows=skiprows)
            print(input_file.split('*'))
            print(str(pwdpath))
            label = file.replace(str(pwdpath)+"/",'').replace(input_file.split('*')[0],'').replace(input_file.split('*')[1],'')
            print("label=%s", label)
            df.plot(x='   X-Coord   ', y=' My_thermo_electric_heat_temperature', label="H%s" % label, ax=ax)
else:
    # Import Dataset
    df = pd.read_csv(input_file, skiprows=skiprows)

    # Get Name of columns
    keys = df.columns.values.tolist()
    print("keys(%d)=" % len(keys), keys)

plt.grid (b=None)
plt.xlabel(r'x[m]')
plt.ylabel(r'T[C]')

plt.show()
# imagefile = input_file.replace(".txt", "")
# plt.savefig('%s_vs_time.png' % imagefile, dpi=300 )
