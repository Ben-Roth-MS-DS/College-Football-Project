#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 15:41:08 2022

@author: Broth
"""
import time
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
api_instance = cfbd.StatsApi(cfbd.ApiClient(configuration))
year = 56 # int | Year filter (required if no team specified) (optional)
week = 56 # int | Week filter (optional)
team = 'team_example' # str | Team filter (required if no year specified) (optional)
opponent = 'opponent_example' # str | Opponent filter (optional)
exclude_garbage_time = True # bool | Filter to remove garbage time plays from calculations (optional)
season_type = 'season_type_example' # str | Season type filter (regular, postseason, or both) (optional)

api_response = api_instance.get_advanced_team_game_stats(year = 2020,
                                                         team = 'Wisconsin',
                                                         exclude_garbage_time = True)