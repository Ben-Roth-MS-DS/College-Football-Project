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

#recruting ranks API to get range 
team_recruiting_instance = cfbd.RecruitingApi(cfbd.ApiClient(configuration))
team_rec_response = team_recruiting_instance.get_recruiting_teams()
team_rec_df = pd.DataFrame(team_rec_response[i].to_dict() for i in range(len(team_rec_response)))

#define years based on min available years in plays api
years = [year for year in range(min(team_rec_df.year), max(team_rec_df.year) + 1) if year >= 2013]

#get list of teams
teams_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))

#get teams
teams_response = teams_instance.get_fbs_teams()
    
#get teams by year
teams_dict = [teams_response[i].to_dict() for i in range(len(teams_response))]

#remove nested dict
teams_dict2 = [{k: v for k, v in teams_dict[i].items() if k != 'location'} for i in range(len(teams_dict))]

#convert dicts to dfs
teams_df = pd.DataFrame(teams_dict2)

#drop duplicates
teams_df = teams_df.drop_duplicates(subset = ['school'])

#populate list of team dataframes
team_stats = []
for team in teams_df.school.values:
    if team == 'James Madison':
        continue
    else:
        team_stats.append(cfbd_stats.stats_function(team, years) )
        print(team)
        time.sleep(1 + np.random.rand())
    
#convert list of dfs to one dfs
stats_df = pd.concat(team_stats)

### Recruiting

#create recruiting dataframe
recruiting_df = pd.DataFrame([team_rec_response[i].to_dict() for i in range(len(team_rec_response))])

#only keep schools in fbs
recruiting_df = recruiting_df.loc[recruiting_df.team.isin(teams_df.school.values), :]

#run recruiting averages function
recruiting_df_list = [cfbd_recruits.recruiting_rolled(df = recruiting_df, team = team) 
                     for team in recruiting_df.team.unique()]

#concat list
recruiting_df_fin = pd.concat(recruiting_df_list)

### Returning Production

#define instance
players_instance = cfbd.PlayersApi(cfbd.ApiClient(configuration))

#get list of responses, returning production api only goes back to 2014
prod_responses = [players_instance.get_returning_production(year = year) for year in years if year > 2013]

#convert to list of dictionaries
prod_lists = [[prod_response[i].to_dict() for i in range(len(prod_response))] for prod_response in prod_responses]

#convert list of dictionaries to list of dfs
prod_dfs = [pd.DataFrame(prod_list) for prod_list in prod_lists]

#convert to single dataframe
prod_df = pd.concat(prod_dfs, axis = 0)


### Games Info





