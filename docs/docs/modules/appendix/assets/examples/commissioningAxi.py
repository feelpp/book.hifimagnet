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
        configname="%s_I%d_IB_%d_Tin%d" % (config, I, IB, input_water_temp)
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

import sys
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--config", help="input txt file (ex. HL-31-Cu5Ag-gmsh)")
parser.add_argument("--exp", help="input experiment data file (ex. M9_2019.06.20-14_36_30.txt)", type=str, default="")
parser.add_argument("--nhelices", help="number of helices (default 14)", type=int, default=14)
parser.add_argument("--input_water_temp", help="water temperature at input [Celsius] (integer only)", type=int, default=20)
parser.add_argument("--bitter_current", help="Bitter current [A] (integer only)", type=int, default=0)
parser.add_argument("--supra_current", help="Supra current [A] (integer only)", type=int, default=0)
parser.add_argument("--field", help="select field to plot (default R[Ohm])", type=str, default='R[Ohm]')
parser.add_argument("--show", help="display graphs instead of saving them (png format)", action='store_true')
args = parser.parse_args()


IB=args.bitter_current
Nhelices=14

Currents=[600,900,1000,2500,5000,7500,10000,12500,15000,17500,20000,22500,25000,27500,27900,28000,29000,30000,31000]
# Currents.reverse()

# Generate colormap
# see https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
NUM_COLORS = len(Currents)
cm = plt.get_cmap('nipy_spectral') #'gist_rainbow'
cNorm  = colors.Normalize(vmin=0, vmax=NUM_COLORS-1)
scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)

ax = plt.gca()

configname="%s_I%d_IB_%d_Tin%d" % (args.config, Currents[0], IB, args.input_water_temp)
input_file=configname + ".dat"
print ("configname=%s" % configname)

if not os.path.isfile(input_file):
    print ("%s no such file" % input_file)
    sys.exit(1)
    
inputdata = pd.read_csv(input_file, sep='\s+', engine='python', skiprows=1)
inputdata.drop(inputdata.tail(2).index,inplace=True)

keys = inputdata.columns.values.tolist()
if not args.field in keys:
    print ("Invalid field %s" % args.field)
    print ("Valid keys are: ",keys)
    sys.exit(1)

resistance = pd.read_csv(input_file, sep='\s+', engine='python', skiprows=1)
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
    'P[MW]' : 'Power',
    'R[Ohm]' : 'Resistance',
    '<T>[C]' : 'Mean Temperature',
    'Tmax[C]' : 'Max Temperature',
    'Hoopmax[MPa]' : 'Max HoopStress'
    }
extitle={
    'P[MW]' : 'Pe1'
    }

legend={
    'P[MW]' : 'Power',
    'R[Ohm]' : 'Resistance',
    '<T>[C]' : 'MeanTemp',
    'Tmax[C]' : 'MaxTemp',
    'Hoopmax[MPa]' : 'MaxHoop'
    }


plt.title("%s: %s for Tin=%d°C" % (args.config, title[args.field], args.input_water_temp) )
plt.ylabel(args.field)
if args.show:
    plt.show()
else:        
    plt.savefig('%s_%s_Helix.png' % (configname, legend[args.field]), dpi=300 )
plt.close()

if args.exp:
    print ("Experiment data")
    # load exp data
    if args.exp.endswith(".csv"):
        expdf = pd.read_csv(args.exp, sep=',', skiprows=0)
    else:
        expdf = pd.read_csv(args.exp, sep='\s+', engine='python', skiprows=1)
        
    print ("exp data keys: ", expdf.columns.values.tolist())
    # pick up exp key
    if args.field in extitle:
        ax = plt.gca()
        # plot expkey/Icoil1

        # for Power:
        num_power = resistance.sum(axis=0).to_frame()
        num_power['I'] = [I for I in Currents]
        print ("num_power=", num_power)

        print ("extitle[%s] = %s" % (args.field, extitle[args.field]) )
        if extitle[args.field] in expdf.columns.values.tolist():
            plt.plot(expdf['Icoil1'].values, expdf[extitle[args.field]], label='exp', marker='o', markevery=20, ls='none')
            plt.plot(num_power['I'].values, num_power[0].values, label='Axi Num', color='r')
        else:
            print ("%s: invalid key" % extitle[args.field])
            print ("valid keys from exp: ", expdf.columns.values.tolist() )
            sys.exit(1)
            
        plt.legend()
        plt.grid(b=True)
        plt.title("%s (%s) : Tin=%d°C" % (args.config, args.exp, args.input_water_temp) )
        plt.ylabel(args.field) 
        plt.xlabel("I[A]")            
        if args.show:
            plt.show()
        else:        
            plt.savefig('%s_%s_cmp_axi_exp-tin%d.png' % (configname, legend[args.field], args.input_water_temp), dpi=300 )
        plt.close()
    

#
#
#


for I in Currents:
    resistance.rename({"%d A" % I: "%g" % I}, axis=1, inplace=True)

# For each helices plot R vs I
Alpha_20 = [None] * Nhelices
Alpha_20[0] = 3.6e-03;
Alpha_20[1] = 3.6e-03;
Alpha_20[2] = 3.6e-03;
Alpha_20[3] = 3.6e-03;
Alpha_20[4] = 3.6e-03;
Alpha_20[5] = 3.6e-03;
Alpha_20[6] = 3.6e-03;
Alpha_20[7] = 3.6e-03;
Alpha_20[8] = 3.6e-03;
Alpha_20[9] = 3.6e-03;
Alpha_20[10] = 3.6e-03;
Alpha_20[11] = 3.6e-03;
Alpha_20[12] = 3.4e-03;
Alpha_20[13] = 3.4e-03;

Alpha_0=[x/(1-x*20) for x in Alpha_20]

R0=[]
if args.field == "R[Ohm]":
    compute_meanT = inputdata
    compute_meanT = extractdata(compute_meanT, args.config, "<T>[C]", Currents, IB, args.input_water_temp)
    # print ("compute_meanT=", compute_meanT)
    # print ("resistance=", resistance)
    for i in range(Nhelices):
        ax = plt.gca()
        row = resistance.iloc[i]
        rho = row.to_frame().reset_index()

        # make sure we use numeric data
        keys = rho.columns.values.tolist()
        for key in keys:
            isnum=pd.api.types.is_numeric_dtype(rho[key])
            #print ("rho[%s] numeric? %s" % (key,isnum ) )
            if not isnum:
                rho[key] = pd.to_numeric(rho[key])
            

        # print ("H%d" % (i+1), "type(row)=%s" % type(row), "type(rho)=%s" % type(rho), rho, rho.index )
        # print ("row=", row)
        # print ("rho=", rho[i])

    
        #row.plot(grid=True, ax=ax, use_index=True)
        #rho.plot(x='index', y=i, kind='scatter', grid=True, ax=ax)
        #rho.plot(x='index', y=i, grid=True, ax=ax, style="-o")
        #ax.legend("R")

        # Fit against second order polynom
        popt, pcov = curve_fit(polyfit, rho['index'].values, rho[i].values)
        fitlegend= "fit: a0=%5.3e, a1=%5.3e, a2=%5.3e" % tuple(popt)
        R0.append(popt)
        print ("H%d: %s" % ((i+1), fitlegend) )

        plt.plot(rho['index'].values, rho[i].values, 'r', label='data', marker="x", ls='none')
        plt.plot(rho['index'].values, polyfit(rho['index'].values, *popt), 'g--', label=fitlegend, marker="+")
    
        # plt.xlim((Currents[0], Currents[-1]))
        plt.xlabel("I[A]")
        plt.ylabel("R[Ohm]")
        plt.title("H%d : R at Tin=20°C" % (i+1) )
        plt.legend()
        plt.grid(b=True)
        if args.show:
            plt.show()
        else:        
            plt.savefig('%s_H%d_Tin%d_R.png' % (configname, i+1, args.input_water_temp) )
        plt.close()

        # Compute meanT from R
        meanT = (rho[i]/popt[0]-1)/Alpha_0[i]
        computed = compute_meanT.iloc[i].to_frame().reset_index()
        plt.plot(rho['index'].values, meanT.values, 'g', label='estimate', marker="x", ls='none')
        plt.plot(rho['index'].values, computed[i].values, 'r', label='computed', marker="o")
        plt.xlabel("I[A]")
        plt.title("H%d : Mean Temperature at Tin=%d°C" % (i+1, args.input_water_temp) )
        plt.legend()
        plt.grid(b=True)
        if args.show:
            plt.show()
        else:        
            plt.savefig('%s_H%d_Tin%d_meanT.png' % (configname, i+1, args.input_water_temp) )
        plt.close()

sys.exit(0)
