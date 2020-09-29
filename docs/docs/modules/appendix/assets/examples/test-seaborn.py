import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", help="input csv file (ex. HL31_2018.04.13.csv)")
args = parser.parse_args()

# Import Dataset
input_file = args.input_file
df = pd.read_csv(input_file, sep='\s+', engine='python', skiprows=1)

# Drop empty columns
df = df.loc[:, (df != 0.0).any(axis=0)]
keys = df.columns.values.tolist()
print("keys=", len(keys))

import datetime
tformat="%Y.%m.%d %H:%M:%S"
start_date=df["Date"].iloc[0]
start_time=df["Time"].iloc[0]
end_time=df["Time"].iloc[-1]
print ("start_time=", start_time, "start_date=", start_date)

t0 = datetime.datetime.strptime(df['Date'].iloc[0]+" "+df['Time'].iloc[0], tformat)


df["t"] = df.apply(lambda row: (datetime.datetime.strptime(row.Date+" "+row.Time, tformat)-t0).total_seconds(), axis=1)
# print("t:", df["t"])

sns.relplot(x="t", y="teb", kind="line", data=df)

plt.show()
