# Aydan Guliyeva
# Bar plot showing how calcium intake varies across different ages and gender in different years across the UK using Plotly Express

# Importing required packages
from pathlib import Path
import numpy as np
import math
import os.path
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import csv
import openpyxl

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px


if __name__ == "__main__":

    # Importing the dataset
    calcium_intake = pd.read_excel(r'/Users/aydanguliyeva/PycharmProjects/coursework-1-groups-group-6-comp0034/data/Dataset.xlsx', engine='openpyxl', sheet_name='Calcium Intake', skiprows= range(0,5))
    print(calcium_intake)

    # Defining the dataframe from the dataset
    data = {'Years':['2008/09 - 2009/10', '2008/09 - 2009/10', '2008/09 - 2009/10', '2008/09 - 2009/10', '2008/09 - 2009/10', '2008/09 - 2009/10',
                     '2008/09 - 2009/10', '2008/09 - 2009/10', '2008/09 - 2009/10', '2008/09 - 2009/10',
                     '2010/11 - 2011/12', '2010/11 - 2011/12', '2010/11 - 2011/12', '2010/11 - 2011/12', '2010/11 - 2011/12', '2010/11 - 2011/12',
                     '2010/11 - 2011/12', '2010/11 - 2011/12', '2010/11 - 2011/12', '2010/11 - 2011/12',
                     '2012/13 - 2013/14', '2012/13 - 2013/14', '2012/13 - 2013/14', '2012/13 - 2013/14', '2012/13 - 2013/14', '2012/13 - 2013/14',
                     '2012/13 - 2013/14', '2012/13 - 2013/14', '2012/13 - 2013/14', '2012/13 - 2013/14',
                     '2014/15 - 2015/16', '2014/15 - 2015/16', '2014/15 - 2015/16', '2014/15 - 2015/16', '2014/15 - 2015/16', '2014/15 - 2015/16',
                     '2014/15 - 2015/16', '2014/15 - 2015/16', '2014/15 - 2015/16', '2014/15 - 2015/16'],
            'Calcium Intake':[839, 767, 859, 692, 909, 741,
                              1015, 817, 833, 803,
                              808, 803, 919, 648, 866, 715,
                              914, 790, 891, 760,
                              811, 749, 889, 706, 912, 743,
                              864, 789, 764, 715,
                              774, 703, 854, 664, 897, 746,
                              887, 764, 885, 693],
            'Gender':['Male', 'Female', 'Male', 'Female', 'Male', 'Female',
                      'Male', 'Female', 'Male', 'Female',
                      'Male', 'Female', 'Male', 'Female', 'Male', 'Female',
                      'Male', 'Female', 'Male', 'Female',
                      'Male', 'Female', 'Male', 'Female', 'Male', 'Female',
                      'Male', 'Female', 'Male', 'Female',
                      'Male', 'Female', 'Male', 'Female', 'Male', 'Female',
                      'Male', 'Female', 'Male', 'Female'],
            'Age':['4-10 years', '4-10 years', '11-18 years', '11-18 years', '19-64 years', '19-64 years',
                   '65-74 years', '65-74 years', '75+ years', '75+ years',
                   '4-10 years', '4-10 years', '11-18 years', '11-18 years', '19-64 years', '19-64 years',
                   '65-74 years', '65-74 years', '75+ years', '75+ years',
                   '4-10 years', '4-10 years', '11-18 years', '11-18 years', '19-64 years', '19-64 years',
                   '65-74 years', '65-74 years', '75+ years', '75+ years',
                   '4-10 years', '4-10 years', '11-18 years', '11-18 years', '19-64 years', '19-64 years',
                   '65-74 years', '65-74 years', '75+ years', '75+ years']
            }
    df = pd.DataFrame(data, columns = ['Years','Calcium Intake','Gender','Age'])


    fig = px.bar(df, x="Years", y="Calcium Intake", color="Age", barmode="group", facet_col="Gender",
                 category_orders={"Years": ["2008/09 - 2009/10", "2010/11 - 2011/12", "2012/13 - 2013/14", "2014/15 - 2015/16"],
                                  "Gender": ["Male", "Female"],
                                  "Age": ["4-10 years", "11-18 years","19-64 years","65-75 years","75+ years"]},
                 labels={
                     "Calcium Intake": "Calcium Intake (mg/day)"
                 },
                 title="Calcium Intake across different ages and gender in the UK")

    fig.show()
    fig.write_html("/Users/aydanguliyeva/PycharmProjects/coursework-1-groups-group-6-comp0034/static/charts/Calcium_Charts.html")