import pandas as pd
import numpy as np
import os

class Predict:

    def generate_csv(self, variables):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        inp_var_file = os.path.join(THIS_FOLDER, 'InputVariables.csv')
        df=pd.read_csv(inp_var_file)
        Variables=df.to_numpy().flatten().tolist()

        # dfCoeff=pd.read_csv("Coefficient.csv")
        coeff=variables
        # print(coeff)
        # dfCoeff=pd.read_csv("Coefficient.csv")
        # coeff=dfCoeff.to_numpy().flatten().tolist()
        print(coeff)
        country_par_file = os.path.join(THIS_FOLDER, '1CountryParametersV2.csv')
        Data2=pd.read_csv(country_par_file)
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
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            country_par_file = os.path.join(THIS_FOLDER, f"Countries/{PickCountry}")

            CountryFixed=pd.read_csv(country_par_file).dropna()
            NewPerMil=CountryFixed["new_cases_per_million"]
            NewPerMilDif=NewPerMil.diff()
            CalRate=m*StrIndex+b
            RatePerDay=np.zeros(14)
            for i in range(1,15):
                Dummy=i*(CalRate-NewPerMilDif.iloc[-1])/14        
                RatePerDay[i-1]=Dummy
            np.random.seed(0)
            FirstPart=NewPerMil.copy().to_frame().reset_index(drop=True)
            
            AddFrame=np.zeros(14)
            i=0
            
            for k in RatePerDay:        
                AddFrame[i]=FirstPart.iloc[-1]+k+np.random.rand()*FirstPart.mean()
                if  AddFrame[i]<=0:
                    AddFrame[i]=0
                i+=1
            Addindex=(FirstPart.index[-1]+1)+np.arange(14)
            df=pd.DataFrame(AddFrame,columns=["new_cases_per_million"],index=Addindex)
            FirstPart=FirstPart.drop(FirstPart[FirstPart["new_cases_per_million"]<0].index)
            return df.values.transpose()[0]
        else:
            return "MathModel cannot predict with selected variables for this country"    
