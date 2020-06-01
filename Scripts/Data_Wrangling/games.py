#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 19:14:00 2019

@author: Broth
"""
import pandas as pd
import numpy as np
from recruiting_ranks import clean_cruits

#turn off warning
pd.options.mode.chained_assignment = None 

#load in relevant df
games = pd.read_csv('../../Data/csv-data/cfb_games_2011-18.csv')


#copy df
cfb_win = games.copy()

#drop irrelevent variables
cfb_win = cfb_win.drop(['Game','Count','Field25','TOP VERIFICATION', 'O/U Total'], axis = 1)

#look at unique team names in cfb_win to see which ones we'll have to change
uniq_cfb = []
uniq_cfb.append(list(cfb_win['Winning'].unique()))


# go through similar process with the recruiting df; compile list of wrongly 
# spelled names, list of correctly spelled names, and columns where those names are
old_win = ['C. Michigan', 'E. Michigan','FAU', 'La. Tech','La.-Lafayette',
           'La.-Monroe','La.Tech','MTSU','Miami, FL','Miami, OH','N.C. State',
           'S. Alabama','Southern Cal','Texs Tech','Vanderbilit','W. Kentucky',
           'W. Michigan','N. Illinois']

new_win = ['Central Michigan','Eastern Michigan','Florida Atlantic','Louisiana Tech',
           'Louisiana Lafayette','Louisiana Monroe','Louisiana Tech',
           'Middle Tennessee','Miami FL','Miami OH','NC State','South Alabama',
           'USC','Texas Tech','Vanderbilt','Western Kentucky','Western Michigan',
           'Northern Illinois']
            


win_columns = ['Winning','Losing']

#apply function to new lists
cfb_win = clean_cruits(wrong_list = old_win, right_list = new_win,
             df = cfb_win, columns = win_columns)


#select columns of interest
games = cfb_win[['Year', 'Week', 'Winning','Losing', 'Winning H/A/N', 'Losing H/A/N', 'Winning Conference', 
                   'Losing Conference','Winning YPPA','Losing YPPA','Winning YPRA',
                   'Losing YPRA', 'Winning TOP', 'Losing TOP', 'Winning TO', 'Losing TO', 'Winning Points', 
                   'Losing Points','Winning Pen Yards','Losing Pen Yards']]


   
games = games.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

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

games = games.replace({'Massachussets':'Massachusetts',
                             'Massachussetts': 'Massachusetts',
                            'Washignton':'Washington',
                            'Virgina Tech': 'Virginia Tech',
                            'Northwesern': 'Northwestern',
                            'Miami, Ohio': 'Miami OH',
                            'Coloardo State': 'Colorado State'})

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

### Note: there are duplicated in the data, but I am not sure how to fix this issue yet


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



#replace invalid value with 0

final_df[['Team YPPA', 'Opponent YPPA']]= final_df[['Team YPPA', 'Opponent YPPA']].replace('#DIV/0!', '0').astype(float)
final_df = final_df.drop(columns = ['Opponent H/A/N'], axis = 1)
        
#replace string values with additional week number, convert to integers
final_df['Week'] = final_df['Week'].replace('BOWL', '17') \
                                   .replace('Bowl', '17') \
                                   .replace('CFP', '17') \
                                   .replace('CFPCG', '18') \
                                   .replace('CFP Champ', '18') \
                                   .astype(int)



#convert to int
final_df['Win'] = final_df['Win'].astype(int)

#strip white space     
final_df = final_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    

#order team games
final_df = final_df.sort_values(['Team','Year', 'Week']).reset_index(drop = True)

#Create team winning percentage past 10 games 
final_df['Team Past 10 Winning Pct'] = final_df.groupby('Team')['Win'].\
                                                 rolling(10, min_periods = 0).\
                                                 mean().\
                                                 round(4).\
                                                 reset_index(drop = True)
                                                 

#order opponent games
final_df = final_df.sort_values(['Opponent','Year', 'Week']).reset_index(drop = True)

#Create opponent winning percentage past 10 games 
final_df['Opponent Past 10 Winning Pct'] = final_df.groupby('Opponent')['Win'].\
                                                    rolling(10, min_periods = 0).\
                                                    mean().\
                                                    round(4).\
                                                    reset_index(drop = True) 
                                                
#subtract 1 from Winning Pct to repressent Opponent Winning pct
final_df['Opponent Past 10 Winning Pct'] = 1 - final_df['Opponent Past 10 Winning Pct']                                          
                                                 
#list of columns to not aggregate
no_cols = ['Team', 'Year', 'Week', 'Win', 'Team H/A/N', 'Opponent', 'Team Conference', 
           'Opponent Conference', 'Team Past 10 Winning Pct', 'Opponent Past 10 Winning Pct']


#list of columns to aggregate
avg_cols = [col for col in final_df.columns if col not in no_cols]

for col in avg_cols:
    #average for team over previous 8 games
    if 'Team' in col:
        #order so that rolling works
        final_df = final_df.sort_values(['Team','Year', 'Week']).reset_index(drop = True)
        final_df[col + ' 8 Game Avg'] = final_df.groupby('Team')[col].\
                                                 rolling(8, min_periods = 0).\
                                                 mean().\
                                                 reset_index(drop = True)
                                                 
    elif 'Opponent' in col:
        final_df = final_df.sort_values(['Opponent','Year', 'Week']).reset_index(drop = True)
        final_df[col + ' 8 Game Avg'] = final_df.groupby('Opponent')[col].\
                                                 rolling(8, min_periods = 0).\
                                                 mean().\
                                                 reset_index(drop = True)

#rolling average columns                                               
rolled_cols = [col for col in final_df if '8 Game Avg' in col]

#final columns of interest
final_cols = no_cols + ['Team Past 10 Winning Pct', 'Opponent Past 10 Winning Pct'] + rolled_cols

final_df = final_df[final_cols]

#safe df            
final_df.to_csv('../../Data/wrangled-data/cfb_win.csv')
         
    
