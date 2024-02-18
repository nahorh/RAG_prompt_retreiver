import pandas as pd
import os

class GenerateDF:
    def __init__(self,results):
        self.results = results
        
    def generate_df(self):
        self.df=pd.DataFrame(self.results)
        print('Data Frame Generated')
    
    def save(self,filename='data.csv'):
        if '.csv' not in filename:
            filename +='.csv'
        self.df.to_csv(os.path.join('./data/',filename),encoding='utf-8',index=False)
        print(f'Data Frame saved in./data/{filename} !')