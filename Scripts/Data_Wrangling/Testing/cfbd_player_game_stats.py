#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 16:59:53 2021

@author: Broth
"""


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
pgs_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
year = 56 # int | Year/season filter for games
week = 56 # int | Week filter (optional)
season_type = 'regular' # str | Season type filter (regular or postseason) (optional) (default to regular)
team = 'team_example' # str | Team filter (optional)
conference = 'conference_example' # str | Conference abbreviation filter (optional)
category = 'category_example' # str | Category filter (e.g defensive) (optional)
game_id = 56 # int | Game id filter (optional)

pgs_response = pgs_instance.get_player_game_stats(year = 2019, team = 'Wisconsin')

type(pgs_response[0])

pd.DataFrame.from_records(pgs_response[0].to_dict())
