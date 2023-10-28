# Author: Bailey Roberts

import numpy as np
import math
import os.path
import xlrd
import tkinter as tk
from tkinter import filedialog
import xlsxwriter
import pandas as pd
import csv
import openpyxl
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input


if __name__ == "__main__":


 # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html, read the excel document, and remove header
    magnesium_cont = pd.read_excel('data/Dataset.xlsx', engine = 'openpyxl', sheet_name='Magnesium Contribution', skiprows= range(0,5), header= None)

# drop all null values
    magnesium_cont = magnesium_cont.dropna()

# In the dataset the contribution of magnesium is made up of headers which are then broken down further.
# Here everything is dropped so that only the headers remain.
    magnesium_cont = magnesium_cont.drop([4,5,6,7,8,9,10,11,12,13,16,17,18,19,20,21,22,23,24,29,30,31,32,33,34,35,36,37,38,48,49,50,53,54,55,56,62,63,66,67,68,69,72,73,76,77,78,79, 81,84], axis = 0)

# Separate the years, the columns are dropped so that each year of the study is broken up.
# Within each of these years, we have contribution of each age  group in that year.
    magnesium_cont_08 = magnesium_cont.drop([7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24], axis=1)
    magnesium_cont_10 = magnesium_cont.drop([1,2,3,4,5,6,13,14,15,16,17,18,19,20,21,22,23,24], axis =1)
    magnesium_cont_12 = magnesium_cont.drop([1,2,3,4,5,6,7,8,9,10,11,12,19,20,21,22,23,24], axis = 1)
    magnesium_cont_14 = magnesium_cont.drop([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], axis =1)

# The renames the columns to numbers, depending on how many columns are in the dataframe.
# the columns are renamed to 0, 1, 2, 3 ...
    magnesium_cont_08.columns = range(magnesium_cont_08.shape[1])
    magnesium_cont_10.columns = range(magnesium_cont_10.shape[1])
    magnesium_cont_12.columns = range(magnesium_cont_12.shape[1])
    magnesium_cont_14.columns = range(magnesium_cont_14.shape[1])

# this produces a list for the years of the study, and dictionary which links the numbered column names to age groups.
# this will be used in the callback
    year_options = ['2008/09-2009/10','2010/11-2011/12','2012/13-2013/14','2014/15-2015/16']
    age_options = [
                  {'label': '1.5-3','value': 1},
                  {'label': '4-10', 'value':  2},
                  {'label': '11-18', 'value': 3},
                  {'label': '19-64', 'value': 4},
                  {'label': '65-74', 'value': 5},
                  {'label': '75+', 'value': 6} ]

# plot the pie chart, the names of the sections in the pie chart are in column 0.
# there are two drop downs here, one which chooses the year, and one which chooses the age group.
# the age group dropdown uses the dictionary above. if '1.5-3' is enetered it will use a value of 1,  which corresponds to column 1, which is for the '1.5-3' age  group.
# the year dropdown creates a dicitonary where the key and value are identical and equal to the strings in  the list above.
    fig = px.pie(magnesium_cont_08,values=1,names=0,title='What foods make up the total magnesium intake for each age group, in each year of the study')
    app = dash.Dash(__name__)
    app.layout = html.Div(children=[html.H1('What foods make up the total magnesium intake for each age group, in each year of the study'), dcc.Graph(figure=fig, id='graph'), html.Label('Please choose which year of the study you would like to visualise:'), dcc.Dropdown(id='year_select',options=[{'label': a, 'value': a } for a in year_options], value= '2008/09-2009/10'), html.Label('Please choose which age group you would like to visualise:'),  dcc.Dropdown(id='age_select',options=age_options,value=1), html.Br(), html.Div(id= "output-panel")])

# In the callback, both  dropdowns are used.
# the if, elif ... means that depending on which year is selected, a different dataframe is used for the plot.
# inside each if, elif, a new figure is plotted and the chart on the dash flask_app changes. The values inside the pie chart change
# depending on the selected age. if the selected age is '1.5-3' then selected_age =  1 according to the dicionary.
# therefore in the dataframe, column 1 is selected for the pie chart, which corresponds to the value for age 1.5-3 in that year.
    @app.callback(Output('graph','figure'),
                  [Input('year_select','value'),
                   Input('age_select', 'value')])
    def generate_chart(selected_year, selected_age):
      if selected_year == '2008/09-2009/10':
         fig = px.pie(magnesium_cont_08, values=selected_age, names=0)
         return fig
      elif selected_year == '2010/11-2011/12':
         fig = px.pie(magnesium_cont_10, values=selected_age, names=0)
         return  fig
      elif selected_year == '2012/13-2013/14':
         fig = px.pie(magnesium_cont_12, values= selected_age, names=0)
         return fig
      elif selected_year == '2014/15-2015/16':
         fig = px.pie(magnesium_cont_14, values = selected_age, names=0)
         return fig

    app.run_server(debug=True)



