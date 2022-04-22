#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 15:04:21 2021

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
api_instance = cfbd.DrivesApi(cfbd.ApiClient(configuration))
year = 56 # int | Year filter
season_type = 'regular' # str | Season type filter (optional) (default to regular)
week = 56 # int | Week filter (optional)
team = 'team_example' # str | Team filter (optional)
offense = 'offense_example' # str | Offensive team filter (optional)
defense = 'defense_example' # str | Defensive team filter (optional)
conference = 'conference_example' # str | Conference filter (optional)
offense_conference = 'offense_conference_example' # str | Offensive conference filter (optional)
defense_conference = 'defense_conference_example' # str | Defensive conference filter (optional)

api_response = api_instance.get_drives(year = 2021, team = 'Wisconsin')

pd.DataFrame.from_dict(api_response[0].to_dict())






