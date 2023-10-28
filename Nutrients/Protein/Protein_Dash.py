# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 03/03/2021
# Name: Protei_Dash_Pie
# Author: Rayan Souissi
# Description: Program to generate a dash flask_app to output different plots to show the protein intake
#               and contribution (of different food groups)
#               for different periods and age classes using interactive Plotly and Dash features

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.io as pio
import dash_bootstrap_components as dbc

from Nutrients.Protein.ProteinData import ProteinData
from Nutrients.Protein.ProteinCharts import ProteinCharts
from dash.dependencies import Output, Input

pio.renderers.default = "browser"

years_dico = {0 : "2008-2010", 1 : "2010-2012", 2 :"2012-2014", 3 : "2014-2016", 4: "2008-2016"}
                                #Disctionary used to convert (in the callbacks) the Slider values (keys) to the years
age_dico = {0 : "1.5-3", 1 : "4-10", 2 : "11-18", 3 : "19-64" , 4 : "65-74" , 5: "75+"}
                                #Disctionary used to convert (in the callbacks) the Drodpwon values (keys) to the ages

# Prepare the data set
data = ProteinData()            #Create the ProteinData instance to have access to all variables and functions
data.process_contribution_data()            #run the process_contribution_data() of the ProteinData instance

# Create the figures
chart = ProteinCharts(data)     #Create the ProteinChart instance to have access to all charts
fig0 = chart.create_pie()            #Generate Pie Chart (Contains traces for each age class and each period)
fig1 = chart.create_bar_2016()                    #Generate Stacked Bar Chart for period 2008-2016
fig2 = chart.create_bar_2008()                #Generate Stacked Bar Chart for period 2008-2010
fig3 = chart.create_bar_2010()              #Generate Stacked Bar Chart for period 2010-2012
fig4 = chart.create_bar_2012()          #Generate Stacked Bar Chart for period 2012-2014
fig5 = chart.create_bar_2014()      #Generate Stacked Bar Chart for period 2014-2016



# Create a Dash flask_app instance
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUX])

# Create the flask_app layout
app.layout = html.Div(children=[

    html.H1(    #App Title
                children='Nutritional Data Visualisation',
                style=  {'textAlign': 'center'}     #Set position
            ),

    dbc.Row([       #Add Row 1: Contains The titles of each nutrient
            #Add Column1 of Row 1: Protein
            dbc.Col(width={'size' : 2, 'offset' : 0.5}, className="bg-dark text-light", children=
            [
                #html.P('col 1'),   #For layout adjustments
                html.H2( children='Protein',className="card-text text-light"),
            ]),
            #Add Column2 of Row 1: Fat
            dbc.Col(width=2, className="bg-dark text-light",children=
            [
                #html.P('col 2'),   #For layout adjustments
                html.H2( children='Fat',className="card-text text-light"),
            ]),
            #Add Column3 of Row 1: Free Sugar
            dbc.Col(width=2, className="bg-dark text-light",children=
            [
                #html.P('col 3'),   #For layout adjustments
                html.H2( children='Free Sugar',className="card-text text-light"),
            ]),
            #Add Column4 of Row 1: Calcium
            dbc.Col(width=2, className="bg-dark text-light",children=
            [
                #html.P('col 4'),   #For layout adjustments
                html.H2( children='Calcium',className="card-text text-light"),
            ]),
            #Add Column5 of Row 1: Magnesium
            dbc.Col(width=2, className="bg-dark text-light",children=
            [
                #html.P('col 5'),   #For layout adjustments
                html.H2( children='Magnesium',className="card-text text-light"),
            ]),

        ],no_gutters=True), #To remove spaces between rows
        #END OF ROW 1

    #App description text
    html.P('A Dash web application framework for Python conceived by Rayan Souissi to analyse '
           'the Protein Intake in g/day and Contribution of different food groups to the Protein Intake, for different '
           'age classes and period of time', className="bg-dark text-light"),

    dbc.Row([   #Add Row 2: Contains the Dropdown, Slider and Panel on Column 1 and Charts on Column 2

            #Add Column1 of Row 2: Period Sider than Age Dropdown then Information Panel then Visualisation dropdown
            dbc.Col(width=3, className="bg-dark text-light", children=
            [
                #html.P('col 1'),   #For layout adjustments
                html.H4('Select Data',className="card-text text-light"),    #Slider and Dropdown Title

                html.Label('Period'),   #Slider Label
                dcc.Slider  #Add Slider
                (
                    id = "Period",
                    min=0,
                    max=4,
                    marks={
                            0:{'label' :'2008-2010',  'style': {'textAlign': 'center', 'color': '#77b0b1'}},
                            1:{'label' :'2010-2012',  'style': {'textAlign': 'center', 'color': '#77b0b1'}},
                            2:{'label' :'2012-2014',  'style': {'textAlign': 'center', 'color': '#77b0b1'}},
                            3:{'label' :'2014-2016',  'style': {'textAlign': 'center', 'color': '#77b0b1'}},
                            4:{'label' :'2008-2016',  'style': {'textAlign': 'center', 'color': '#77b0b1'}},
                          },
                    value = 4,
                    step = None,
                    included = False,
                ),
                html.Br(),  #Jump a line

                html.Label('Age Class'),    #Drodpwon Label
                dcc.Dropdown    #Add dropdown
                (
                    id = "Age Class",
                    options=[
                                {'label': '1.5 to 3 years old', "value":0},
                                {'label': '4 to 10 years old', "value":1},
                                {'label': '11 to 18 years old', "value":2},
                                {'label': '19 to 64 years old', "value":3},
                                {'label': '65 to 75 years old', "value":4},
                                {'label': '75+ years old', "value":5},
                            ],
                    style={'textAlign': 'center','color': 'black','background-color': 'white',},
                    value = 0,
                    placeholder = "Select Age Range"
                ),
                html.Br(),#Jump a line

                html.H4("Information", className="card-text text-light"),   #Add Information Panel title
                html.Div(id="output-panel"),    #Add output panel
                html.Br(),  #jump a line

                html.H4('Select Visualisation', className="card-text text-light"),  #Add Visualisation dropdown title
                html.Br(),  #jump a line
                dcc.Dropdown    #Add drodowpn
                (
                    id = "Visualisation",
                    options=[
                                {'label': 'Pie Chart', "value":1},
                                {'label': 'Bar Chart', "value":2},
                            ],
                    style={'textAlign': 'center','color': 'black','background-color': 'white',},
                    value = 1,
                    placeholder = "Select Visualisaion"
                ),
                html.Br(),

            ]),     #END OF COLUMN1 ROW2

            #Add Column2 of Row 2: Chart
            dbc.Col(width=9, children=
            [
                dcc.Graph( id='Chart' ),
            ]),     #END OF COLUMN2 ROW2

        ],no_gutters=True ),    #To remove spaces between rows
        #END OF ROW 2

])  #END OF DASH APP LAYOUT


#Callback to update the chart according to year, period, and visualisation type
@app.callback(
    Output('Chart', 'figure'),      #output
    [Input('Period', 'value'), Input('Age Class', 'value'), Input('Visualisation', 'value')],   #list of input
)

#Add method to update which chart to output and the trace (if pie chart), and the title of the chart
def update_output(selected_year, selected_age, visu):
    #Make all traces not visibles
    fig0.update_traces(selector=dict(visible = True), visible = False)
    #Set the visible pie chart trace
    fig0.update_traces(selector=dict(name= str(selected_year) + " - " + str(selected_age)), visible = True)
    #Set Pie Chart Title
    fig0.update_layout(title_text =  "{} Protein Intake for the {}".format(years_dico[selected_year],
                                                                           age_dico[selected_age])+" years old" )

    if visu == 2:
        if selected_year == 4:
            return fig1             #Output Bar chart for 2008-2016
        elif selected_year == 0:
            return fig2             #Output Bar chart for 2008-2010
        elif selected_year == 1:
            return fig3             #Output Bar chart for 2010-2012
        elif selected_year == 2:
            return fig4             #Output Bar chart for 2012-2014
        elif selected_year == 3:
            return fig5             #Output Bar chart for 2014-2016

    return fig0         #Output Chart

#Callback to update the information panel
@app.callback(
    Output("output-panel", "children"),     #output
    [Input('Period', 'value'), Input('Age Class', 'value')],    #list of inputs
)

#Add method to output and update panel informations according to inputs
def render_output_panel(selected_year, selected_age):
    age = age_dico[selected_age]        #translate dropdown value to age
    year = years_dico[selected_year]        #translate slider value to period

    data.process_intake_data()  #get the intake for the age and period selected
    panel = html.Div([
        dbc.Card(body=True, className="bg-dark text-light", children=[
            html.H6("Period:", className="card-title"),
            html.H4(year, className="card-text text-light"),
            html.Br(),
            html.H6("Age Class:", className="card-title"),
            html.H4("{} years old".format(age), className="card-text text-light"),
            html.Br(),
            html.H6("Protein Intake:", className="card-title"),
            html.H4("{} g/day".format(round(data.protein_contrib_intake[selected_age],1)), className="card-text text-light"),
        ])
    ])
    return panel

app.run_server(debug=True)      #run the dashapp
