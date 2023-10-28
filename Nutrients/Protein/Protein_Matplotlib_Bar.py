# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 03/03/2021
# Name: Protein_Matplotlib
# Author: Rayan Souissi
# Description: Program to generate a plot of the mean protein intake
#               between 2008 and 2016 for different age classes using Matplotlib


import numpy as np
import pandas as pd
import openpyxl

import matplotlib
import matplotlib.pyplot as plt

if __name__ == "__main__":


    ''' 1. Load the xlsx file into a pandas DataFrame and skip the first lines which contain introduction to the dataset'''

    xlsxfile = 'data/Dataset1.xlsx'
    protein_intake = pd.read_excel(xlsxfile, engine='openpyxl', sheet_name='Protein Intake',
                                   names = ["Age", "2008-2010", "2010-2012", "2012-2014", "2014-2016"], nrows = 114,  skiprows= range(0,7))
    #print(protein_intake)    # for debug

    '''2. Extracting the three types General (men and Women), Men and Women'''

    '''2.1 Extracting only general'''
    protein_intake_g = protein_intake
    for i in range(6,len(protein_intake_g.index),18):           #removing men and women
        protein_intake_g = protein_intake_g.drop(range(i,i+12))
    protein_intake_g = protein_intake_g.reset_index(level=0, drop=True)     #resetting index

    for i in range(0,len(protein_intake_g.index),6):        #keeping only mean (removing standard deviation, 1st quartil, etc)
        protein_intake_g = protein_intake_g.drop([i])
        protein_intake_g = protein_intake_g.drop(range(i+2,i+6))
    protein_intake_g = protein_intake_g.reset_index(level=0, drop=True)     #resetting index
    protein_intake_g['Age'] = [2, 7, 15, 42, 65, 70, 75]                #Setting label
    protein_intake_g = protein_intake_g.drop([0, 4])                            #Removing the 65+
    protein_intake_g = protein_intake_g.reset_index(level=0, drop=True)         #resetting index
    #print(protein_intake_g)    # for debug


    '''2.2 Extracting only male'''
    protein_intake_m = protein_intake
    for i in range(12,len(protein_intake_m.index),18):              #removing general and women
        protein_intake_m = protein_intake_m.drop(range(i,i+12))
    protein_intake_m = protein_intake_m.drop(range(0,6))
    protein_intake_m = protein_intake_m.reset_index(level=0, drop=True)     #resetting index

    for i in range(0,len(protein_intake_m.index),6):         #keeping only mean (removing standard deviation, 1st quartil, etc)
        protein_intake_m = protein_intake_m.drop([i])
        protein_intake_m = protein_intake_m.drop(range(i+2,i+6))
    protein_intake_m = protein_intake_m.reset_index(level=0, drop=True)     #resetting index
    protein_intake_m['Age'] = [7, 15, 42, 65, 70, 75]                   #Setting label
    protein_intake_m = protein_intake_m.drop([3])                               #Removing the 65+
    protein_intake_m = protein_intake_m.reset_index(level=0, drop=True)         #resetting index
    #print(protein_intake_m)    # for debug


    '''2.3 Extracting only women'''
    protein_intake_w = protein_intake
    for i in range(0,len(protein_intake_w.index)-18,18):            #deleting general and women
        protein_intake_w = protein_intake_w.drop(range(i,i+12))
    protein_intake_w = protein_intake_w.reset_index(level=0, drop=True)     #resetting index
    protein_intake_w = protein_intake_w.drop(range(36,42))

    for i in range(0,len(protein_intake_w.index),6):         #keeping only mean (removing standard deviation, 1st quartil, etc)
        protein_intake_w = protein_intake_w.drop([i])
        protein_intake_w = protein_intake_w.drop(range(i+2,i+6))
    protein_intake_w = protein_intake_w.reset_index(level=0, drop=True)     #resetting index
    protein_intake_w['Age'] = [7, 15, 42, 65, 70, 75]                   #Setting label
    protein_intake_w = protein_intake_w.drop([3])                               #Removing the 65+
    protein_intake_w = protein_intake_w.reset_index(level=0, drop=True)         #resetting index
    #print(protein_intake_w)    # for debug


    '''3. Generate the data frames for the mean over the four eyars periods'''

    #For General
    z = [protein_intake_g['2008-2010'], protein_intake_g['2010-2012'], protein_intake_g['2012-2014'], protein_intake_g['2014-2016']]
    mean_df = pd.DataFrame(np.mean(z, axis=0), columns = ["General"])

    #Adding Men
    z = [protein_intake_m['2008-2010'], protein_intake_m['2010-2012'], protein_intake_m['2012-2014'], protein_intake_m['2014-2016']]
    mean_df["Men"] = pd.DataFrame(np.mean(z, axis=0))

    #Adding Women
    z = [protein_intake_w['2008-2010'], protein_intake_w['2010-2012'], protein_intake_w['2012-2014'], protein_intake_w['2014-2016']]
    mean_df["Women"] = pd.DataFrame(np.mean(z, axis=0))


    '''4. Plotting'''

    labels = [4, 10, 11, 18, 19, 64, 65, 74, 75]        #the plot ticks labels

    x = np.arange(len(labels))  # the label locations

    x1 = np.array([0, 2, 4, 6, 8])  # the label locations for men
    x2 = np.array([1, 3, 5, 7, 9])  # the label locations for Women
    x3 = np.array([0.5, 2.5, 4.5, 6.5, 8.5])  # the label locations for Men and Women

    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()        #Create the plot
    rects1 = ax.bar(x1 + width/2, round(mean_df["Men"],1), width, label='Men')
    rects2 = ax.bar(x2 - width/2, round(mean_df["Women"],1), width, label='Women')
    rects3 = ax.bar(x3 , round(mean_df["General"],1), width-0.05, label='Men and Women')
    ax.set(title = 'Mean Protein Intake in the UK between 2008 and 2016',
           ylim=[40, 100], ylabel='Protein Intake (g/day)',xlabel='Age Class (years)',
           xticks = x, xticklabels = labels)
    ax.legend()


    '''5. Adjut plot layout and show plot'''
    def autolabel(rects, color, offset):
        for rect in rects:

            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(offset, 4),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        color = color)


    autolabel(rects1, "blue", 0)
    autolabel(rects3, "green", 5)
    autolabel(rects2, "orange", 7)

    fig.tight_layout()
    plt.title('Mean Protein Intake in the UK between 2008 and 2016', weight = 'bold')
    plt.show()

