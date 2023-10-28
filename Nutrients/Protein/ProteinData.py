# Organisation: University College London
# Module: Application Programming for Data Science
# Module Code: COMP0034
# Date: 03/03/2021
# Name: ProteinData
# Author: Rayan Souissi
# Description: Program to import and process the data from Data/Dataset.xlsx into usable dataframes


from pathlib import Path
import numpy as np
import pandas as pd
import openpyxl


class ProteinData:
    """Class for retrieving and structuring the data."""

    def __init__(self, xlsxfile):
        '''Method to set all the class attributes'''
        self.xlsxfile = xlsxfile
        self.ages = []
        self.years = []
        self.food_groups = []
        self.protein_contrib = pd.DataFrame()
        self.protein_contrib_2008 = pd.DataFrame()
        self.protein_contrib_2010 = pd.DataFrame()
        self.protein_contrib_2012 = pd.DataFrame()
        self.protein_contrib_2014 = pd.DataFrame()
        self.protein_contrib_mean = pd.DataFrame()
        self.protein_contrib_intake = pd.DataFrame()

        self.protein_intake = pd.DataFrame()
        self.protein_intake_g = pd.DataFrame()
        self.protein_intake_m = pd.DataFrame()
        self.protein_intake_w = pd.DataFrame()
        self.get_data()

    def get_data(self):
        '''Method to import data from excel sheet'''
        engine = 'openpyxl'
        contrib_skip_rows = [0, 1, 2, 3, 4, 5, 44, 45, 47, 48, 49, 50]
        self.protein_contrib = pd.read_excel(self.xlsxfile, engine=engine, usecols = range(1,25),
                                    sheet_name='Protein Contribution',nrows = 78,  skiprows = contrib_skip_rows)
        self.protein_intake = pd.read_excel(self.xlsxfile, engine=engine, sheet_name='Protein Intake',
                                   names = ["Age", "2008-2010", "2010-2012", "2012-2014", "2014-2016"], nrows = 114,
                                            skiprows= range(0,7))

    def process_intake_data(self):
        '''Method to format the INTAKE data into three dataframes for Men, Women and General (Men&Women)'''

        '''1. Extracting only general'''
        self.protein_intake_g = self.protein_intake
        for i in range(6,len(self.protein_intake_g.index),18):           #removing men and women
            self.protein_intake_g = self.protein_intake_g.drop(range(i,i+12))
        self.protein_intake_g = self.protein_intake_g.reset_index(level=0, drop=True)     #resetting index

        for i in range(0,len(self.protein_intake_g.index),6):        #keeping only mean (removing standard deviation, 1st quartil, etc)
            self.protein_intake_g = self.protein_intake_g.drop([i])
            self.protein_intake_g = self.protein_intake_g.drop(range(i+2,i+6))
        self.protein_intake_g = self.protein_intake_g.reset_index(level=0, drop=True)     #resetting index
        self.protein_intake_g['Age'] = [2, 7, 15, 42, 65, 70, 75]                #Setting label
        self.protein_intake_g = self.protein_intake_g.drop([0, 4])                            #Removing the 65+
        self.protein_intake_g = self.protein_intake_g.reset_index(level=0, drop=True)         #resetting index
        #print(self.protein_intake_g)    # for debug


        '''2. Extracting only male'''
        self.protein_intake_m = self.protein_intake
        for i in range(12,len(self.protein_intake_m.index),18):              #removing general and women
            self.protein_intake_m = self.protein_intake_m.drop(range(i,i+12))
        self.protein_intake_m = self.protein_intake_m.drop(range(0,6))
        self.protein_intake_m = self.protein_intake_m.reset_index(level=0, drop=True)     #resetting index

        for i in range(0,len(self.protein_intake_m.index),6):         #keeping only mean (removing standard deviation, 1st quartil, etc)
            self.protein_intake_m = self.protein_intake_m.drop([i])
            self.protein_intake_m = self.protein_intake_m.drop(range(i+2,i+6))
        self.protein_intake_m = self.protein_intake_m.reset_index(level=0, drop=True)     #resetting index
        self.protein_intake_m['Age'] = [7, 15, 42, 65, 70, 75]                   #Setting label
        self.protein_intake_m = self.protein_intake_m.drop([3])                               #Removing the 65+
        self.protein_intake_m = self.protein_intake_m.reset_index(level=0, drop=True)         #resetting index
        #print(self.protein_intake_m)    # for debug


        '''3. Extracting only women'''
        self.protein_intake_w = self.protein_intake
        for i in range(0,len(self.protein_intake_w.index)-18,18):            #deleting general and women
            self.protein_intake_w = self.protein_intake_w.drop(range(i,i+12))
        self.protein_intake_w = self.protein_intake_w.reset_index(level=0, drop=True)     #resetting index
        self.protein_intake_w = self.protein_intake_w.drop(range(36,42))

        for i in range(0,len(self.protein_intake_w.index),6):         #keeping only mean (removing standard deviation, 1st quartil, etc)
            self.protein_intake_w = self.protein_intake_w.drop([i])
            self.protein_intake_w = self.protein_intake_w.drop(range(i+2,i+6))
        self.protein_intake_w = self.protein_intake_w.reset_index(level=0, drop=True)     #resetting index
        self.protein_intake_w['Age'] = [7, 15, 42, 65, 70, 75]                   #Setting label
        self.protein_intake_w = self.protein_intake_w.drop([3])                               #Removing the 65+
        self.protein_intake_w = self.protein_intake_w.reset_index(level=0, drop=True)         #resetting index
        #print(protein_intake_w)    # for debug


        '''4. Generate the data frames for the mean over the four years periods'''

        #For General
        z = [self.protein_intake_g['2008-2010'], self.protein_intake_g['2010-2012'], self.protein_intake_g['2012-2014'], self.protein_intake_g['2014-2016']]
        self.protein_intake_g['2008-2016'] = pd.DataFrame(np.mean(z, axis=0))

        #Adding Men
        z = [self.protein_intake_m['2008-2010'], self.protein_intake_m['2010-2012'], self.protein_intake_m['2012-2014'], self.protein_intake_m['2014-2016']]
        self.protein_intake_m['2008-2016'] = pd.DataFrame(np.mean(z, axis=0))

        #Adding Women
        z = [self.protein_intake_w['2008-2010'], self.protein_intake_w['2010-2012'], self.protein_intake_w['2012-2014'], self.protein_intake_w['2014-2016']]
        self.protein_intake_w['2008-2016'] = pd.DataFrame(np.mean(z, axis=0))



    def process_contribution_data(self):
        '''Method to format the INTAKE data into five dataframes for each time-periods'''

        self.ages = ["1.5-3", "4-10", "11-18", "19-64", "65-74", "75+"]
        self.years = ["2008-2010", "2010-2012", "2012-2014", "2014-2016", "2008-2016"]
        self.food_groups = ["Cereals and cereal products", "Milk and milk products", "Cheese", "Meat and meat products",
                  "Fish and fish dishes", "Vegetables and potatoes", "Fruit","Sugar, preserves and confectionery ",
                            "Miscellaneous (Soups and Sauces)", "Other (Savour snacks, Nuts and seeds, and beverages)"]

        self.protein_contrib_intake = self.protein_contrib.iloc[71]
                                                    #Save the intake of protein (g/day) for all contribution columns

        '''1. Drop all the non-necessary lines'''
        self.protein_contrib = self.protein_contrib.drop(range(1,12))
        self.protein_contrib = self.protein_contrib.drop(range(13,18))
        self.protein_contrib = self.protein_contrib.drop(range(19,25))
        self.protein_contrib = self.protein_contrib.drop(range(26,39))
        self.protein_contrib = self.protein_contrib.drop(range(40,44))
        self.protein_contrib = self.protein_contrib.drop(range(45,50))
        self.protein_contrib = self.protein_contrib.drop(range(54,57))
        self.protein_contrib = self.protein_contrib.drop(range(58,61))
        self.protein_contrib = self.protein_contrib.drop(range(62,64))
        self.protein_contrib = self.protein_contrib.drop(range(65,72))
        self.protein_contrib = self.protein_contrib.reset_index(level=0, drop=True) #reset index

        '''2. Regroup the mean of "Savour Snacks", "Nuts and Seeds", Alcoholic beverages", and "Non-Alcolholic beverages"
        and put it at the end of dataframe for new food-group "other"'''

        z=[]
        t=0
        for j in range(0,24):
            for i in range(6,8):
                t += self.protein_contrib.iloc[i,j]
            for i in range(10,12):
                t += self.protein_contrib.iloc[i,j]
            z.append(t)
            t = 0

        '''3. Drop the lines that are now regrouped in "Other" (last line)'''
        self.protein_contrib.loc[len(self.protein_contrib.index)] = z
        self.protein_contrib = self.protein_contrib.drop(range(6,8))
        self.protein_contrib = self.protein_contrib.drop(range(10,12))
        self.protein_contrib = self.protein_contrib.reset_index(level=0, drop=True) #reset index

        '''4. Assign to each period dataframe its values (in the columns of the general contrib dataframe'''
        self.protein_contrib_2008 = self.protein_contrib.iloc[:, 0:6]
        self.protein_contrib_2008.columns = self.ages
        self.protein_contrib_2010 = self.protein_contrib.iloc[:, 6:12]
        self.protein_contrib_2010.columns = self.ages
        self.protein_contrib_2012 = self.protein_contrib.iloc[:, 12:18]
        self.protein_contrib_2012.columns = self.ages
        self.protein_contrib_2014 = self.protein_contrib.iloc[:, 18:24]
        self.protein_contrib_2014.columns = self.ages

        '''5. Create dataframe for mean contribution between 2008 and 2016'''
        z = [self.protein_contrib_2008, self.protein_contrib_2010, self.protein_contrib_2012, self.protein_contrib_2014]
        self.protein_contrib_mean = pd.DataFrame(np.mean(z, axis=0))    #reset index
        self.protein_contrib_mean.columns = self.ages
