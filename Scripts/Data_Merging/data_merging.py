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

games.Winning = games.Winning.str.strip()
games.Losing = games.Losing.str.strip()

old_names = ['La. Lafayette', 'Massachussetts', 'Coloardo State', 'Miami, Ohio',
             'Northwesern', 'Virgina Tech', 'Washignton', 'Massachussets']

new_names = ['Louisiana Lafayette', 'Massachusetts', 'Colorado State', 'Miami OH',
             'Northwestern', 'Virginia Tech', 'Washington', 'Massachusetts']

for i in range(len(old_names)):
    #set values
    old = old_names[i]
    new = new_names[i]

    games.loc[games.Winning == old, 'Winning'] = new
    games.loc[games.Losing == old, 'Losing'] = new

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

team_cols = ['Team YPPA', 'Team YPRA', 'Team TOP', 'Team TO', 'Team Points', 'Team Pen Yards', 'Team Conference']

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

#remove flag column
time_df.drop('Flag', axis = 1, inplace = True)

#merge back into main dataframes
team_df = pd.merge(team_df, time_df, on = ['Year', 'Week'], how = 'left')
opp_df = pd.merge(opp_df, time_df, on = ['Year', 'Week'], how = 'left')

#ensure date type 
team_df.syn_date = pd.to_datetime(team_df.syn_date).dt.date
opp_df.syn_date = pd.to_datetime(opp_df.syn_date).dt.date

#change duplicate dates
idx_team = team_df[team_df.groupby(['Team', 'Week', 'Year']).cumcount() > 0].index
idx_opp = opp_df[opp_df.groupby(['Opponent', 'Week', 'Year']).cumcount() > 0].index

team_df.loc[idx_team, 'syn_date'] = team_df.syn_date + datetime.timedelta(days = 3)
opp_df.loc[idx_opp, 'syn_date'] = opp_df.syn_date + datetime.timedelta(days = 3)

#define rolling functions
def rolling_lagging_group_by(dataframe, group, columns, window, index, min_roll_period = 2,  lag_period = 1):
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
    dataframe =  dataframe.set_index(index)
    
  
    #create new column
    new_columns = {column: column + '_' + str(window) + '_game_average' for column in columns}
        
    #rolling average, reset index
    grouped_dataframe = dataframe\
                             .groupby(group)[columns]\
                             .rolling(min_periods = min_roll_period, window = window).mean()\
                             .reset_index()
    
    #rename columns
    grouped_dataframe.rename(new_columns, axis = 1, inplace = True)
    
    return(grouped_dataframe)
                             
        
## create group data frame for avg quarter season, half season and full season= ##

#set agg columns
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

#rename win columns, convert to numeric the get win pct last n games
team_df.rename({'Win':'Team Win'}, inplace = True, axis = 1)
team_df['Team Win'] = team_df['Team Win'].astype(int)

opp_df.rename({'Win':'Opp Win'}, inplace = True, axis = 1)
opp_df['Opp Win'] = opp_df['Opp Win'].astype(int)

team_columns = [column for column in team_df.select_dtypes(include=numerics).columns if ' ' in column]
opp_columns = [column for column in opp_df.select_dtypes(include=numerics).columns if ' ' in column] 

#ensure columns are proper datatype
team_df[team_columns] = team_df[team_columns].apply(pd.to_numeric, errors='coerce')
opp_df[opp_columns] = opp_df[opp_columns].apply(pd.to_numeric, errors='coerce')

#3 games team df
grouped_team_3 = rolling_lagging_group_by(dataframe = team_df, 
                                          group = 'Team',
                                          columns = team_columns,
                                          window = 3, 
                                          index = 'syn_date')

#6 games team df
grouped_team_6 = rolling_lagging_group_by(dataframe = team_df, 
                                          group = 'Team',
                                          columns = team_columns,
                                          window = 6, 
                                          index = 'syn_date')

#12 games team df
grouped_team_12 = rolling_lagging_group_by(dataframe = team_df, 
                                          group = 'Team',
                                          columns = team_columns,
                                          window = 12, 
                                          index = 'syn_date')

#3 games opp df
grouped_opp_3 = rolling_lagging_group_by(dataframe = opp_df, 
                                         group = 'Opponent',
                                         columns = opp_columns,
                                         window = 3, 
                                         index = 'syn_date')

#6 games opp df
grouped_opp_6 = rolling_lagging_group_by(dataframe = opp_df, 
                                         group = 'Opponent',
                                         columns = opp_columns,
                                         window = 6, 
                                         index = 'syn_date')

#12 games opp df
grouped_opp_12 = rolling_lagging_group_by(dataframe = opp_df, 
                                         group = 'Opponent',
                                         columns = opp_columns,
                                         window = 12, 
                                         index = 'syn_date')


#join in single dataframes
team_grouped = pd.merge(grouped_team_3, 
                        grouped_team_6, 
                        on = ['Team', 'syn_date'], how = 'left')
team_grouped = pd.merge(team_grouped, 
                        grouped_team_12, 
                        on = ['Team', 'syn_date'], how = 'left')

opp_grouped = pd.merge(grouped_opp_3, 
                       grouped_opp_6, 
                       on = ['Opponent', 'syn_date'], 
                       how = 'left')
opp_grouped = pd.merge(opp_grouped, 
                       grouped_opp_12, 
                       on = ['Opponent', 'syn_date'],
                       how = 'left')

### work with other dataframes ### 

#convert coaches from wide to long
coaches_long = pd.melt(coaches, id_vars='FBS Team', 
                       value_name='coach_change', 
                       var_name = 'year')

#convert rosters from wide to long
rosters_long = pd.melt(rosters, 
                       id_vars='Year', 
                       value_name='roster change amount', 
                       var_name = 'Team')

#clean up expenses columns
expenses.drop(labels = ['IPEDS ID', 'NCAA Subdivision', 'FBS Conference'],
              axis = 1,
              inplace = True)

#join coaches into 

#create base dataset to merge everything into 
base = team_df[['Team', 'Opponent', 'syn_date', 'Year', 'Team Win', 'Team Earned Conference', 'Team Allowed Conference']]
base.rename({'Team Earned Conference':'Team Conference', 'Team Allowed Conference':'Opponent Conference'}, axis = 1, inplace = True)

base = pd.merge(base, team_grouped, on =  ['Team', 'syn_date'], how = 'left')
base = pd.merge(base, opp_grouped, on = ['Opponent', 'syn_date'], how = 'left')

#create team and oppoent coaches dataframe, merge into 
coaches_team = coaches_long.rename(columns = {'FBS Team':'Team', 'year':'Year', 'coach_change':'Team Coach Change'})
coaches_opp = coaches_long.rename(columns = {'FBS Team':'Opponent', 'year':'Year', 'coach_change':'Opp Coach_Change'})

base = pd.merge(base, coaches_team, on = ['Team', 'Year'], how = 'left')
base = pd.merge(base, coaches_opp, on = ['Opponent', 'Year'], how = 'left')

#fix rosters-team names
rosters_long.Team = rosters_long.Team.str.replace('-', ' ')
rosters_long.Team = rosters_long.Team.str.title()

#replace mismatching names
old_ros = ['Brigham Young', 'Bowling Green State', 'Florida International',
           'Louisiana State', 'Miami Fl', 'Miami Oh', 'Middle Tennessee State',
           'Southern Methodist', 'Southern Mississippi', 'Texas Christian', 'Texas Am',
           'Ucla', 'Nevada Las Vegas', 'Southern California', 'North Carolina State',
           'Alabama Birmingham', 'Central Florida', 'Texas El Paso', 'Texas San Antonio',
           'Florida']

new_ros = ['BYU', 'Bowling Green', 'FIU', 'LSU', 'Miami FL', 'Miami OH',
           'Middle Tennessee', 'SMU', 'Southern Miss' , 'TCU', 'Texas A&M', 'UCLA',
           'UNLV', 'USC', 'NC State', 'UAB',  'UCF', 'UTEP', 'UTSA', 'Florida']


for i in range(len(old_ros)):
    old = old_ros[i]
    new = new_ros[i]
    
    rosters_long.loc[rosters_long.Team == old, 'Team'] = new

#title columns 
rosters_long.columns = rosters_long.columns.str.title()

#join
base = pd.merge(base, 
                rosters_long.rename({'Roster Change Amount':'Team Roster Change Amount'}, axis = 1),
                on = ['Team', 'Year'],
                how = 'left')

base = pd.merge(base, 
                rosters_long.rename({'Roster Change Amount':'Opp Roster Change Amount', 'Team':'Opponent'}, axis = 1),
                on = ['Opponent', 'Year'],
                how = 'left')


# expenses, rename columns
expenses.rename({'Data':'Team'}, axis = 1, inplace = True)

#specify types
base.Team = base.Team.astype(str)
expenses.Team = expenses.Team.astype(str)

#rename expense columns
old_exp = ['Miami', 'Ole Miss', 'NIU', 'UNC', 'Pennsylvania State', 'Central Florida', 'Massachusetts']
new_exp = ['Miami OH', 'Mississippi', 'Northern Illinois', 'North Carolina', 
           'Penn State', 'UCF', 'Massachussetts']

for i in range(len(old_exp)):
    #set values
    old = old_exp[i]
    new = new_exp[i]
    
    expenses.loc[expenses.Team == old, 'Team'] = new

# join
team_dict = {col:'Team ' + col for col in expenses.columns if col != 'Year' and col != 'Team'}
base = pd.merge(base,
                expenses.rename(team_dict, axis = 1),
                left_on = ['Team', 'Year'],
                right_on = ['Team', 'Year'],
                how = 'left')


opp_dict = {col:'Opp ' + col for col in expenses.columns if col != 'Year' and col != 'Team'}
opp_dict = {**opp_dict, **{'Team':'Opponent'}}

base = pd.merge(base,
                expenses.rename(opp_dict, axis = 1),
                on = ['Opponent', 'Year'],
                how = 'left'
                )

#replace weird conference values
old_conf = ['Big12', 'independent']
new_conf = ['Big 12', 'Independent']

for i in range(len(old_conf)):
    #get vals
    old = old_conf[i]
    new = new_conf[i]
    
    #replace team and opp
    base.loc[base['Team Conference'] == old, 'Team Conference'] = new
    base.loc[base['Opponent Conference'] == old, 'Opponent Conference'] = new


#save
base.to_csv('./Data/model-data/model_data.csv', index = True)
