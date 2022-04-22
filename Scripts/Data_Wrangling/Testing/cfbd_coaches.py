#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 17:11:39 2022

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
api_instance = cfbd.CoachesApi(cfbd.ApiClient(configuration))
first_name = 'first_name_example' # str | First name filter (optional)
last_name = 'last_name_example' # str | Last name filter (optional)
team = 'team_example' # str | Team name filter (optional)
year = 56 # int | Year filter (optional)
min_year = 56 # int | Minimum year filter (inclusive) (optional)
max_year = 56 # int | Maximum year filter (inclusive) (optional)

api_response = api_instance.get_coaches(year = 2020)

api_response