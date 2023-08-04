#!/usr/bin/env python
# coding: utf-8

# In[164]:


import requests
import pandas as pd
import numpy as np


# In[2]:


url = 'https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws/mentorskool/v1/sales'

response = requests.get(url, headers = {"access_token":"fe66583bfe5185048c66571293e0d358"}, params = {"offset":30})

response.json()


# In[3]:


fetch_records = []
fetch_record_order = []
fetch_record_product = []
final_df = []
url = 'https://zucwflxqsxrsmwseehqvjmnx2u0cdigp.lambda-url.ap-south-1.on.aws/mentorskool/v1/sales'
offset = 0
limit = 100
headers = {'access_token' : 'fe66583bfe5185048c66571293e0d358'}
for i in range(5):
    params = {'offset': offset, 'limit': limit}
    response = requests.get(url, headers = headers , params = params)
    data = response.json()
    fetch_records.extend(data["data"])
    offset+=limit

df = pd.DataFrame.from_dict(fetch_records, orient='columns')


# In[4]:


df


# In[184]:


df1 = pd.json_normalize(fetch_records)
df1


# In[9]:


df1['item_count'] = df1['product.sizes'].apply(len)


# In[8]:


max_value = df1['item_count'].max()


# In[10]:


max_index = df1['item_count'].idxmax()
row_with_max_value = df1.loc[max_index]
row_with_max_value


# In[14]:


matching_rows = df1[df1['product.product_name'] == 'Mitel 5320 IP Phone VoIP phone']

matching_rows


# In[18]:


from datetime import datetime
df1['order_purchase_date'] = pd.to_datetime(df1['order.order_purchase_date'])


# In[19]:


df1


# In[52]:


df1['Month'] = df1['order_purchase_date'].dt.month
df1['Year'] = df1['order_purchase_date'].dt.year
df1


# In[55]:


pivot_df = df1.pivot_table(index='Month', columns='Year', values=['sales_amt', 'profit_amt'], aggfunc='sum')
pivot_df.reset_index()


# In[185]:


df1 = df1.applymap(lambda x: None if x == 'null' else x)


# In[100]:


profit_2017 = pivot_df['profit_amt'].iloc[:, 0]
profit_2018 = pivot_df['profit_amt'].iloc[:, 1]
sales_2017 = pivot_df['sales_amt'].iloc[:, 0]
sales_2018 = pivot_df['sales_amt'].iloc[:, 1]
data_2017 = {"profit": profit_2017, "sales":sales_2017}
data_2018 = {"profit": profit_2018, "sales":sales_2018}
df_2017 = pd.DataFrame(data_2017)
df_2018 = pd.DataFrame(data_2018)


# In[104]:


df_2017.reset_index()


# In[91]:


df_2018.reset_index()


# In[108]:


df_2017["Profit_perc"] = df_2017["profit"]*100/df_2017["sales"]
df_2017


# In[109]:


df_2018["Profit_perc"] = df_2018["profit"]*100/df_2018["sales"]
df_2018


# In[112]:


df1['order.order_delivered_customer_date']
df1['order.order_estimated_delivery_date']


# In[148]:


df_dates = df1.iloc[:,8:13]
df_dates


# In[149]:


df_dates['order.order_delivered_customer_date'] = pd.to_datetime(df_dates['order.order_delivered_customer_date'])
df_dates['order.order_estimated_delivery_date'] = pd.to_datetime(df_dates['order.order_estimated_delivery_date'])
df_dates['order.order_purchase_date'] = pd.to_datetime(df_dates['order.order_purchase_date'])


# In[157]:


df_dates['Delay'] = (df_dates['order.order_delivered_customer_date'] - df_dates['order.order_purchase_date']).dt.days
df_dates


# In[159]:


count_greater_than_zero = df_dates['Delay'].apply(lambda x: x > 4).sum()
count_greater_than_zero


# In[161]:


df1.drop(columns=['profit_perc', 'Month', 'Year'], inplace=True)
df1


# In[165]:


df1.replace(np.nan, None, inplace=True)
df1


# In[172]:


df1['order.order_purchase_date'] = pd.to_datetime(df1['order.order_purchase_date'])
df1['order.order_delivered_customer_date'] = pd.to_datetime(df1['order.order_delivered_customer_date'])
df1['Delay'] = (df1['order.order_delivered_customer_date'] - df1['order.order_purchase_date']).dt.days
delay_counts = df1[df1['Delay'] > 4].groupby('order.vendor.VendorID').size()


# In[173]:


delay_counts


# In[180]:


df1['order.customer.customer_name']


# In[187]:


df1 = df1[df1['order.customer.customer_name'].duplicated()]
count_name = sum(name.split()[0] == 'Alan' for name in df1['order.customer.customer_name'])
count_name


# In[189]:


df1


# In[188]:


df1['order.customer.customer_name']


# In[ ]:




