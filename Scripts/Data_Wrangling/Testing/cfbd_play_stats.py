#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 16:53:09 2022

@author: Broth
"""
import cfbd
import pandas as pd
import numpy as np


#get api key
file = open('../../Data/key.txt')
key = file.read().replace("\n", " ")
file.close()

# Configure API key authorization: ApiKeyAuth
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = key
configuration.api_key_prefix['Authorization'] = 'Bearer'



# create an instance of the API class
api_instance = cfbd.PlaysApi(cfbd.ApiClient(configuration))
year = 56 # int | Year filter (optional)
week = 56 # int | Week filter (optional)
team = 'team_example' # str | Team filter (optional)
game_id = 56 # int | gameId filter (from /games endpoint) (optional)
athlete_id = 56 # int | athleteId filter (from /roster endpoint) (optional)
stat_type_id = 56 # int | statTypeId filter (from /play/stat/types endpoint) (optional)
season_type = 'season_type_example' # str | regular, postseason, or both (optional)
conference = 'conference_example' # str | conference abbreviation filter (optional)

api_response = api_instance.get_play_stats(year = 2020, team = 'Wisconsin')

api_response[0]

tst = pd.DataFrame.from_records([api_response[0].to_dict()])