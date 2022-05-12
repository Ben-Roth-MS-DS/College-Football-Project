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
import cfbd_games
import time

#get api key
file = open('../../Data/key.txt')
key = file.read().replace("\n", " ")
file.close()

# Configure API key authorization: ApiKeyAuth
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = key
configuration.api_key_prefix['Authorization'] = 'Bearer'

############
### Prep ###
############

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

#############
### Stats ###
#############

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

##################
### Recruiting ###
##################

#create recruiting dataframe
recruiting_df = pd.DataFrame([team_rec_response[i].to_dict() for i in range(len(team_rec_response))])

#only keep schools in fbs
recruiting_df = recruiting_df.loc[recruiting_df.team.isin(teams_df.school.values), :]

#run recruiting averages function
recruiting_df_list = [cfbd_recruits.recruiting_rolled(df = recruiting_df, team = team) 
                     for team in recruiting_df.team.unique()]

#concat list
recruiting_df_fin = pd.concat(recruiting_df_list)

############################
### Returning Production ###
############################

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



##################
### Games Info ###
##################

games_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))

#lists of regular season games
games_responses = [games_instance.get_games(year = year) for year in years]

#lists of postseason games
postseason_responses = [games_instance.get_games(year = year, season_type = 'postseason') for year in years]


#convert to lists of dictionaries
games_lists = [[games_response[i].to_dict() for i in range(len(games_response))] for games_response in games_responses]
postseason_lists = [[postseason_response[i].to_dict() for i in range(len(postseason_response))] for postseason_response in postseason_responses]


#convert to list of dataframes
games_dfs = [pd.DataFrame(games_list) for games_list in games_lists]
postseason_dfs = [pd.DataFrame(postseason_list) for postseason_list in postseason_lists]

#flatten list of dataframes to single dataframe
games_df = pd.concat(games_dfs)
postseason_df = pd.concat(postseason_dfs)

#combine to single df
games_final_df = pd.concat([games_df, postseason_df], axis = 0).sort_values('id').reset_index(drop = True)

#create postseason flag 
games_final_df.loc[games_final_df.season_type == 'postseason', 'postseason_flag'] = 1
games_final_df.postseason_flag.fillna(0, inplace = True)


#keep columns of interest
games_final_df = games_final_df[['id', 'season', 'week', 'start_date', 'neutral_site','postseason_flag',
                                 'conference_game', 'home_team', 'home_conference', 'home_points',
                                 'home_line_scores', 'home_pregame_elo', 'away_team', 'away_conference', 
                                 'away_points', 'away_line_scores', 'away_pregame_elo']]

#run games rolling averages
games_rolled_dfs = [cfbd_games.all_games(df = games_final_df, team = team) for team in recruiting_df.team.unique()]

#flatten list of dataframes to single dataframe
games_rolled_df = pd.concat(games_rolled_dfs)


### Final Joins

#rename team_team and opp_team columns
games_rolled_df.rename(columns = {'team_team':'team', 'opp_team': 'opp'}, inplace = True)

#join frames together
games_recruiting = pd.merge(left = games_rolled_df, 
                            right = recruiting_df_fin,
                            left_on = ['season', 'team'],
                            right_on = ['year', 'team'])

#remove join columns, rename points to recruiting points
games_recruiting.drop('year', axis = 1).rename(columns = {'points':'rec_points'}, inplace = True)

#join production
gr_prod = pd.merge(left = games_rolled_df,
                   right = prod_df,
                   on = ['season', 'team'])

#drop unnecessary columns
gr_prod.drop(columns = ['conference'], inplace = True)

#join stats data
team_final = pd.merge(left = gr_prod,
                      right = stats_df,
                      left_on = ['id', 'team'],
                      right_on = ['game_id', 'team'])


#drop game_id column
team_final.drop(columns = ['game_id'], inplace = True)


### Create table for team and opponent rolling performance
game_cols = [col for col in games_rolled_df.columns if column not in ]














