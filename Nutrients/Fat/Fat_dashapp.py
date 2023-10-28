# Created by Youssef ALAOUI MRANI
# Description:
# This code was used to generate the fat intake dash flask_app.

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output

from Nutrients.Fat.DatasetOrg import df_tot, year_2010, year_2012, year_2008, year_2014
from Nutrients.Fat.Fatchart import FatBarChart, FatPopulationChart, BarChartYears, Pie_chart

# Prepare the data set
data = df_tot

ages = {0: "4-10", 1: "11-18", 2: "19-64", 3: "65+", 4: "65-74", 5: "75+"}
option = [{"label": "2008 - 2010", "value": "1-2"}, {"label": "2010 - 2012", "value": "3-4"},
          {"label": "2012 - 2014", "value": "5-6"}, {"label": "2014 - 2016", "value": "7-8"}]
option_pie = [{"label": "2008 - 2010", "value": 'year_2008'}, {"label": "20010 - 2012", "value": 'year_2010'},
              {"label": "2012 - 2014", "value": 'year_2012'}
    , {"label": "2014 - 2016", "value": 'year_2014'}]

dict_pie = {'year_2008': year_2008, 'year_2010': year_2010, "year_2012": year_2012, 'year_2014': year_2014}

ages_pie = {0: "1.5-3", 1: "4-10", 2: "11-18", 3: "19-64", 4: "65-74", 5: "75+"}
# Create the figures

fc = FatBarChart(data)
fig = fc.create_chart("1-2")

fpc = FatPopulationChart(data)
fig1 = fpc.create_chart("1-2")

fbc = BarChartYears(data)
fig2 = fbc.create_chart(0)

fp = Pie_chart(year_2008)
fig3 = fp.create_pie_fat(0)

# Create a Dash flask_app (using bootstrap).
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])

# Create the flask_app layout using Bootstrap fluid container
app.layout = dbc.Container(fluid=True, children=[
    html.Br(),
    html.H1('Nutrition data visualisation'),
    html.P(
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum..',
        className='lead'),
    html.H2('Fat intake'),
    dbc.Tabs(className="nav nav-pills", children=[

        dbc.Tab(
            dbc.Row([
                # Add the first column here. This is for the area selector and the statistics panel.
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
                        dbc.Tab(dcc.Graph(id="fat-year", figure=fig), label="Fat intake per age group"),
                        dbc.Tab(dcc.Graph(id="fat-population-year", figure=fig1),
                                label="Fat intake population pyramid"),

                    ])
                ]),

            ]), label="Per Age group"),
        dbc.Tab(

            dbc.Row([
                # Add the first column here. This is for the area selector

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

            ]), label="Per year"),
        dbc.Tab(

            dbc.Row([
                # Add the first column here. This is for the area selector and the statistics panel.

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

                        dbc.Col([dcc.Slider(id="Age_group_select_pie", min=0, max=5, step=None, marks=ages_pie
                                            , value=0)])

                    ]),
                    html.Br(),
                    html.Div(id="output-panel-pie-chart")

                ]),
                # Add the second column here. This is for the figure.
                dbc.Col(width=9, children=[

                    dbc.Tab(dcc.Graph(id="fat-pie", figure=fig3),
                            label="Contribution"),

                ]),

            ]), label="Contribution")
    ])
])


@app.callback(Output("fat-year", "figure"), [Input("period_select", "value")])
def update_fat_chart(period_select):
    figA = fc.create_chart(period_select)
    return figA


@app.callback(Output("fat-population-year", "figure"), [Input("period_select", "value")])
def update_fat_chart(period_select):
    figB = fpc.create_chart(period_select)
    return figB


@app.callback(Output("fat-age", "figure"), [Input("Age_group_select", "value")])
def update_age_chart(Age_group_select):
    figC = fbc.create_chart(Age_group_select)
    return figC


@app.callback(Output("fat-pie", "figure"),
              [Input("Age_group_select_pie", "value"), Input("period_select_pie", "value")])
def update_pie_chart(Age_group_select_pie, period_select_pie):
    fp = Pie_chart(dict_pie[period_select_pie])
    figP = fp.create_pie_fat(Age_group_select_pie)
    return figP


if __name__ == '__main__':
    app.run_server(debug=True)
