# Module: COMP0034 Application Programming for Data Science
# Author: Ho Yan Or
# Description: Interactive bar chart showing the average free sugar intake for each gender and age group in
#              a selected time period

# Import relevant packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.widgets import Button
import openpyxl

if __name__ == "__main__":
    # Read xlsx file with the dataset and create a pandas dataframe with the selected rows
    excel_path = 'C:/Users/admin/PycharmProjects/coursework-1-groups-group-6-comp0034/data/Dataset.xlsx'
    df = pd.read_excel(excel_path, engine='openpyxl', sheet_name='Free Sugar Intake', skiprows=8, nrows=109)

    # Year list
    years = ['2008 - 2010', '2010 - 2012', '2012 - 2014', '2014 - 2016']

    # extract general sugar intake data into a separate dataframe
    sugar_intake_g = df.iloc[18::18, :]
    sugar_intake_g = sugar_intake_g.drop(df.index[[72]])
    sugar_intake_g = sugar_intake_g.reset_index(drop=True)
    sugar_intake_g['Children 1.5-3 years'] = ['4 to 10', '11 to 18', '19 to 64', '65 to 74', '75+']
    sugar_intake_g.columns = ['Age', '2008 - 2010', '2010 - 2012', '2012 - 2014', '2014 - 2016']

    # extract male sugar intake into a separate dataframe
    sugar_intake_m = df.iloc[6::18, :]
    sugar_intake_m = sugar_intake_m.drop(df.index[[60]])
    sugar_intake_m = sugar_intake_m.reset_index(drop=True)
    sugar_intake_m['Children 1.5-3 years'] = ['4 to 10', '11 to 18', '19 to 64', '65 to 74', '75+']
    sugar_intake_m.columns = ['Age', '2008 - 2010', '2010 - 2012', '2012 - 2014', '2014 - 2016']

    # extract female sugar intake into a separate dataframe
    sugar_intake_f = df.iloc[12::18, :]
    sugar_intake_f = sugar_intake_f.drop(df.index[[66]])
    sugar_intake_f = sugar_intake_f.reset_index(drop=True)
    sugar_intake_f['Children 1.5-3 years'] = ['4 to 10', '11 to 18', '19 to 64', '65 to 74', '75+']
    sugar_intake_f.columns = ['Age', '2008 - 2010', '2010 - 2012', '2012 - 2014', '2014 - 2016']

    # bar chart parameters
    pos = list(range(len(sugar_intake_f['Age'])))
    width = 0.23

    # create figure and axis at a selected size
    fig, ax = plt.subplots(figsize=(9, 6))


    # Function to create a bar chart for a selected time period
    def barchart(year):
        # general sugar intake bar
        ax.bar(pos, sugar_intake_g[year], width, color='#770737')
        # Male sugar intake bar
        ax.bar([p + width * 2 for p in pos], sugar_intake_m[year], width, color='#3CA2C8')
        # Female sugar intake bar
        ax.bar([p + width for p in pos], sugar_intake_f[year], width, color='#E37383')
        ax.set_title('UK average sugar intake per day')
        ax.set_xticks([p + 1 * width for p in pos])
        ax.set_yticks(np.arange(0, 100, step=10))
        ax.set_xticklabels(sugar_intake_g['Age'])
        ax.set_ylabel('Sugar Intake [g/day]')
        ax.legend(['All', 'Female', 'Male'], loc='upper left')
        return fig, ax


    # Function for the '2008-10' button to show the bar chart that time period
    def b1(val):
        global button_1
        ax.cla()
        barchart(years[0])
        button_1.label.set_color('blue')
        button_2.label.set_color('black')
        button_3.label.set_color('black')
        button_4.label.set_color('black')


    # Function for the '2010-12' button to show the bar chart that time period
    def b2(val):
        global button_2
        ax.cla()
        barchart(years[1])
        button_1.label.set_color('black')
        button_2.label.set_color('blue')
        button_3.label.set_color('black')
        button_4.label.set_color('black')


    # Function for the '2012-14' button to show the bar chart that time period
    def b3(val):
        global button_3
        ax.cla()
        barchart(years[2])
        button_1.label.set_color('black')
        button_2.label.set_color('black')
        button_3.label.set_color('blue')
        button_4.label.set_color('black')


    # Function for the '2014-16' button to show the bar chart that time period
    def b4(val):
        global button_4
        ax.cla()
        barchart(years[3])
        button_1.label.set_color('black')
        button_2.label.set_color('black')
        button_3.label.set_color('black')
        button_4.label.set_color('blue')


    # Grid Button
    def grid(val):
        ax.grid()
        fig.canvas.draw()
        return val


    # Plot the initial bar chart
    barchart(years[0])
    plt.legend(['All', 'Female', 'Male'], loc='upper left')
    plt.subplots_adjust(bottom=0.19)
    plt.figtext(0.10, 0.06, "Select Year: ", fontsize=12, fontname='Verdana')

    # Create button for 2008-10
    button_1 = Button(plt.axes([0.25, 0.04, 0.10, 0.06]), years[0], color='white', hovercolor='grey')
    button_1.on_clicked(b1)
    button_1.label.set_color('blue')

    # Create button for 2010-12
    button_2 = Button(plt.axes([0.40, 0.04, 0.10, 0.06]), years[1], color='white', hovercolor='grey')
    button_2.on_clicked(b2)

    # Create button for 2012-14
    button_3 = Button(plt.axes([0.55, 0.04, 0.10, 0.06]), years[2], color='white', hovercolor='grey')
    button_3.on_clicked(b3)

    # Create button for 2014-16
    button_4 = Button(plt.axes([0.70, 0.04, 0.10, 0.06]), years[3], color='white', hovercolor='grey')
    button_4.on_clicked(b4)

    # Create button to turn on grid
    grid_button = Button(plt.axes([0.85, 0.10, 0.05, 0.06]), 'Grid', color='yellow', hovercolor='grey')
    grid_button.on_clicked(grid)

    # Show plot
    plt.show()
