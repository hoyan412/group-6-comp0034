# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 03/03/2021
# Authors: Rayan Souissi - Youssef Alaoui Mrani - Ho Yan Or - Bailey Roberts - Aydan Guliyeva
# Description:
from pathlib import Path

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output

from Nutrients.Fat.DatasetOrg import DataOrg
from Nutrients.Fat.Fatchart import FatBarChart, FatPopulationChart, BarChartYears, Pie_chart

from Nutrients.Protein.ProteinData import ProteinData
from Nutrients.Protein.ProteinCharts import ProteinCharts
import pandas as pd
import plotly.express as px


xlsxfile = Path(__file__).parent.parent.joinpath('data/Dataset.xlsx')



##################################     YOUSSEF'S FAT INITIALISATION      ###########################################
# Call the dataset and prepare the labels

data = DataOrg(xlsxfile).DataSet_Org()
year = DataOrg(xlsxfile).org_year()
ages = {0: "4-10", 1: "11-18", 2: "19-64", 3: "65+", 4: "65-74", 5: "75+"}
option = [{"label": "2008 - 2010", "value": "1-2"}, {"label": "2010 - 2012", "value": "3-4"},
          {"label": "2012 - 2014", "value": "5-6"}, {"label": "2014 - 2016", "value": "7-8"}]
option_pie = [{"label": "2008 - 2010", "value": 'year_2008'}, {"label": "20010 - 2012", "value": 'year_2010'},
              {"label": "2012 - 2014", "value": 'year_2012'}
    , {"label": "2014 - 2016", "value": 'year_2014'}]

dict_pie = {'year_2008': year[0], 'year_2010': year[1], "year_2012": year[2], 'year_2014': year[3]}

ages_pie = {0: "1.5-3", 1: "4-10", 2: "11-18", 3: "19-64", 4: "65-74", 5: "75+"}

#Initialise the figures
fc = FatBarChart(data)
fig0 = fc.create_chart("1-2")

fpc = FatPopulationChart(data)
fig1 = fpc.create_chart("1-2")

fbc = BarChartYears(data)
fig2 = fbc.create_chart(0)

fp = Pie_chart(year[0])
figf3 = fp.create_pie_fat(0)

##################################     RAYAN'S PROTEIN INITIALISATION      ###########################################

protein_years_dico = {0: "2008-2010", 1: "2010-2012", 2: "2012-2014", 3: "2014-2016", 4: "2008-2016"}
protein_age_dico = {0: "1.5-3", 1: "4-10", 2: "11-18", 3: "19-64", 4: "65-74", 5: "75+"}

# Prepare the Protein data set
protein_data = ProteinData(xlsxfile)
protein_data.process_contribution_data()

# Create the figures
protein_chart = ProteinCharts(protein_data)
figP0 = protein_chart.create_pie()  # Generate Pie Chart (Contains traces for each age class and each period)
figP1 = protein_chart.create_bar_2016()  # Generate Stacked Bar Chart for period 2008-2016
figP2 = protein_chart.create_bar_2008()  # Generate Stacked Bar Chart for period 2008-2010
figP3 = protein_chart.create_bar_2010()  # Generate Stacked Bar Chart for period 2010-2012
figP4 = protein_chart.create_bar_2012()  # Generate Stacked Bar Chart for period 2012-2014
figP5 = protein_chart.create_bar_2014()  # Generate Stacked Bar Chart for period 2014-2016

##################################     HO YAN'S FREE SUGAR INITIALISATION      #########################################
# Import Dataset
excel_path = xlsxfile
df = pd.read_excel(excel_path, engine='openpyxl', sheet_name='Free Sugar Contribution', skiprows=5, nrows=55)

# Arrange data by year of study
y1 = df.iloc[:, 1:7]
y2 = df.iloc[:, 7:13]
y3 = df.iloc[:, 13:19]
y4 = df.iloc[:, 19:25]


def pie_data(year):
    year = year.drop(year.index[0])
    year = year.dropna()
    year = year.reset_index(drop=True)
    year = year.drop(year.index[1:10])
    year = year.drop(year.index[2:7])
    year = year.drop(year.index[3:9])
    year = year.drop(year.index[4:8])
    year = year.drop(year.index[6:8])
    year = year.drop(year.index[7:14])
    year = year.drop(year.index[8:])
    year = year.reset_index(drop=True)
    year.columns = ['1.5-3', '4-10', '11-18', '19-64', '65-74', '75+']
    food_cat = ['Cereal Products', 'Milk Products', 'Meat', 'Vegetable and potatoes', 'Sugar preserves and '
                                                                                      'Confectionery',
                'Non-alcoholic beverages', 'Alcohol beverages', 'Others']
    year.insert(loc=0, column='Food Categories', value=food_cat)
    return year


year_1 = pie_data(y1)
year_2 = pie_data(y2)
year_3 = pie_data(y3)
year_4 = pie_data(y4)
category = year_1['Food Categories']

fig_sugar = px.pie(year_1, values=year_1['19-64'], names=category,
                   title='Free Sugar Contribution for 19-64 years old [2008-10]',
                   hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)

##################################     BAILEY'S MAGNESIUM INITIALISATION      ##########################################

magnesium_cont = pd.read_excel(xlsxfile,
                        engine='openpyxl', sheet_name='Magnesium Contribution', skiprows=range(0, 5), header=None)
magnesium_cont = magnesium_cont.dropna()
magnesium_cont = magnesium_cont.drop(
    [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 48,
     49, 50, 53, 54, 55, 56, 62, 63, 66, 67, 68, 69, 72, 73, 76, 77, 78, 79, 81, 84], axis=0)
magnesium_cont_08 = magnesium_cont.drop([7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], axis=1)
magnesium_cont_10 = magnesium_cont.drop([1, 2, 3, 4, 5, 6, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], axis=1)
magnesium_cont_12 = magnesium_cont.drop([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19, 20, 21, 22, 23, 24], axis=1)
magnesium_cont_14 = magnesium_cont.drop([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], axis=1)
magnesium_cont_08.columns = range(magnesium_cont_08.shape[1])
magnesium_cont_10.columns = range(magnesium_cont_10.shape[1])
magnesium_cont_12.columns = range(magnesium_cont_12.shape[1])
magnesium_cont_14.columns = range(magnesium_cont_14.shape[1])
year_options = ['2008/09-2009/10', '2010/11-2011/12', '2012/13-2013/14', '2014/15-2015/16']
age_options = [
    {'label': '1.5-3', 'value': 1},
    {'label': '4-10', 'value': 2},
    {'label': '11-18', 'value': 3},
    {'label': '19-64', 'value': 4},
    {'label': '65-74', 'value': 5},
    {'label': '75+', 'value': 6}]
fig = px.pie(magnesium_cont_08, values=1, names=0,
             title='What foods make up the total magnesium intake for each age group, in each year of the study')

##################################     AYDAN'S CALCIUM INITIALISATION      ###########################################
# Importing the dataset
calcium_contribution = pd.read_excel(xlsxfile,
                        engine='openpyxl', sheet_name='Calcium Contribution', skiprows=range(0, 5), header=None)
calcium_contribution = calcium_contribution.dropna()
pd.set_option("display.max_rows", None, "display.max_columns", None)
calcium_contribution = calcium_contribution.drop(
    [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 35, 36, 46, 47, 48,
     51, 52, 53, 54, 60, 63, 64, 65, 66, 69, 70, 73, 74, 75, 76, 78, 81], axis=0)
calcium_contribution08 = calcium_contribution.drop(
    [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], axis=1)
calcium_contribution10 = calcium_contribution.drop([1, 2, 3, 4, 5, 6, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
                                                   axis=1)
calcium_contribution12 = calcium_contribution.drop([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19, 20, 21, 22, 23, 24],
                                                   axis=1)
calcium_contribution14 = calcium_contribution.drop([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                                                   axis=1)
calcium_contribution08.columns = range(calcium_contribution08.shape[1])
calcium_contribution10.columns = range(calcium_contribution10.shape[1])
calcium_contribution12.columns = range(calcium_contribution12.shape[1])
calcium_contribution14.columns = range(calcium_contribution12.shape[1])
year_options = ['2008/09-2009/10', '2010/11-2011/12', '2012/13-2013/14', '2014/15-2015/16']
age_options = [
    {'label': '1.5-3 years', 'value': 1},
    {'label': '4-10 years', 'value': 2},
    {'label': '11-18 years', 'value': 3},
    {'label': '19-64 years', 'value': 4},
    {'label': '65-74 years', 'value': 5},
    {'label': '75+ years', 'value': 6}]
figpie = px.pie(calcium_contribution08, values=1, names=0,
                title='Percentage contribution of food groups to average daily calcium intake')



#######################################      DASH APP       ############################################################


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(server=server, routes_pathname_prefix='/dashapp/', external_stylesheets=[dbc.themes.LUX])

    # Create the flask_app layout using Bootstrap fluid container
    dash_app.layout = dbc.Container(fluid=True, children=[
        dbc.Tabs(className="nav nav-pills", children=[
            dbc.Tab(
                dbc.Tabs(className="nav nav-pills", children=[

                    dbc.Tab(
                        dbc.Row([
                            # Add the first column here. This is for the year selector
                            dbc.Col(width=3, children=[
                                dbc.FormGroup([
                                    html.H4("Select Year"),

                                    dcc.Dropdown(id="period_select", options=option
                                                 , value="1-2")
                                ]),
                                html.Br(),
                                html.Div(id="output-panel")

                            ]),
                            # Add the second column here. This is for the figure.
                            dbc.Col(width=9, children=[

                                dbc.Tabs(className="nav nav-pills", children=[
                                    dbc.Tab(dcc.Graph(id="fat-year", figure=fig0), label="Fat intake per age group"),
                                    dbc.Tab(dcc.Graph(id="fat-population-year", figure=fig1),
                                            label="Fat Intake population pyramid"),

                                ])
                            ]),

                        ]), label=" Intake with variable year"),

                    dbc.Tab(

                        dbc.Row([
                            # Add the first column here. This is for the age selector

                            dbc.Col(width=3, children=[
                                dbc.FormGroup([

                                    html.H4("Select age group"),

                                    dbc.Col([dcc.Slider(id="Age_group_select", min=0, max=5, step=None, marks=ages
                                                        , value=0, vertical=True)])

                                ]),
                                html.Br(),
                                html.Div(id="output-panel-p2")

                            ]),
                            # Add the second column here. This is for the figure.
                            dbc.Col(width=9, children=[

                                dbc.Tabs(className="nav nav-pills", children=[
                                    dbc.Tab(dcc.Graph(id="fat-age", figure=fig2),
                                            label="Fat intake per year for different age groups"),

                                ])
                            ]),

                        ]), label="Intake with variable age group"),
                    dbc.Tab(

                        dbc.Row([
                            # Add the first column here. This is for the year and age selector.

                            dbc.Col(width=3, children=[

                                dbc.FormGroup([
                                    html.H4("Select Year"),

                                    dcc.Dropdown(id="period_select_pie", options=option_pie
                                                 , value="year_2008")
                                ]),
                                html.Br(),
                                html.Div(id="output-panel-pie-1"),
                                dbc.FormGroup([

                                    html.H4("Select age group"),
                                    # dash-core-components (dcc) provides a dropdown

                                    dbc.Col(
                                        [dcc.Slider(id="Age_group_select_pie", min=0, max=5, step=None, marks=ages_pie
                                                    , value=0)])

                                ]),
                                html.Br(),
                                html.Div(id="output-panel-pie-chart")

                            ]),
                            # Add the second column here. This is for the figure.
                            dbc.Col(width=9, children=[

                                dbc.Tab(dcc.Graph(id="fat-pie", figure=figf3),
                                        label="Contribution"),

                            ]),

                        ]), label="Contribution to fat intake")
                ]), label=("Fat")),

            dbc.Tab(  #######################################RAYAN'S TAB################################################

                # Add Row 2: Contains the Dropdown, Slider and Panel on Column 1 and Charts on Column 2
                dbc.Row([
                    dbc.Col(width=3, children=
                    [
                        html.Br(),  # Jump line
                        html.H4('Select Data', ),  # Slider and Dropdown Title

                        html.Label('Period'),  # Slider Label
                        dcc.Slider  # Add Slider
                            (
                            id="Protein Period",
                            min=0,
                            max=4,
                            marks=
                            {
                                0: {'label': '2008-2010', 'style': {'textAlign': 'center', 'color': 'black'}},
                                1: {'label': '2010-2012', 'style': {'textAlign': 'center', 'color': 'black'}},
                                2: {'label': '2012-2014', 'style': {'textAlign': 'center', 'color': 'black'}},
                                3: {'label': '2014-2016', 'style': {'textAlign': 'center', 'color': 'black'}},
                                4: {'label': '2008-2016', 'style': {'textAlign': 'center', 'color': 'black'}},
                            },
                            value=4,
                            step=None,
                            included=False,
                        ),
                        html.Br(),  # Jump line

                        html.Label('Age Class'),  # Drodpwon Label
                        dcc.Dropdown  # Add dropdown
                            (
                            id="Protein Age Class",
                            options=
                            [
                                {'label': '1.5 to 3 years old', "value": 0, },
                                {'label': '4 to 10 years old', "value": 1},
                                {'label': '11 to 18 years old', "value": 2},
                                {'label': '19 to 64 years old', "value": 3},
                                {'label': '65 to 75 years old', "value": 4},
                                {'label': '75+ years old', "value": 5},
                            ],
                            style={'textAlign': 'center', },
                            value=0,
                            placeholder="Select Age Range"
                        ),
                        html.Br(),  # Jump line

                        html.H4("Information", ),  # Add Information Panel title
                        html.Div(id="Protein output-panel"),  # Add output panel
                        html.Br(),  # Jump line

                        html.H4('Select Visualisation', ),  # Add Visualisation dropdown title
                        html.Br(),  # Jump line
                        dcc.Dropdown  # Add drodowpn
                            (
                            id="Protein Visualisation",
                            options=
                            [
                                {'label': 'Pie Chart', "value": 1},
                                {'label': 'Bar Chart', "value": 2},
                            ],
                            style={'textAlign': 'center', },
                            value=1,
                            placeholder="Select Visualisaion"
                        ),
                        html.Br(),  # Jump line

                    ]),  # END OF COLUMN 1

                    # Add Column2 of Row 2: Chart
                    dbc.Col(width=9, children=
                    [
                        # html.P('col 2'),
                        dcc.Graph(id='Protein Chart'
                                  ),
                    ]),  # END OF COLUMN 2

                ], no_gutters=True, ),  # END OF ROW

                label=("Protein")

            ),  ################################      END OF RAYAN'S TAB   #########################################

            dbc.Tab(######################################HO YAN'S TAB################################################
                html.Div([
                dbc.Row(dbc.Col(html.H3("Food group contribution to free sugar intake in the UK"),
                                style={'width': '75%', 'margin': 25, 'textAlign': 'center'}
                                ),
                        ),
                dbc.Row(dbc.Col(html.Div(
                    "Different food groups contribute differently to the average sugar intake of individuals in the UK. This "
                    "is "
                    "shown in the pie chart below. Through selecting the options in the dropdown menus, you can visualise the "
                    "contribution of food groups to free sugar intake for a selected age group and time period."),
                    style={'margin': 5}
                    ),
                ),

                dbc.Row(dbc.Col(html.H6("Select Data: "), width={'offset': 2},
                        )
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Dropdown(id='select_year', placeholder='Select time period',
                                             options=[
                                                 {"label": "2008 - 10", "value": '2008-10'},
                                                 {"label": "2010 - 12", "value": '2010-12'},
                                                 {"label": "2012 - 14", "value": '2012-14'},
                                                 {"label": "2014 - 16", "value": '2014-16'}]),
                                width={'size': 3, 'offset': 2, 'order': 1},
                                style={'textAlign': 'center'},
                                ),

                        dbc.Col(dcc.Dropdown(id='select_age', placeholder='Select age group',
                                             options=[
                                                 {"label": "1.5 - 3 years old", "value": '1.5-3'},
                                                 {"label": "4 - 10 years old", "value": '4-10'},
                                                 {"label": "11 - 18 years old", "value": '11-18'},
                                                 {"label": "19 - 64 years old", "value": '19-64'},
                                                 {"label": "65 - 74 years old", "value": '65-74'},
                                                 {"label": "75+ years old", "value": '75+'}]),
                                width={'size': 3, 'offset': 1, 'order': 2},
                                style={'textAlign': 'center'},
                                ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(id='pie_chart', figure=fig_sugar),
                                width=8, lg={'size': 9, "offset": 1}
                                ),
                    ]
                )
            ]),

                label="Free Sugar"),

            dbc.Tab(  ########################## Baileys Tab
                html.Div(children=[html.H1(
                    'What foods make up the total magnesium intake for each age group, in each year of the study'),
                                   dcc.Graph(figure=fig, id='graph'),
                                   html.Label('Please choose which year of the study you would like to visualise:'),
                                   dcc.Dropdown(id='year_select',
                                                options=[{'label': a, 'value': a} for a in year_options],
                                                value='2008/09-2009/10'),
                                   html.Label('Please choose which age group you would like to visualise:'),
                                   dcc.Dropdown(id='age_select', options=age_options, value=1),
                                   html.Br(),
                                   html.Div(id="output-panel-magnesium")]),
                label="Magnesium"),

            dbc.Tab(
                #######################################AYDAN'S TAB################################################)
                html.Div(
                    children=[
                        html.Br(),
                        html.H1('Percentage contribution of food groups to average daily calcium intake'),
                        dcc.Graph(figure=figpie, id='piechart'),
                        html.Label('Select the year to visualise:'),
                        dcc.Dropdown(id='year_slct', options=[{'label': y, 'value': y} for y in year_options],
                                           value='2008/09-2009/10'),
                        html.Label('Select the age group to visualise:'),
                        dcc.Dropdown(id='age_slct', options=age_options, value=1),
                        html.Br(),
                        html.Div(id="output-panel-calcium")]),
                label=("Calcium"),
            )
        ]),

    ])


    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):

    ################################### YOUSSEF'S FAT CALLBACKS############################################

    @dash_app.callback(Output("fat-year", "figure"), [Input("period_select", "value")])
    def update_fat_chart(period_select):
        figA = fc.create_chart(period_select)
        return figA

    @dash_app.callback(Output("fat-population-year", "figure"), [Input("period_select", "value")])
    def update_fat_chart(period_select):
        figB = fpc.create_chart(period_select)
        return figB

    @dash_app.callback(Output("fat-age", "figure"), [Input("Age_group_select", "value")])
    def update_age_chart(Age_group_select):
        figC = fbc.create_chart(Age_group_select)
        return figC

    @dash_app.callback(Output("fat-pie", "figure"),
                  [Input("Age_group_select_pie", "value"), Input("period_select_pie", "value")])
    def update_pie_chart(Age_group_select_pie, period_select_pie):
        fp = Pie_chart(dict_pie[period_select_pie])
        figP = fp.create_pie_fat(Age_group_select_pie)
        return figP


    ###################################      RAYAN'S PROTEIN CALLBACKS      ###########################################

    # Callback to update the chart according to year, period, and visualisation type
    @dash_app.callback(
        Output('Protein Chart', 'figure'),  # output
        [Input('Protein Period', 'value'), Input('Protein Age Class', 'value'),
         Input('Protein Visualisation', 'value')],  # list of input
    )
    # Add method to update which chart to output and the trace (if pie chart), and the title of the chart
    def update_protein_pie_chart(selected_year, selected_age, visu):
        # Make all traces not visible
        figP0.update_traces(selector=dict(visible=True), visible=False)
        # Set the visible pie chart trace
        figP0.update_traces(selector=dict(name=str(selected_year) + " - " + str(selected_age)), visible=True)
        # Set Pie Chart Title
        figP0.update_layout(title_text="Percentage Contribution to Protein Intake for the {}"
                                       " years old in the UK between {}".format(protein_age_dico[selected_age],
                                                                                protein_years_dico[selected_year]))
        if visu == 2:
            if selected_year == 4:
                return figP1  # Output Bar chart for 2008-2016
            elif selected_year == 0:
                return figP2  # Output Bar chart for 2008-2010
            elif selected_year == 1:
                return figP3  # Output Bar chart for 2010-2012
            elif selected_year == 2:
                return figP4  # Output Bar chart for 2012-2014
            elif selected_year == 3:
                return figP5  # Output Bar chart for 2014-2016

        return figP0  # Output Pie Chart

    # Callback to update the information panel
    @dash_app.callback(
        Output("Protein output-panel", "children"),
        [Input('Protein Period', 'value'), Input('Protein Age Class', 'value')],
    )
    # Add method to output and update panel informations according to inputs
    def render_protein_output_panel(selected_year, selected_age):
        age = protein_age_dico[selected_age]  # translate dropdown value to age
        year = protein_years_dico[selected_year]  # translate slider value to period

        protein_data.process_intake_data()  # get the intake for the age and period selected
        panel = html.Div([
            dbc.Card(body=True, children=[
                html.H6("Period:"),
                html.H4(year),
                html.Br(),
                html.H6("Age Class:"),
                html.H4("{} years old".format(age)),
                html.Br(),
                html.H6("Protein Intake:"),
                html.H4("{} g/day".format(round(protein_data.protein_contrib_intake[selected_age], 1))),
            ])
        ])
        return panel


    ###################################        HO YAN'S FREE SUGAR CALLBACK      #######################################

    @dash_app.callback(Output('pie_chart', 'figure'),
                  [Input('select_year', 'value'),
                   Input('select_age', 'value')])
    def create_pie(year, age):
        if age is None:
            return fig_sugar
        elif year == '2008-10':
            fig1 = px.pie(year_1, values=year_1[age], names=category,
                          hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
            return fig1

        elif year == '2010-12':
            fig2 = px.pie(year_2, values=year_2[age], names=category,
                          hole=0.4, color_discrete_sequence=px.colors.sequential.YlGnBu)
            return fig2

        elif year == '2012-14':
            fig3 = px.pie(year_3, values=year_3[age], names=category,
                          hole=0.4, color_discrete_sequence=px.colors.sequential.thermal)
            return fig3

        elif year == '2014-16':
            fig4 = px.pie(year_4, values=year_4[age], names=category,
                          hole=0.4, color_discrete_sequence=px.colors.sequential.matter)
            return fig4

        else:
            return fig_sugar


    ######################################       Bailey Magnesium Callback     ######################################

    @dash_app.callback(Output('graph', 'figure'),
                  [Input('year_select', 'value'),
                   Input('age_select', 'value')])
    def generate_chart(selected_year, selected_age):
        if selected_year == '2008/09-2009/10':
            fig = px.pie(magnesium_cont_08, values=selected_age, names=0)
            return fig
        elif selected_year == '2010/11-2011/12':
            fig = px.pie(magnesium_cont_10, values=selected_age, names=0)
            return fig
        elif selected_year == '2012/13-2013/14':
            fig = px.pie(magnesium_cont_12, values=selected_age, names=0)
            return fig
        elif selected_year == '2014/15-2015/16':
            fig = px.pie(magnesium_cont_14, values=selected_age, names=0)
            return fig


    ###################################     AYDAN'S CALCIUM CALLBACKS      ############################################

    @dash_app.callback(Output('piechart', 'figure'),
                  [Input('year_slct', 'value'),
                   Input('age_slct', 'value')])
    def generate_chart(slctd_year, slctd_age):
        if slctd_year == '2008/09-2009/10':
            figpie = px.pie(calcium_contribution08, values=slctd_age, names=0)
            return figpie
        elif slctd_year == '2010/11-2011/12':
            figpie = px.pie(calcium_contribution10, values=slctd_age, names=0)
            return figpie
        elif slctd_year == '2012/13-2013/14':
            figpie = px.pie(calcium_contribution12, values=slctd_age, names=0)
            return figpie
        elif slctd_year == '2014/15-2015/16':
            figpie = px.pie(calcium_contribution14, values=slctd_age, names=0)
            return figpie
