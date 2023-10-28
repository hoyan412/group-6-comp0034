# Aydan Guliyeva
# Pie chart showing the percentage contribution of food groups to average daily calcium intake using Plotly Dash

# Importing required packages
import numpy as np
import math
import os.path
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import csv
import openpyxl
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input


if __name__ == "__main__":

    # Importing the dataset
    calcium_contribution = pd.read_excel(r'/Users/aydanguliyeva/PycharmProjects/coursework-1-groups-group-6-comp0034/data/Dataset.xlsx', engine = 'openpyxl', sheet_name='Calcium Contribution', skiprows= range(0,5), header= None)

    calcium_contribution = calcium_contribution.dropna()

    pd.set_option("display.max_rows", None, "display.max_columns", None)
    #print(calcium_contribution)

    calcium_contribution = calcium_contribution.drop([4,5,6,7,8,9,10,11,12,13,16,17,18,19,20,21,22,23,24,25,30,31,32,33,34,35,36,46,47,48,51,52,53,54,60,63,64,65,66,69,70,73,74,75,76,78,81], axis = 0)


    calcium_contribution08 = calcium_contribution.drop([7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24], axis=1)
    calcium_contribution10 = calcium_contribution.drop([1,2,3,4,5,6,13,14,15,16,17,18,19,20,21,22,23,24], axis=1)
    calcium_contribution12 = calcium_contribution.drop([1,2,3,4,5,6,7,8,9,10,11,12,19,20,21,22,23,24], axis=1)
    calcium_contribution14 = calcium_contribution.drop([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18], axis=1)

    print(calcium_contribution08)
    print(calcium_contribution08.columns)

    calcium_contribution08.columns = range(calcium_contribution08.shape[1])
    calcium_contribution10.columns = range( calcium_contribution10.shape[1])
    calcium_contribution12.columns = range(calcium_contribution12.shape[1])
    calcium_contribution14.columns = range(calcium_contribution12.shape[1])

    year_options = ['2008/09-2009/10','2010/11-2011/12','2012/13-2013/14','2014/15-2015/16']

    age_options = [
        {'label': '1.5-3 years','value': 1},
        {'label': '4-10 years', 'value':  2},
        {'label': '11-18 years', 'value': 3},
        {'label': '19-64 years', 'value': 4},
        {'label': '65-74 years', 'value': 5},
        {'label': '75+ years', 'value': 6} ]


    fig = px.pie(calcium_contribution08,values=1,names=0,title='Percentage contribution of food groups to average daily calcium intake')
    app = dash.Dash(__name__)
    app.layout = html.Div(
        children=[html.H1('Percentage contribution of food groups to average daily calcium intake'),
                  dcc.Graph(figure=fig, id='piechart'),
                  html.Label('Select the year to visualise:'),
                  dcc.Dropdown(id='year_slct',options=[{'label': y, 'value': y } for y in year_options], value= '2008/09-2009/10'),
                  html.Label('Select the age group to visualise:'),
                  dcc.Dropdown(id='age_slct',options=age_options,value=1),
                  html.Br(),
                  html.Div(id= "output-panel")])


    @app.callback(Output('piechart','figure'),
                  [Input('year_slct','value'),
                   Input('age_slct', 'value')])
    def generate_chart(slctd_year, slctd_age):
        if slctd_year == '2008/09-2009/10':
            fig = px.pie(calcium_contribution08, values=slctd_age, names=0)
            return fig
        elif slctd_year == '2010/11-2011/12':
            fig = px.pie(calcium_contribution10, values=slctd_age, names=0)
            return  fig
        elif slctd_year == '2012/13-2013/14':
            fig = px.pie(calcium_contribution12, values= slctd_age, names=0)
            return fig
        elif slctd_year == '2014/15-2015/16':
            fig = px.pie(calcium_contribution14, values = slctd_age, names=0)
            return fig



    app.run_server(debug=True)








