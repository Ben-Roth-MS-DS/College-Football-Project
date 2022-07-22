#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 13:40:49 2022

@author: Broth
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_poisson_deviance
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from xgboost.sklearn import XGBRegressor
from xgboost import plot_importance

#read in dataframe
df = pd.read_csv('../../Data/model-data/model_data.csv', index_col = 0 )

#remove nulls
df = df.dropna()


#define columns to keep in model that are covered in list comprefension of drop columns
keep_cols =  ['Team_ACC','Team_American Athletic','Team_Big 12', 'Team_Big Ten', 'Team_Conference USA', 
 'Team_FBS Independents', 'Team_Mid-American', 'Team_Mountain West', 'Team_Pac-12', 'Team_SEC', 
 'Team_Sun Belt', 'Opp_ACC', 'Opp_American Athletic', 'Opp_Big 12', 'Opp_Big Ten', 'Opp_Conference USA', 
 'Opp_FBS Independents', 'Opp_Mid-American', 'Opp_Mountain West', 'Opp_Pac-12', 
 'Opp_SEC', 'Opp_Sun Belt', 'ot_flag',  'team_pregame_elo',  'opp_pregame_elo']

#define columns not to put in model, including how team performed that game
drop_cols = [column for column in df.columns if 'avg' not in column and column not in keep_cols]

#split data based on season
train_df = df.loc[df.season < 2020, :]
test_df = df.loc[df.season >= 2020, :]

#define inputs and target
X_train = train_df[[column for column in df.columns if column not in drop_cols]].reset_index(drop = True)
y_train = train_df.team_points.reset_index(drop = True)


X_test = test_df[[column for column in df.columns if column not in drop_cols]].reset_index(drop = True)
y_test = test_df.team_points.reset_index(drop = True)

#convert values to float
X_train = X_train.astype(float)
X_test = X_test.astype(float)

#XGBoost Testing

#define parameters
params =  {
    'learning_rate': [0.01, 0.05, 0.10, 0.25],
    'max_depth': [ 3, 5, 6],
    'min_child_weight' : [1, 3, 5, 7],
    'gamma': [ 0.0, 0.1, 0.2 , 0.3, 0.4, 0.5, 0.6, 0.7],
    'colsample_bytree': [ 0.3, 0.4, 0.5 , 0.7],
    'subsample': [0.6, 0.7, 0.8]
    }

model = XGBRegressor(random_state = 1234,
                     booster = 'gblinear',
                     objective = 'count:poisson')

#train_test split time series

xgb_search = RandomizedSearchCV(estimator = model, 
                   param_distributions = params,
                   scoring = 'neg_mean_poisson_deviance', 
                   verbose = 0)

xgb_search.fit(X_train, y_train)


best_model = XGBRegressor(random_state = 1234,
                          booster = 'gblinear',
                          objective = 'count:poisson', 
                          subsample = xgb_search.best_params_['subsample'],
                          learning_rate = xgb_search.best_params_['learning_rate'],
                          max_depth = xgb_search.best_params_['max_depth'],
                          min_child_weight = xgb_search.best_params_['min_child_weight'],
                          gamma = xgb_search.best_params_['gamma'],
                          colsample_bytree = xgb_search.best_params_['colsample_bytree'])
best_model.fit(X_train, y_train)

best_predictions = best_model.predict(X_test)

xgb_mpd = mean_poisson_deviance(y_true = y_test, y_pred = best_predictions)


#Reduce Dimensions of Dataset

#define standardize data function
def standardizer(df):
    '''
    Function that standardizes input data frame
    '''
    #standardize dataframe
    df_std = StandardScaler().fit_transform(df)
    
    #convert standardized matrix to dataframe
    df_out = pd.DataFrame(df_std, columns = df.columns)
    
    return(df_out)

#define binary columns
bin_cols =[column for column in X_train.columns if (len(X_train[column].unique()) == 2 and max(X_train[column].values) == 1 and min(X_train[column].values) == 0)]

#standardize data
X_train_std = standardizer(X_train[[col for col in X_train.columns if col not in bin_cols]])
X_test_std = standardizer(X_test[[col for col in X_train.columns if col not in bin_cols]])

#run PCA
pca = PCA().fit(X_train_std)

#return number of components where explained variance is first equal or greater than 95%
n = 0
exp_var = 0
while exp_var <= 0.95:
    exp_var = np.cumsum(pca.explained_variance_ratio_)[n]
    n += 1 

#initiate pca
pca = PCA(n_components = n)

#fit to X_train
pca.fit(X_train_std)

#transform X_train and X_test
X_train_pca = pd.DataFrame(pca.transform(X_train_std))
X_test_pca = pd.DataFrame(pca.transform(X_test_std))


X_train_pca.columns = ['pca_comp_' + str(i) for i in range(len(X_train_pca.columns))]
X_test_pca.columns = ['pca_comp_' + str(i) for i in range(len(X_test_pca.columns))]

#add binary columns to pca dfs
X_train_pca = pd.concat([X_train_pca, X_train[bin_cols]], axis = 1)
X_test_pca = pd.concat([X_test_pca, X_test[bin_cols]], axis = 1)

#convert to np matrix to eliminate "training data did not have following fields" error
X_train_pca = X_train_pca.to_numpy()
X_test_pca = X_test_pca.to_numpy()

#run model on pca dataframe

model_pca = XGBRegressor(random_state = 1234,
                         booster = 'gblinear',
                         objective = 'count:poisson')


xgb_search_pca = RandomizedSearchCV(estimator = model_pca, 
                   param_distributions = params,
                   scoring = 'neg_mean_poisson_deviance', 
                   verbose = 0)

xgb_search_pca.fit(X_train_pca, y_train)


best_model_pca = XGBRegressor(random_state = 1234,
                              booster = 'gblinear',
                              objective = 'count:poisson', 
                              learning_rate = xgb_search_pca.best_params_['learning_rate'], 
                              subsample = xgb_search_pca.best_params_['subsample'],
                              max_depth = xgb_search_pca.best_params_['max_depth'],
                              min_child_weight = xgb_search_pca.best_params_['min_child_weight'],
                              gamma = xgb_search_pca.best_params_['gamma'],
                              colsample_bytree = xgb_search_pca.best_params_['colsample_bytree'])

best_model_pca.fit(X_train_pca, y_train)

best_predictions_pca = best_model_pca.predict(X_test_pca)

xgb_pca_mpd = mean_poisson_deviance(y_true = y_test, y_pred = best_predictions_pca)


#feature importance xgboost model
best_features = X_train.columns[np.abs(best_model.feature_importances_) >= np.percentile(np.abs(best_model.feature_importances_), np.arange(0, 100, 10))[8]]


#run model on best features

model_features = XGBRegressor(random_state = 1234,
                              booster = 'gblinear',
                              objective = 'count:poisson')


xgb_search_features = RandomizedSearchCV(estimator = model_features, 
                                         param_distributions = params,
                                         scoring = 'neg_mean_poisson_deviance', 
                                         verbose = 0)
    
xgb_search_features.fit(X_train[best_features], y_train)


best_model_features = XGBRegressor(random_state = 1234,
                                   booster = 'gblinear',
                                   objective = 'count:poisson', 
                                   learning_rate = xgb_search_features.best_params_['learning_rate'], 
                                   subsample = xgb_search_features.best_params_['subsample'],
                                   max_depth = xgb_search_features.best_params_['max_depth'],
                                   min_child_weight = xgb_search_features.best_params_['min_child_weight'],
                                   gamma = xgb_search_features.best_params_['gamma'],
                                   colsample_bytree = xgb_search_features.best_params_['colsample_bytree'])

best_model_features.fit(X_train[best_features], y_train)

best_predictions_feat = best_model_features.predict(X_test[best_features])

xgb_feat_mpd = mean_poisson_deviance(y_true = y_test, y_pred = best_predictions_feat)

## run models to compare performance across various training periods and how often 

#define function
def xgboost_period_testing(n, df, param_dict, periods):
        
    '''
    Purpose
        - Visualize and compare model decay based on how many years the model is 
          trained on to determine what length of time of model produces best result
          both in terms of retraining and re-tuning
          
    Inputs
        - n (int): Number of years to train model on
        - df (pd.DataFrame): DataFrame to train on
        - param_dict (dict): Dictionary of parameters to tune 
        - periods (list): List of periods for which to slice and train model on
                                  
    Outputs
        - run_numbers (list): List of run counts
        - mean_poisson_deviances (list): List of mean_poisson_deviances 
                                         associated with a run number
        
    '''

## models have to be retrained

##  One Year training period

# retraining every year

# retraining every other year

# retraining every three years

# retraining every four years

# retraining every five years

# retraining every six years


## Two Year Training Period

# retraining every year

# retraining every two years

# retraining every three years

# retraining
## Three Year Training Period
train_df = df.loc[df.season < 2020, :]
test_df = df.loc[df.season >= 2020, :]





    




