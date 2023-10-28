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

import plotly.express as px


if __name__ == "__main__":


 # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_excel.html, read the excel document, and remove header and some unneeded information from the final rows.
    magnesium_intake = pd.read_excel('data/Dataset.xlsx', engine = 'openpyxl', sheet_name='Magnesium Intake', skiprows= range(0,5), skipfooter=21, header= None)

 # Drop everything that has no values, this means that only the rows called 'mean, median ...' remain.
    magnesium_intake = magnesium_intake.dropna()

# I was stuggling to work with the column containing 'mean, median ...' so it will be removed here, and will be added back in as an index.
# multiindex is used, it should be easier to work with.
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.MultiIndex.html
    magnesium_intake = magnesium_intake.drop(columns= 0, axis=1)
    test = pd.MultiIndex.from_product([['Children  1.5-3', 'Boys 4-10', 'Girls 4-10', 'Children 4-10','Boys 1-18','Girls 10-18', 'Children 10-18','Men 19-64','Women 19-16','Adults 19-64','Men 65 and over', 'Women 65 and over','Adults 64 and over','Men 65-74','Women 65-74','Adults 65-74','Men 75 and over','Women 75 and over','Adults 75 and over'],['Mean','Median','SD','2.5th percentile','97.5th percentile','Mean as %RNI','Median as %RNI','% bellow LRNI']])

    magnesium_intake = magnesium_intake.set_index(test)
    magnesium_intake_male = magnesium_intake
    magnesium_intake_female = magnesium_intake

 # Here for each gender, all other gender information is dropped, the 65+ data is also dropped as it clashes with 65 - 75 and 75+ so will cause confusion in some plots.
    for i in ['Boys 4-10', 'Girls 4-10','Boys 1-18','Girls 10-18','Men 19-64','Women 19-16','Men 65 and over', 'Women 65 and over','Adults 64 and over','Men 65-74','Women 65-74','Men 75 and over','Women 75 and over']:
        magnesium_intake = magnesium_intake.drop(index=i, level= 0)

    for i in ['Children 4-10', 'Girls 4-10','Children 10-18','Girls 10-18','Adults 19-64','Women 19-16','Men 65 and over', 'Women 65 and over','Adults 64 and over','Adults 65-74','Women 65-74','Adults 75 and over','Women 75 and over']:
        magnesium_intake_male = magnesium_intake_male.drop(index=i, level= 0)

    for i in ['Boys 4-10', 'Children 4-10','Boys 1-18','Children 10-18','Men 19-64','Adults 19-64','Men 65 and over', 'Women 65 and over','Adults 64 and over','Men 65-74','Adults 65-74','Men 75 and over','Adults 75 and over']:
        magnesium_intake_female = magnesium_intake_female.drop(index=i, level= 0)

 # now that only the correct gendered information remains, the mean value is taken for each age group in each year.
    for i in ['Median','SD','2.5th percentile','97.5th percentile','Mean as %RNI','Median as %RNI','% bellow LRNI']:
        magnesium_intake = magnesium_intake.drop(index=i, level= 1)

    for i in ['Median','SD','2.5th percentile','97.5th percentile','Mean as %RNI','Median as %RNI','% bellow LRNI']:
        magnesium_intake_male = magnesium_intake_male.drop(index=i, level= 1)

    for i in ['Median','SD','2.5th percentile','97.5th percentile','Mean as %RNI','Median as %RNI','% bellow LRNI']:
        magnesium_intake_female = magnesium_intake_female.drop(index=i, level= 1)

# Here from the magnesium intake, ungendered dataframe each age group is extracted contaning all years and transposed so that rows become columns.
# Each transposed list is added to a new dataframe, an index is added so we can see the age range and gender.
    children_1 = magnesium_intake.loc['Children  1.5-3', 'Mean'].transpose().reset_index(drop=True)
    children_2 = magnesium_intake.loc['Children 4-10', 'Mean'].transpose().reset_index(drop=True)
    children_3 = magnesium_intake.loc['Children 10-18', 'Mean'].transpose().reset_index(drop=True)
    adults_1 = magnesium_intake.loc['Adults 19-64', 'Mean'].transpose().reset_index(drop=True)
    adults_2 = magnesium_intake.loc['Adults 65-74', 'Mean'].transpose().reset_index(drop=True)
    adults_3 = magnesium_intake.loc['Adults 75 and over', 'Mean'].transpose().reset_index(drop=True)
    wisker = pd.DataFrame([children_1, children_2, children_3, adults_1, adults_2, adults_3])
    wisker['age'] = ['1.5-3', '4-10', '10-18', '19-64', '65-74', '75 and over']
    wisker['gender'] = ['general','general','general','general','general','general']

# the process above is repeated for each gendered data frame. the final product is 3 dataframes, one for each gender which contains the means values for age group and each year of the study.
    children_male_1 = magnesium_intake_male.loc['Children  1.5-3', 'Mean'].transpose().reset_index(drop=True)
    children_male_2 = magnesium_intake_male.loc['Boys 4-10', 'Mean'].transpose().reset_index(drop=True)
    children_male_3 = magnesium_intake_male.loc['Boys 1-18', 'Mean'].transpose().reset_index(drop=True)
    adults_male_1 = magnesium_intake_male.loc['Men 19-64', 'Mean'].transpose().reset_index(drop=True)
    adults_male_2 = magnesium_intake_male.loc['Men 65-74', 'Mean'].transpose().reset_index(drop=True)
    adults_male_3 = magnesium_intake_male.loc['Men 75 and over', 'Mean'].transpose().reset_index(drop=True)
    wisker_male = pd.DataFrame([children_male_1, children_male_2, children_male_3, adults_male_1, adults_male_2, adults_male_3])
    wisker_male['age'] = ['1.5-3', '4-10', '10-18', '19-64', '65-74', '75 and over']
    wisker_male['gender'] = ['male', 'male', 'male' ,'male','male','male']

    children_female_1 = magnesium_intake_female.loc['Children  1.5-3', 'Mean'].transpose().reset_index(drop=True)
    children_female_2 = magnesium_intake_female.loc['Girls 4-10', 'Mean'].transpose().reset_index(drop=True)
    children_female_3 = magnesium_intake_female.loc['Girls 10-18', 'Mean'].transpose().reset_index(drop=True)
    adults_female_1 = magnesium_intake_female.loc['Women 19-16', 'Mean'].transpose().reset_index(drop=True)
    adults_female_2 = magnesium_intake_female.loc['Women 65-74', 'Mean'].transpose().reset_index(drop=True)
    adults_female_3 = magnesium_intake_female.loc['Women 75 and over', 'Mean'].transpose().reset_index(drop=True)
    wisker_female = pd.DataFrame([children_female_1, children_female_2, children_female_3, adults_female_1, adults_female_2, adults_female_3])
    wisker_female['age'] = ['1.5-3', '4-10', '10-18', '19-64', '65-74', '75 and over']
    wisker_female['gender'] = ['female', 'female', 'female', 'female', 'female', 'female']

# the 3 dataframes are appended, so that all the dataframes are joined together.
# The new dataframe contains the age range and gender columns, and mean values for all 4 years of the study
    wisker_final = wisker.append(wisker_male).append(wisker_female)

# The box plot is produced, specifing that the xaxis will be the age, which has been specified in all 3 dataframes above.
# the y axis is the mean values in table, where 0 - 3 represent the years of the study.
# colour='gender' splits the graph into genders, which again have been specified in all 3 dataframes above.
    fig = px.box(wisker_final, x='age', y=[0,1,2,3],color='gender',
                 labels={'age':'Age Group (years)',
                         'value':'Magnesium  Intake (mg/day)',
                         'gender':'Gender'}, title='Boxplot showing the distribution of magnesium intake between the years of the study, for each age group and gender')
    fig.show()
    fig.write_html('static/charts/Magnesium_Charts/magnesium.html')


















