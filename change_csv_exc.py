import pandas as pd



df = pd.read_csv(r'15ability_detect.csv',index_col=None)

df.to_excel("15ability_data.xlsx",index=None)
