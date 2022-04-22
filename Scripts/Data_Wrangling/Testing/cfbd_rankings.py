#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 16:03:42 2021

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
api_instance = cfbd.RankingsApi(cfbd.ApiClient(configuration))
year = 56 # int | Year/season filter for games
week = 56 # int | Week filter (optional)
season_type = 'regular' # str | Season type filter (regular or postseason) (optional) (default to regular)

api_response = api_instance.get_rankings(year = 2020)

api_response[0]