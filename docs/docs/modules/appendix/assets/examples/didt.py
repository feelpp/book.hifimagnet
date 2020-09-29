from __future__ import unicode_literals
import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
import matplotlib.pyplot as plt

import pandas as pd

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", help="input txt file (ex. HL31_2018.04.13.txt)")
args = parser.parse_args()

sep=str(",")
skiprows=0
input_file = args.input_file

if input_file.endswith(".txt"):
    output_file = input_file.replace(".txt", ".csv")
    skiprows=1
    sep='\s+'
    
# Import Dataset
df = pd.read_csv(input_file, sep=sep, engine='python', skiprows=skiprows)
keys = df.columns.values.tolist()
print("keys=", keys)

# Get Name of columns
newdf = pd.concat([df['Time'], df['Icoil1'], df['Icoil15']], axis=1)
newdf['datetime'] = pd.to_datetime(newdf['Time'])
newdf = newdf.set_index('datetime')
newdf.drop(['Time'], axis=1, inplace=True)
print("newdf:", newdf)

dv=newdf.diff()
print("numer=", dv)
dt=newdf.index.to_series().diff().dt.total_seconds()
print("deno=", dt)

newdf['dIcoil1dt']=dv['Icoil1']/dt
newdf['dIcoil15dt']=dv['Icoil15']/dt
print("res=", newdf)

# Inductances from MagnetTools:
L=2.3195642547e-03
M=2.3391491498e-03

# # Inductances from Getdp Axi:
# L=2.318e-3
# M=1.1696e-3 ## bizarre: a peu pres 2x la valeur estimee analytique???

newdf['InductCorrection']=L*newdf['dIcoil1dt']+M*newdf['dIcoil15dt']

ax = plt.gca()
newdf.reset_index().plot(x='datetime', y='Icoil1', ax=ax)
newdf.reset_index().plot(x='datetime', y='Icoil15', ax=ax)
plt.show()

ax = plt.gca()
newdf.reset_index().plot(x='datetime', y='dIcoil1dt', ax=ax)
newdf.reset_index().plot(x='datetime', y='dIcoil15dt', ax=ax)
plt.show()

ax = plt.gca()
newdf.reset_index().plot(x='datetime', y='InductCorrection', ax=ax)
plt.show()

newdf.to_csv("CorrectionInduction.csv", index=False, header=True)
