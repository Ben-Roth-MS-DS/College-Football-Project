#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 15:50:58 2021

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
api_instance = cfbd.ConferencesApi(cfbd.ApiClient(configuration))

api_response = api_instance.get_conferences()
