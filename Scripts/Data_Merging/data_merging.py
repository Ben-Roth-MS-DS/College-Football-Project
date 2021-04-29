#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 16:08:46 2019

@author: Broth
"""

import pandas as pd
import numpy as np
import datetime
import os
from datetime import timedelta

os.chdir(os.getcwd())

#turn off warning
pd.options.mode.chained_assignment = None 

rosters = pd.read_csv('./Data/wrangled-data/roster_changes.csv')
rosters = rosters.drop(['Unnamed: 0'], axis = 1)

coaches = pd.read_csv('./Data/wrangled-data/clean_coaches.csv')
coaches = coaches.drop(['Unnamed: 0'], axis = 1)                     

games = pd.read_csv('./Data/wrangled-data/cfb_win.csv')
games = games.drop(['Unnamed: 0'], axis = 1)

#select columns of interest
games = games[['Year', 'Week', 'Winning','Losing', 'Winning H/A/N', 'Losing H/A/N','Winning Conference', 
                   'Losing Conference','Winning YPPA','Losing YPPA','Winning YPRA',
                   'Losing YPRA', 'Winning TOP', 'Losing TOP', 'Winning TO', 'Losing TO', 'Winning Points', 
                   'Losing Points','Winning Pen Yards','Losing Pen Yards']]

recruiting = pd.read_csv('./Data/wrangled-data/rec_rank.csv')
recruiting = recruiting.drop(['Unnamed: 0'], axis = 1)

expenses = pd.read_csv('./Data/wrangled-data/expenses.csv')
expenses = expenses.drop(['Unnamed: 0'], axis = 1)

        
team_list = sorted(games['Winning'].unique())


#generate columns of interest for winning teams
win_cols = [col for col in games.columns if 'Winning' in col]
lose_cols = [col for col in games.columns if 'Losing' in col]
other_cols = ['Week', 'Year']

final_wins = other_cols + win_cols + lose_cols
final_loss = other_cols + lose_cols + win_cols


#rename win columns

#list for rename columns
new_wins1 = [word.replace('Winning', 'Team') for word in win_cols]
new_wins2 = [word.replace('Losing', 'Opponent') for word in lose_cols]
new_wins = other_cols + new_wins1 + new_wins2

new_losses1 = [word.replace('Losing', 'Team') for word in lose_cols]
new_losses2 = [word.replace('Winning', 'Opponent') for word in win_cols]
new_losses = other_cols + new_losses1 + new_losses2

win_df = pd.DataFrame(columns = ['Team', 'Year', 'Week', 'Win'])

lose_df = pd.DataFrame(columns = ['Team', 'Year', 'Week', 'Win'])


for row in range(len(games)):
    wins = list(games[['Winning', 'Year', 'Week']].values[row])
    wins.append(1)
    win_series = pd.Series(wins, index = win_df.columns)
    win_df = win_df.append(win_series, ignore_index = True)
    
    loss = list(games[['Losing', 'Year', 'Week']].values[row])
    loss.append(0)
    loss_series = pd.Series(loss, index = lose_df.columns)
    lose_df = lose_df.append(loss_series, ignore_index = True)
    
#create winning df

#reorder columns
win_games = games[final_wins]

#rename columns
win_rename_dict = {x:y for x,y in zip(final_wins,new_wins)}
win_games.rename(columns = win_rename_dict, inplace=True)


#merge in additional data
win_df = pd.merge(win_df, win_games, left_on = ['Team', 'Year', 'Week'], right_on = ['Team', 'Year', 'Week'])     

win_df['Year'] = win_df['Year'].astype(int)
win_df = win_df.drop_duplicates()

### Note: there are duplicates in the data, but I am not sure how to fix this issue yet


#Perform same operation on losing columns

#reorder columns
lose_games = games[final_loss]

#rename columns
lose_rename_dict = {x:y for x,y in zip(final_loss, new_losses)}
lose_games.rename(columns = lose_rename_dict, inplace=True)

#merge in additional data
lose_df = pd.merge(lose_df, lose_games, left_on = ['Team', 'Year', 'Week'], right_on = ['Team', 'Year', 'Week'])     
lose_df['Year'] = lose_df['Year'].astype(int)
lose_df = lose_df.drop_duplicates()    

#append two dataframes together
final_df = win_df.append(lose_df, ignore_index = True)

#drop duplicates
final_df = final_df.drop_duplicates()

final_df['Team YPPA'] = final_df['Team YPPA'].replace('#DIV/0!', '0').astype(float)

final_df['Week'] = final_df['Week'].replace('BOWL', '17') \
                                   .replace('Bowl', '17') \
                                   .replace('CFP', '17') \
                                   .replace('CFPCG', '18') \
                                   .replace('CFP Champ', '18') \
                                   .astype(int)

final_df = final_df.sort_values(['Year', 'Week', 'Team'])

#create date value for rolling average
start_date = '-09-01'
final_df['Date_Syn'] = pd.to_datetime(final_df['Year'].apply(lambda x: datetime.datetime.strptime(str(x) + start_date, '%Y-%m-%d')) +\
                                      final_df['Week'].apply(lambda x: datetime.timedelta(days = 7 * x))).dt.date

final_df.Date_Syn = pd.DatetimeIndex(final_df.Date_Syn)

base_cols = ['Team', 'Opponent', 'Year', 'Week', 'Win']

team_cols = ['Team YPPA', 'Team YPRA', 'Team TOP', 'Team TO', 'Team Points', 'Team Pen Yards']

opp_cols = [x.replace('Team', 'Opponent') for x in team_cols]


team_df = pd.DataFrame(columns = base_cols + team_cols + opp_cols)
opp_df = pd.DataFrame(columns = base_cols + opp_cols + team_cols)


for row in range(len(final_df)):
    teams = list(final_df[team_df.columns].values[row])
    team_series = pd.Series(teams, index = team_df.columns)
    team_df = team_df.append(team_series, ignore_index = True)
    
    opps = list(final_df[opp_df.columns].values[row])
    opp_series = pd.Series(opps, index = opp_df.columns)
    opp_df = opp_df.append(opp_series, ignore_index = True)
    
# rename columns to appropriate offense and defense
new_team_columns = team_df.columns
new_team_columns = [col.replace('Opponent ', 'Team Allowed ') for col in [col2.replace('Team ', 'Team Earned ') for col2 in team_df.columns]]

new_opp_columns = opp_df.columns
new_opp_columns = [col2.replace('Team ', 'Opponent Allowed ') for col2 in [col.replace('Opponent ', 'Opponent Earned ') for col in opp_df.columns]]   

#rename columns
team_rename_dict = {x:y for x,y in zip(team_df.columns, new_team_columns)}
team_df.rename(columns = team_rename_dict, inplace=True)

opp_rename_dict = {x:y for x,y in zip(opp_df.columns, new_opp_columns)}
opp_df.rename(columns = opp_rename_dict, inplace=True)


#create date table for time series index
time_df = team_df[['Year', 'Week']].drop_duplicates().reset_index(drop = True)

#find first week by year
min_week = time_df.groupby('Year')['Week'].min().to_frame()
min_week['Flag'] = 1

#merge together, fill flag with 0 for non-min weeks
time_df = pd.merge(time_df, min_week, on = ['Year', 'Week'], how = 'left').fillna({'Flag':0})

#create start week by year
time_df.loc[time_df.Flag == 1, 'syn_date'] = '-09-01'
time_df.syn_date = pd.to_datetime(time_df.Year.astype(str) + time_df.syn_date).dt.date

# fill in the rest of dates
for i in time_df.index:
    if pd.notnull(time_df.iloc[i, 3]):
        continue
    else:
        time_df.iloc[i, 3] = time_df.iloc[i - 1, 3] + timedelta(7)

#merge back into main dataframes
team_df = pd.merge(team_df, time_df, on = ['Year', 'Week'], how = 'left')
opp_df = pd.merge(opp_df, time_df, on = ['Year', 'Week'], how = 'left')



final_df2 = team_df.join(opp_df, left_on = 'Opponent', right_on = 'Team')


def rolling_lagging_group_by(dataframe, group, columns, window, min_roll_period = 2, index, lag_period = 1):
    '''
    Function that creates rolling averages, returns dataframe with new columns
    for each column of interest
    
    Inputs
    - dataframe: dataframe of interest. must have datetime index
    - group: column where averages are grouped by. Can only be single column
    - columns: list of columns to be grouped by
    - window: number of observations to be averaged
    - min_period: minimum number of observations to be included in 
    - index: datetime index value
    - lag_period: number of previous observations by which to lag by
    
    Output
    - dataframe: dataframe with rolled columns
    '''
    #set datetime index
    dataframe =  dataframe\
                     .groupby(group)\
                     .apply(lambda x: x.set_index(index).resample('1D').first()).dropna(subset = [index])
    
    #create rolling average
    for column in columns:
        #create new column
        new_column = column + '_' + str(window) + '_game_average'
        
        #rolling average
        dataframe = dataframe.groupby([index])[column]\
                             .apply(lambda x: x.shift().rolling(min_periods = min_period,window = window).mean())\
                             .reset_index(name = new_column)    



