# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 19:20:41 2021

@author: Ege
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression,Lasso
from sklearn.preprocessing import PolynomialFeatures
import warnings
warnings.filterwarnings('ignore')

# Data=pd.read_csv("Joined_Value.csv")
# Data["slope"]=(Data["100"]-Data["0"])/100
# Data["smokers"]=Data["female_smokers"]+Data["male_smokers"]
# Data=Data.drop(columns=["female_smokers","male_smokers","25","50","75"])
# Data.to_csv("Joined_Value_Updated.csv")

Data1=pd.read_csv("Joined_Value_Updated.csv")
df=pd.read_csv("Variables.csv")
Variables=df.to_numpy().flatten().tolist()
# Variables=["population","population_density","gdp_per_capita",\
                 # "cardiovasc_death_rate","diabetes_prevalence",\
                     # "life_expectancy","human_development_index","smokers","AirPolutioIndex"]
Data1=Data1.set_index("location")
Data1["intercept"]=Data1["0"]
# DataFil=Data1[Data1["slope"]>-5]
DataFil=Data1.sort_values(by="slope")
DataFil=DataFil.head(int(len(Variables)))


Slope=DataFil["slope"]
Intercept=DataFil["intercept"]
DataFil=DataFil[Variables]


A_s=DataFil.to_numpy()
C_s=Slope.to_numpy()
B_s=np.dot(np.linalg.inv(A_s),C_s)

A_int=DataFil.to_numpy()
C_int=Intercept.to_numpy()
B_int=np.dot(np.linalg.inv(A_int),C_int)


Data2=pd.read_csv("C:/NTNU_Master/1st_Semester/DataBase/Project/Data/Country/1CountryParametersV2.csv")
Data2=Data2.set_index("location")

DataWrite=pd.DataFrame({"Country":"0","Rate":0.0,"Intercept":0.0,"Use":True},index=[0])
for i in range(len(Data2)):
    # print(Data2.index[i],np.dot(B,Data2.iloc[i][Variables].to_numpy()))
    
    if bool(np.dot(B_s,Data2.iloc[i][Variables].to_numpy())<0) & bool(np.dot(B_int,Data2.iloc[i][Variables].to_numpy())>0):
        Use=True
    else:
        Use=False
    Add=[Data2.index[i],np.dot(B_s,Data2.iloc[i][Variables].to_numpy()),np.dot(B_int,Data2.iloc[i][Variables].to_numpy()),Use]
    DataWrite.loc[len(DataWrite)] =Add
DataWrite=DataWrite.drop([0])
DataWrite=DataWrite.set_index("Country")
DataWrite.to_csv("RateOutput.csv")



