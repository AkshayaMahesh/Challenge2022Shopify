#!/usr/bin/env python
# coding: utf-8

# ## Question 1

# In[5]:


import pandas as pd
import numpy as np


# In[3]:


data=pd.read_csv('/Users/akshayamahesh/Downloads/ShopifyData.csv')
data.head()


# In[7]:


data.shape


# In[8]:


data.isnull().sum()


# In[15]:


data.dtypes


# In[10]:


# counts the number of unique shops in our data
print("Numbers of unique shops: "+ str(len(data.shop_id.unique())))


# ### a. what could be going wrong with our calculation and a better way to evaluate this data

# Let us analyse the `order_amount` column and analyse it's statistics. This will give us a better idea of how our dataset for this variable looks like

# In[11]:


# calculating summary statistics of order_amount variable
data.order_amount.describe()


# __count__ gives the number of non-empty values. Therefore, we can cross verify this with 'data.isnull().sum()'<br>
# __mean__ is 3145.128 USD<br>
# __std__ here represents the standard deviation of the `order_amount` column. The value is 41282.53 USD which seems 
# very large when compared to mean.<br> That is, we can find that there is a large spread of data 
# and presence of potential __*outliers*__. Let us see if we can remove these outliers to see how our data exactly is.<br>
# Also, significant amount of data i.e, 50 percentile or the median is 284.00 USD 
# (50% of data seems to be below 284.00 and 75% of data is below 390.00 USD)
#                                                                                   

# In[23]:


#pip install plotly


# In[24]:


import plotly.express as px


# In[48]:


plot_fig = px.scatter(data, x="created_at",y="order_amount", 
                 color="shop_id",
                 size_max=50,
                 log_x=False, 
                 template="gridon",
                  labels={
                     "created_at": "Time",
                     "order_amount": "Order Amount (in USD)",
                 },
                 title="Sales Distribution" )
plot_fig.show()


# In[64]:


# plot for shop 42
shop_42 = data[data['shop_id'] == 42]
plot_fig = px.scatter(shop_42, x="created_at",y="order_amount",
                      color="shop_id",
                      log_x=False, 
                      size_max=60,
                      hover_data=["total_items"],
                      template="gridon",
                      labels={
                          "created_at": "Time",
                          "order_amount": "Order Amount (in USD)",
                      },
                      title="Sales Distribution of Shop 42" )
plot_fig.show()


# There is a constant purchase of 2000 items that every time amounts to 704k USD (almost on a regular basis). We therefore, need to have a close look of this to examine if these are outliers. Since there is a possibility that there can be a bulk order placement that results in such high `order_amount` we can say that this causes skewness in distribution of data yet not an outlier as such.

# In[67]:


group_by_Total = data.groupby('total_items')['order_amount'].sum().rename_axis('total_items').reset_index(name='total')
total_items_count = data.total_items.value_counts().rename_axis('total_items').reset_index(name='count')
group_by_Total


# In[66]:


# plot for shop 78
shop_78 = data[data['shop_id'] == 78]
plot_fig = px.scatter(shop_78, x="created_at",
                 y="order_amount", 
                 color="shop_id",log_x=False,
                      hover_data=["total_items"],
                 size_max=60, template="gridon",
                 labels={
                     "created_at": "Time",
                     "order_amount": "Order Amount (in USD)",
                 },
                 title="Sales Distribution of Shop 78" )
plot_fig.show()


# This shows that data is distributed over a wide range. On randomly hovering over the data points we find that each
# pair of sneakers costs over 25k USD (maybe this shop sells expensive/high-end) products when compared to other 
# shops. Therefore,this also causes skewness in data and is also not a potential outlier.

# ### b.What metric would you report for this dataset?

# Using the `order_amount` as a metric may not be appropriate here as the data evidently shows skewness.
# From visualization, we found that shop 42 sells bulk orders of 2000 items amounting to 704000 and shop 78 
# which sells high end products that typically seemed to start from 25k USD (which resulted in skewness).<br>
# I personally feel that using a single metric might lead to incorrect insights. But using them in a different 
# way can help us get better insights.<br>
# We need to separate orders on the basis of the total items and see how much the quantity of items 
# contribute to sales cost by grouping them.<br>
# Also, in cases where a single product is sold for a comparatively expensive amount we can strt by looking
# at the standard deviation and median sales of that to form better insights.
# 

# ### c. What is its value?

# Let us now calculate the required metrics,

# In[78]:


groupby_total_items = data.groupby('total_items')['order_amount'].mean().rename_axis('Total Items in Order').reset_index(name='Average of Order Value')
groupby_total_items


# In[80]:


std_dev = data.groupby('total_items')['order_amount'].std().rename_axis('Total Items in Order').reset_index(name='std')['std']
median =  data.groupby('total_items')['order_amount'].median().rename_axis('Total Items in Order').reset_index(name='Median')['Median']


# In[81]:


groupby_total_items['Median of Order Value'] = median
groupby_total_items['Standard Deviation'] = std_dev


# In[82]:


groupby_total_items


# There is a single order in the dataset in which 8 items were ordered, that explains the NaN Standard deviation.
# The orders where 2000 items were ordered amounts to 704k USD that explains for the 0 standard deviation.

# Therefore, grouping data on the basis of quantity of items purchased gives us more meaningful insights. 
# Also, the median of order values gives us a good idea about how data is distributed over the 50th percentile. 
# We can find what part of order values range below and above 50%. <br>
# Rather than looking at a single metric for analysis, comibining the Average Order Value (AOV), Median Order Value(MOV),
# and the Standard Deviation gives us a good insight about the distribution of order amounts. The variation or difference between the Median Order Value
# and Average of Order Value gives an approximate estimate of the skew in the data distribution. 
# Additionally, the standard deviation gives information about how much our order values vary. 
