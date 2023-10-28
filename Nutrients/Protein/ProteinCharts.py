# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 03/03/2021
# Name: ProteinPieChart
# Author: Rayan Souissi
# Description: Program to generate the Plotly Charts to be outputed in the Dash App using the program Protein_Dash_Pie

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


class ProteinCharts:
    """ Creates the protein charts to be used in the dashboard"""

    def __init__(self, data):
        self.data = data

    def create_pie(self):

        ####PLOTING
        fig0 = go.Figure()

        '''Traces for the 2008-2012 Protein Intake Contribution, for the 6 age-groups'''
        fig0.add_trace(go.Pie(name = "0 - 0", visible = False, values= self.data.protein_contrib_2008.loc[:,'1.5-3'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "0 - 1", visible = False, values=self.data.protein_contrib_2008.loc[:,'4-10'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "0 - 2", visible = False, values=self.data.protein_contrib_2008.loc[:,'11-18'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "0 - 3", visible = False, values=self.data.protein_contrib_2008.loc[:,'19-64'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "0 - 4", visible = False, values=self.data.protein_contrib_2008.loc[:,'65-74'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "0 - 5", visible = False, values=self.data.protein_contrib_2008.loc[:,'75+'], labels = self.data.food_groups))

        '''Traces for the 2010-2012 Protein Intake Contribution, for the 6 age-groups'''
        fig0.add_trace(go.Pie(name = "1 - 0", visible = False, values=self.data.protein_contrib_2010.loc[:,'1.5-3'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "1 - 1", visible = False, values=self.data.protein_contrib_2010.loc[:,'4-10'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "1 - 2", visible = False, values=self.data.protein_contrib_2010.loc[:,'11-18'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "1 - 3", visible = False, values=self.data.protein_contrib_2010.loc[:,'19-64'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "1 - 4", visible = False, values=self.data.protein_contrib_2010.loc[:,'65-74'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "1 - 5", visible = False, values=self.data.protein_contrib_2010.loc[:,'75+'], labels = self.data.food_groups))

        '''Traces for the 2012-2014 Protein Intake Contribution, for the 6 age-groups'''
        fig0.add_trace(go.Pie(name = "2 - 0", visible = False, values=self.data.protein_contrib_2012.loc[:,'1.5-3'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "2 - 1", visible = False, values=self.data.protein_contrib_2012.loc[:,'4-10'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "2 - 2", visible = False, values=self.data.protein_contrib_2012.loc[:,'11-18'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "2 - 3", visible = False, values=self.data.protein_contrib_2012.loc[:,'19-64'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "2 - 4", visible = False, values=self.data.protein_contrib_2012.loc[:,'65-74'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "2 - 5", visible = False, values=self.data.protein_contrib_2012.loc[:,'75+'], labels = self.data.food_groups))

        '''Traces for the 2014-2016 Protein Intake Contribution, for the 6 age-groups'''
        fig0.add_trace(go.Pie(name = "3 - 0", visible = False, values=self.data.protein_contrib_2014.loc[:,'1.5-3'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "3 - 1", visible = False, values=self.data.protein_contrib_2014.loc[:,'4-10'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "3 - 2", visible = False, values=self.data.protein_contrib_2014.loc[:,'11-18'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "3 - 3", visible = False, values=self.data.protein_contrib_2014.loc[:,'19-64'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "3 - 4", visible = False, values=self.data.protein_contrib_2014.loc[:,'65-74'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "3 - 5", visible = False, values=self.data.protein_contrib_2014.loc[:,'75+'], labels = self.data.food_groups))

        '''Traces for the 2008-2016 Protein Intake Contribution, for the 6 age-groups'''
        fig0.add_trace(go.Pie(name = "4 - 0", visible = True, values=self.data.protein_contrib_mean.loc[:,'1.5-3'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "4 - 1", visible = False, values=self.data.protein_contrib_mean.loc[:,'4-10'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "4 - 2", visible = False, values=self.data.protein_contrib_mean.loc[:,'11-18'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "4 - 3", visible = False, values=self.data.protein_contrib_mean.loc[:,'19-64'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "4 - 4", visible = False, values=self.data.protein_contrib_mean.loc[:,'65-74'], labels = self.data.food_groups))
        fig0.add_trace(go.Pie(name = "4 - 5", visible = False, values=self.data.protein_contrib_mean.loc[:,'75+'], labels = self.data.food_groups))

        #set preliminary title
        fig0.update_layout(title_text = "Percentage Contribution of different food groups to Protein Intake in the UK between 2008 and 2016",
                           title_x = 0.5, font_size = 15, template = "simple_white",)

        return fig0

    def create_bar_2016(self):
        '''Stacked bar-char for the 2008-2016 Protein Intake Contribution, according to age group'''
        fig1 = go.Figure(data=[
            go.Bar(name=self.data.food_groups[0], x=self.data.ages, y=self.data.protein_contrib_mean.iloc[0]),
            go.Bar(name=self.data.food_groups[1], x=self.data.ages, y=self.data.protein_contrib_mean.iloc[1]),
            go.Bar(name=self.data.food_groups[2], x=self.data.ages, y=self.data.protein_contrib_mean.iloc[2]),
            go.Bar(name=self.data.food_groups[3], x=self.data.ages, y=self.data.protein_contrib_mean.iloc[3]),
            go.Bar(name=self.data.food_groups[4], x=self.data.ages, y=self.data.protein_contrib_mean.iloc[4]),
            go.Bar(name=self.data.food_groups[5], x=self.data.ages, y=self.data.protein_contrib_mean.iloc[5]),
            go.Bar(name=self.data.food_groups[6], x=self.data.ages, y=self.data.protein_contrib_mean.iloc[6]),
            go.Bar(name=self.data.food_groups[7], x=self.data.ages, y=self.data.protein_contrib_mean.iloc[7]),
            go.Bar(name=self.data.food_groups[8], x=self.data.ages, y=self.data.protein_contrib_mean.iloc[8]),
            go.Bar(name=self.data.food_groups[9], x=self.data.ages, y=self.data.protein_contrib_mean.iloc[9]),
        ])
        # Change the bar mode
        fig1.update_layout(barmode='stack', xaxis_title = "Age Class (years)", yaxis_title = "Contribution to Protein (%)",
                           title_text = "Percentage Contribution to Protein Intake in the UK between 2008 and 2016",
                           title_x = 0.5, font_size = 15, template = "simple_white",)

        return fig1


    def create_bar_2008(self):
        '''Stacked bar-char for the 2008-2010 Protein Intake Contribution, according to age group'''
        fig2 = go.Figure(data=[
            go.Bar(name=self.data.food_groups[0], x=self.data.ages, y=self.data.protein_contrib_2008.iloc[0]),  #"Cereals and cereal products"
            go.Bar(name=self.data.food_groups[1], x=self.data.ages, y=self.data.protein_contrib_2008.iloc[1]),  #"Milk and milk products"
            go.Bar(name=self.data.food_groups[2], x=self.data.ages, y=self.data.protein_contrib_2008.iloc[2]),  #"Cheese"
            go.Bar(name=self.data.food_groups[3], x=self.data.ages, y=self.data.protein_contrib_2008.iloc[3]),  #"Meat and meat products"
            go.Bar(name=self.data.food_groups[4], x=self.data.ages, y=self.data.protein_contrib_2008.iloc[4]),  #"Fish and fish dishes"
            go.Bar(name=self.data.food_groups[5], x=self.data.ages, y=self.data.protein_contrib_2008.iloc[5]),  #"Vegetables and potatoes"
            go.Bar(name=self.data.food_groups[6], x=self.data.ages, y=self.data.protein_contrib_2008.iloc[6]),  #"Fruit"
            go.Bar(name=self.data.food_groups[7], x=self.data.ages, y=self.data.protein_contrib_2008.iloc[7]),  #"Sugar, preserves and confectionery "
            go.Bar(name=self.data.food_groups[8], x=self.data.ages, y=self.data.protein_contrib_2008.iloc[8]),  #"Miscellaneous (Soups and Sauces)"
            go.Bar(name=self.data.food_groups[9], x=self.data.ages, y=self.data.protein_contrib_2008.iloc[9]),  #"Other (Savour snacks, Nuts and seeds, and beverages)"
        ])

        # Change the bar mode and update title
        fig2.update_layout(barmode='stack', xaxis_title = "Age Class (years)", yaxis_title = "Contribution to Protein (%)",
                           title_text = "Percentage Contribution to Protein Intake in the UK between 2008 and 2010",
                           title_x = 0.5, font_size = 15, template = "simple_white",)

        return fig2


    def create_bar_2010(self):
        '''Stacked bar-char for the 2010-2012 Protein Intake Contribution, according to age group'''
        fig3 = go.Figure(data=[
            go.Bar(name=self.data.food_groups[0], x=self.data.ages, y=self.data.protein_contrib_2010.iloc[0]),
            go.Bar(name=self.data.food_groups[1], x=self.data.ages, y=self.data.protein_contrib_2010.iloc[1]),
            go.Bar(name=self.data.food_groups[2], x=self.data.ages, y=self.data.protein_contrib_2010.iloc[2]),
            go.Bar(name=self.data.food_groups[3], x=self.data.ages, y=self.data.protein_contrib_2010.iloc[3]),
            go.Bar(name=self.data.food_groups[4], x=self.data.ages, y=self.data.protein_contrib_2010.iloc[4]),
            go.Bar(name=self.data.food_groups[5], x=self.data.ages, y=self.data.protein_contrib_2010.iloc[5]),
            go.Bar(name=self.data.food_groups[6], x=self.data.ages, y=self.data.protein_contrib_2010.iloc[6]),
            go.Bar(name=self.data.food_groups[7], x=self.data.ages, y=self.data.protein_contrib_2010.iloc[7]),
            go.Bar(name=self.data.food_groups[8], x=self.data.ages, y=self.data.protein_contrib_2010.iloc[8]),
            go.Bar(name=self.data.food_groups[9], x=self.data.ages, y=self.data.protein_contrib_2010.iloc[9]),
        ])

        # Change the bar mode and update title
        fig3.update_layout(barmode='stack', xaxis_title = "Age Class (years)", yaxis_title = "Contribution to Protein (%)",
                           title_text = "Percentage Contribution to Protein Intake in the UK between 2010 and 2012",
                           title_x = 0.5, font_size = 15, template = "simple_white",)

        return fig3


    def create_bar_2012(self):
        '''Stacked bar-char for the 2012-2014 Protein Intake Contribution, according to age group'''
        fig4 = go.Figure(data=[
            go.Bar(name=self.data.food_groups[0], x=self.data.ages, y=self.data.protein_contrib_2012.iloc[0]),
            go.Bar(name=self.data.food_groups[1], x=self.data.ages, y=self.data.protein_contrib_2012.iloc[1]),
            go.Bar(name=self.data.food_groups[2], x=self.data.ages, y=self.data.protein_contrib_2012.iloc[2]),
            go.Bar(name=self.data.food_groups[3], x=self.data.ages, y=self.data.protein_contrib_2012.iloc[3]),
            go.Bar(name=self.data.food_groups[4], x=self.data.ages, y=self.data.protein_contrib_2012.iloc[4]),
            go.Bar(name=self.data.food_groups[5], x=self.data.ages, y=self.data.protein_contrib_2012.iloc[5]),
            go.Bar(name=self.data.food_groups[6], x=self.data.ages, y=self.data.protein_contrib_2012.iloc[6]),
            go.Bar(name=self.data.food_groups[7], x=self.data.ages, y=self.data.protein_contrib_2012.iloc[7]),
            go.Bar(name=self.data.food_groups[8], x=self.data.ages, y=self.data.protein_contrib_2012.iloc[8]),
            go.Bar(name=self.data.food_groups[9], x=self.data.ages, y=self.data.protein_contrib_2012.iloc[9]),
        ])

        # Change the bar mode and update title
        fig4.update_layout(barmode='stack', xaxis_title = "Age Class (years)", yaxis_title = "Contribution to Protein (%)",
                           title_text = "Percentage Contribution to Protein Intake in the UK between 2012 and 2014", title_x = 0.5, font_size = 15, template = "simple_white",)

        return fig4


    def create_bar_2014(self):
        '''Stacked bar-char for the 2014-2016 Protein Intake Contribution, according to age group'''
        fig5 = go.Figure(data=[
            go.Bar(name=self.data.food_groups[0], x=self.data.ages, y=self.data.protein_contrib_2014.iloc[0]),
            go.Bar(name=self.data.food_groups[1], x=self.data.ages, y=self.data.protein_contrib_2014.iloc[1]),
            go.Bar(name=self.data.food_groups[2], x=self.data.ages, y=self.data.protein_contrib_2014.iloc[2]),
            go.Bar(name=self.data.food_groups[3], x=self.data.ages, y=self.data.protein_contrib_2014.iloc[3]),
            go.Bar(name=self.data.food_groups[4], x=self.data.ages, y=self.data.protein_contrib_2014.iloc[4]),
            go.Bar(name=self.data.food_groups[5], x=self.data.ages, y=self.data.protein_contrib_2014.iloc[5]),
            go.Bar(name=self.data.food_groups[6], x=self.data.ages, y=self.data.protein_contrib_2014.iloc[6]),
            go.Bar(name=self.data.food_groups[7], x=self.data.ages, y=self.data.protein_contrib_2014.iloc[7]),
            go.Bar(name=self.data.food_groups[8], x=self.data.ages, y=self.data.protein_contrib_2014.iloc[8]),
            go.Bar(name=self.data.food_groups[9], x=self.data.ages, y=self.data.protein_contrib_2014.iloc[9]),
        ])

        # Change the bar mode and update title
        fig5.update_layout(barmode='stack', xaxis_title = "Age Class (years)", yaxis_title = "Contribution to Protein (%)",
                           title_text = "Percentage Contribution to Protein Intake in the UK between 2014 and 2016",
                           title_x = 0.5, font_size = 15, template = "simple_white",)

        return fig5