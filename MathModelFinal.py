


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df=pd.read_csv("InputVariables.csv")
dfCoeff=pd.read_csv("Coefficient.csv")
coeff=dfCoeff.to_numpy().flatten().tolist()
Variables=df.to_numpy().flatten().tolist()


Data2=pd.read_csv("1CountryParametersV2.csv")
Data2=Data2.set_index("location")

DataWrite=pd.DataFrame({"Country":"0","Rate":0.0,"Intercept":0.0,"Use":True},index=[0])
B_s=[0.016519248240453296,-0.00021618917797569417, 6.644167226834074,-1.5382232847345065, 3.253999167803337, -23.76469908837231, 0.2350044564912759]

B_int=[-0.048370999869491116, 0.010373424371363557, -315.3608118511198, 52.9317365217468, -123.2276442825312, 986.7726072467151, -6.155353276908965]
for i in range(len(Data2)):
    
    if bool(np.dot(B_s,Data2.iloc[i][Variables].to_numpy())<0) & bool(np.dot(B_int,Data2.iloc[i][Variables].to_numpy())>0):
        Use=True
    else:
        Use=False
    Data3=np.multiply(Data2[Variables].copy().to_numpy()[i],coeff)
    Add=[Data2.index[i],np.dot(B_s,Data3),np.dot(B_int,Data3),Use]
    DataWrite.loc[len(DataWrite)] =Add
    
DataWrite=DataWrite.drop([0])
DataWrite=DataWrite.set_index("Country")
DataWrite.to_csv("RateOutput.csv")

