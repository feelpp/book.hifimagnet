from __future__ import unicode_literals
import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
import matplotlib.pyplot as plt

import pandas as pd
import freesteam as st

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="input txt file (ex. HL31_2018.04.13.txt)")
args = parser.parse_args()

input_file = args.input_file
output_file = input_file.replace(".txt", ".cvs")

# Import Dataset
df = pd.read_csv(input_file, sep='\s+', engine='python', skiprows=1)
#print df.count()

# Get Name of columns
keys = df.columns.values.tolist()
print keys

df['DP1'] = df['HP1'] - df['BP']
df['DT1'] = df['Tout'] - df['Tin1']
df['Tw1'] = df.apply(lambda row: (row.Tin1 + row.Tout)/2., axis=1)
df['P1'] = df.apply(lambda row: (row.HP1 + row.BP)/2., axis=1)

df['U1'] = df['Ucoil1'] + df['Ucoil2'] + df['Ucoil3'] + df['Ucoil4'] + df['Ucoil5'] + df['Ucoil6'] + df['Ucoil7']
df['Pe1'] = df.apply(lambda row: row.U1 * row.Icoil1  / 1.e+6, axis=1)

# Bitter
df['DP2'] = df['HP2'] - df['BP']
df['DT2'] = df['Tout'] - df['Tin2']
df['Tw2'] = df.apply(lambda row: (row.Tin2 + row.Tout)/2., axis=1)
df['P2'] = df.apply(lambda row: (row.HP2 + row.BP)/2., axis=1)

df['U2'] = df['Ucoil15'] + df['Ucoil16']
df['Pe2'] = df.apply(lambda row: row.U2 * row.Icoil15  / 1.e+6, axis=1)

# # Get Water property
# df['rho'] = df.apply(lambda row: st.steam_pT(row.P1*1e+5,row.Tw1+273.).rho / 1., axis=1)
# df['cp'] = df.apply(lambda row: st.steam_pT(row.P1*1e+5,row.Tw1+273.).cp / 1., axis=1)
# df['rhocp'] = df['rho']*df['cp']

df['Power'] = df['Pe1'] + df['Pe2']
df['rhoCp'] = df.apply(lambda row: row.Power*1.e+6/(row.DT1 * row.Flow1 * 1.e-3)/1000.  if (row.Flow1*row.DT1 > 0 and row.Power != 0) else np.NaN, axis=1)
df['Cp1'] = df.apply(lambda row: row.Pe1*1.e+6/(row.DT1 * row.Flow1 * 1.e-3)/1000.  if (row.Flow1*row.DT1 > 0 and row.Pe1 != 0) else np.NaN, axis=1)
df['Cp2'] = df.apply(lambda row: row.Pe2*1.e+6/(row.DT2 * row.Flow2 * 1.e-3)/1000.  if (row.Flow2*row.DT2 > 0 and row.Pe2 != 0) else np.NaN, axis=1)

# Check data type
# print pd.api.types.is_string_dtype(df['Icoil1'])
# print pd.api.types.is_numeric_dtype(df['Icoil1'])
# df[['Field', 'Icoil1']] = df[['Field', 'Icoil1']].apply(pd.to_numeric)

# Plot
# df.plot(x='Tw1', y='Pmagnet',kind='scatter',color='green')
# df.plot(x='Tw1', y='DT1',kind='scatter',color='red')
# df.plot(x='Tw1', y='P1',kind='scatter',color='blue')
# df.plot(x='Tw1', y='rhoCp',kind='scatter',color='red')
# df.plot(x='Tw1', y='rho',kind='scatter',color='red')
# df.plot(x='Tw1', y='cp',kind='scatter',color='red')
# df.plot(x='Time', y='rhoCp')

# Plot on the same graph
ax = plt.gca()
df.plot(x='Time', y='P1', ax=ax)
df.plot(x='Time', y='Tw1', ax=ax)

df.plot(x='Time', y='Tin1', ax=ax)
df.plot(x='Time', y='Tin2', ax=ax)
df.plot(x='Time', y='Tout', ax=ax)

df.plot(x='Time', y='rhoCp')
df.plot(x='Time', y='Cp1')
df.plot(x='Time', y='Pe1')
df.plot(x='Time', y='Cp2')
df.plot(x='Time', y='Pe2')
plt.show()

# Plot Rho*Cp on P,T range
def rhocp(bar, celsius):
    pascal = bar * 1e+5
    kelvin = celsius+273.
    rho = st.steam_pT(pascal, kelvin).rho
    cp = st.steam_pT(pascal, kelvin).cp
    return rho*cp

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

#rhocp = lambda bar, celsius: st.steam_pT(bar * 1e+5, celsius+273.).rho * st.steam_pT(bar * 1e+5, celsius+273.).cp
T = np.arange(10, 40, 1)
P = np.arange(5,  25, 5)

for p in P:
    plt.plot(T, [cp(p, x) for x in T], label='%d bar' % p)
plt.legend(loc='best')
plt.xlabel(r'T[C]')
plt.ylabel(r'$C_p[SI]$')
plt.show()

for p in P:
    plt.plot(T, [rho(p, x) for x in T], label='%d bar' % p)
plt.legend(loc='best')
plt.xlabel(r'T[C]')
plt.ylabel(r'$\rho[kg/m^3]$')
plt.show()

# ax1 = plt.gca()
# # df.plot(x='Time', y='Ptot', ax=ax1)
# df.plot(x='Time', y='Pmagnet', ax=ax1)
# # df.plot(x='Time', y='PBitter', ax=ax1)
# df.plot(x='Time', y='Pe1', ax=ax1)
# df.plot(x='Time', y='Pe2', ax=ax1)
# df.plot(x='Time', y='Power', ax=ax1)
# df.plot(x='Time', y='Field', ax=ax1)
# plt.show()

# ax1 = plt.gca()
# # df.groupby(['Ucoil1','Ucoil2']).count()['U1'].plot(ax=ax1)
# # df.groupby(['Ucoil15','Ucoil16']).count()['U2'].plot(ax=ax1)
# df.plot(x='Time', y='U1', ax=ax1)
# df.plot(x='Time', y='U2', ax=ax1)
# df.plot(x='Time', y='Field', ax=ax1)
# plt.show()

# for key in keys:
#     if key != 'Time' and key != 'Date' :
#         print "plot: %s" % key


# Save to CSV
df.to_csv(output_file, index=False, header=False, date_format=str)


