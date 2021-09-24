# explore chicago.csv
import pandas as pd
import numpy as np
import time as t

# evade the data truncate problem
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


df = pd.read_csv("chicago.csv")
print('columns = ',df.columns)  # start by viewing the first few rows of the dataset!
print(df.describe())
print()
print(df.info())
print(df['Gender'].value_counts()) # no. of male and female user
print(df['Gender'].unique())

print('Male' in df['Gender'].any()) # if male exists at any point in this
print('number of NaNs: {} out of {}'.format(df.isnull().sum().sum(),df.count()))
print('user types count: ', df['User Type'].value_counts())
