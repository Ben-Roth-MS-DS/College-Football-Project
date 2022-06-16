#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 16:13:17 2021

@author: Broth
"""
#!pip install cfbd

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
team_recruiting_instance = cfbd.RecruitingApi(cfbd.ApiClient(configuration))
start_year = 2013 # int | Starting year (optional)
end_year = 2021 # int | Ending year (optional)

#pull team recruiting, convert to dataframe
team_rec_response = team_recruiting_instance.get_recruiting_teams(year = 2013)
teams_df = pd.DataFrame([team_rec_response[i].to_dict() for i in range(len(team_rec_response))])




