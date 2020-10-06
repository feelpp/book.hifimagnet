import pandas as pd
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", help="input txt file (ex. HL31_2018.04.13.txt)")
args = parser.parse_args()

# Import Dataset
input_file = args.input_file
df = pd.read_csv(input_file, sep='\s+', engine='python', skiprows=1)

# Get Name of columns
keys = df.columns.values.tolist()
#print ("keys=", len(keys))

# Drop empty columns
df = df.loc[:, (df != 0.0).any(axis=0)]
keys = df.columns.values.tolist()
print ("keys=", len(keys))

print( "=== Correlation ===")
correlation = df.corr(method="pearson", min_periods=10)
print( correlation )
# print( df.corr(method=‘kendall’, min_periods=1) )
# print( df.corr(method=‘spearman’, min_periods=1) )

import matplotlib.pyplot as plt

# f = plt.figure(figsize=(20, 15))
# plt.matshow(correlation, fignum=f.number)
# plt.xticks(range(df.shape[1]), df.columns, fontsize=8, rotation=45)
# plt.yticks(range(df.shape[1]), df.columns, fontsize=8)
# cb = plt.colorbar()
# cb.ax.tick_params(labelsize=14)
# plt.title('Correlation Matrix', fontsize=16)
# plt.show()


import seaborn as sns
sns.heatmap(correlation, 
            xticklabels=correlation.columns.values,
            yticklabels=correlation.columns.values)
plt.show()
# sns.pairplot(df)
