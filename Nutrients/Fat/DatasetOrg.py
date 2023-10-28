#Created by Youssef ALAOUI MRANI
#Used to treat the dataset.
#The first part of the code treats the data for the bar charts while the second part treats it for the pie charts

import pandas as pd
import plotly.express as px
import plotly.io as pio

class DataOrg:
    def __init__(self, xlsxfile):
        '''Method to set all the class attributes'''
        self.excelPath = xlsxfile

    def DataSet_Org(self):
        excelPath = self.excelPath
        df = pd.read_excel(excelPath, sheet_name = "Fat Intake",usecols="A:E", skiprows=4, skipfooter = 271, engine = "openpyxl")
        # df2 = df.loc[:,['          Years 1-2']]
        df2 = df.iloc[4]
        df2 = df2.dropna()
        df2 = df2.reset_index(drop=True)
        # print(df2)

        # print(df2[0])

        df3 = df



        for i in range(len(df)):
            if (df.iloc[i][0]!="    Mean"):
                df3 = df3.drop([i])

        df_M = df3.iloc[[1]]

        for i in range(1,6):

            df_M = df_M.append(df3.iloc[1+(3*i)])
        # df_M = df3.iloc[[1]]
        # df_M = df_M.append(df3.iloc[[4]])
        # df_M = df_M.append(df3.iloc[[7]])

        df_F = df3.iloc[[2]]
        for i in range(1,6):
            df_F = df_F.append(df3.iloc[2+(3*i)])



        n = df_M.columns [0]

        # df_M.drop(n, axis = 1, inplace = True)

        # label = [(4+10)/2, (11+18)/2, (19+64)/2, 65, (65+74)/2, 75]
        label = ["4-10", "11-18", "19-64", "65+", "65-74", "75+"]

        df_M[n] = label
        df_F[n] = label

        df_M = df_M.rename(columns={"Unnamed: 0": "Age groups", "          Years 1-2": "Men 1-2","      Years 3-4": "Men 3-4","       Years 5-6": "Men 5-6","          Years 7-8": "Men 7-8" })
        df_F = df_F.rename(columns={"Unnamed: 0": "Age groups", "          Years 1-2": "Women 1-2","      Years 3-4": "Women 3-4","       Years 5-6": "Women 5-6","          Years 7-8": "Women 7-8" })

        df_M = df_M.reset_index(drop = True)
        df_F = df_F.reset_index(drop = True)



        df_tot = df_F
        df_tot["Men 1-2"] = df_M["Men 1-2"]
        df_tot["Men 3-4"] = df_M["Men 3-4"]
        df_tot["Men 5-6"] = df_M["Men 5-6"]
        df_tot["Men 7-8"] = df_M["Men 7-8"]



        return df_tot


    def pie_org(self, year):
        # Organisation for pie chart:



        year = year.drop(year.index[0])

        year = year.dropna()

        year = year.reset_index(drop=True)
        year = year.drop(year.index[1:10])
        year = year.drop(year.index[2:10])

        year = year.drop(year.index[4:10])
        year = year.drop(year.index[5:18])

        year = year.drop(year.index[6:9])

        year = year.drop(year.index[7:14])

        year = year.drop(year.index[8:17])

        year = year.drop(year.index[9:])

        year.iloc[8] = 100 - (year.sum() - year.iloc[8])

        year = year.reset_index(drop=True)
        year.columns = ['1.5-3', '4-10', '11-18', '19-64', '65-74', '75+']
        food_cat = ['Cereal Products', 'Milk Products', 'Egg and egg dishes', 'Fat spreads', 'Meat', 'Fish',
                    'Vegetable and potatoes', 'Sugar preserves and '
                                              'Confectionery',
                    'Others']
        year.insert(loc=0, column='Food Categories', value=food_cat)

        return year

    def org_year(self):
        df = pd.read_excel(self.excelPath, sheet_name='Fat Contribution', engine=
        'openpyxl', skiprows=5)

        year_2008 = df.iloc[:, 1:7]
        year_2010 = df.iloc[:, 7:13]
        year_2012 = df.iloc[:, 13:19]
        year_2014 = df.iloc[:, 19:25]

        df.dropna()
        year_2008 = self.pie_org(year_2008)
        year_2010 = self.pie_org(year_2010)
        year_2012 = self.pie_org(year_2012)
        year_2014 = self.pie_org(year_2014)
        return year_2008, year_2010, year_2012, year_2014
