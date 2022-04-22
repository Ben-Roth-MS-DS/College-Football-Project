#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 11:07:04 2021

@author: Broth
"""

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
pu_instance = cfbd.PlayersApi(cfbd.ApiClient(configuration))
year = 2020 # int | Year filter (default to 2020)
team = 'team_example' # str | Team filter (optional)
conference = 'conference_example' # str | Conference abbreviation filter (optional)
position = 'position_example' # str | Position abbreviation filter (optional)
player_id = 56 # int | Player id filter (optional)
exclude_garbage_time = True # bool | Filter to remove garbage time plays from calculations (optional)

 # Player usage metrics broken down by season
pu_response = pu_instance.get_player_usage(year)#, team=team, conference=conference, \
                                            #position=position, player_id=player_id, \
                                            #exclude_garbage_time=exclude_garbage_time)
                                            
pu_response[0]
                                            
 