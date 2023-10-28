# Module: COMP0034 Application Programming for Data Science
# Author: Ho Yan Or
# Description: Pie chart showing contribution of different food groups to the average free sugar intake for
#              a selected age group and year of study

# Import relevant packages
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import openpyxl

if __name__ == "__main__":
    # Read xlsx file with the dataset and create a pandas dataframe with the selected rows
    excel_path = 'C:/Users/admin/PycharmProjects/coursework-1-groups-group-6-comp0034/data/Dataset.xlsx'
    df = pd.read_excel(excel_path, engine='openpyxl', sheet_name='Free Sugar Contribution', skiprows=5, nrows=55)

    # extract data for the years - 2008-10 (year 1), 2010-12 (y2), 2012-14 (y3) and 2014-16 (y4)
    y1 = df.iloc[:, 1:7]
    y2 = df.iloc[:, 7:13]
    y3 = df.iloc[:, 13:19]
    y4 = df.iloc[:, 19:25]


    # Function to extract data used for creating a pie chart for a selected year range
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


    # Save the data for each time period into a variable
    year_1 = pie_data(y1)
    year_2 = pie_data(y2)
    year_3 = pie_data(y3)
    year_4 = pie_data(y4)
    category = year_1['Food Categories']

    # Create initial pie chart figure
    fig_sugar = px.pie(year_1, values=year_1['19-64'], names=category,
                       title='Free Sugar Contribution for 19-64 years old [2008-10]',
                       hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)

    # Define the CSS style sheets to be used
    external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"]

    #
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # App layout
    app.layout = html.Div([
        dbc.Row(  # Row 1: App title
            dbc.Col(html.H3("UK Nutrition Data Visualisation"),
                    style={'width': '75%', 'margin': 25, 'textAlign': 'center'}
                    ),
        ),

        dbc.Row(  # Row 2: Subtitle
            dbc.Col(html.H5("Free Sugar Intake"),
                    style={'margin': 5}
                    ),
        ),
        dbc.Row(  # Row 3: Description
            dbc.Col(html.Div(
                "Different food groups contribute differently to the average sugar intake of individuals in the UK. "
                "This is shown in the pie chart below. Through selecting the options in the dropdown menus, you can "
                "visualise the contribution of food groups to free sugar intake for a selected age group and time "
                "period."),
                style={'margin': 5}
            ),
        ),

        dbc.Row(  # Row 4: Heading
            dbc.Col(html.H6("Select Data: "),
                    width={'offset': 2},
                    )
        ),
        dbc.Row(  # Row 5: dropdowns for time period and age group
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
        dbc.Row(  # Row 6: display pie chart
            [
                dbc.Col(dcc.Graph(id='pie_chart', figure=fig_sugar),
                        width=8, lg={'size': 9, "offset": 1}
                        ),
            ]
        )
    ])


    # Callback to update chart for a selected time period and age group
    @app.callback(Output('pie_chart', 'figure'),
                  [Input('select_year', 'value'),
                   Input('select_age', 'value')])
    # Method to update the pie chart to the selected year range and age group
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


    # run the web flask_app server
    app.run_server(debug=True)
