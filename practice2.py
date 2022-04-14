
from flask import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




df = pd.read_csv('C:/Users/sumit/OneDrive/Desktop/TRILAB_EM.csv')
new_df = df[['TS', 'Total_kW', 'kWh']]
lst = []
for i in new_df['Total_kW']:
    if i < 2.20:
        lst.append('Level_1')
    elif i > 2.20 and i < 2.35:
        lst.append('Level_2')
    elif i > 2.35:
        lst.append('Leve_3')

status = {'state': lst}
new_df_1 = pd.DataFrame(status)
result = pd.concat([new_df, new_df_1], axis=1)

Total_kW_raw=new_df['Total_kW'].values.tolist()

# --------------------------------------

no_time_change=[]
no_kwh_change=[]
no_change_state=[]


first =result['state'][0]
first_TS = result['TS'][0]
first_kwh = result['kWh'][0]
for i in result.index:
    if result['state'][i]!=first:
        # for no change state
        no_change_state.append(first)
        no_time_change.append(result['TS'][i-1]-first_TS)
        no_kwh_change.append(result['kWh'][i-1]-first_kwh)

        first = result['state'][i]
        first_TS = result['TS'][i]
        first_kwh = result['kWh'][i]


no_change = pd.DataFrame(list(zip(no_kwh_change,no_time_change,no_change_state))
                          ,columns=['kWh','TS','state'])

level_2=[]
level_3=[]
level_1=[]
for i in no_change.index:
    if no_change['state'][i]=='Level_2':
        level_2.append(no_change['kWh'][i])
    elif no_change['state'][i]=='Leve_3':
        level_3.append(no_change['kWh'][i])
    else:
        level_1.append(no_change['kWh'][i])


def Average(lst):
    return sum(lst) / len(lst)

def min_func(lst):
    min = lst[0]
    for i in lst:
        if i < min:
            min = i
    return min

def max_func(lst):
    max=lst[0]
    for i in lst:
        if i > max:
            max = i
    return max

min=[]
max=[]
avg=[]
for i in [level_1,level_2,level_3]:
    min.append(min_func(i))

for i in [level_1,level_2,level_3]:
    max.append(max_func(i))

for i in [level_1,level_2,level_3]:
    avg.append(Average(i))


final = pd.DataFrame(list(zip(min,max,avg)),columns=['MIN','MAX','AVG'],index=['LEVEL-1','LEVEL-2','LEVEL-3'])
print(final)




