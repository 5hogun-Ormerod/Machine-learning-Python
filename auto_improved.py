# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 23:00:47 2017

@author: Chris
"""

import pandas as pd
import sklearn
from sklearn import preprocessing


auto = pd.read_csv("./data/autos.csv", sep=',', header=0, encoding='cp1252')

# Data Cleaning

auto.drop(['seller','offerType','abtest','dateCrawled','model', 'nrOfPictures', 'monthOfRegistration', 'lastSeen', 'postalCode', 'dateCreated'], axis='columns', inplace=True)
auto_clean = auto.drop_duplicates(['name','price','vehicleType','yearOfRegistration'
                         ,'gearbox','powerPS','kilometer','fuelType'
                         ,'notRepairedDamage'])

print("Too new: %d" % auto.loc[auto.yearOfRegistration >= 2017].count()['name'])
print("Too old: %d" % auto.loc[auto.yearOfRegistration < 1950].count()['name'])
print("Too cheap: %d" % auto.loc[auto.price < 100].count()['name'])
print("Too expensive: " , auto.loc[auto.price > 150000].count()['name'])
print("Too few km: " , auto.loc[auto.kilometer < 5000].count()['name'])
print("Too many km: " , auto.loc[auto.kilometer > 200000].count()['name'])
print("Too few PS: " , auto.loc[auto.powerPS < 10].count()['name'])
print("Too many PS: " , auto.loc[auto.powerPS > 500].count()['name'])

# Cleaning data
#valid_models = df.dropna()

#### Removing the duplicates
auto_clean = auto.drop_duplicates(['name','price','vehicleType','yearOfRegistration'
                         ,'gearbox','powerPS','kilometer','fuelType'
                         ,'notRepairedDamage'])

#### Removing the outliers
auto_clean = auto_clean[
        (auto_clean.yearOfRegistration <= 2016) 
      & (auto_clean.yearOfRegistration >= 1950) 
      & (auto_clean.price >= 100) 
      & (auto_clean.price <= 150000) 
      & (auto_clean.powerPS >= 10) 
      & (auto_clean.powerPS <= 500)]

#auto_clean = auto_clean[(auto_clean.yearOfRegistration > Year_min) &
#                        (auto_clean.price > Price_min)]

auto_clean['notRepairedDamage'].fillna(value='not-declared', inplace=True)
auto_clean['fuelType'].fillna(value='not-declared', inplace=True)
auto_clean['gearbox'].fillna(value='not-declared', inplace=True)
auto_clean['vehicleType'].fillna(value='not-declared', inplace=True)

#

categorical_cols = ['vehicleType','gearbox','brand','fuelType','notRepairedDamage']
for cat in categorical_cols:
    print(cat,":",auto_clean[cat].unique())
    
l_encs = dict()    
for cat in categorical_cols:
    l_encs[cat] = preprocessing.LabelEncoder()
    l_encs[cat].fit(auto_clean[cat])
    new_col = l_encs[cat].transform(auto_clean[cat])
    auto_clean.loc[:, cat + '_new'] = pd.Series(new_col, index=auto_clean.index)

ohe = preprocessing.OneHotEncoder(sparse=False)
transformed = ohe.fit_transform(auto_clean[[x+'_new' for x in categorical_cols]])
labels = [list(l_encs[cat].classes_) for cat in categorical_cols]
new_labels = [[categorical_cols[k]+labels[k][m] for m in range(len(labels[k]))] for k in range(len(categorical_cols))]

lab_tot = list()
for k in range(len(labels)):
    lab_tot = lab_tot + new_labels[k]

auto_trans = pd.DataFrame(transformed,columns=lab_tot)
auto_trans.loc[:,'yearOfRegistration'] = pd.Series(auto_clean['yearOfRegistration'],index=auto_clean.index)
auto_trans.loc[:,'kilometer'] = pd.Series(auto_clean['kilometer'],index=auto_clean.index)
auto_trans.loc[:,'powerPS'] = pd.Series(auto_clean['powerPS'],index=auto_clean.index)
auto_trans.loc[:,'price'] = pd.Series(auto_clean['price'],index=auto_clean.index)

auto_trans = auto_trans[auto_trans.price >0]
auto_price = auto_trans['price']
auto_trans.drop('price',axis='columns',inplace=True)
