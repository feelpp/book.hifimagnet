#!/usr/bin/env python
# encoding: UTF-8

from __future__ import unicode_literals
from scipy.optimize import curve_fit
import numpy as np
import matplotlib
# matplotlib.rcParams['text.usetex'] = True
# matplotlib.rcParams['text.latex.unicode'] = True
import matplotlib.pyplot as plt
import matplotlib.cm as mplcm
import matplotlib.colors as colors

import pandas as pd

import sys
import os

def polyfit(x, a0, a1, a2):
    return a0 + a1 * x + a2 * x**2

def extractdata(data, config, field, Currents, IB, input_water_temp):
    keys = data.columns.values.tolist()
    for key in keys:
        if key != args.field:
            del data[key]
    data.rename({args.field: 'init'}, axis=1, inplace=True)
    #print ("init data:", data)

    for n,I in enumerate(Currents):
        configname="%s_I%d_IB_%d_Tin%d_cooling" % (config, I, IB, input_water_temp)
        input_file=configname + ".dat"
        print ("Load data for I=%g A: %s" % (I,input_file) )

        df = pd.read_csv(input_file, sep='\s+', engine='python', skiprows=1)
        df.drop(df.tail(2).index,inplace=True)

        keys = df.columns.values.tolist()
        for key in keys:
            isnum=pd.api.types.is_numeric_dtype(df[key])
            # print ("df[%s] numeric? %s" % (key,isnum ) )
            if not isnum:
                df[key] = pd.to_numeric(df[key])

        # print ("keys=", keys)
        # print ("H=", df['H'])
        # print ("R=", df['R[Ohm]'])
    
        #color = scalarMap.to_rgba(n)
        #df.plot(x='H', y='R[Ohm]', ax=ax, kind="bar", grid=True, color=color)

        data[field] = df[field]
        data.rename({field: "%d A" % I}, axis=1, inplace=True)

    del data['init']
    # print ("data:", data)
    return data

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--config", help="input txt file (ex. HL-31-Cu5Ag-gmsh)")
parser.add_argument("--nhelices", help="number of helices (default 14)", type=int, default=14)
parser.add_argument("--input_water_temp", help="water temperature at input [Celsius] (integer only)", type=int, default=20)
parser.add_argument("--bitter_current", help="Bitter current [A] (integer only)", type=int, default=0)
parser.add_argument("--supra_current", help="Supra current [A] (integer only)", type=int, default=0)
parser.add_argument("--field", help="select field to plot (default Flux[])", type=str, default='Flux[]')
parser.add_argument("--show", help="display graphs instead of saving them (png format)", action='store_true')
args = parser.parse_args()


IB=args.bitter_current
Nhelices=14
NChannels=Nhelices+1

Currents=[600,900,1000,2500,5000,7500,10000,12500,15000,17500,20000,22500,25000,27500,27900,28000,29000,30000,31000]
# Currents.reverse()

# Generate colormap
# see https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
NUM_COLORS = len(Currents)
cm = plt.get_cmap('nipy_spectral') # 'gist_rainbow'
cNorm  = colors.Normalize(vmin=0, vmax=NUM_COLORS-1)
scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)

ax = plt.gca()

configname="%s_I%d_IB_%d_Tin%d_cooling" % (args.config, Currents[0], IB, args.input_water_temp)
input_file=configname + ".dat"

if not os.path.isfile(input_file):
    print ("%s no such file" % input_file)
    sys.exit(1)

resistance = pd.read_csv(input_file, sep='\s+', engine='python', skiprows=1)
keys = resistance.columns.values.tolist()
if not args.field in keys:
    print ("Invalid field %s" % args.field)
    print ("Valid keys are: ",keys)
    sys.exit(1)

resistance.drop(resistance.tail(2).index,inplace=True)
resistance = extractdata(resistance, args.config, args.field, Currents, IB, args.input_water_temp)    

#resistance.plot.bar()
resistance.plot(ax=ax, kind="bar", grid=True, colormap=cm)
ax.legend(["I=%d A" % I for I in Currents])
ax.set_xticklabels(["H%d" % I for I in range(Nhelices)])

fig = plt.gcf()
fig.set_size_inches(16, 12)

# select title and legend according to args.key
title={
    'Flux[]' : 'Power per cooling channel',
    'DT[C]' : 'Temperature rise per cooling channel',
    'Flowrate[m3/s]' : 'Flow rate',
    'S[mm2]' : 'cooling channel section',
    'h[]' : 'Heat exchange coefficient'
    }
legend={
    'Flux[]' : 'Power_per_channel',
    'DT[C]' : 'TempRise',
    'Flowrate[m3/s]' : 'Flowrate',
    'S[mm2]' : 'CoolingSection',
    'h[]' : 'HeatExchange'
    }

plt.title("%s: %s for Tin=%d°C" % (args.config, title[args.field], args.input_water_temp) )
plt.ylabel(args.field)
if args.show:
    plt.show()
else:        
    plt.savefig('%s_%s_Helix.png' % (configname, legend[args.field]), dpi=300 )
plt.close()

sys.exit(0)
