#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 17:13:23 2021

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
game_media_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
year = 56 # int | Year filter
week = 56 # int | Week filter (optional)
season_type = 'season_type_example' # str | Season type filter (regular, postseason, or both) (optional)
team = 'team_example' # str | Team filter (optional)
conference = 'conference_example' # str | Conference filter (optional)
media_type = 'media_type_example' # str | Media type filter (tv, radio, web, ppv, or mobile) (optional)

game_media_response = game_media_instance.get_game_media(year = 2020, team = 'Wisconsin')

game_media_response[0]