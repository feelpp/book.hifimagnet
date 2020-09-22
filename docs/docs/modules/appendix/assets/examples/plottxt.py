import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
df = pd.read_csv("M9_2019.06.20-14_36_30.csv")
# keys = df.columns.values.tolist()
# print("keys=", keys, " type(keys)=", type(keys))

#fig = px.scatter(df,  x="Time", y=["Tsb"])
# for multiplot:
fig = px.scatter(df,  x="Time", y=["Tin2","Tin1","tsb"])
# for multiplot: fig.add_scatter(x=df['Time'], y=df['Tin1'], mode='lines')


xbuttonlist = []
for col in df.columns:
    xbuttonlist.append(
        dict(
            args=['x',[df[str(col)]], {"xaxis_title": str(col)} ],
            label=str(col),
            method='restyle'
        )
    )
ybuttonlist = []
for col in df.columns:
    ybuttonlist.append(
        dict(
            args=['y',[df[str(col)]], {"yaxis_title": str(col)} ],
            label=str(col),
            method='restyle'
        )
    )
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
    title="Test data",
    showlegend=True,
    #yaxis_title="BField",
    #xaxis_title="Time",
    # Add dropdown
    updatemenus=[
        go.layout.Updatemenu(
            buttons=xbuttonlist,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
        go.layout.Updatemenu(
            buttons=ybuttonlist,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.4,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
        # go.layout.Updatemenu(
        #     buttons=y1buttonlist,
        #     direction="down",
        #     pad={"r": 10, "t": 10},
        #     showactive=True,
        #     x=0.7,
        #     xanchor="left",
        #     y=1.1,
        #     yanchor="top"
        # ),
    ],
    annotations=[
        dict(text="xField", x=0, xref="paper", y=1.06, yref="paper",
                             align="left", showarrow=False),
        dict(text="yField", x=0.3, xref="paper", y=1.06,
                             yref="paper", showarrow=False),
    ],
    autosize=True
)


fig.show()
