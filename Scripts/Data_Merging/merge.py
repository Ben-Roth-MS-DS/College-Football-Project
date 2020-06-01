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
        

##  Roster changes   ##
roster_changes = pd.read_csv('../../Data/wrangled-data/roster_changes.csv', index_col = 0)

#change column name formats to match what will be in final df
roster_changes = roster_changes.rename(columns = lambda x : x.replace('-', ' '))
roster_changes = roster_changes.rename(columns = lambda x : x.title())

#find name differences between roster change columns and model_df
model_rost_diffs = np.setdiff1d(model_df.Team.unique(), roster_changes.columns, assume_unique = True)
rost_diffs = np.setdiff1d(roster_changes.columns, model_df.Team.unique(), assume_unique = True)

#create roster col dicts
rost_cols = {
        'Bowling Green State': 'Bowling Green',
        'Brigham Young': 'BYU',
        'Florida International': 'FIU',
        'Louisiana State': 'LSU',
        'Miami Fl': 'Miami FL',
        'Miami Oh': 'Miami OH',
        'Middle Tennessee State': 'Middle Tennessee',
        'Nevada Las Vegas': 'UNLV',
        'North Carolina State': 'NC State',
        'Southern Methodist': 'SMU',
        'Texas Am': 'Texas A&M',
        'Southern Mississippi': 'Southern Miss',
        'Texas Christian': 'TCU',
        'Alabama Birmingham': 'UAB',
        'Central Florida': 'UCF',
        'Ucla': 'UCLA',
        'Southern California': 'USC',
        'Texas El Paso': 'UTEP',
        'Texas San Antonio': 'UTSA',
        }

roster_changes = roster_changes.rename(columns = rost_cols)

#get roster years
ros_years = roster_changes['Year'].values
for team in roster_changes:
    if team != 'Year':
        for year in ros_years:
    
            #get roster change from past year 
            val = roster_changes[roster_changes['Year'] == year][team].iloc[0]
            
            #replace nan with value for team and year
            model_df.loc[(model_df.Team == team) & (model_df.Year == int(year)), 'Team Roster Changes'] = val
        
            #replace nan with value for team and year
            model_df.loc[(model_df.Opponent == team) & (model_df.Year == year), 'Opponent Roster Changes'] = val
            
    else:
        continue
        

     

