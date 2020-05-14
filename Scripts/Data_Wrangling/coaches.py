#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 19:14:00 2019

@author: Broth
"""

import pandas as pd
import numpy as np
from recruiting_ranks import clean_cruits

## Coaches df
coaches = pd.read_excel('../../Data/original-data/Football_Coach_Database.xlsx')

#create new df, fill in teams
clean_coaches = coaches.copy()

new_years =  np.arange(2011,2020)

#1 if same coach, 0 if old coach
for year in reversed(new_years):
    clean_coaches[year] = (clean_coaches[year] == clean_coaches[year-1]).astype('int')

#drop columns from years not in games df
clean_coaches = clean_coaches.drop([2019,2010], axis = 1)


#match school names
old_coaches = ['Central Florida', 'Florida International', 'Louisiana-Lafayette', 
               'Louisian-Monroe', 'North Carolina State', 'Northern Illinois', 'Pitt']

new_coaches = ['UCF', 'FIU', 'Louisiana Lafayette', 'Louisian Monroe', 'NC State',
               'NIU','Pittsburgh']

clean_cruits(wrong_list = old_coaches, right_list = new_coaches,
             df = clean_coaches, columns = ['FBS Team'])

clean_coaches.to_csv('../../Data/wrangled-data/clean_coaches.csv')

