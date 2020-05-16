#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 19:29:39 2020

@author: Broth
"""

#import necessary modules
import pandas as pd
import numpy as np

#read in datasets

games = pd.read_csv('../../Data/wrangled-data/cfb_win.csv', index_col=0)
expenses = pd.read_csv('../../Data/wrangled-data/expenses.csv', index_col = 0)

## Final Expenses Transformations ##

#find name diffs
model_diffs = np.setdiff1d(games['Team'].unique(), expenses['Team'].unique(), assume_unique = True)

exp_diffs = np.setdiff1d( expenses['Team'].unique().games['Team'].unique(), assume_unique = True)

#get rid of scientific notation in numeric columns
cols = [col for col in expenses.columns if not ['Team', 'Year']]

expenses[cols] = expenses[cols].round(0)
#create expenses data to merge for opponents 
expenses_opp = expenses.copy()

#rename columns except team and year
expenses_opp.columns = ['Opponent ' + col if loc > 1 else col for loc, col in enumerate(expenses_opp.columns)]

#rename
expenses_opp = expenses_opp.rename(columns = {'Team':'Opponent'})

#merge on team
model_df = pd.merge(games, expenses, on = ['Team', 'Year'], how = 'left')

#merge on opponent
model_df = pd.merge(model_df, expenses_opp, on = ['Opponent', 'Year'], how = 'left')



