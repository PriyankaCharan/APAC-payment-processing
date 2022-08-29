#!/usr/bin/env python
# coding: utf-8

# # INTRODUCTION:
# Here are some notes and comments about this datasets : This data set contains information about 10,000 movies collected from The Movie Database (TMDb), including user ratings and revenue.
# 
# Certain columns, like ‘cast’ and ‘genres’

# # The questions about this dataset:
# Which company and merchant had the highest revenue? (performance tracking)
# Which merchant had the hightest transactions in a month
# Customer's Region Analysis (which country do the top custoemrs reside in)
# Most preferred payment methods by customers and deep dive to see the most used scheme of card used
# Analysis using Authentication Rate
# Fraud transaction Analysis

# In[1]:


import seaborn as sns 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


df = pd.read_csv("APAC Data Analytics Case Study.csv")


# # Exploring Data Set
# 1. Looking at the head of the data and checkinng for the data types and Null value.
# 2. Replacing Null value with appropriate value.
# 3. Removing columns that would not be required for the Analysis

# In[3]:


df.head()


# In[4]:


df.shape


# In[5]:


df.describe()


# In[6]:


df.dtypes


# In[7]:


df.isnull().sum()


# In[8]:


# drop unuseful columns 
df.drop(['Unnamed: 0','pspreference','bin', 'received'],axis=1,inplace=True)


# In[9]:


df.nunique()


# In[10]:


# Handlilng missing data for issuercountrycode
# Using string "missing" to replace all NUll values
df['issuercountrycode'].fillna('missing',inplace=True )


# In[11]:


# confirm the data 
df.isnull().sum()


# In[12]:


#checking for duplicates
df.duplicated().sum()


# In[13]:


df.company.value_counts().plot(kind='bar')


# #1. Which merchant had the hightest transactions in a month ---- Ans. ABC_IDR

# In[14]:



df.merchant.value_counts().plot(kind='bar')


# In[15]:


# Checking the revenue for the merchant 
df.groupby('merchant').amount.sum().sort_values(ascending=False)


# In[16]:


# The above is misleading because of amount received in different currency
#Let us try to covert the amount in common currency for comparision
cur_change = {'currencycode':['IDR','TBH','SGD','MYR'],'onedollar':[0.000067,0.028,0.72,0.22]}


# In[17]:


df_curr= pd.DataFrame(cur_change)


# In[18]:


df_curr


# In[19]:


df = df.merge(df_curr, on='currencycode', how='left')


# In[20]:


df['amount_USD']= df['amount'] * df['onedollar']


# In[21]:


df.head()


# #2.WWhich company and merchant had the highest revenue? (performance tracking)

# In[22]:


#Now let us checking the revenue for the merchant in USD
df.groupby('merchant').amount_USD.sum().round().sort_values(ascending=False)

##WE CAN SEE THAT ABC_SGD HAS THE HIGHEST REVENUE


# In[23]:


#3.Customer's Region Analysis (which country do the top custoemrs reside in?)


# In[24]:



df.issuercountrycode.value_counts().head(5)

# TOP 5 COUNTRIES OF MOST CUSTOMERS


# In[25]:


df.groupby(['merchant','issuercountrycode']).amount.count().sort_values(ascending=False).head(20)

#MERCHANT ABC_IDR HAS HIGHEST TRANSACTIONS BY PEOPLE RESIDING IN Indonasia
# CAN SEE THAT MERCHANT IS GETTING HIGHEST TRANSACTION FROM ITS OWN COUNTRY PEOPLE


# In[26]:


df_ABC_IDR =df[df['merchant']=='ABC_IDR']


# In[27]:


df_ABC_IDR.issuercountrycode.value_counts().head(10).plot(kind='bar')


# # 4.Most preferred payment methods by customers and deep dive to see the most used scheme of card used
# Ans: premiumcredit, standardcredit and standard debit are the most used payment methods for 10 merchants with VISA used,preferrably as a card network shceme

# In[28]:


df.paymentmethod.value_counts().plot(kind='barh')


# In[29]:


df.scheme.value_counts()


# In[30]:


#Also look at the cards with highest trsactions amount
df.groupby('paymentmethod').amount_USD.agg(['sum','max']).round().sort_values(by='sum',ascending=False)

# premiumcredit and standarddebit were used widely by customers to make huge payments to merchants


# In[31]:


df.groupby(['merchant','paymentmethod']).amount_USD.agg(['sum','max']).round().sort_values(by='max',ascending=False).head(5)
# IT'S INTERESTING TO NOTE THAT SINGAPORE MERCHANTS HAVE THE HIGHEST AMOUNT TRANSACTED(USD 71928) FOR THIER PRODUCTS
#IF IT IS A HIGH AMOUNT OF PAYMENT CUSTOMERS TRUST credit and staadartcredit and premiumcredit for payments


# In[32]:


df.groupby(['merchant','issuercountrycode','paymentmethod']).amount_USD.agg(['sum','max']).round().sort_values(by='max',ascending=False).head(5)
#POINT TO NOTE: CUSTOMER WHO MADE PAYMENT USING CREDIT HAS NO ISSUERCCOUNTRYCODE. SAME AMOUNT HAS BEEN TRANSACTED FOR DEF_SGD AND ABC_SGD


# In[33]:


#6. Fraud transaction Analysis
df['Fraudulant_trans'] = df['genericresponse'].apply(lambda x: 'Fraud' if x == 'FRAUD' else 'Not Fraud')

Fraud_count = df.Fraudulant_trans.value_counts()
Fraud_count


# In[34]:


#Fraudulant transactions in data are 18188

Fraud_count.plot(kind='pie',figsize=(5,5))


# In[35]:


grouped = df.groupby(['Fraudulant_trans','issuercountrycode']).amount.count().sort_values(ascending=False).head(5)


# In[36]:


grouped


# # TOP 5 COUNTRIES OF CUSTOMER INVOLVED IN FRAUD TRANSACTIONS(Hightest in Indonasia)

# In[37]:


df.groupby(['issuercountrycode']).apply(lambda x: x[x['Fraudulant_trans'] == 'Fraud']['amount'].count()).sort_values(ascending=False).head(5)


# In[38]:


type(grouped)


# In[39]:


grouped['Fraud']


# In[40]:


grouped_test=df.groupby(['Fraudulant_trans','merchant','issuercountrycode','paymentmethod']).amount.count().sort_values(ascending=False)


# In[41]:


# standarddebit is used the most by Indonasian customers that had their transactions rendered FRAUD(IDR merchants most attacked)
grouped_test['Fraud']


# # AUTHENTICATION RATE ANLAYSIS

# In[60]:



df['Auth_Rate'] = (df.approved/df.approved.count())*100


# In[61]:


df['Auth_Rate']


# In[ ]:


df.head()


# In[ ]:





# In[ ]:





# In[ ]:




