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

exp_diffs = np.setdiff1d(expenses['Team'].unique(), games['Team'].unique(), assume_unique = True)

#get rid of scientific notation in numeric columns
cols = [col for col in expenses.columns if col not in ['Team', 'Year']]

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

## Coaches Merge ##
coaches = pd.read_csv('../../Data/wrangled-data/clean_coaches.csv', index_col = 0)


coach_years = [col for col in coaches.columns if col not in ['FBS Team']]

#fill coach change
for year in coach_years:
    for team in coaches['FBS Team'].values:
        #find 1 or 0 for new coach or not
        val = coaches[(coaches['FBS Team'] == team)][year].iloc[0]
        
        #replace nan with value for team and year
        model_df.loc[(model_df.Team == team) & (model_df.Year == int(year)), 'Team Same Coach'] = val
        
        #replace nan with value for opponent and year
        model_df.loc[(model_df.Opponent == team) & (model_df.Year == int(year)), 'Opponent Same Coach'] = val
        
        
        
## Recruiting Ranks ##
recruiting = pd.read_csv('../../Data/wrangled-data/rec_rank.csv', index_col = 0)

#use same technique as coaching changes to fill in recruiting ranks
rec_years = [col for col in recruiting.columns if col[:1] == '4' and int(col[-4:]) < max(model_df['Year'])]

col = 'Recruiting Rank Avg Past 4 Years'

#fill recruiting rank
for year in rec_years:
    for team in recruiting['Team'].values:
        #find 1 or 0 for new coach or not
        val = recruiting[(recruiting['Team'] == team)][year].iloc[0]
        
        #replace nan with value for team and year
        model_df.loc[(model_df.Team == team) & (model_df.Year == int(year[-4:]) + 1), 'Team ' + col] = val
        
        #replace nan with value for team and year
        model_df.loc[(model_df.Opponent == team) & (model_df.Year == int(year[-4:]) + 1), 'Opponent ' + col] = val
        
     

