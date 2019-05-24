from __future__ import unicode_literals
import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
import matplotlib.pyplot as plt

import pandas as pd
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", help="input file (ex. V_cmp.dat)")
parser.add_argument("--title", help="title (ex. V_cmp)", type=str, default="Compare V probes")
parser.add_argument("--show", help="show graph", action='store_true')
args = parser.parse_args()

input_file = args.input_file
title = args.title

print ("title=%s" % title)
# Import Dataset
df = pd.read_csv(input_file, sep='\s+', engine='python')

# Get Name of columns
keys = df.columns.values.tolist()
print "keys=", keys, len(keys)

dx = df[['Ucoil1','Ucoil2','Ucoil3','Ucoil4','Ucoil5','Ucoil6','Ucoil7']].plot(kind='bar', title ="V comp", figsize=(15, 10), legend=True, fontsize=12, rot=0)
dx.set_xticklabels(df['Type'])

# dx.set_xlabel("Type", fontsize=12)
dx.set_ylabel("V", fontsize=12)
plt.grid('on', which='major', axis='y' )
plt.title(args.title)
if args.show:
    plt.show()
else:
    plt.savefig('V_cmp.png')
