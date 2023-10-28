# Created by Youssef ALAOUI MRANI
# Description:
# Used to create the charts used in the Fat intake category of the Dash flask_app.
import plotly.graph_objects as go
import plotly.express as px


class FatBarChart:
    """ Creates the recycling bar chart to be used in the dashboard
    TODO: format the chart, add titles etc
    """

    def __init__(self, data):
        self.data = data

    List_periods = ["1-2", "3-4", "5-6", "7-8"]

    def create_chart(self, period):
        if period not in self.List_periods:
            raise ValueError("The value should be in [1-2, 3-4, 5-6, 7-8]\n")
        data = self.data

        fig = go.Figure(data=[
            go.Bar(name=('Men'), x=data["Age groups"], y=data[("Men " + period)], marker=dict(color="lightsteelblue"),
                   ),
            go.Bar(name='Women', x=data["Age groups"], y=data[("Women " + period)], marker=dict(color="lightcoral"))])

        fig.update_layout(
            title=("Fat intake per gender - year " + period),
            xaxis=dict(
                showgrid=False,
                showline=True,
                linecolor='rgb(102, 102, 102)',
                tickfont_color='rgb(102, 102, 102)',
                showticklabels=True,
                ticks='outside',
                tickcolor='rgb(102, 102, 102)'
            ),

            margin=dict(l=140, r=40, b=50, t=80),
            legend=dict(
                font_size=10,
                yanchor='middle',
                xanchor='right',
            ),
            yaxis=dict(gridcolor="DarkGrey", range=[0, 86]),
            width=800,
            height=600,
            paper_bgcolor='white',
            plot_bgcolor='white',
            hovermode='closest',

        )
        fig.update_layout(title="Fat intake per gender",

                          xaxis_title="Age groups",
                          yaxis_title="Fat intake (g/day)", font_color="Black")

        return fig


class FatPopulationChart:
    def __init__(self, data):
        self.data = data

    List_periods = ["1-2", "3-4", "5-6", "7-8"]

    def create_chart(self, period):
        data = self.data
        fig = go.Figure(data=[
            go.Bar(orientation='h', name=('Men '), y=data["Age groups"], x=data[("Men " + period)],
                   marker=dict(color="lightsteelblue")),
            go.Bar(orientation='h', name='Women', y=data["Age groups"], x=- data["Women " + period],
                   marker=dict(color="lightcoral"))])
        fig.update_layout(title="Fat intake year " + period, barmode="overlay",
                          xaxis=dict(gridcolor="DarkGrey", range=[-90, 90],
                                     tickvals=[-80, -60, -40, -20, 0, 20, 40, 60, 80],
                                     ticktext=[80, 60, 40, 20, 0, 20, 40, 60, 80], showgrid=False,
                                     showline=True,
                                     linecolor='rgb(102, 102, 102)',
                                     tickfont_color='rgb(102, 102, 102)',
                                     showticklabels=True,
                                     ticks='outside',
                                     tickcolor='rgb(102, 102, 102)'),

                          margin=dict(l=140, r=40, b=50, t=80),
                          legend=dict(
                              font_size=10,
                              yanchor='bottom',
                              xanchor='right'),
                          yaxis=dict(gridcolor="DarkGrey"),
                          width=800,
                          height=600,
                          paper_bgcolor='white',
                          plot_bgcolor='white',
                          hovermode='closest',
                          ),

        return fig


class BarChartYears:
    def __init__(self, data):
        self.data = data

        self.year = ["2008-2010", "2010-2012", "2012-2014", "2014-2016"]

    def create_chart(self, Range):
        data = self.data

        M = [data["Men 1-2"][Range], data["Men 3-4"][Range], data["Men 5-6"][Range], data["Men 7-8"][Range]]
        F = [data["Women 1-2"][Range], data["Women 3-4"][Range], data["Women 5-6"][Range], data["Women 7-8"][Range]]
        fig = go.Figure(data=[
            go.Bar(name=('Men '), y=M, x=self.year, marker=dict(color="lightsteelblue")),
            go.Bar(name=('Women '), y=F, x=self.year, marker=dict(color="lightcoral"))])
        fig.update_layout(
            title=("Fat intake per year "),
            xaxis=dict(
                showgrid=False,
                showline=True,
                linecolor='rgb(102, 102, 102)',
                tickfont_color='rgb(102, 102, 102)',
                showticklabels=True,
                ticks='outside',
                tickcolor='rgb(102, 102, 102)'
            ),

            margin=dict(l=140, r=40, b=50, t=80),
            legend=dict(
                font_size=10,
                yanchor='middle',
                xanchor='right',
            ),
            yaxis=dict(gridcolor="DarkGrey", range=[0, 86]),
            width=800,
            height=600,
            paper_bgcolor='white',
            plot_bgcolor='white',
            hovermode='closest',

        )
        fig.update_layout(title="Fat intake per year",

                          xaxis_title="Age groups",
                          yaxis_title="Fat intake (g/day)", font_color="Black")

        return fig


class Pie_chart:
    def __init__(self, data):
        self.data = data
        self.list_of_ages = ["1.5-3", "4-10", "11-18", "19-64", "65-74", "75+"]

    def create_pie_fat(self, Age):
        data = self.data
        color_discrete_map = {'Thur': 'lightcyan',
                              'Fri': 'cyan',
                              'Sat': 'royalblue',
                              'Sun': 'darkblue'}

        fig = px.pie(data, values=self.list_of_ages[Age], names=data['Food Categories'],
                     title='Contribution to Fat intake for {} years olds'.format(self.list_of_ages[Age]),
                     color_discrete_sequence=px.colors.sequential.OrRd, width=1000, height=800)
        return fig
