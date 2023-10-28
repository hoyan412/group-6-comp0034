#Created by Youssef ALAOUI MRANI
#Description:
#This code is used to create the dumbbell dots plots using plotly express.
#The first part of the code focuses on organising the dataset correctly while the second part of the code
#plots the graph. Note that the lines to save the plot are commented out.

# Import pandas and plotly express
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

pio.renderers.default = "browser"

df = pd.read_excel("/Users/youssefalaouimrani/Desktop/UCL /UCL 3rd Year/AppliedSoftware/coursework-1-groups-group-6-comp0034/data/Dataset.xlsx", sheet_name="Fat Intake", usecols="A:E", skiprows=4, skipfooter=271,
                   engine="openpyxl")

df2 = df.iloc[4]
df2 = df2.dropna()
df2 = df2.reset_index(drop=True)

df3 = df

for i in range(len(df)):
    if (df.iloc[i][0] != "    Mean"):
        df3 = df3.drop([i])

df_M = df3.iloc[[1]]

for i in range(1, 6):
    df_M = df_M.append(df3.iloc[1 + (3 * i)])

df_F = df3.iloc[[2]]
for i in range(1, 6):
    df_F = df_F.append(df3.iloc[2 + (3 * i)])

n = df_M.columns[0]

label = ["4-10", "11-18", "19-64", "65+", "65-74", "75+"]

df_M[n] = label
df_F[n] = label

df_M = df_M.rename(columns={"Unnamed: 0": "Age groups", "          Years 1-2": "Men 1-2", "      Years 3-4": "Men 3-4",
                            "       Years 5-6": "Men 5-6", "          Years 7-8": "Men 7-8"})
df_F = df_F.rename(
    columns={"Unnamed: 0": "Age groups", "          Years 1-2": "Women 1-2", "      Years 3-4": "Women 3-4",
             "       Years 5-6": "Women 5-6", "          Years 7-8": "Women 7-8"})

df_M = df_M.reset_index(drop=True)
df_F = df_F.reset_index(drop=True)

df_tot = df_F
df_tot["Men 1-2"] = df_M["Men 1-2"]
df_tot["Men 3-4"] = df_M["Men 3-4"]
df_tot["Men 5-6"] = df_M["Men 5-6"]
df_tot["Men 7-8"] = df_M["Men 7-8"]

Years_1 = [["Women 1-2", "Men 1-2"], ["Women 3-4", "Men 3-4"], ["Women 5-6", "Men 5-6"], ["Women 7-8", "Men 7-8"]]
Years = ["Women 1-2", "Men 1-2", "Women 3-4", "Men 3-4", "Women 5-6", "Men 5-6", "Women 7-8", "Men 7-8"]

df = pd.melt(df_tot, id_vars=["Age groups"], value_vars=Years)

test_list = []
gender_list = []
for element in df["variable"]:
    test_list.append(element[-3:])
    if element[:-3] == "Men ":
        gender_list.append("Men")
    else:
        gender_list.append("Women")

df["Year"] = test_list
df["Gender"] = gender_list

fig = px.scatter(df, x="value", y="Age groups", animation_frame="Year", width=800, height=600, range_x=[50, 90],
                 range_y=[-1, 6], color='Gender',color_discrete_sequence=["lightcoral", "lightsteelblue"])

fig.update_traces(mode='markers', marker=dict(line_width=1, symbol='circle', size=16))

fig.update_layout(
    title="Fat intake per gender",
    xaxis=dict(
        showgrid=False,
        showline=True,
        linecolor='rgb(102, 102, 102)',
        tickfont_color='rgb(102, 102, 102)',
        showticklabels=True,
        dtick=10,
        ticks='outside',
        tickcolor='rgb(102, 102, 102)'),

    margin=dict(l=140, r=40, b=50, t=80),
    legend=dict(
        font_size=10,
        yanchor='middle',
        xanchor='right',
    ),
    yaxis=dict(gridcolor="DarkGrey"),
    width=800,
    height=600,
    paper_bgcolor='white',
    plot_bgcolor='white',
    hovermode='closest',

)
fig.update_layout(title="Fat intake per gender in 2009/2010",
                  yaxis_title="Age groups",
                  xaxis_title="Fat intake (g/day)", font_color="black", width = 1350, height = 800)
# fig.write_html('static/charts/Fat_Charts/Fat_PltExpress.html')
fig.show()
