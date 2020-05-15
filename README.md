# College-Football-Project
Collecting, cleaning, transforming, merging, and modelling college football data

## Overview 

The overall purpose of this project is to develop a model to predict the winner of a given college football game. The eventual dependent variable will be a 1/0 binary variable (1 being if a team one their matchup, 0 if they lost), with input variables including each team's average stats (Yards per passing attempt, turnovers forced, rushing yards, etc) over the past n games, each team's opponents average stats over the past n games, team & opponent conference, team & opponent recruiting ranks over past 4 years, team & opponent university football spending from past year, coaching record over past n games, and changes in players on roster form past year. 

With the exception of roster information which was scraped, data used in the project was found online, and will be sourced at the end of the document. Once the data was downloaded, slight edits were made in Excel so that it could be loaded into Python

## Phase 1 - Data Cleaning and Transformation
**For phase 1, the data will be transformed, cleaned, and reformatted in a way so that they may be merged with other data to be used for modelling.**

### Cleaning
* [X] Find data sources

* [X] Clean expenditure data

* [X] Clean coaching data

* [X] Clean recruiting data

* [X] Create and clean roster data

* [X] Clean game data

### Transformation
* [X] Game data transformed so that each team and their opponent have rolling, average stats (Points, turnovers, etc.) from previous 8 games.

* [ ] Transform remaing data sets so that they may be merged together, with games as the base dataframe

## Phase 2 - Data Merging and Final Data Prep

* [ ] Merge data together.

* [ ] Perform and final data wrangling tasks

## Phase 3 - Final Data Visual and Tabular Exploration

* [ ] Develop compelling visualizations and tables to show how the data is distributed.

## Phase 4 - Data Modeling and Results Visualization

* [ ] Explore various modeling algorithms, hyper-parameter tuning, and model results comparison.

## Data Sources

* [Historical game scores and stats data](https://github.com/cjmasini/football_predictor/blob/master/CFB%202011%202018.xlsx "Game data")
  
* [Historical team coach data](https://docs.google.com/spreadsheets/d/1UXbBC7T4NtN1JwJs6Gk5Qm_y_pI1JXnOFtVuE3Iu3OQ/edit#gid=0)
  
* [Historical university expenses database website](http://cafidatabase.knightcommission.org/fbs)
  
* Historical recruiting rank data for each school
  * Having trouble finding data source, downloaded over a year ago.
