from __future__ import unicode_literals
import numpy as np
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
import matplotlib.pyplot as plt

import pandas as pd
import freesteam as st

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

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", help="input txt file (ex. HL31_2018.04.13.txt)")
parser.add_argument("--plot_vs_time", help="select key(s) to plot (ex. \"Field[;Ucoil1]\")")
parser.add_argument("--plot_key_vs_key", help="select pair(s) of keys to plot (ex. \"Field-Icoil1")
parser.add_argument("--output_time", help="output key(s) for time")
parser.add_argument("--output_key", help="output key(s) for time")
parser.add_argument("--show", help="display graphs instead of saving them (png format)", action='store_true')
args = parser.parse_args()

input_file = args.input_file
output_file = input_file.replace(".txt", ".csv")

# Import Dataset
df = pd.read_csv(input_file, sep='\s+', engine='python', skiprows=1)

# Get Name of columns
keys = df.columns.values.tolist()
#print "keys=", len(keys)

# Drop empty columns
df = df.loc[:, (df != 0.0).any(axis=0)]
keys = df.columns.values.tolist()
print "keys=", len(keys)

# Add some more columns
# Helix Magnet
df['U1'] = 0
for i in range(15):
    ukey = "Ucoil%d" % i
    if ukey in keys:
        df['U1'] += df[ukey]
    
# df['U1'] = df['Ucoil1'] + df['Ucoil2'] + df['Ucoil3'] + df['Ucoil4'] + df['Ucoil5'] + df['Ucoil6'] + df['Ucoil7'] \
#            + df['Ucoil8'] + df['Ucoil9'] + df['Ucoil10'] + df['Ucoil11'] + df['Ucoil12'] + df['Ucoil13'] + df['Ucoil14']
df['Pe1'] = df.apply(lambda row: row.U1 * row.Icoil1  / 1.e+6, axis=1)
df['DP1'] = df['HP1'] - df['BP']

# Get Water property
df['rho1'] = df.apply(lambda row: st.steam_pT(row.BP*1e+5,row.Tin1+273.).rho / 1., axis=1)
df['cp1'] = df.apply(lambda row: st.steam_pT(row.BP*1e+5,row.Tin1+273.).cp / 1., axis=1)

df['DT1'] =  df.apply(lambda row: row.Pe1*1.e+6 / ( row.rho1 * row.cp1 * row.Flow1 * 1.e-3)  if (row.Flow1 != 0) else row.Tin1, axis=1)
df['Tout1'] = df['Tin1'] + df['DT1']
df['Tw1'] = df.apply(lambda row: row.Tin1 + row.DT1/2., axis=1)
df['P1'] = df.apply(lambda row: (row.HP1 + row.BP)/2., axis=1)


# Bitter
if 'Ucoil15' in keys:
    df['U2'] = df['Ucoil15'] + df['Ucoil16']
    df['Pe2'] = df.apply(lambda row: row.U2 * row.Icoil15  / 1.e+6, axis=1)

# Get Water property
    df['rho2'] = df.apply(lambda row: st.steam_pT(row.BP*1e+5,row.Tin2+273.).rho / 1., axis=1)
    df['cp2'] = df.apply(lambda row: st.steam_pT(row.BP*1e+5,row.Tin2+273.).cp / 1., axis=1)

    df['DP2'] = df['HP2'] - df['BP']
    df['DT2'] =  df.apply(lambda row: row.Pe2*1.e+6 / ( row.rho2 * row.cp2 * row.Flow2 * 1.e-3)  if (row.Flow2 != 0) else row.Tin2, axis=1)
    df['Tout2'] = df['Tin2'] + df['DT2']
    df['Tw2'] = df.apply(lambda row: row.Tin2 + row.DT2/2., axis=1)
    df['P2'] = df.apply(lambda row: (row.HP2 + row.BP)/2., axis=1)



    df['Power'] = df['Pe1'] + df['Pe2']
    df['Toutg'] = (df['rho1']*df['cp1']*df['Flow1'] * df['Tout1']+ df['rho2']*df['cp2']*df['Flow2'] * df['Tout2'])/(df['rho1']*df['cp1']*df['Flow1'] + df['rho2']*df['cp2']*df['Flow2'])

# Check data type
# print pd.api.types.is_string_dtype(df['Icoil1'])
# print pd.api.types.is_numeric_dtype(df['Icoil1'])
# df[['Field', 'Icoil1']] = df[['Field', 'Icoil1']].apply(pd.to_numeric)

# Get Name of columns
keys = df.columns.values.tolist()
dkeys={keys[i]: keys[i] for i in range(0, len(lst))} 

if args.plot_vs_time:
    ax = plt.gca()
    # split into keys
    items = args.plot_vs_time.split(';')
    print "items=", items
    # loop over key
    for key in items:
        if key in keys:
            df.plot(x='Time', y=key, ax=ax)
        else:
            print "unknown key: %s" % key
            print "valid keys: ", keys
            exit(1)
    if args.show:
        plt.show()
    else:
        imagefile = input_file.replace(".txt", "")
        plt.savefig('%s_vs_time.png' % imagefile, dpi=300 )
    plt.close()
        
if args.plot_key_vs_key:
    # split pairs in key1, key2
    pairs = args.plot_key_vs_key.split(';') 
    for pair in pairs:
        ax = plt.gca()
        #print "pair=", pair, " type=", type(pair)
        items = pair.split('-')
        if len(items) != 2:
            print "invalid pair of keys: %s" % pair
            exit(1)
        key1= items[0]
        key2 =items[1]
        if key1 in keys and key2 in keys:
            df.plot(x=key1, y=key2,kind='scatter',color='red') # on graph per pair
        else:
            print "unknown pair of keys: %s" % pair
            print "valid keys: ", keys
            exit 
        if args.show:
            plt.show()
        else:
            imagefile = input_file.replace(".txt", "")
            plt.savefig('%s_%s_vs_%s.png' % (imagefile, key1, key2), dpi=300 )
        plt.close()

if args.output_time:
    times = args.output_time.split(";")
    if args.output_key:
        keys = args.output_key.split(";")
        print df[df['Time'].isin(times)][keys]
    else:
        print df[df['Time'].isin(times)]

#rhocp = lambda bar, celsius: st.steam_pT(bar * 1e+5, celsius+273.).rho * st.steam_pT(bar * 1e+5, celsius+273.).cp
T = np.arange(min(df['Tin1'].min(),df['Tin2'].min()), df['Tout'].max(), 1)
P = np.arange(df['BP'].min(), max(df['HP1'].max(),df['HP2'].max()), 1)

# for p in P:
#     plt.plot(T, [cp(p, x) for x in T], label='%d bar' % p)
# plt.legend(loc='best')
# plt.xlabel(r'T[C]')
# plt.ylabel(r'$C_p[SI]$')
# plt.show()

# for p in P:
#     plt.plot(T, [rho(p, x) for x in T], label='%d bar' % p)
# plt.legend(loc='best')
# plt.xlabel(r'T[C]')
# plt.ylabel(r'$\rho[kg/m^3]$')
# plt.show()



# Save to CSV
df.to_csv(output_file, index=False, header=True, date_format=str)


