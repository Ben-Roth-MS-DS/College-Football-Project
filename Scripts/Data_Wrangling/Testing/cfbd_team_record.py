#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 16:41:50 2021

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


trec_instance= cfbd.GamesApi(cfbd.ApiClient(configuration))
year = 2020# int | Year filter (optional)
team = 'Wisconsin'
 # str | Team filter (optional)
#conference = 'conference_example' # str | Conference filter (optional)

 # Team records
team_records = trec_instance.get_team_records(team = team, year = 2010)

team_records

