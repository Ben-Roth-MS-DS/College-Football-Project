#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 15:48:34 2022

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


api_instance = cfbd.RatingsApi(cfbd.ApiClient(configuration))
year = 56 # int | Season filter (required if team not specified) (optional)
team = 'team_example' # str | Team filter (required if year not specified) (optional)
conference = 'conference_example' # str | Conference filter (optional)

api_response = api_instance.get_srs_ratings(year = 2020)
 
api_response[0]   

api_response


