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
parser.add_argument("--pressure", help="input pressure (pascal)", type=float, default=5.e+5)
parser.add_argument("--temperature", help="input temperature (kelvin)", type=float, default=293)
parser.add_argument("--celsius", help="use celsius instead of kelvin", action='store_true')
parser.add_argument("--bar", help="use bar instead of pascal", action='store_true')
parser.add_argument("--all", help="display all outputs (rho, Cp, mu, k)", action='store_true')
args = parser.parse_args()

pressure = args.pressure
temperature = args.temperature

if args.bar:
    pressure = pressure * 1e+5
if args.celsius:
    temperature = temperature + 273.

# Get Water property
Steam = st.steam_pT(pressure,temperature) 
rho = Steam.rho
cp = Steam.cp

if args.all:
    mu = Steam.mu
    k = Steam.k
    res="%g;%g;%g;%g" % (rho, cp, mu, k)
    print(res)
else:
    print(rho*cp)
