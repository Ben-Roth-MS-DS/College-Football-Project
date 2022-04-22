#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 15:32:27 2022

@author: Broth
"""
import cfbd
import functools
import pandas as pd
import numpy as np
import cfbd_stats

#get api key
file = open('../../Data/key.txt')
key = file.read().replace("\n", " ")
file.close()

# Configure API key authorization: ApiKeyAuth
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = key
configuration.api_key_prefix['Authorization'] = 'Bearer'

#recruting ranks API to get range 
team_recruiting_instance = cfbd.RecruitingApi(cfbd.ApiClient(configuration))
team_rec_response = team_recruiting_instance.get_recruiting_teams()
team_rec_df = pd.DataFrame(team_rec_response[i].to_dict() for i in range(len(team_rec_response)))

#define years based on min available years in plays api
years = [year for year in range(min(team_rec_df.year), max(team_rec_df.year) + 1) if year >= 2013]

#get list of teams
teams_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))

#get teams
teams_response = teams_instance.get_teams()
    
#get teams by year
teams_dict = [teams_response[i].to_dict() for i in range(len(teams_response))]

#remove nested dict
teams_dict2 = [{k: v for k, v in teams_dict[i].items() if k != 'location'} for i in range(len(teams_dict))]

#convert dicts to dfs
teams_df = pd.DataFrame(teams_dict2)

#drop duplicates
teams_df = teams_df.drop_duplicates(subset = ['school'])

team_stats = [cfbd_stats.stats_function(team, years) for team in teams_df.school.values]
    
### get list of teams/years
### run on everything
### get recruiting
### aggregate recruiting
### see if can figure out games_advanced_response

games_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))

games_response = games_instance.get_games(year = year, team = team)

games_list = [games_response[i].to_dict() for i in range(len(games_response))]

games_df = pd.DataFrame.from_records(games_list)


games_advanced_response = games_instance.get_advanced_box_score(game_id = int(games_df['id'][5]))


game_ids = play_stats_df.game_id.unique()