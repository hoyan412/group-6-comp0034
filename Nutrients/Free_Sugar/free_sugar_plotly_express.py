# Module: COMP0034 Application Programming for Data Science
# Author: Ho Yan Or
# Description: Bar chart showing the change in average free sugar intake over the years of study for each age
#              group in the UK

# Import relevant packages
import pandas as pd
import plotly.express as px
import openpyxl

if __name__ == "__main__":
    # Read xlsx file with the dataset and create a pandas dataframe with the selected rows
    excel_path = 'C:/Users/admin/PycharmProjects/coursework-1-groups-group-6-comp0034/data/Dataset.xlsx'
    df = pd.read_excel(excel_path, engine='openpyxl', sheet_name='Free Sugar Intake', skiprows=8, nrows=109)
    years = ['2008 - 2010', '2010 - 2012', '2012 - 2014', '2014 - 2016']

    # extract general sugar intake data into another dataframe
    sugar_intake_g = df.iloc[18::18, 1:]
    sugar_intake_g = sugar_intake_g.drop(df.index[[72]])
    sugar_intake_g = sugar_intake_g.reset_index(drop=True)
    sugar_intake_g = sugar_intake_g.T
    sugar_intake_g.columns = ['4 to 10', '11 to 18', '19 to 64', '65 to 74', '75+']
    sugar_intake_g['years'] = years

    # Restructure the two-variable dataframe into a one-variable dataframe
    df1 = sugar_intake_g.drop(columns=['11 to 18', '19 to 64', '65 to 74', '75+'])
    df1['age'] = ['4 to 10'] * 4
    df1 = df1.rename(columns={'4 to 10': 'free sugar intake'})

    df2 = sugar_intake_g.drop(columns=['4 to 10', '19 to 64', '65 to 74', '75+'])
    df2['age'] = ['11 to 18'] * 4
    df2 = df2.rename(columns={'11 to 18': 'free sugar intake'})

    df3 = sugar_intake_g.drop(columns=['4 to 10', '11 to 18', '65 to 74', '75+'])
    df3['age'] = ['19 to 64'] * 4
    df3 = df3.rename(columns={'19 to 64': 'free sugar intake'})

    df4 = sugar_intake_g.drop(columns=['4 to 10', '11 to 18', '19 to 64', '75+'])
    df4['age'] = ['65 to 74'] * 4
    df4 = df4.rename(columns={'65 to 74': 'free sugar intake'})

    df5 = sugar_intake_g.drop(columns=['4 to 10', '11 to 18', '19 to 64', '65 to 74'])
    df5['age'] = ['75+'] * 4
    df5 = df5.rename(columns={'75+': 'free sugar intake'})

    # Combine to create the final dataframe
    frames = [df1, df2, df3, df4, df5]
    df_final = pd.concat(frames)
    df_final = df_final.reset_index(drop=True)

    # Create bar chart
    fig = px.bar(df_final, x="years", y="free sugar intake", color='years', facet_col="age",
                 title='How does average free sugar intake differ over the years of study for each age group?',
                 labels={'years': 'Time Period', 'age': 'Age'})

    fig.show()
