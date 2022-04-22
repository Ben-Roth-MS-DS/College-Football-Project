#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 10:52:30 2021

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

#define list of teams instance
teams_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))

teams_response = teams_instance.get_fbs_teams()
    
teams_response[0].to_dict()

len(teams_response)



