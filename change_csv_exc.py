import pandas as pd



df = pd.read_csv(r'output.csv',index_col=None)

df.to_excel("origin_data.xlsx",index=None)
