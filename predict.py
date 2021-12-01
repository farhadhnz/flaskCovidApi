import pandas as pd
import numpy as np

class Predict:

    def generate_csv(self, variables):
        Data1=pd.read_csv("Joined_Value_Updated.csv")
        Data1=Data1.set_index("location")
        Data1["intercept"]=Data1["0"]
        # DataFil=Data1[Data1["slope"]>-5]
        DataFil=Data1.sort_values(by="slope")
        DataFil=DataFil.head(int(len(variables)))


        Slope=DataFil["slope"]
        Intercept=DataFil["intercept"]
        DataFil=DataFil[variables]


        A_s=DataFil.to_numpy()
        C_s=Slope.to_numpy()
        B_s=np.dot(np.linalg.inv(A_s),C_s)

        A_int=DataFil.to_numpy()
        C_int=Intercept.to_numpy()
        B_int=np.dot(np.linalg.inv(A_int),C_int)


        Data2=pd.read_csv("1CountryParametersV2.csv")
        Data2=Data2.set_index("location")

        DataWrite=pd.DataFrame({"Country":"0","Rate":0.0,"Intercept":0.0,"Use":True},index=[0])
        for i in range(len(Data2)):
            # print(Data2.index[i],np.dot(B,Data2.iloc[i][Variables].to_numpy()))
            
            if bool(np.dot(B_s,Data2.iloc[i][variables].to_numpy())<0) & bool(np.dot(B_int,Data2.iloc[i][variables].to_numpy())>0):
                Use=True
            else:
                Use=False
            Add=[Data2.index[i],np.dot(B_s,Data2.iloc[i][variables].to_numpy()),np.dot(B_int,Data2.iloc[i][variables].to_numpy()),Use]
            DataWrite.loc[len(DataWrite)] =Add
        DataWrite=DataWrite.drop([0])
        DataWrite=DataWrite.set_index("Country")
        DataWrite.to_csv("RateOutput.csv")


    def predict_cases(self, country, str_index):
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

    
        CountSel=country
        StrIndex=float(str_index)
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
            # df_date=pd.DataFrame(AddFrame,columns=["date"],index=Addindex)
            Prediction=pd.concat([Deneme,df],ignore_index=True)
            return df.values.transpose()[0]
        else:
            return "MathModel cannot predict with selected variables for this country"    
