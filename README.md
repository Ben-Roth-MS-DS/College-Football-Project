# College-Football-Project
Collecting, cleaning, transforming, merging, visualizing, and modelling college football data

## Overview 

The overall purpose of this project is to develop a model to predict the score of each team in a given college football game. In turn, this prediction will give the overall winner, the margin by which that team won, and the total number of points scored in the game. The eventual dependent variable will be a team's score during a given, with input variables including each team's average stats (Yards per passing attempt, turnovers forced, rushing yards, etc) over the past n games, each team's opponents average stats over the past n games, team & opponent conference, and team & opponent recruiting ranks over past 4 years. 

The data for the project will be obtained through the cfbd api.

## Phase 1 - Data Cleaning and Transformation
**For phase 1, the data will be transformed, cleaned, and reformatted in a way so that they may be merged with other data to be used for modelling.**

### Cleaning & Transformation
* [X] Find data sources

* [X] Clean and transform team game data

* [X] Create rolling averages for statistics of interest from previous 3, 6, 12 games

* [] Clean and transform team recruiting data

* [] Join game and recruiting data

* [] Create fields for opponent game data and recruiting

## Phase 3 - Final Data Visual and Tabular Exploration

* [ ] Develop compelling visualizations and tables to show how the data is distributed.

## Phase 4 - Data Modeling and Results Visualization

* [ ] Compare un-tuned base model algorithms to determine which will be used for further modelling efforts

* [ ] Determine which period of time (1 season of data, 2 seasons of data, etc.) creates best model results 

## Data Sources

* [cfbd API](https://github.com/CFBD/cfbd-python)
  
