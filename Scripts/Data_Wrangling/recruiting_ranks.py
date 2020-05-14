#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 19:14:00 2019

@author: Broth
"""

#import necessary modules
import pandas as pd
import numpy as np

recruiting = pd.read_csv('../../Data/csv-data/cfb_recruit_rankings_2002-18.csv')


#turn off warning
pd.options.mode.chained_assignment = None 


recruiting.head()
## if look through recruiting rankings database, there are a few inconsistencies ##
## with some of the school names. In no particular order, the issues: ##
## 1. 'State' schools are sometimes referred to as 'St' ##
## 2. 'Tennessee' is spelled with an extra 'e' in 2014 ##
## 3. Miami (FL) and Miami (OH) are each given different names in different years ##
## 4. Washington St. Misspelled in 2011 ##
## 5. Arkansas St. mispelled a few different times ##
## 6. UCF changes from Central Florida ##
## 7. FIU changes from Florida International ##
## 8. t in North Texas not always capitalized ##
## 9. Middle Tennessee changes from MTSU ##
## 10. UTSA changes from Texas-San Antonio ##
## 11. NIU changes from Northern Illinois ##
## 12. San Jose State mispelled ##

#create list of years of columns

years = [str(year) for year in range(2002,2019)]

#turn off warning
pd.options.mode.chained_assignment = None 

#create list of what I want to change in recruiting
old_cruits = ['Northern Illinois','Washignton St',
                'Arksansas State','MTSU','Tennesseee','North texas',
                'Central Florida','Florida International','Louisiana-Monroe','Louisiana-Lafayette',
                'San Jsoe State']

#create list of what I want to be the replacement in recruiting
new_cruits = ['NIU','Washington St','Arkansas State','Middle Tennessee','Tennessee'
              ,'North Texas','UCF','FIU','Louisiana Monroe',
             'Louisiana Lafayette', 'San Jose State']


# create function for cleaning the recruiting list
def clean_cruits(wrong_list = None, right_list = None, df = None, columns = None):
    '''
    Function for cleaning the recruiting data set
    
    Inputs:
    - wrong_list: list of the incorrectly named schools
        
    - right_list: list of the correctly named schools (matching index with wrong)
                
                
    - df: the data frame that we want to clean
    
    - columns: list of columns in the dataset we're interested in iterating through
    
    Output:
    - A cleaned data frame
    '''
    for x in range(len(wrong_list)):
        for column in columns:
            for team in df[column]:
            #try/except typeerror to go around nan floats
                try:
                    #if team matches index, rename. *TO BE FIXED LATER*
                    if team == wrong_list[x]:
                        df[column][df.loc[df[column] == team].index[0]] = df[
                        column][df.loc[df[column] == team].index[0]].replace(
                        wrong_list[x],right_list[x])
                        
                    else:
                        continue
                    
                except TypeError:
                    continue
                
    return df

recruiting = clean_cruits(wrong_list = old_cruits, right_list = new_cruits,
             df = recruiting, columns = years)



#test run
#for year in years:
#    for team in recruiting[year]:
#        if team == 'Florida International':
#            recruiting[year][recruiting.loc[recruiting[
#            year] == team].index[0]] = recruiting[year][
#            recruiting.loc[recruiting[year] == team].index[
#            0]].replace('Florida International','FIU')


#can't think of a way to incorporate Miami and St issues in the function. Tried
#to, but I was having a hard time with how it was iterating through

for year in years:
    for team in recruiting[year]:
        try:
            if 'Miami' in team:
                if 'FL' in team:
                    continue
                elif 'OH' in team:
                    recruiting[year] = recruiting[year].str.replace('Miami-OH','Miami OH')
                else:
                    if team == 'Miami':
                        recruiting[year][
                        recruiting.loc[recruiting[year] == team].index[
                                0]] = recruiting[year][
                        recruiting.loc[recruiting[year] == team].index[
                                0]].replace('Miami','Miami FL')
                    else:
                        continue
            
            elif 'ate' not in team:
                if ' St' in team:
                    recruiting[year][
                        recruiting.loc[recruiting[year] == team].index[
                                0]] = recruiting[year][
                        recruiting.loc[recruiting[year] == team].index[
                                0]].replace(' St',' State')
                
                    #also can't think of a way to incorporate the Miami issues 
                    #without lopping in Miami OH with the just Miami
            
            else:
                continue
        except TypeError:
            continue

# continue with recruiting rankings; I want to get the recruiting data in a form
# so that the columns are school and each year. The school column obviously has
# each distinct school name, and the year column has that school's ranking in 
# that year
                                
recruiting['2013'][112] = 'San Jose State'
  
                            
# create new data frame with team names, and years
rec_rank = pd.DataFrame(columns = ['Team','2018','2017','2016','2015',
                                      '2014','2013','2012','2011','2010','2009',
                                      '2008','2007','2006','2005','2004','2003',
                                      '2002'])

# import all team names into new dataframe 
rec_rank['Team'] = recruiting['2018']

#since Idaho was FCS in 2018, add them in real quick
rec_rank = rec_rank.append(pd.Series(), ignore_index=True)
rec_rank['Team'][130] = 'Idaho'

# Add recruiting rank in year for each team based on their index from the 
# recruiting data set

for index in range(len(recruiting['Rank'])):
    for team in rec_rank['Team']:
        for year in years:
            if team == recruiting[year][index]:
                rec_rank[year][rec_rank.loc[rec_rank['Team'] == team].index[
                0]] = recruiting.loc[recruiting[year] == team].index[0] + 1
            else:
                continue

#average 4-year rank
start = 2002

int_years = [x for x in np.arange(start, start + 4, 1)]


while max(int_years) < 2019:
    str_years = [str(x) for x in int_years]
    rec_rank['4year_rec_avg'+str(max(int_years))] = rec_rank[str_years].mean(axis=1)
    int_years = [x+1 for x in int_years]
    
rec_rank.to_csv('../../Data/wrangled-data/rec_rank.csv')
