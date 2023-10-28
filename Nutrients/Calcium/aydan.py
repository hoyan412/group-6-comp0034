# Aydan Guliyeva
# Bar plot showing how calcium intake varies across different ages and gender in the UK using Matplotlib

# Importing required packages
from pathlib import Path
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

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

if __name__ == "__main__":

    # Importing the dataset
    calcium_intake = pd.read_excel(r'/Users/aydanguliyeva/PycharmProjects/coursework-1-groups-group-6-comp0034/data/Dataset.xlsx', engine='openpyxl', sheet_name='Calcium Intake', skiprows= range(0,5))
    print(calcium_intake)

    n_groups = 5
    male = (808, 880, 896, 920, 843)
    female = (756, 676, 736, 790, 743)

    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, male, bar_width,
                     alpha=opacity,color='b',label='Male')

    rects2 = plt.bar(index + bar_width, female, bar_width,
                     alpha=opacity, color='m',label='Female')

    plt.xlabel('Age')
    plt.ylabel('Calcium Intake (mg/day)')
    plt.title('Age VS Calcium Intake in the UK')
    plt.xticks(index + bar_width, ('4-10', '11-18','19-64','65-74', '75+' ) )
    plt.legend()

    plt.tight_layout()
    plt.show()

    fig.savefig('calcium_intake_vs_age.png', transparent=True, bbox_inches='tight')
