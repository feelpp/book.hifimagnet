from __future__ import unicode_literals
import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
import matplotlib.pyplot as plt

import pandas as pd

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", help="input txt file (ex. prob_volt.data")
parser.add_argument("--exp_file", help="experimental data txt file (ex. prob_volt.data)")
parser.add_argument("--bp", help="activate BP probes", action='store_true')
parser.add_argument("--plot", help="activate plot", action='store_true')
args = parser.parse_args()

input_file = args.input_file

# Import Dataset
df = pd.read_csv(input_file, sep='\s+', engine='python', skiprows=[1])
keys = df.columns.values.tolist()
#print ("keys=", len(keys))

# print (df['potential'])
# df['U'] = df['potential'] - df['potential'][0]
# print (df['U'])

# Import Exp Data
exp = pd.read_csv(args.exp_file, sep='\s+', engine='python', skiprows=1)
keys = exp.columns.values.tolist()
# print (keys)
# print (exp['Ucoil1'])

index_max = 8
if args.bp:
    index_max = 15

Uprobes = []    
output=""
header=""
for i in range(1,index_max):
    numkey = "U%d" % i
    Uprobes.append("Ucoil%d" % i)
    exp[numkey] = exp.apply(lambda row: df['potential'][i] - df['potential'][i-1], axis=1)
    # print (numkey, (df['potential'][i] - df['potential'][i-1]))
    output += "%s " % str(df['potential'][i] - df['potential'][i-1])
    header += "%s[V]\t" % numkey
print (header)
print (output)

if args.plot:    
    ax = plt.gca()
    # loop over key
    for key in Uprobes:
        numkey = key.replace("coil",'')
        #print (key, numkey)
        if key in keys:
            exp.plot(x='Time', y=key, ax=ax)
            color = ax.get_lines()[-1].get_color() 
            # print ("color=", color)
            exp.plot(x='Time', y=numkey, style="^", markevery=800, color=color, ax=ax) #
        else:
            print( "unknown key: %s" % args.plot_vs_time )
            print( "valid keys: ", keys )
            exit(1)
    plt.show()
