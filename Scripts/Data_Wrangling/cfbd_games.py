#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:23:19 2022

@author: Broth
"""
import pandas as pd

def teamify(df, team):
    '''
    Purpose
        -  Function converts dataframe with home/away values to team/opp values
        
    Inputs
        - df (DataFrame): Dataframe containing cfbd game data
        - team (str): Team of interest
                                  
    Outputs
        - team_games(pd.DataFrame): Dataframe at the game_id level that contains 
    '''
    #split into home/away dataframes
    home = df.loc[df.home_team == team, :]
    away = df.loc[df.away_team == team, :]
    
    #rename home/away columns to team/opp
    home.columns = [home_col.replace('home', 'team') for home_col in home.columns]
    home.columns = [away_col.replace('away', 'opp') for away_col in home.columns]
    
    #rename away/home columns to team/opp
    away.columns = [home_col.replace('home', 'opp') for home_col in away.columns]
    away.columns = [away_col.replace('away', 'team') for away_col in away.columns]
    
    #combine to single dataframe
    team_games = pd.concat([home, away], axis = 0).sort_values(['id'])
    
    return(team_games.drop_duplicates(subset = 'id'))


def rolling_games(df,
                  stats = ['team_points', 'team_pregame_elo', 'team_q1_score', 'team_q2_score',
                         'team_q3_score', 'team_q4_score', 'opp_points', 'opp_pregame_elo', 
                         'opp_q1_score', 'opp_q2_score', 'opp_q3_score', 'opp_q4_score'],
                  rolling_numbers = [3, 6, 12]):
     
    '''
    Purpose
        - Function that counts and calculates rolling occurances games
          
    Inputs
        - df (pd.DataFrame): Dataframe at the team-game level
        - stat (str): Stat (e.g. team_points) that is to be rolled up
        - rolling_numbers (list): List of numbers that defines the number of 
                                  previous game averages wished to be calculated
                                  
    Outputs
        - df_game_team(pd.DataFrame): Dataframe at the team_game_id level that contains
                                      rolled up stats

    '''
    #sort by game id
    df = df.sort_values('id').reset_index(drop = True)
    
    #create rolling averages
    rolling_team_list = [df[stats].\
                           rolling(window, 1).\
                           mean().\
                           reset_index(drop = True).\
                           rename(columns = {column:column+'_' + str(window) + '_game_avg' for column in stats})
                        for window in rolling_numbers]
        
    #flatten to dataframe
    rolling_team_df = pd.concat(rolling_team_list, axis = 1).reset_index(drop = True)
        
    #combine to main df    
    df_game_team = pd.concat([df, rolling_team_df], axis = 1)
    
    return(df_game_team)


#create function to flatten quarter scores
def line_fixer(x):
    '''
    Purpose
        - This function intakes a list of scores either for 4 quarters or 
          4 quarters + n OT periods and outputs a list of 4 quarter scores,
          the total number of points scored after quarter 4, and a flag denoting
          whether there was overtime
          
    Input
        - x (list): List of scores by period 
        
    Output
        - fixed (list): List of scores by quarter, total OT points, and OT flag
    
    '''
    if len(x) > 4:
        fixed = x[:4] + [sum(x[4:])] + [1]
        return(fixed)
        
    else:
        #fill with zeros if rained out game
        while len(x) < 4:
            x.append(0)
        
        fixed = x + [0] + [0]
        return(fixed)
    
    
    
    

#define final function
def all_games(df,
              team,
              stats = ['team_points', 'team_pregame_elo', 'ot_flag', 'team_q1_score', 'team_q2_score',
                       'team_q3_score', 'team_q4_score', 'team_ot_score' 'opp_points', 'opp_pregame_elo', 
                       'opp_q1_score', 'opp_q2_score', 'opp_q3_score', 'opp_q4_score', 'opp_ot_score'],
              rolling_numbers = [3, 6, 12]):
    '''
    
    '''
    #teamify dataframe
    teamify_df = teamify(df = df,
                         team = team)
    
    #run fixer column on lines
    teamify_df.team_line_scores = teamify_df.team_line_scores.apply(lambda x: line_fixer(x))
    teamify_df.opp_line_scores = teamify_df.opp_line_scores.apply(lambda x: line_fixer(x))    
    
    
    teamify_df[['team_q1_score', 'team_q2_score', 'team_q3_score', 'team_q4_score', 'team_ot_score', 'ot_flag']] = teamify_df.team_line_scores.to_list()
    teamify_df[['opp_q1_score', 'opp_q2_score', 'opp_q3_score', 'opp_q4_score', 'opp_ot_score', 'ot_flag']] = teamify_df.opp_line_scores.to_list()

    #drop quarter score list columns
    teamify_df.drop(['team_line_scores', 'opp_line_scores'], axis = 1, inplace = True)
    
    #run rolling aggregates on function
    df_game_team = rolling_games(df = teamify_df)
    
    return(df_game_team)
    
    
