#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:23:19 2022

@author: Broth
"""
import cfbd
import functools
import pandas as pd
import numpy as np
import cfbd_stats
import cfbd_recruits
import time

#get api key
file = open('../../Data/key.txt')
key = file.read().replace("\n", " ")
file.close()

# Configure API key authorization: ApiKeyAuth
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = key
configuration.api_key_prefix['Authorization'] = 'Bearer'

games_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))

#list of regular season games
games_response = games_instance.get_games(year = year, team = team)

#list of postseason games
postseason_response = games_instance.get_games(year = year, team = team, season_type = 'postseason')

#convert to list of dictionaries
games_list = [games_response[i].to_dict() for i in range(len(games_response))]
postseason_list = [postseason_response[i].to_dict() for i in range(len(postseason_response))]

#convert to dataframe
games_df = pd.DataFrame(games_list)
postseason_df = pd.DataFrame(postseason_list)

#combine to single df
games_df = pd.concat([games_df, postseason_df], axis = 0)

#create postseason flag 
games_df.loc[games_df.season_type == 'postseason', 'postseason_flag'] = 1
games_df.postseason_flag.fillna(0, inplace = True)



#keep columns of interest
games_df = games_df[['id', 'season', 'week', 'start_time_tbd', 'neutral_site','postseason_flag',
                     'conference_game', 'home_team', 'home_conference', 'home_points',
                     'home_line_scores', 'home_pregame_elo', 'away_team', 'away_conference', 
                     'away_points', 'away_line_scores', 'away_pregame_elo']]

def teamify(df, team):
    '''
    Purpose
        -  Function converts dataframe with home/away values to team/opponent values
        
    Inputs
        - df (DataFrame): Dataframe containing cfbd game data
        - team (str): Team of interest
                                  
    Outputs
        - team_games(pd.DataFrame): Dataframe at the game_id level that contains 
    '''
    #split into home/away dataframes
    home = df.loc[df.home_team == team, :]
    away = df.loc[df.away_team == team, :]
    
    #rename home/away columns to team/opponent
    home.columns = [home_col.replace('home', 'team') for home_col in home.columns]
    home.columns = [away_col.replace('away', 'opponent') for away_col in home.columns]
    
    #rename away/home columns to team/opponent
    away.columns = [home_col.replace('home', 'opponent') for home_col in away.columns]
    away.columns = [away_col.replace('away', 'team') for away_col in away.columns]
    
    #combine to single dataframe
    team_games = pd.concat([home, away], axis = 0).sort_values(['id'])
    
    return(team_games.drop_duplicates(subset = 'id'))
    
teamify_df = teamify(games_df, 'Arizona State')

teamify_df.team_line_scores.to_list()





