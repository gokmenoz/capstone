import pandas as pd
import numpy as np
import dill

df=pd.read_csv('static/ProjectsGrid.csv')

idx=df.groupby(['District-Ward_Name','Vote_Year','Category_re-coded'])['Votes'].sum()

data=pd.DataFrame([[i[0],i[1],i[2]] for i in idx.index.values],columns=['cd','year','need'])

data['Votes']=list(idx)

data1=data.groupby(['cd','year'])['Votes'].apply(lambda x:x.nlargest(3))

data1_temp=pd.DataFrame([[i[0],i[1]] for i in data1.index.values],columns=['cd','year'])
data1_temp['Votes']=list(data1)

data1=pd.merge(data,data1_temp,on=['cd','year','Votes'])

