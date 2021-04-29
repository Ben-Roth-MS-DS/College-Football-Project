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

#fill recruiting rank
col = 'Recruiting Rank Avg Past 4 Years'
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

#rename columns to match what is in final dataset
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
        
    
#create dict to make uniform conference names
conf_dict = {
        'Big 10': 'Big Ten',
        'independent': 'Ind.',
        'Independent': 'Ind.',
        'Big12':'Big 12'
        }

#use dict to change conference values
for wrong,right in conf_dict.items():
    model_df.loc[model_df['Team Conference'] == wrong, 'Team Conference'] = right
    model_df.loc[model_df['Opponent Conference'] == wrong, 'Opponent Conference'] = right

#### remove conferences that no longer exist, replace that value with team's next conference ####

#set max year
max_year = max(model_df.Year.values)

#list of 'modern' conferences
recent_conf = model_df[model_df['Year'] == max_year]['Team Conference'].unique()

#data frame of incorrect team/values
still_wrong = model_df.loc[~model_df['Team Conference'].isin(recent_conf), ['Team', 'Year']] .\
                       drop_duplicates()
                       
#sort value so take most recent year (meaning the following year will be 'right')
still_wrong = still_wrong.sort_values('Year', ascending = False)

                       
#go through each unique team/conference/year where conference is wrong
while len(still_wrong) > 0 :
    for team, year in still_wrong.itertuples(index = False):
        #take next years conference
        new_val = model_df.loc[(model_df['Team'] == team) & (model_df['Year'] == year + 1), 'Team Conference'].\
                           values[0]
        
        #replace 'wrong' conference with 'right' conference 
        model_df.loc[(model_df['Team'] == team) & (model_df['Year'] == year), 'Team Conference'] = new_val
        model_df.loc[(model_df['Opponent'] == team) &  (model_df['Year'] == year), 'Opponent Conference'] = new_val

        #reset still wrong variable so won't contain most recent fix
        #data frame of incorrect team/values
        still_wrong = model_df.loc[~model_df['Team Conference'].isin(recent_conf), ['Team', 'Team Conference', 'Year']] .\
                               drop_duplicates()
        still_wrong = still_wrong.sort_values('Year', ascending = False)
    
#save final df
model_df.to_csv('../../Data/model-data/model_data.csv')
