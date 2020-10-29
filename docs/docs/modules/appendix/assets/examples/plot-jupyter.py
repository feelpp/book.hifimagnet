import datetime
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.plotly as py

from ipywidgets import widgets

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", help="input txt file (ex. HL31_2018.04.13.txt)")
args = parser.parse_args()

# Import Dataset
insert=None
input_file = args.input_file
with open(input_file, "r") as f:
    insert=f.readline().split()[-1]
    print("Insert=", insert)
    
df = pd.read_csv(input_file, sep='\s+', engine='python', skiprows=1)

# Get Name of columns
keys = df.columns.values.tolist()
#print ("keys=", len(keys))

# Drop empty columns
df = df.loc[:, (df != 0.0).any(axis=0)]

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

# Get keys
keys = df.columns.values.tolist()
print ("keys=", len(keys))

# Create plot

xdata="t"
ydata="Tin2"
#ydata=["Tin2","Tin1","Tout"]
fig = px.scatter(df,  x=xdata, y=ydata)

fig = go.FigureWidget()
scatt = fig.add_scatter(x=df["t"], y=df["Tin2"])
iplot(f)
