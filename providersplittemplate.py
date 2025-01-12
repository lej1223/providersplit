#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
pd.set_option('display.max_rows', 100)
import openpyxl


# In[2]:


dtypes = {'Awardee': object,
          'Document Type': object,
          'Order Number': float,
          'Item Number': float,
          'NDC': object,
          'Ordering Intention': object,
          'Fund Type': object,
          'VFC Qty': int,
          '317 Qty': int,
          'STATE Qty': int,
          'CHIP Qty': int,
          'Order Qty': float}


# In[3]:


excel_file_path= "chip_awardees_fy22.xlsx"


# In[4]:


df= pd.read_excel(excel_file_path, sheet_name= 'CHIP Awardees_ALL', dtype=dtypes, thousands=',')


# In[5]:


print(df)


# In[6]:


df.head()


# In[7]:


df.tail()


# In[8]:


df= df.loc[df['Document Type']=='ZKB',]
df.info()


# In[9]:


indirect= df.loc[(df['NDC'] != '00006-4171-00') & (df['NDC'] != '00006-4827-00')]


# In[10]:


for_pivot = indirect[['Awardee', 'Fund Type']].copy()


# In[13]:


table= pd.crosstab(for_pivot['Awardee'], for_pivot['Fund Type'])
table


# In[15]:


table['Total'] = table[317]+table['CHP']+table['S/L']+table['SPL']+table['VFC']
table


# In[16]:


table['Percent SPL'] = table['SPL']/table['Total']
table


# In[17]:


table['Percent CHP'] = table['CHP']/table['Total']
table


# In[18]:


table['Percent VFC'] = table['VFC']/table['Total']
table


# In[22]:


table.to_csv('fy22_spl_percents.csv')


# In[30]:


table.head()


# In[32]:


table['Percent 317'] = table[317]/table['Total']
table


# In[33]:


table['Percent S/L'] = table['S/L']/table['Total']
table


# In[42]:


table['No Split']= table['Percent CHP']+table['Percent VFC']+table['Percent 317']+table['Percent S/L']
table


# In[43]:


table['True Split']= 1-table['No Split']
table


# In[45]:


table.to_csv('fy22_true_splits.csv')


# In[46]:


indirect.head()


# In[47]:


def split(num_of_zeros):
    if num_of_zeros == 3:
        return f'no split'
    else:
        return f'split'


# In[48]:


indirect['num_of_zeros'] = indirect['num_of_zeros'].map(split)


# In[49]:


table = pd.crosstab(indirect['Awardee'], indirect['num_of_zeros'])
table.head()


# In[50]:


table['total'] = table['no split'] + table['split']
table['percent_spl'] = table['split']/table['total']
table.head()


# In[51]:


table.to_csv('true_spl.csv')

