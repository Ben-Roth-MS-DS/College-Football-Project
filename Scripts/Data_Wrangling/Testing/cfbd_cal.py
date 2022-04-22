#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 17:18:23 2021

@author: Broth
"""


#get api key
file = open('../../Data/key.txt')
key = file.read().replace("\n", " ")
file.close()

# Configure API key authorization: ApiKeyAuth
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = key
configuration.api_key_prefix['Authorization'] = 'Bearer'


# create an instance of the API class
cal_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
year = 2020 # int | Year filter

cal_response = cal_instance.get_calendar(year)

cal_response