# Author: Bailey Roberts

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


import matplotlib.pyplot as plt


if __name__ == "__main__":

 # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html, read the excel document, and remove header and some unneeded information from the final rows.
    magnesium_intake = pd.read_excel('data/Dataset.xlsx', engine = 'openpyxl', sheet_name='Magnesium Intake', skiprows= range(0,5), skipfooter=21)

 # Drop everything that has no values, this means that only the rows called 'mean, median ...' remain.
    magnesium_intake = magnesium_intake.dropna()

# I was stuggling to work with the column containing 'mean, median ...' so it will be removed here, and will be added back in as an index.
# multiindex is used, it should be easier to work with.
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.MultiIndex.html
    magnesium_intake = magnesium_intake.drop(columns='Unnamed: 0', axis=1)
    test = pd.MultiIndex.from_product([['Children  1.5-3', 'Boys 4-10', 'Girls 4-10', 'Children 4-10','Boys 1-18','Girls 10-18', 'Children 10-18','Men 19-64','Women 19-16','Adults 19-64','Men 65 and over', 'Women 65 and over','Adults 64 and over','Men 65-74','Women 65-74','Adults 65-74','Men 75 and over','Women 75 and over','Adults 75 and over'],['Mean','Median','SD','2.5th percentile','97.5th percentile','Mean as %RNI','Median as %RNI','% bellow LRNI']])
    magnesium_intake = magnesium_intake.set_index(test)

# the new dataframe with the multiindex is copied 3 times for each gender.
    magnesium_intake_general = magnesium_intake
    magnesium_intake_male = magnesium_intake
    magnesium_intake_female = magnesium_intake

# Here for each gender, all other gender information is dropped, the 65+ data is also dropped as it clashes with 65 - 75 and 75+ so will cause confusion in some plots.
    for i in ['Boys 4-10', 'Girls 4-10', 'Boys 1-18','Girls 10-18','Men 19-64','Women 19-16','Men 65 and over', 'Women 65 and over','Adults 64 and over','Men 65-74','Women 65-74','Men 75 and over','Women 75 and over']:
        magnesium_intake_general = magnesium_intake_general.drop(index=i, level=0)

    for i in ['Children 4-10', 'Girls 4-10', 'Children 10-18', 'Girls 10-18', 'Adults 19-64', 'Women 19-16', 'Men 65 and over','Women 65 and over', 'Adults 64 and over', 'Adults 65-74', 'Women 65-74', 'Adults 75 and over', 'Women 75 and over']:
        magnesium_intake_male = magnesium_intake_male.drop(index=i, level=0)

    for i in ['Children 4-10', 'Boys 4-10', 'Children 10-18', 'Boys 1-18', 'Adults 19-64', 'Men 19-64', 'Men 65 and over','Women 65 and over', 'Adults 64 and over', 'Adults 65-74', 'Men 65-74', 'Adults 75 and over', 'Men 75 and over']:
        magnesium_intake_female = magnesium_intake_female.drop(index=i, level=0)

# now that only the correct gendered information remains, the mean value is taken for each age group in each year.
    for i in ['Median','SD','2.5th percentile','97.5th percentile','Mean as %RNI','Median as %RNI','% bellow LRNI']:
        magnesium_intake_general = magnesium_intake_general.drop(index=i, level= 1)

    for i in ['Median','SD','2.5th percentile','97.5th percentile','Mean as %RNI','Median as %RNI','% bellow LRNI']:
        magnesium_intake_male = magnesium_intake_male.drop(index=i, level= 1)

    for i in ['Median','SD','2.5th percentile','97.5th percentile','Mean as %RNI','Median as %RNI','% bellow LRNI']:
        magnesium_intake_female = magnesium_intake_female.drop(index=i, level= 1)

# The data from the first year of the study is taken from each gendered dataframe, and dded to a new data frame with a new index, general, male female
    magnesium_intake_general_1 = magnesium_intake_general.loc[:, '   (2008/09 - 2009/10)'].values

    magnesium_intake_male_1 = magnesium_intake_male.loc[:, '   (2008/09 - 2009/10)'].values

    magnesium_intake_female_1 = magnesium_intake_female.loc[:, '   (2008/09 - 2009/10)'].values

    chartdata = pd.DataFrame(data={'general': magnesium_intake_general_1, 'male': magnesium_intake_male_1, 'female': magnesium_intake_female_1})

 # This is repeated for the other years of the study, producing 4 dataframes, each contaning, male, female and general values for each age group. The values are the mean values from the orignal dataset.
    magnesium_intake_general_2 = magnesium_intake_general.loc[:, '    (2010/11 - 2011/12)'].values

    magnesium_intake_male_2 = magnesium_intake_male.loc[:, '    (2010/11 - 2011/12)'].values

    magnesium_intake_female_2 = magnesium_intake_female.loc[:, '    (2010/11 - 2011/12)'].values

    chartdata_2 = pd.DataFrame(data={'general': magnesium_intake_general_2, 'male': magnesium_intake_male_2, 'female': magnesium_intake_female_2})

    magnesium_intake_general_3 = magnesium_intake_general.loc[:, '    (2012/13 - 2013/14)'].values

    magnesium_intake_male_3 = magnesium_intake_male.loc[:, '    (2012/13 - 2013/14)'].values

    magnesium_intake_female_3 = magnesium_intake_female.loc[:, '    (2012/13 - 2013/14)'].values

    chartdata_3 = pd.DataFrame(data={'general': magnesium_intake_general_3, 'male': magnesium_intake_male_3, 'female': magnesium_intake_female_3})

    magnesium_intake_general_4 = magnesium_intake_general.loc[:, '    (2014/15-2015/16)'].values

    magnesium_intake_male_4 = magnesium_intake_male.loc[:, '    (2014/15-2015/16)'].values

    magnesium_intake_female_4 = magnesium_intake_female.loc[:, '    (2014/15-2015/16)'].values

    chartdata_4 = pd.DataFrame(data={'general': magnesium_intake_general_3, 'male': magnesium_intake_male_3, 'female': magnesium_intake_female_3})

 # A figure is created with 4 subplots https://matplotlib.org/stable/gallery/recipes/create_subplots.html
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(18,12), sharex= True, sharey= True)
    fig.suptitle('Comparison of magnesium intake for each age group and between genders.')

# each subplot is specified as chartdata, which contains one year data for each gender and age group.
    chartdata.plot.bar(ax=axes[0,0])
    axes[0,0].set_xlabel('Age Group (years)')
    axes[0,0].set_ylabel('Magnesium  Intake (mg/day)')
    axes[0,0].set_title('Data from the year (2008/09 - 2009/10)')

    chartdata_2.plot.bar(ax=axes[0,1])
    axes[0,1].set_xlabel('Age Group (years)')
    axes[0,1].set_ylabel('Magnesium  Intake (mg/day)')
    axes[0,1].set_title('Data from the year (2010/11 - 2011/12)')

    chartdata_3.plot.bar(ax=axes[1,0])
    axes[1,0].set_xlabel('Age Group (years)')
    axes[1,0].set_ylabel('Magnesium  Intake (mg/day)')
    axes[1,0].set_title('Data from the year (2012/13 - 2013/14)')

    chartdata_4.plot.bar(ax=axes[1,1])
    axes[1,1].set_xlabel('Age Group (years)')
    axes[1,1].set_ylabel('Magnesium  Intake (mg/day)')
    axes[1,1].set_title('Data from the year (2014/15 - 2015/16)')

#xticks changes the x axis values to show the correct age group values
    plt.xticks([0,1,2,3,4,5], ['1.5-3','4-10','10-18','19-64','65-74','75+'])
    plt.show()

# the  plot automatically shows each gender and produces the legend.












