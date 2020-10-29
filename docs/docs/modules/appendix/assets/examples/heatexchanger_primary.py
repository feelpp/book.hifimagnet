from __future__ import unicode_literals
import numpy as np
import matplotlib
# print("matplotlib=", matplotlib.rcParams.keys())
matplotlib.rcParams['text.usetex'] = True
# matplotlib.rcParams['text.latex.unicode'] = True key not available
import matplotlib.pyplot as plt

import pandas as pd
import freesteam as st

def rho(bar, celsius):
    pascal = bar * 1e+5
    kelvin = celsius+273.
    rho = st.steam_pT(pascal, kelvin).rho
    return rho

def cp(bar, celsius):
    pascal = bar * 1e+5
    kelvin = celsius+273.
    cp = st.steam_pT(pascal, kelvin).cp
    return cp

from ht import *

# steam/oil crossflow
# internal (magnet) / external (drac) counterflow

#subtype='crossflow, mixed Cmax'
#subtype='counterflow'
def heatexchange(Tci, Thi, Debitc, Debith, Pci, Phi, subtype='counterflow'):
    U = 4041 # 4485 # W/m^2/K
    A = 1063.4 # m^2
    Cp_oil = cp(Pci, Tci) # 4.18e+3 # J/kg/K
    Cp_steam = cp(Phi,Thi) #4.19e+3 # J/kg/K
    m_steam = rho(Phi,Thi)*Debith*1.e-3 #5.2 # kg/s rho(Tout)*(Flow1+Flow2)??
    m_oil = rho(Pci, Tci)*Debitc/3600. #0.725 # kg/s rho*(teb)*debitbrut??

    #Thi = 130 # °C Tout
    #Tci = 15 # °C teb
    Cmin = calc_Cmin(mh=m_steam, mc=m_oil, Cph=Cp_steam, Cpc=Cp_oil)
    Cmax = calc_Cmax(mh=m_steam, mc=m_oil, Cph=Cp_steam, Cpc=Cp_oil) # ?? 36000 kW??
    Cr = calc_Cr(mh=m_steam, mc=m_oil, Cph=Cp_steam, Cpc=Cp_oil)
    NTU = NTU_from_UA(UA=U*A, Cmin=Cmin)
    #eff = effectiveness_from_NTU(NTU=NTU, Cr=Cr, subtype='crossflow, mixed Cmax')
    eff = effectiveness_from_NTU(NTU=NTU, Cr=Cr, subtype=subtype)
    Q = eff*Cmin*(Thi - Tci)
    Tco = Tci + Q/(m_oil*Cp_oil)
    Tho = Thi - Q/(m_steam*Cp_steam)

    #print("NTU=", NTU, "eff=", eff, "Q=", Q, "Cmax=", Cmax, "Cr=", Cr, "Cp_oil=", Cp_oil, "Cp_steam=", Cp_steam, "m_oil=", m_oil, "m_steam=", m_steam)

    return (Tco, Tho, Q)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", help="input txt file (ex. M10_2020.10.04_20-2009_43_31.txt)")
parser.add_argument("--nhelices", help="specify number of helices", type=int, default=14)
parser.add_argument("--subtype", help="specify type of heat exchanger", type=str, default='crossflow, mixed Cmax')
parser.add_argument("--check", help="returns True if active voltage taps==nhelices", action='store_true')
args = parser.parse_args()

sep=str("\t")
skiprows=1
input_file = args.input_file

# Import Dataset
insert=None
input_file = args.input_file
with open(input_file, "r") as f:
    insert=f.readline().split()[-1]
    insert = insert.replace("_", "\_")
    print("Insert=", insert)
    
#df = pd.read_csv(input_file, sep=sep, engine='python', skiprows=skiprows)
df = pd.read_csv(input_file, sep='\s+', engine='python', skiprows=1)

# Get Name of columns
keys = df.columns.values.tolist()
#print ("keys=", len(keys))

# Drop empty columns
df = df.loc[:, (df != 0.0).any(axis=0)]

# Add a time column
import datetime
tformat="%Y.%m.%d %H:%M:%S"
start_date=df["Date"].iloc[0]
start_time=df["Time"].iloc[0]
end_time=df["Time"].iloc[-1]
print ("start_time=", start_time, "start_date=", start_date)

t0 = datetime.datetime.strptime(df['Date'].iloc[0]+" "+df['Time'].iloc[0], tformat)


df["t"] = df.apply(lambda row: (datetime.datetime.strptime(row.Date+" "+row.Time, tformat)-t0).total_seconds(), axis=1)

del df['Date']
del df['Time']

# If M9: Icoil1=Idcct1+Iddct2, If M10/M8: Icoil2=Idcct3+Iddct4
df["I1"] = df["Idcct1"] + df["Idcct2"]
df["I2"] = df["Idcct3"] + df["Idcct4"]

del df['Idcct1']
del df['Idcct2']
del df['Idcct3']
del df['Idcct4']

df = df[df.columns.drop(list(df.filter(regex='DRcoil')))]
df = df[df.columns.drop(list(df.filter(regex='Tcal')))]

# Remove ICoil
keys = df.columns.values.tolist()
max_tap=0
for i in range(1,args.nhelices+1):
    ukey = "Ucoil%d" % i
    # print ("Ukey=%s" % ukey, (ukey in keys) )
    if ukey in keys:
        max_tap=i
if args.check:
    #print ("max_tap=%d" % max_tap)
    print (max_tap == args.nhelices)
    exit(0)

print ("max_tap=%d" % max_tap)
for i in range(2,max_tap):
    ikey = "Icoil%d" % i 
    del df[ikey]

if "Icoil16" in keys:
    del df["Icoil16"]

# Create a dct for key/units

ax = plt.gca()
df.plot(x='t', y='Field',ax=ax)
plt.xlabel(r't [s]')
plt.ylabel(r'Q [l/s]')
plt.grid(b=True)
plt.title(insert) # replace _ by \_ before adding title
plt.show()

# # Plot "Flow1" to check units   
# ax = plt.gca()
# df.plot(x='t', y='Flow1',ax=ax)
# df.plot(x='t', y='Flow2',ax=ax)
# df.plot(x='t', y='debitbrut',ax=ax)
# plt.xlabel(r't [s]')
# plt.ylabel(r'Q [l/s]')
# plt.grid(b=True)
# plt.title("insert:") # replace _ by \_ before adding title
# plt.show()

# Compute Tin, Tsb
df['cTin'] = df.apply(lambda row: heatexchange(row.teb, row.Tout, row.debitbrut, row.Flow1+row.Flow2, 10, row.BP, args.subtype)[1], axis=1)
df['ctsb'] = df.apply(lambda row: heatexchange(row.teb, row.Tout, row.debitbrut, row.Flow1+row.Flow2, 10, row.BP, args.subtype)[0], axis=1)

ax = plt.gca()
df.plot(x='t', y='ctsb', ax=ax, color='red')
df.plot(x='t', y='tsb', ax=ax, color='blue')
plt.xlabel(r't [s]')
plt.ylabel(r'T[C]')
plt.grid(b=True)
plt.title(args.subtype)
plt.show()

ax = plt.gca()
df.plot(x='t', y='cTin', ax=ax, color='red')
df.plot(x='t', y='Tin1', ax=ax, color='blue')
df.plot(x='t', y='Tin2', ax=ax, color='green')
plt.xlabel(r't [s]')
plt.ylabel(r'T[C]')
plt.grid(b=True)
plt.title(args.subtype)
plt.show()

df['QNTU'] = df.apply(lambda row: heatexchange(row.teb, row.Tout, row.debitbrut, row.Flow1+row.Flow2, 10, row.BP, args.subtype)[2], axis=1)
df["Qhprimaire"] = df.apply(lambda row: (row.Flow1+row.Flow2)*1.e-3*(rho(row.BP, row.Tout)*cp(row.BP, row.Tout)*row.Tout-rho(row.HP1, row.Tin1)*cp(row.HP1, row.Tin1)*row.Tin1), axis=1)
df["Qcprimaire"] = df.apply(lambda row: row.debitbrut/3600.*(rho(10, row.Tout)*cp(10, row.tsb)*row.tsb-rho(10, row.teb)*cp(10, row.teb)*row.Tin1), axis=1)


ax = plt.gca()
df.plot(x='t', y='QNTU', ax=ax, color='red')
df.plot(x='t', y='Qhprimaire', ax=ax, color='blue')
df.plot(x='t', y='Qcprimaire', ax=ax, color='green')
plt.xlabel(r't [s]')
plt.ylabel(r'Q[W]')
plt.grid(b=True)
plt.title(args.subtype)
plt.show()
