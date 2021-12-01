# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 12:40:32 2021

@author: Ege
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


Countries=["BelgiumCovid.csv","CzechiaCovid.csv","FranceCovid.csv","GermanyCovid.csv",\
           "GreeceCovid.csv","ItalyCovid.csv","NetherlandsCovid.csv","PolandCovid.csv",\
           "PortugalCovid.csv","RomaniaCovid.csv","RussiaCovid.csv","SpainCovid.csv",\
           "SwedenCovid.csv","UkraineCovid.csv","United KingdomCovid.csv",\
           "USCovid.csv","CanadaCovid.csv","NorwayCovid.csv"]
    
Countries2=["Belgium","Czechia","France","Germany",\
           "Greece","Italy","Netherlands","Poland",\
           "Portugal","Romania","Russia","Spain",\
           "Sweden","Ukraine","United Kingdom",\
           "United States","Canada","Norway"]

    
CountSel=input("Country: ")
StrIndex=float(input("StrIndex: "))
for j in range (len(Countries2)):
    if Countries2[j]==CountSel:
        PickCountry=Countries[j]


Rates=pd.read_csv("RateOutput.csv")
if (Rates[Rates["Country"]==CountSel]["Use"].iloc[0]):
    m=Rates[Rates["Country"]==CountSel]["Rate"]
    b=Rates[Rates["Country"]==CountSel]["Intercept"]
    CountryFixed=pd.read_csv(f"Countries/{PickCountry}").dropna()
    NewPerMil=CountryFixed["new_cases_per_million"]
    NewPerMilDif=NewPerMil.diff()
    CalRate=m*StrIndex+b
    RatePerDay=np.zeros(14)
    for i in range(1,15):
        Dummy=i*(CalRate-NewPerMilDif.iloc[-1])/14        
        RatePerDay[i-1]=Dummy
        
    Deneme=NewPerMil.copy().to_frame().reset_index(drop=True)
    
    AddFrame=np.zeros(14)
    i=0
    
    for k in RatePerDay:
        
        # Deneme=Deneme.reset_index(drop=True)
        
        # Deneme=Deneme.append(pd.DataFrame({"new_cases_per_million":float(Deneme.iloc[-1]+k)},index=[0]))
        
        AddFrame[i]=Deneme.iloc[-1]+k
        if  AddFrame[i]<=0:
            AddFrame[i]=0
        i+=1
    Addindex=(Deneme.index[-1]+1)+np.arange(14)
    df=pd.DataFrame(AddFrame,columns=["new_cases_per_million"],index=Addindex)
    Prediction=pd.concat([Deneme,df],ignore_index=True)
    print(df)
    plt.plot(Prediction)
else:
    print("MathModel cannot predict with selected variables for this country")    






