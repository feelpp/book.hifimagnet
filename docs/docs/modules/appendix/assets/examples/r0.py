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

import re

def polyfit(x, a0, a1, a2):
    return a0 + a1 * x + a2 * x**2


import sys
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--num", help="input num data")
parser.add_argument("--alpha20", help="specify alpha(T=20°C)", action='append')
parser.add_argument("--exp", help="input experiment data file (ex. Icoil1-Ucoil1.csv)", type=str, default="")
parser.add_argument("--magfile", help="magfile from controlcommand (ex. MAGFile.conf)", type=str, default="")
parser.add_argument("--show", help="display graphs instead of saving them (png format)", action='store_true')
args = parser.parse_args()

# TODO: get alpha0 from MAGFILE if defined
if not args.alpha20:
    args.alpha20 = 3.6e-3

print ("alpha20(%s)=" % type(args.alpha20), args.alpha20)    

# Extract input water temp from input_name
input_water_temp=args.num.replace("R_Tin","").replace(".dat", "")
if "_perH" in args.num:
    input_water_temp=input_water_temp.replace("_perH", "")

(temp, correlation) = input_water_temp.split("_")
input_water_temp=int(temp)
print ("input_water_temp=", temp)
print ("correlation=", correlation)

coeff0=None
coeff1=None
coeff2=None
alpha0=None
if args.magfile:
    with open(args.magfile, 'r') as f:
        magdata=''.join(f.readlines())
        # print(magdata)

        # print("looking for r0_coil")
        m = re.findall(r"\br0_coil\d+=\".*\"", magdata)
        nm = [re.sub(r"\br0_coil\d+=\"", "", x) for x in m]
        coeff0 = [re.sub(r"\"", "", x) for x in nm]
        
        # print("looking for a0_coil")
        m = re.findall(r"\ba0_coil\d+=\".*\"", magdata)
        nm = [re.sub(r"\ba0_coil\d+=\"", "", x) for x in m]
        coeff1 = [re.sub(r"\"", "", x) for x in nm]

        # print("looking for b0_coil")
        m = re.findall(r"\bb0_coil\d+=\".*\"", magdata)
        nm = [re.sub(r"\bb0_coil\d+=\"", "", x) for x in m]
        coeff2 = [re.sub(r"\"", "", x) for x in nm]

        # # print("looking for ct_coil (aka alpha at Tref=0)")
        # m = re.findall(r"\bct\d+=\".*\"", magdata)
        # nm = [re.sub(r"\bct\d+=\"", "", x) for x in m]
        # alpha0 = [re.sub(r"\"", "", x) for x in nm]

        # for i in xrange(len(coeff0)):
        #     print(coeff0[i], coeff1[i], coeff2[i])

print("loading input data")
input_file=args.num
if not os.path.isfile(input_file):
    print ("%s no such file" % input_file)
    sys.exit(1)

num = pd.read_csv(input_file, sep='\s+', engine='python', skiprows=0)
keys = num.columns.values.tolist()
ntaps=0
for key in keys:
    if key.startswith("V"):
        ntaps += 1

if not alpha0:
    if isinstance(args.alpha20, float):
        alpha0=[args.alpha20/(1-args.alpha20*20.) for i in range(ntaps)]
        print alpha0
    elif isinstance(args.alpha20, list):
        if len(args.alpha20) != ntaps:
            print ("alpha20: should have %d values only %d provided" % (ntaps, len(args.alpha20)) )
            exit(1)
        else:
            alpha0=[float(alpha)/(1-float(alpha)*20.) for alpha in args.alpha20]
print ("alpha0=", alpha0)

# print ("Valid keys are: ",keys)
tap=0
for key in keys:
    if key.startswith("V"):
        alpha=alpha0[tap]
        print ("tap=%d, alpha0=%g" % (tap, alpha0[tap]) )
        tap+=1
        rkey=key.replace("V","R", 1)
        rkey=rkey.replace("V","mOhm", 1)
        num[rkey] = num[key].abs()/num['I[A]']/1.e-3
        r0key=rkey.replace("R","R0_", 1)
        if '<Tw>[K]' in keys:
            num[r0key] = num[rkey]/(1+alpha*(num['<Tw>[K]']-273.15))
        else:
            print("no key for <Tw>[K]")
            sys.exit(1)
            
# Update keys
keys = num.columns.values.tolist()
        
# print ("num=",num)
# print ("alpha=",alpha0, "(", args.alpha20, ")")
# print ("Tw=", num['<Tw>[K]']-273.15)
# print("R1=", num['R1[mOhm]'])
# print("R0_1=", num['R0_1[mOhm]'])

if args.exp:
    ekey = args.expdf.split("-")[-1]

    print ("Experiment data")
    # load exp data
    if args.exp.endswith(".csv"):
        expdf = pd.read_csv(args.exp, sep=',', skiprows=0)
        ekey = ekey.replace(".csv", "")
    else:
        expdf = pd.read_csv(args.exp, sep='\s+', engine='python', skiprows=1)
        ekey = ekey.replace(".txt", "")

    key = int(ekey.replace("Coil", ""))
    expdf[2]=expdf[1]*2/100.
    
    print ("exp data keys: ", expdf.columns.values.tolist())
    print ("exp[0].values type: ", type(expdf[0].values))
    
    ax = plt.gca()
    plt.errorbar(expdf[0].values, expdf[1].values, yerr=expdf[2], fmt='o', color='black',
                                  ecolor='lightgray', elinewidth=3, capsize=0);
    plt.plot(num['I[A]'].values, num[key].values, 'r--', label="3D Num")
    
    plt.legend()
    plt.grid(b=True)
    plt.title("%s : Tin=%d°C" % (ekey, input_water_temp) )
    plt.ylabel('V') 
    plt.xlabel("I[A]")            
    if args.show:
        plt.show()
    else:        
        plt.savefig('%s_%s_cmp_3D_exp-tin%d.png' % (ekey, correlation, input_water_temp), dpi=300 )
    plt.close()
    sys.exit(0)

# Inputfile contains: I V1...V7 <Tw> <T1>...<T7>
# Compute Ri=Vi/I
# Compute R0i=Ri/(1+alpha0*<Tw>)
# Fit R0i
# Get R0 from MAGFile
# Plot R0i vs R0 from MAGFile
# Plot <Ti> vs estimated value from ROi

# Fit against second order polynom

print("R0 Polynomials\n")
print("     | error(a0)   | error(a2)  | error(a2)")
print("-----|-------------|------------|----------")

i=0
tap=0
for key in keys:
    if key.startswith("R0_"):
        alpha=alpha0[tap]
        print ("key=%s, tap=%d, alpha0=%g, alpha=%g" % (key, tap, alpha0[tap], alpha) )
        tap+=1
        popt, pcov = curve_fit(polyfit, num['I[A]'].values, num[key].values)
        fitlegend= "Num: a0=%5.3e, a1=%5.3e, a2=%5.3e" % tuple(popt)
        print("fit[", key, " =", fitlegend)
        #print("popt=", type(popt), popt)

        ax = plt.gca()
        plt.plot(num['I[A]'].values, polyfit(num['I[A]'].values, *popt), 'g--', label=fitlegend, marker="+")
        if len(coeff1):
            exp_popt=np.array([float(coeff0[i]), float(coeff1[i]), float(coeff2[i])])
            explegend= "Exp: a0=%5.3e, a1=%5.3e, a2=%5.3e" % tuple(exp_popt)
            #print("coil%d" % (i+1), (coeff0[i], coeff1[i], coeff2[i]))
            plt.plot(num['I[A]'].values, polyfit(num['I[A]'].values, *exp_popt ), 'r--', label=explegend, marker="o")
            i+=1

            #TODO compute L2 error between num and MAGFILE
            print("coil%d" % (i+1), abs(1-popt[0]/coeff1[i]), abs(1-popt[1]/coeff1[i]), abs(1-popt[2]/coeff2[i]))
            
        plt.legend()
        plt.grid(b=True)
        plt.title("%s : Tin=%d°C, alpha=%g" % (key.replace("0_","").replace("[mOhm]",""), input_water_temp, alpha ) )
        plt.ylabel('mOhm') 
        plt.xlabel("I[A]")            
        if args.show:
            plt.show()
        else:        
            plt.savefig('%s_cmp_3D_exp-tin%d.png' % (key.replace("[mOhm]",""), input_water_temp), dpi=300 )
        plt.close()

        # Estimated temp
        rkey = key.replace("R0_", "R")
        tkey = key.replace("R0_", "meanT_").replace("[mOhm]","[C]")
        mkey = key.replace("R0_", "<T").replace("[mOhm]",">[K]")
        maxkey = mkey.replace("<T","max(").replace(">",")")
        num[tkey] = (num[rkey]/popt[0]-1)
        num[tkey] = num[tkey].abs()/alpha
        ### print(tkey, num[tkey]) #, num[nkey]
        
        ax = plt.gca()
        plt.plot(num['I[A]'].values, num[tkey].values, 'r--', label="Estimated", marker="+")
        if mkey in keys:
            num[mkey]=num[mkey]-273.15
            plt.plot(num['I[A]'].values, num[mkey].values, 'g--', label="Num Mean", marker="+")
        if maxkey in keys:
            num[maxkey]=num[maxkey]-273.15
            plt.plot(num['I[A]'].values, num[maxkey].values, 'g--', label="Num Max", marker="+")

        plt.legend()
        plt.grid(b=True)
        plt.title("%s : Tin=%d°C, Alpha0=%g" % (tkey, input_water_temp, alpha) )
        plt.ylabel('C') 
        plt.xlabel("I[A]")            
        if args.show:
            plt.show()
        else:        
            plt.savefig('%s_%s_cmp_3D_exp-tin%d.png' % (tkey.replace("[C]",""), correlation, input_water_temp), dpi=300 )
        plt.close()
            
print("-----|-------------|------------|----------")
sys.exit(0)
