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


#create rankings by team/year
def recruiting_rolled(df,
                      team,
                      rolling_numbers = [2,3,4]):
    '''
    Purpose
        -  Function that aggregates recruiting points and ranking for past 2, 3, 4
           years
    
    Inputs
        - df (DataFrame): Dataframe containing cfbd recruiting data
        - team (str): Team whose recruiting info are getting aggregated
        - rolling_numbers (list): List of numbers that defines the number of 
                                  previous year recruiting averages wished to be calculated
                                  
    Outputs
        - df_recruit_fin (pd.DataFrame): Dataframe at the game_id level that contains
                                 rolled up stats
    '''

    df_team = df.loc[df.team == team, :]
    
    df_team.sort_values('year').reset_index(inplace = True)
    
    rolling_teams_list =  [df_team.\
                        rolling(window, 1).\
                        mean()[['rank', 'points']].\
                        #reset_index(drop = True).\
                        rename(columns = {column:'rec_' + column+'_' + str(window) + '_year_avg' for column in ['rank', 'points']})
                        for window in rolling_numbers]
        
    #column-wise concatenate the list of dataframes
    rolling_teams_df = pd.concat(rolling_teams_list, axis = 1)
    
    #bring back to large df_grp
    df_recruit_fin = pd.concat([df_team, rolling_teams_df], axis = 1)
    
    return(df_recruit_fin)


    
    
    
    
    

