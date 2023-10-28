# Created by Youssef ALAOUI MRANI
# Description:
# This file is used to create the matplotlib horizontal bar charts. Note that this code first treats the dataset
# before creating the corresponding plot.
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel("Final Dataset.xlsx", sheet_name="Fat Intake", usecols="A:E", skiprows=4, skipfooter=271)

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

list_men = ["Men 1-2", "Men 3-4", "Men 5-6", "Men 7-8"]
list_women = ["Women 1-2", "Women 3-4", "Women 5-6", "Women 7-8"]
list_years = ["2008-2010", "2010-2012", "2012-2014", "2014-2016"]

list_men[0
]
fig, ax = plt.subplots(2, 2, figsize=(10, 10))
height = 0.3

counter = 0
for i in range(2):
    for j in range(2):
        test_1 = ax[i, j].barh(width=df_tot[list_men[counter]], y=np.arange(len(df_tot["Age groups"])) - height / 2,
                               height=height, tick_label=df_tot["Age groups"], color="lightsteelblue", label="Men")
        test_2 = ax[i, j].barh(width=(df_tot[list_women[counter]]), y=np.arange(len(df_tot["Age groups"])) + height / 2,
                               height=height, label="Women", color="purple")

        ax[i, j].set_yticks(np.arange(len(df_tot["Age groups"]) + 1))
        ax[i, j].set_ylabel("Age groups", fontsize=18)
        ax[i, j].set_xlabel("Fat intake in g/day", fontsize=18)
        ax[i, j].set_title('Fat intake in {}'.format(list_years[counter]), fontsize=26)
        ax[i, j].legend(fontsize=7)
        ax[i, j].tick_params(axis='x', labelsize=18)
        ax[i, j].tick_params(axis='y', labelsize=18)

        ax[i, j].set_xlim([0, 90])
        ax[i, j].grid()


        def yautolabel(var, i, j):
            for rect in var:
                w = rect.get_width()
                ax[i, j].annotate('{:.1f}'.format(w),
                                  xy=(w + 5.5, rect.get_y() + rect.get_height() / 4),
                                  xytext=(0, 0),  # 3 points vertical offset
                                  textcoords="offset points",
                                  ha='center', va='bottom', fontsize=13)


        yautolabel(test_1, i, j)
        yautolabel(test_2, i, j)
        counter += 1
# fig.show()
# fig.savefig("Fat_intake_matplotlib.png")
