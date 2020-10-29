import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import math

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", help="input txt file (ex. HL31_2018.04.13.txt)")
parser.add_argument("--nhelices", help="specify number of helices", type=int, default=14)
parser.add_argument("--check", help="returns True if active voltage taps==nhelices", action='store_true')
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

# Try to detect plateaus

I1_max=df["I1"].max()
regime = df["I1"].to_numpy()
df['regime']=pd.Series(regime)

diff = np.diff(regime)
df['diff']=pd.Series(diff)

ndiff = np.where(abs(diff) >= 3., diff, 0)
df['ndiff']=pd.Series(ndiff)

gradient = np.sign(df["ndiff"].to_numpy())
df['gradient']=pd.Series(gradient)

del df['ndiff']
del df['diff']
del df['regime']

# # Add (tsb-teb)/((Tout-Tin1+Tin2)/2.)
# df["ratio"] = df.apply(lambda row: (row.Tout - (row.Tin1+row.Tin2)/2.)/(row.tsb-row.teb), axis=1)
# print("mean<ratio>=", df["ratio"].mean(), "std=", df["ratio"].std())

# Get keys
keys = df.columns.values.tolist()
print ("keys=", len(keys))

isVisible=[]
for i,key in enumerate(keys):
    isVisible.append(False)
    if key in ["t", "Tin2"]:
        print (key, i)
        
# Create plot

xdata="t"
ydata="Tin1"

xindex=df.columns.get_loc(xdata)
yindex=df.columns.get_loc(ydata)

#ydata=["Tin2","Tin1","Tout"]
fig = px.scatter(df,  x=xdata, y=ydata)

##fig = go.Figure()

# Define buttons

mymethod="restyle" # "restyle replot data only, "update" not working, "relayout" not working
xbuttonlist = []
for i,col in enumerate(df.columns):
    isVisible[i]=True
    xbuttonlist.append(
        dict(
            args=['x',[df[str(col)]]],
            label=str(col),
            method=mymethod
        )
    )
    isVisible[i]=False
ybuttonlist = []
for col in df.columns:
    isVisible[i]=True
    ybuttonlist.append(
        dict(
            args=['y',[df[str(col)]]],
            label=str(col),
            method=mymethod
        )
    )
    isVisible[i]=False
# y1buttonlist = []
# y1buttonlist.append(dict(args=['y1','None'], label='None', method='restyle'))
# for col in df.columns:
#     y1buttonlist.append(
#         dict(
#             args=['y1',[df[str(col)]], {"yaxis_title": str(col)} ],
#             label=str(col),
#             method='restyle'
#         )
#     )

fig.update_layout(
    title="M9: "+insert+" (t0="+str(t0)+")",
    showlegend=True,
    hovermode="x unified",
    xaxis_title="xField",
    yaxis_title="yField",
    # Add dropdown
    updatemenus=[
        go.layout.Updatemenu(
            buttons=xbuttonlist,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.05,
            yanchor="top",
            active=xindex
        ),
        go.layout.Updatemenu(
            buttons=ybuttonlist,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.4,
            xanchor="left",
            y=1.05,
            yanchor="top",
            active=yindex
        ),
        # go.layout.Updatemenu(
        #     buttons=y1buttonlist,
        #     direction="down",
        #     pad={"r": 10, "t": 10},
        #     showactive=True,
        #     x=0.7,
        #     xanchor="left",
        #     y=1.05,
        #     yanchor="top"
        # ),
    ],
    annotations=[
        dict(text="xField", x=0.05, xref="paper", y=1.04, yref="paper",
                             align="left", showarrow=False),
        dict(text="yField", x=0.35, xref="paper", y=1.04,
                             yref="paper", showarrow=False),
        # dict(text="y1Field", x=0.65, xref="paper", y=1.04,
        #                      yref="paper", showarrow=False),
    ],
    autosize=True
)

# # Add scatter
# fig.add_trace(go.Scatter(
#     x=df["t"],
#     y=df["Tin2"],
#     mode = 'markers'
# ))
# fig.add_trace(go.Scatter(
#     x=df["t"],
#     y=df["Tin1"],
#     mode = 'markers'
# ))


#print("fig=", fig)
fig.show()
