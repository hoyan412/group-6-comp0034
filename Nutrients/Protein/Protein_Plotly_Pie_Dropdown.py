
# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 03/03/2021
# Name: Protein_Plotly_Pie_Dropdown
# Author: Rayan Souissi
# Description: Program to generate a plot of the contribution of different food groups to the mean
#               protein intake between 2008 and 2016, selecting a specific age classes (wit a Dropdown menu), using Plotly


import numpy as np
import pandas as pd
import plotly.express as px
# You need to uncomment the following two lines if you are using PyCharm
import plotly.io as pio
pio.renderers.default = "browser"
import plotly.graph_objects as go


if __name__ == "__main__":

    xlsxfile = '/Users/rayan/PycharmProjects/coursework-1-groups-group-6-comp0034/data/Dataset.xlsx'
    Ages = ["1.5-3", "4-10", "11-18", "19-64", "65-74", "75+"]
    Food_group = ["Cereals and cereal products", "Milk and milk products", "Cheese", "Meat and meat products",
                  "Fish and fish dishes", "Vegetables and potatoes", "Fruit", "Sugar, preserves and confectionery ",
                  "Miscellaneous (Soups and Sauces)", "Other (Savour snacks, Nuts and seeds, and beverages)"]
    skip_rows = [0, 1, 2, 3, 4, 5, 44, 45, 47, 48, 49, 50]


    '''0. Load the xlsx file into a pandas DataFrame and skip the first lines which contain introduction to the dataset'''
    protein_contrib = pd.read_excel(xlsxfile, engine='openpyxl', usecols = range(1,25),
                                    sheet_name='Protein Contribution',nrows = 78,  skiprows = skip_rows)

    '''1. Drop all the non-necessary lines'''
    protein_contrib = protein_contrib.drop(range(1,12))
    protein_contrib = protein_contrib.drop(range(13,18))
    protein_contrib = protein_contrib.drop(range(19,25))
    protein_contrib = protein_contrib.drop(range(26,39))
    protein_contrib = protein_contrib.drop(range(40,44))
    protein_contrib = protein_contrib.drop(range(45,50))
    protein_contrib = protein_contrib.drop(range(54,57))
    protein_contrib = protein_contrib.drop(range(58,61))
    protein_contrib = protein_contrib.drop(range(62,64))
    protein_contrib = protein_contrib.drop(range(65,72))
    protein_contrib = protein_contrib.reset_index(level=0, drop=True)

    '''2. Regroup the mean of "Savour Snacks", "Nuts and Seeds", Alcoholic beverages", and "Non-Alcolholic beverages"
        and put it at the end of dataframe for new food-group "other"'''
    z=[]
    t=0
    for j in range(0,24):                   #Regrouping the mean of "Savour Snacks", "Nuts and Seeds",
        for i in range(6,8):                                    #Alcoholic beverages", and "Non-Alcolholic beverages"
            t += protein_contrib.iloc[i,j]
        for i in range(10,12):
            t += protein_contrib.iloc[i,j]
        z.append(t)
        t = 0
    protein_contrib.loc[len(protein_contrib.index)] = z

    '''3. Drop the lines that are now regrouped in "Other" (last line)'''
    protein_contrib = protein_contrib.drop(range(6,8))
    protein_contrib = protein_contrib.drop(range(10,12))
    protein_contrib = protein_contrib.reset_index(level=0, drop=True)

    '''4. Assign to each period dataframe its values (in the columns of the general contrib dataframe'''
    protein_contrib_2008 = protein_contrib.iloc[:, 0:6]
    protein_contrib_2008.columns = Ages
    protein_contrib_2010 = protein_contrib.iloc[:, 6:12]
    protein_contrib_2010.columns = Ages
    protein_contrib_2012 = protein_contrib.iloc[:, 12:18]
    protein_contrib_2012.columns = Ages
    protein_contrib_2014 = protein_contrib.iloc[:, 18:24]
    protein_contrib_2014.columns = Ages

    '''5. Create dataframe for mean contribution between 2008 and 2016'''
    z = [protein_contrib_2008, protein_contrib_2010, protein_contrib_2012, protein_contrib_2014]
    mean_df = pd.DataFrame(np.mean(z, axis=0))
    mean_df.columns = Ages

    '''6. Create the traces for each year group and the dropdown and plot'''

    fig = go.Figure()

    fig.add_trace(go.Pie(visible = True, values=mean_df.loc[:,'1.5-3'], labels = Food_group))
    fig.add_trace(go.Pie(visible = False, values=mean_df.loc[:,'4-10'], labels = Food_group))
    fig.add_trace(go.Pie(visible = False, values=mean_df.loc[:,'11-18'], labels = Food_group))
    fig.add_trace(go.Pie(visible = False, values=mean_df.loc[:,'19-64'], labels = Food_group))
    fig.add_trace(go.Pie(visible = False, values=mean_df.loc[:,'65-74'], labels = Food_group))
    fig.add_trace(go.Pie(visible = False, values=mean_df.loc[:,'75+'], labels = Food_group))

    # Add title and dropdown to select the desired age group
    fig.update_layout(
        title_text="Percentage Contribution of different food groups to Protein Intake in the UK between 2008 and 2016",
        title_x = 0.5,
        font_size = 15,
        template = "simple_white",

        legend=dict(yanchor="top", y=0.81, xanchor="left", x=0.92),

        updatemenus=[
            dict
            (
                active=0,
                buttons=list
                ([
                    dict(label="1.5-3",
                         method="update",
                         args=[{"visible": [True, False, False, False, False, False]},
                               {"title": "Contribution to Protein Intake for the 1.5 to 3 years old between 2008 and 2016"}]),
                    dict(label="4-10",
                         method="update",
                         args=[{"visible": [False, True, False, False, False]},
                               {"title": "Contribution to Protein Intake for the 4 to 10 years old between 2008 and 2016"}]),
                    dict(label="11-18",
                         method="update",
                         args=[{"visible": [False, False, True, False, False]},
                               {"title": "Contribution to Protein Intake for the 11 to 18 years old between 2008 and 2016"}]),
                    dict(label="19-64",
                         method="update",
                         args=[{"visible": [False, False, False, True, False, False, False]},
                               {"title": "Contribution to Protein Intake for the 19 to 64 years old between 2008 and 2016"}]),
                    dict(label="65-75",
                         method="update",
                         args=[{"visible": [False, False, False, False, True, False]},
                               {"title": "Contribution to Protein Intake for the 65 to 74 years old between 2008 and 2016"}]),
                    dict(label="75+",
                         method="update",
                         args=[{"visible": [False, False, False, False, False, True]},
                               {"title": "Contribution to Protein Intake for the 75+ years old between 2008 and 2016"}])
                ]),
                showactive=True,
                x=0.2,
                y=0.8,
            ),
        ]
    )

    #Add dropdown annotation
    fig.add_annotation(x=0, y=0.79, text="Select Age Range", showarrow=False)

    #fig.write_html("/Users/rayan/PycharmProjects/coursework-1-groups-group-6-comp0034/data/Dataset.xlsx")
    fig.show()

