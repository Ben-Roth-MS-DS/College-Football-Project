#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 11:55:50 2022

@author: Broth
"""


#  ['athlete_id', 'athlete_name', 'clock', 'conference', 'distance', 'down',
#   'drive_id', 'game_id', 'opponent', 'opponent_score', 'period',
#   'play_id', 'season', 'stat', 'stat_type', 'team', 'team_score', 'week',
#   'yards_to_goal']

#define function compiling average for yardage stats
def yardage_rolling(df,
                    stat, 
                    rolling_numbers = [3, 6, 12]):
    
    '''
    Purpose
        - Function that counts and calculates rolling averages for stats
          associated with yardage gains
          
    Inputs
        - df (pd.DataFrame): Dataframe at the team-play level
        - stat (str): Stat with yardage (e.g. 'Rush') that is to be rolled up
        - rolling_numbers (list): List of numbers that defines the number of 
                                  previous game averages wished to be calculated
                                  
    Outputs
        - df_grp_fin (pd.DataFrame): Dataframe at the game_id level that contains
                                     rolled up stats
    '''
    #order df by game
    df = df.sort_values(['season', 'week']).reset_index(drop = True)
    
    #create initial grouped counting stats
    df_grp = df.loc[df.stat_type == stat, : ].\
                groupby('game_id').\
                agg({'play_id':'count', 'drive_id':lambda x: x.nunique(), 'stat':'sum'}).\
                reset_index().\
                rename(columns = {'play_id':stat + '_plays', 'drive_id':'drives', 'stat':stat + '_yards'})

    #create stats by unit
    df_grp[stat + '_yards_play'] = df_grp[stat + '_yards']/df_grp[stat + '_plays']
    df_grp[stat + '_yards_drive'] = df_grp[stat + '_yards']/df_grp['drives']
    df_grp[stat + '_plays_drive'] = df_grp[stat + '_plays']/df_grp['drives']

    #define columns to be rolled
    rolling_columns = [column for column in df_grp.columns if column not in 'game_id']

    #create list of rolled up dataframes
    rolling_avg_list = [df_grp.\
                           rolling(window, 1).\
                           mean()[rolling_columns].\
                           reset_index(drop = True).\
                           rename(columns = {column:column+'_' + str(window) + '_game_avg' for column in rolling_columns})
                        for window in rolling_numbers]

    #column-wise concatenate the list of dataframes
    rolling_avg_df_grp = pd.concat(rolling_avg_list, axis = 1)
    
    #bring back to large df_grp
    df_grp_fin = pd.concat([df_grp, rolling_avg_df_grp], axis = 1)
    
    return(df_grp_fin)


def non_yardage_rolling(df,
                        stat, 
                        rolling_numbers = [3, 6, 12]):
    
    '''
    Purpose
        - Function that counts and calculates rolling occurances for non-yardage
          based stats (e.g. 'Fumble')
          
    Inputs
        - df (pd.DataFrame): Dataframe at the team-play level
        - stat (str): Stat with yardage (e.g. 'Rush') that is to be rolled up
        - rolling_numbers (list): List of numbers that defines the number of 
                                  previous game averages wished to be calculated
                                  
    Outputs
        - df_grp_fin (pd.DataFrame): Dataframe at the game_id level that contains
                                     rolled up stats
    '''
    #order df by game
    df = df.sort_values(['season', 'week']).reset_index(drop = True)
    
    #create initial grouped counting stats
    if stat == 'Explosive_Play':
        df_grp = df.groupby('game_id').\
                       agg({'play_id':'count', 
                            'drive_id':lambda x: x.nunique(),
                            'Explosive_Play':'sum'}).\
                       reset_index().\
                       rename(columns = {'play_id': 'plays',
                                         'drive_id': 'drives',
                                         'Explosive_Play': stat + 's'})
    else: 
        df_grp = df.groupby('game_id').\
                       agg({'play_id':'count', 
                            'drive_id':lambda x: x.nunique(),
                            'stat_type': lambda x: sum(x == stat)}).\
                       reset_index().\
                       rename(columns = {'play_id': 'plays',
                                         'drive_id': 'drives',
                                         'stat_type': stat + 's'})

    #create stats by unit
    df_grp[stat + 's_drive'] = df_grp[stat + 's']/df_grp['drives']
    df_grp[stat + 's_play'] = df_grp[stat + 's']/df_grp['plays']
    
    df_grp.drop(['drives', 'plays'], axis = 1, inplace = True)

    #define columns to be rolled
    rolling_columns = [column for column in df_grp.columns if column not in ['game_id', 'drives']]

    #create list of rolled up dataframes
    rolling_avg_list = [df_grp.\
                           rolling(window, 1).\
                           mean()[rolling_columns].\
                           reset_index(drop = True).\
                           rename(columns = {column:column+'_' + str(window) + '_game_avg' for column in rolling_columns})
                        for window in rolling_numbers]

    #column-wise concatenate the list of dataframes
    rolling_avg_df_grp = pd.concat(rolling_avg_list, axis = 1)
    
    #bring back to large df_grp
    df_grp_fin = pd.concat([df_grp, rolling_avg_df_grp], axis = 1)
    
    return(df_grp_fin)


#define function for all stats
def all_rolling(df,
                stat, 
                rolling_numbers = [3, 6, 12]):
    '''
    Purpose
        - Function that decides which bucket a stat falls into and applies the
          appropriate rolling function
          
    Inputs
        - df (pd.DataFrame): Dataframe at the team-play level
        - stat (str): Stat with yardage (e.g. 'Rush') that is to be rolled up
        - rolling_numbers (list): List of numbers that defines the number of 
                                  previous game averages wished to be calculated
                                  
    Outputs
        - df_fin (pd.DataFrame): Dataframe at the game_id level that contains
                                     rolled up stats    
    '''
    
    if stat in ['Rush', 'Completion']:
        df_out = yardage_rolling(df = df,
                                 stat = stat)
        
        return(df_out)
    
    else:
        df_out = non_yardage_rolling(df = df,
                                     stat = stat)
        
        return(df_out)
    

### get per down
def yardage_rolling_downs(df,
                          down,
                          stat, 
                          rolling_numbers = [3, 6, 12]):
    
    '''
    Purpose
        - Function that counts and calculates rolling averages for stats
          associated with yardage gains on a per down basis
          
    Inputs
        - df (pd.DataFrame): Dataframe at the team-play level
        - down (int): Down that the stats will be rolled up on 
        - stat (str): Stat with yardage (e.g. 'Rush') that is to be rolled up
        - rolling_numbers (list): List of numbers that defines the number of 
                                  previous game averages wished to be calculated
                                  
    Outputs
        - df_grp_fin (pd.DataFrame): Dataframe at the game_id level that contains
                                     rolled up stats
    '''
    #order df by game
    df = df.sort_values(['season', 'week']).reset_index(drop = True)
    
    #create initial grouped counting stats
    df_grp = df.loc[(df.stat_type == stat) & (df.down == down), : ].\
                groupby('game_id').\
                agg({'play_id':'count',
                     'stat':'sum'}).\
                reset_index().\
                rename(columns = {'play_id':stat + '_' + str(down) + 'down_plays',
                                  'stat':stat + '_' + str(down) + 'down_yards'})

    #create stats by unit
    df_grp[stat + '_yards_' + str(down) +'down'] = df_grp[stat + '_' + str(down) + 'down_yards']/\
                                                   df_grp[stat + '_' + str(down) + 'down_plays']

    #define columns to be rolled
    rolling_columns = [column for column in df_grp.columns if column not in 'game_id']

    #create list of rolled up dataframes
    rolling_avg_list = [df_grp.\
                           rolling(window, 1).\
                           mean()[rolling_columns].\
                           reset_index(drop = True).\
                           rename(columns = {column:column+'_' + str(window) + '_game_avg' for column in rolling_columns})
                        for window in rolling_numbers]

    #column-wise concatenate the list of dataframes
    rolling_avg_df_grp = pd.concat(rolling_avg_list, axis = 1)
    
    #bring back to large df_grp
    df_grp_fin = pd.concat([df_grp, rolling_avg_df_grp], axis = 1)
    
    return(df_grp_fin)


def non_yardage_rolling_downs(df,
                              down,
                              stat, 
                              rolling_numbers = [3, 6, 12]):
    
    '''
    Purpose
        - Function that counts and calculates rolling occurances for non-yardage
          based stats (e.g. 'Fumble') on a per down basis
          
    Inputs
        - df (pd.DataFrame): Dataframe at the team-play level
        - down (int): Down that the stats will be rolled up on 
        - stat (str): Stat with yardage (e.g. 'Rush') that is to be rolled up
        - rolling_numbers (list): List of numbers that defines the number of 
                                  previous game averages wished to be calculated
                                  
    Outputs
        - df_grp_fin (pd.DataFrame): Dataframe at the game_id level that contains
                                     rolled up stats
    '''
    #order df by game
    df = df.sort_values(['season', 'week']).reset_index(drop = True)
    
    #create initial grouped counting stats
    if stat == 'Explosive_Play':
        df_grp = df.loc[df.down == down, ].\
                    groupby('game_id').\
                    agg({'play_id':'count', 
                         'Explosive_Play':'sum'}).\
                    reset_index().\
                    rename(columns = {'play_id': stat + '_' + str(down) + 'down_plays',
                                      'Explosive_Play':str(down) + 'down_' + stat + 's'})
    else: 
        df_grp = df.loc[df.down == down, ].\
                    groupby('game_id').\
                    agg({'play_id':'count', 
                         'stat_type': lambda x: sum(x == stat)}).\
                    reset_index().\
                    rename(columns = {'play_id': stat + '_' + str(down) + 'down_plays',
                                      'stat_type': str(down) + 'down_' + stat + 's'})

    #create stats by unit
    df_grp[stat + '_rate_' + str(down) +'down'] = df_grp[str(down) + 'down_' + stat + 's']/\
                                                   df_grp[stat + '_' + str(down) + 'down_plays']
    

    #define columns to be rolled
    rolling_columns = [column for column in df_grp.columns if column not in ['game_id', 'drives']]

    #create list of rolled up dataframes
    rolling_avg_list = [df_grp.\
                           rolling(window, 1).\
                           mean()[rolling_columns].\
                           reset_index(drop = True).\
                           rename(columns = {column:column+'_' + str(window) + '_game_avg' for column in rolling_columns})
                        for window in rolling_numbers]

    #column-wise concatenate the list of dataframes
    rolling_avg_df_grp = pd.concat(rolling_avg_list, axis = 1)
    
    #bring back to large df_grp
    df_grp_fin = pd.concat([df_grp, rolling_avg_df_grp], axis = 1)
    
    return(df_grp_fin)


def all_rolling_downs(df,
                      down,
                      stat, 
                      rolling_numbers = [3, 6, 12]):
    '''
    Purpose
        - Function that decides which bucket a stat falls into and applies the
          appropriate rolling function
          
    Inputs
        - df (pd.DataFrame): Dataframe at the team-play level
        - stat (str): Stat with yardage (e.g. 'Rush') that is to be rolled up
        - rolling_numbers (list): List of numbers that defines the number of 
                                  previous game averages wished to be calculated
                                  
    Outputs
        - df_fin (pd.DataFrame): Dataframe at the game_id level that contains
                                     rolled up stats    
    '''
    
    if stat in ['Rush', 'Completion']:
        df_out = yardage_rolling_downs(df = df,
                                       down = down,
                                       stat = stat)
        
        return(df_out)
    
    else:
        df_out = non_yardage_rolling_downs(df = df,
                                           down = down,
                                           stat = stat)
        
        return(df_out)

    
def stats_function(team,
                   years,
                   stats = ['Rush', 'Completion', 'Incompletion', 'Sack Taken', 'Touchdown', 
                            'Interception Thrown', 'Fumble Forced', 'Fumble Recovered', 'Fumble',
                            'Interception', 'Sack', 'Explosive_Play', 'Pass Breakup'],
                   downs = [1, 2, 3, 4],
                   rolling_numbers = [3, 6, 12]):
    
    '''
    Purpose
        -  Function that aggregates stats for a given team in a given year
    
    Inputs
        - team (str): Team whose stats are getting aggregated
        - year (list): List of years for stat aggregations
        - stats (list): List of stats to be aggregates
        - rolling_numbers (list): List of numbers that defines the number of 
                                  previous game averages wished to be calculated
                                  
    Outputs
        - df_fin (pd.DataFrame): Dataframe at the game_id level that contains
                                 rolled up stats
    '''
    # create an instance of the plays API 
    plays_instance = cfbd.PlaysApi(cfbd.ApiClient(configuration))

    #load in plays for team
    play_stats_responses = [plays_instance.get_play_stats(year = year, team = team) for year in years]

    #convert plays to list
    play_stats_lists = [[play_stats_response[i].to_dict() for i in range(len(play_stats_response))] for play_stats_response in play_stats_responses] 

    #convert plays to list dfs
    dfs = [pd.DataFrame.from_records(play_stats_list) for play_stats_list in play_stats_lists]

    #concat to single df
    df = pd.concat(dfs, axis = 0)
    
    #ensure df is ordered correctly
    df = df.sort_values(['season', 'week']).reset_index(drop = True)
    
    for result in df.stat_type.unique():
        df[result] = np.where(df.stat_type == result, 1, 0)

    # replace incorrect yardage amounts
    df.loc[df.stat_type.isin(['Incompletion', 'Target', 'Interception Thrown', 'Fumble',
                                                              'Fumble Forced', 'Fumble Recovered']), 'stat']  = 0

    #create explosive plays field
    df.loc[((df.stat >= 12) & (df.stat_type == 'Rush')) | \
           ((df.stat >= 15) & (df.stat_type == 'Completion')) \
           , 'Explosive_Play'] = 1  
    
    df.loc[df.Explosive_Play.isna(), 'Explosive_Play'] = 0

    #create list of rolled functions
    stats_rolled = [all_rolling(df, stat) for stat in stats]
    
    #combine list of dataframes into single dataframe
    stats_flat = functools.reduce(lambda x, y: pd.merge(x, y, on = 'game_id'), stats_rolled)

    #remove drives column
    stats_flat.drop([column for column in stats_flat.columns if column[:5] == 'drive'], axis = 1, inplace = True)

    #calculate drives and plays
    rolled_basic = df.groupby('game_id').\
                      agg({'play_id':'count', 
                           'drive_id':lambda x: x.nunique()}).\
                      reset_index().\
                      rename(columns = {'play_id': 'plays',
                                        'drive_id': 'drives'})

    #calculate plays/drives rolling averages
    rolled_basic_avg = [rolled_basic.\
                        rolling(window, 1).\
                        mean()[['plays', 'drives']].\
                        #reset_index(drop = True).\
                        rename(columns = {column:column+'_' + str(window) + '_game_avg' for column in ['plays', 'drives']})
                        for window in [3, 6, 12]]
    
    #combine play counts/amounts and rolling averages into one
    rolled_all = pd.concat([rolled_basic, pd.concat(rolled_basic_avg, axis = 1)], axis = 1)    

    #join with rest of statistics
    all_df = pd.merge(left = rolled_all,
                      right = stats_flat,
                      on = 'game_id')



    #create list of rolled functions
    downs_rolled = [[all_rolling_downs(df, down, stat) for stat in stats] for down in downs]
    
    #combine list of dataframes into lists by down
    downs_rolled2 = [functools.reduce(lambda x, y: pd.merge(x, y, on = 'game_id'), downs_list) for downs_list in downs_rolled]

    #flatten into single dataframe
    downs_flat = functools.reduce(lambda x, y: pd.merge(x, y, on = 'game_id'), [down_df for down_df in downs_rolled2 if len(down_df) > 0])

    #merge with other list
    all_df2= pd.merge(all_df, downs_flat, on = 'game_id')

    return(all_df2)



    