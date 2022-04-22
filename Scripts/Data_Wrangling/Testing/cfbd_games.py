#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 16:52:48 2021

@author: Broth
"""


from __future__ import print_function
import time
import cfbd
import pandas as pd
import numpy as np
import pprint
from cfbd.rest import ApiException


#get api key
file = open('../../Data/key.txt')
key = file.read().replace("\n", " ")
file.close()

# Configure API key authorization: ApiKeyAuth
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = key
configuration.api_key_prefix['Authorization'] = 'Bearer'


# create an instance of the API class
games_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
#year = 56 # int | Year/season filter for games
#week = 56 # int | Week filter (optional)
#season_type = 'regular' # str | Season type filter (regular or postseason) (optional) (default to regular)
#team = 'team_example' # str | Team (optional)
#home = 'home_example' # str | Home team filter (optional)
#away = 'away_example' # str | Away team filter (optional)
#conference = 'conference_example' # str | Conference abbreviation filter (optional)
#id = 56 # int | id filter for querying a single game (optional)

games_response = games_instance.get_games(team = 'Wisconsin', year = 2020)

games_response