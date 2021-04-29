#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 19:14:00 2019

@author: Broth
"""
## Want model to take the following form, most likely a multinomial logit ##

##  conf_win,lagged_win_conf_rank ~ conf_lose + lagged_lose_conf_rank 
##  + lagged_recruit(4yr avg) + w_L_past_10_games + new_coach(1 or 0) + 
##  coach_career_win_pct + expenses + factor(year) + seniors lost + avg_off(lagged 12 games)
## + avg_def(lagged 12 games)


#import necessary modules
import os
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver


# import the data (see READ.md for data citations)
expenses = pd.read_csv('./Data/csv-data/cfb_expenses_2005-18.csv')
games = pd.read_csv('./Data/csv-data/cfb_games_2011-18.csv')
recruiting = pd.read_csv('./Data/csv-data/cfb_recruit_rankings_2002-18.csv')


recruiting.head()
## if look through recruiting rankings database, there are a few inconsistencies ##
## with some of the school names. In no particular order, the issues: ##
## 1. 'State' schools are sometimes referred to as 'St' ##
## 2. 'Tennessee' is spelled with an extra 'e' in 2014 ##
## 3. Miami (FL) and Miami (OH) are each given different names in different years ##
## 4. Washington St. Misspelled in 2011 ##
## 5. Arkansas St. mispelled a few different times ##
## 6. UCF changes from Central Florida ##
## 7. FIU changes from Florida International ##
## 8. t in North Texas not always capitalized ##
## 9. Middle Tennessee changes from MTSU ##
## 10. UTSA changes from Texas-San Antonio ##
## 11. NIU changes from Northern Illinois ##
## 12. San Jose State mispelled ##

#create list of years of columns

years = [str(year) for year in range(2002,2019)]

#turn off warning
pd.options.mode.chained_assignment = None 

#create list of what I want to change in recruiting
old_cruits = ['Northern Illinois','Washignton St',
                'Arksansas State','MTSU','Tennesseee','North texas',
                'Central Florida','Florida International','Louisiana-Monroe','Louisiana-Lafayette',
                'San Jsoe State']

#create list of what I want to be the replacement in recruiting
new_cruits = ['NIU','Washington St','Arkansas State','Middle Tennessee','Tennessee'
              ,'North Texas','UCF','FIU','Louisiana Monroe',
             'Louisiana Lafayette', 'San Jose State']


# create function for cleaning the recruiting list
def clean_cruits(wrong_list = None, right_list = None, df = None, columns = None):
    '''
    Function for cleaning the recruiting data set
    
    Inputs:
    - wrong_list: list of the incorrectly named schools
        
    - right_list: list of the correctly named schools (matching index with wrong)
                
                
    - df: the data frame that we want to clean
    
    - columns: list of columns in the dataset we're interested in iterating through
    
    Output:
    - A cleaned data frame
    '''
    for x in range(len(wrong_list)):
        for column in columns:
            for team in df[column]:
            #try/except typeerror to go around nan floats
                try:
                    if team == wrong_list[x]:
                        df[column][df.loc[df[column] == team].index[0]] = df[
                        column][df.loc[df[column] == team].index[0]].replace(
                        wrong_list[x],right_list[x])
                        
                    else:
                        continue
                    
                except TypeError:
                    continue
                
    return df[column].head()

clean_cruits(wrong_list = old_cruits, right_list = new_cruits,
             df = recruiting, columns = years)


#test run
#for year in years:
#    for team in recruiting[year]:
#        if team == 'Florida International':
#            recruiting[year][recruiting.loc[recruiting[
#            year] == team].index[0]] = recruiting[year][
#            recruiting.loc[recruiting[year] == team].index[
#            0]].replace('Florida International','FIU')


#can't think of a way to incorporate Miami and St issues in the function. Tried
#to, but I was having a hard time with how it was iterating through

for year in years:
    for team in recruiting[year]:
        try:
            if 'Miami' in team:
                if 'FL' in team:
                    continue
                elif 'OH' in team:
                    recruiting[year] = recruiting[year].str.replace('Miami-OH','Miami OH')
                else:
                    if team == 'Miami':
                        recruiting[year][
                        recruiting.loc[recruiting[year] == team].index[
                                0]] = recruiting[year][
                        recruiting.loc[recruiting[year] == team].index[
                                0]].replace('Miami','Miami FL')
                    else:
                        continue
            
            elif 'ate' not in team:
                if ' St' in team:
                    recruiting[year][
                        recruiting.loc[recruiting[year] == team].index[
                                0]] = recruiting[year][
                        recruiting.loc[recruiting[year] == team].index[
                                0]].replace(' St',' State')
                
                    #also can't think of a way to incorporate the Miami issues 
                    #without lopping in Miami OH with the just Miami
            
            else:
                continue
        except TypeError:
            continue

# continue with recruiting rankings; I want to get the recruiting data in a form
# so that the columns are school and each year. The school column obviously has
# each distinct school name, and the year column has that school's ranking in 
# that year
                                
recruiting['2013'][112] = 'San Jose State'
  
                            
# create new data frame with team names, and years
rec_rank = pd.DataFrame(columns = ['Team','2018','2017','2016','2015',
                                      '2014','2013','2012','2011','2010','2009',
                                      '2008','2007','2006','2005','2004','2003',
                                      '2002'])

# import all team names into new dataframe 
rec_rank['Team'] = recruiting['2018']

#since Idaho was FCS in 2018, add them in real quick
rec_rank = rec_rank.append(pd.Series(), ignore_index=True)
rec_rank['Team'][130] = 'Idaho'

# Add recruiting rank in year for each team based on their index from the 
# recruiting data set

for index in range(len(recruiting['Rank'])):
    for team in rec_rank['Team']:
        for year in years:
            if team == recruiting[year][index]:
                rec_rank[year][rec_rank.loc[rec_rank['Team'] == team].index[
                0]] = recruiting.loc[recruiting[year] == team].index[0] + 1
            else:
                continue

#average 4-year rank

int_years = [2008,2009,2010,2011]


while max(int_years) < 2019:
    str_years = [str(x) for x in int_years]
    rec_rank['4year_rec_avg'+str(max(int_years))] = rec_rank[str_years].mean(axis=1)
    int_years = [x+1 for x in int_years]

#df['avg'] = df[['Monday', 'Tuesday']].mean(axis=1)
              
            
## Now that we have clean the ranking, now to merge df with relevent variables 

#create new data base
cfb_win = games.copy()

#drop irrelevent variables
cfb_win = cfb_win.drop(['Game','Count','Field25','TOP VERIFICATION', 'O/U Total'], axis = 1)

#look at unique team names in cfb_win to see which ones we'll have to change
uniq_cfb = []
uniq_cfb.append(list(cfb_win['Winning'].unique()))


# go through similar process with the recruiting df; compile list of wrongly 
# spelled names, list of correctly spelled names, and columns where those names are
old_win = ['C. Michigan', 'E. Michigan','FAU', 'La. Tech','La.-Lafayette',
           'La.-Monroe','La.Tech','MTSU','Miami, FL','Miami, OH','N.C. State',
           'S. Alabama','Southern Cal','Texs Tech','Vanderbilit','W. Kentucky',
           'W. Michigan','N. Illinois']

new_win = ['Central Michigan','Eastern Michigan','Florida Atlantic','Louisiana Tech',
           'Louisiana Lafayette','Louisiana Monroe','Louisiana Tech',
           'Middle Tennessee','Miami FL','Miami OH','NC State','South Alabama',
           'USC','Texas Tech','Vanderbilt','Western Kentucky','Western Michigan',
           'Northern Illinois']
            
win_columns = ['Winning','Losing']

#apply function to new lists
clean_cruits(wrong_list = old_win, right_list = new_win,
             df = cfb_win, columns = win_columns)


## Now go through the cleaning process for expenses. except more removing than
## replacing. Also this process will be more involved than with the other two
## dfs, since this df has each school's 'official' name (e.g. Virginia Polytechnic...')
## Also need to change dollar amounts to ints from strings($x,xxx,xxx) 

#first step of the cleaning process, same as the other two, focusing on general
#differences first


expenses = pd.read_csv('./Data/csv-data/cfb_expenses_2005-18.csv')


#more generizable things that can change
old_expense = ['University', ', The State', ' of ','-','and Agricultural & Mechanical College',
               ' at ', 'A & M','The','United States','Academy']

new_expense = ['','','','','A&M','','A&M','','','']


#modify function so that line after try: includes 'in' and not '=='
for x in range(len(old_expense)):
    for team in expenses['Data']:
        #try/except typeerror to go around nan floats
        if old_expense[x] in team:
            expenses['Data'][expenses.loc[expenses['Data'] == team].index[0]] = expenses[
                'Data'][expenses.loc[expenses['Data'] == team].index[0]].replace(
                old_expense[x],new_expense[x])
                        
        else:
            continue


#remove white space at beginning&end of team names
expenses['Data'] = expenses['Data'].str.rstrip()
expenses['Data'] = expenses['Data'].str.lstrip()

# Now have to get into greater specificity with replacing names to conform to 
# other data sets

old_expense2 = ['Bowling Green State','California State Fresno','Florida International',
                'Georgia InstituteTechnology','Indiana Bloomington',
                'Louisiana State  A&M','Middle Tennessee State','North Carolina State',
                'Northern Illinois','Pennslyvania State','Rutgers New JerseyNew Brunswick',
                'Virginia Polytechnic Institute and State','WisconsinMadison',
                'Southern Mississippi','North CarolinaCharlotte','North CarolinaChapel Hill',
                'NevadaReno','NevadaLas Vegas','NebraskaLincoln','MissouriColumbia',
                'Mississippi','MinnesotaTwin Cities','Massachusetts Amherst',
                'MarylandCollege Park','LouisianaMonroe','LouisianaLafayette',
                'IllinoisUrbanaChampaign','HawaiiManoa','Colorado Boulder',
                'CaliforniaLos Angeles','CaliforniaBerkeley','AlabamaBirmingham',
                'Buffalo New York','Military','TexasSan Antonio','TexasEl Paso',
                'TexasAustin','North Carolina State Raleigh']

new_expense2 = ['Bowling Green','Fresno State','FIU','Georgia Tech', 'Indiana',
                'LSU','Middle Tennessee','NC State', 'NIU','Penn State','Rutgers',
                'Virginia Tech','Wisconsin','Southern Miss','Charlotte','UNC',
                'Nevada','UNLV','Nebraska','Missouri','Ole Miss','Minnesota',
                'Massachusetts','Maryland','Louisiana Monroe','Louisiana Lafayette',
                'Illinois','Hawaii','Colorado','UCLA','California','UAB','Buffalo',
                'Army','UTSA','UTEP','Texas','NC State']

#column that changes
name_column = ['Data']


#clean less generizable stuff
clean_cruits(wrong_list = old_expense2, right_list = new_expense2,
             df = expenses, columns = name_column)

expenses['Total Football Spending'] = expenses['Medical'] + expenses['Recruiting'] + expenses['Game Expenses and Travel'] + \
                                      expenses['Coaches Compensation'] +  expenses['Athletic Student Aid']

expenses = expenses.dropna(subset = ['Total Football Spending', 'Total Expenses'])


expenses['football_expense_pct'] = expenses['Total Football Spending']/expenses['Total Expenses']


## Coaches df
coaches = pd.read_excel('./Data/original-data/Football_Coach_Database.xlsx')

#create new df, fill in teams
clean_coaches = coaches.copy()

new_years =  np.arange(2011,2020)

#1 if same coach, 0 if old coach
for year in reversed(new_years):
    clean_coaches[year] = (clean_coaches[year] == clean_coaches[year-1]).astype('int')

#drop columns from years not in games df
clean_coaches = clean_coaches.drop([2019,2010], axis = 1)


#match school names
old_coaches = ['Central Florida', 'Florida International', 'Louisiana-Lafayette', 
               'Louisian-Monroe', 'North Carolina State', 'Northern Illinois', 'Pitt']

new_coaches = ['UCF', 'FIU', 'Louisiana Lafayette', 'Louisian Monroe', 'NC State',
               'NIU','Pittsburgh']

clean_cruits(wrong_list = old_coaches, right_list = new_coaches,
             df = clean_coaches, columns = ['FBS Team'])



#### Roster Scrape ####



#select years of interest
year_cols = [col for col in recruiting.columns if '20' in col[:4]]


#scrape list of team names
team_url = "https://www.sports-reference.com/cfb/schools/"
team_page = requests.get(team_url)
soup = BeautifulSoup(team_page.content, 'html.parser')

#only keep team name and years active
team_table = pd.read_html(team_url)[0].iloc[:, [1,3]]

#rename columns
team_table.columns = ['School','To']

#remove nas
team_table = team_table.dropna(how = 'all')

#convert year to int
team_table['To'] = pd.to_numeric(team_table['To'], errors = 'coerce')

#boolean if is current team
is_current = team_table['To'] > games.Year.min() - 1
team_table = team_table[is_current]

#get team names into proper format
team_table['School'] = team_table['School'].str.replace(' ','-')
team_table['School'] = team_table['School'].str.lower()

#school names that need to be changed
team_table['School'] = team_table['School'].replace({
        'pitt':'pittsburgh',
        'byu':'brigham-young',
        'utsa':'texas-san-antonio',
        'utep': 'texas-el-paso',
        'louisiana': 'louisiana-lafayette',
        'lsu': 'louisiana-state',
        'texas-a&m': 'texas-am',
        'uab':'alabama-birmingham',
        'ucf': 'central-florida',
        'usc': 'southern-california',
        'smu': 'southern-methodist',
        'ole-miss': 'mississippi',
        'miami-(fl)': 'miami-fl',
        'miami-(oh)': 'miami-oh'})

#alternative websites if roster not on sports-reference
team_pages = {
        'appalachian-state': 'https://appstatesports.com/sports/football/roster/',
        'charlotte': 'https://charlotte49ers.com/sports/football/roster/',
        'coastal-carolina': 'https://goccusports.com/sports/football/roster/',
        'florida-atlantic': 'https://fausports.com/sports/football/roster/',
        'florida-international': 'https://fiusports.com/sports/football/roster/',
        'georgia-southern': 'https://gseagles.com/sports/football/roster/',
        'georgia-state': 'https://georgiastatesports.com/sports/football/roster/',
        'massachusetts': 'https://umassathletics.com/sports/football/roster/',
        'old-dominion': 'https://odusports.com/sports/football/roster/',
        'south-alabama': 'https://usajaguars.com/sports/football/roster/',
        'texas-state': 'https://txstatebobcats.com/sports/football/roster/',
        }    

#initialize empty df  
rosters = pd.DataFrame()
#initialize driver 
driver = webdriver.Chrome(os.getcwd() + '/chromedriver')

for team in team_table['School']:
    for year in year_cols:
        try:
            url = "https://www.sports-reference.com/cfb/schools/" + team + "/" + year + "-roster.html"
            page =requests.get(url)
            
            if page.url == url:
                soup = BeautifulSoup(page.content, 'html.parser')
                team_rost = pd.DataFrame()
                team_rost[team + '.' + year] = pd.read_html(url)[0]['Player']
                rosters = pd.concat([rosters, team_rost], axis = 1)
            else:
                continue
            
        except:
            try:
                if team == 'texas-state':
                    #get url for team specific roster site
                    url = team_pages[team] + year + '-' + str(int(year) + 1)
                    page =requests.get(url)
                    
                    if page.url == url:
                    
                        #get url in driver
                        driver.get(url)

                        #list of player names
                        all_names = driver.find_elements_by_class_name('sidearm-roster-player-name')
                        names = []
                        for name in all_names:
                            names.append(name.text)
                        
                        #clean list of names
                        names = [name.split("\n",1)[1] for name in names]
                        
                        #add to larger df
                        team_rost = pd.DataFrame()
                        team_rost[team + '.' + year] = names
                        rosters = pd.concat([rosters, team_rost], axis = 1)    
                
                        driver.close()
                    
                else:
                    #get url for team specific roster site
                    url = team_pages[team] + year
                
                    page = requests.get(url)
                    
                    if page == url:
                        #get url in driver
                        driver.get(url)

                        #list of player names
                        all_names = driver.find_elements_by_class_name('sidearm-roster-player-name')
                        names = []
                        for name in all_names:
                            names.append(name.text)
                        
                        #clean list of names
                        names = [name.split("\n",1)[1] for name in names]
                        
                        #add to larger df
                        team_rost = pd.DataFrame()
                        team_rost[team + '.' + year] = names
                        rosters = pd.concat([rosters, team_rost], axis = 1)    
                
                        driver.close()
                    
                    else:
                        continue
                
            except:
                print(team, year)
                
            continue


driver.quit()

cols = rosters.columns

#if include regex = true, get 'nothing to repeat' error
rosters[cols] = rosters[cols].replace({'*':''})
rosters[cols] = rosters[cols].replace({',':'', '\.':''}, regex = True)

rosters[cols] = rosters[cols].apply(lambda x: x.astype(str).str.lower())


roster_changes = pd.DataFrame(columns = team_table['School'], index = year_cols[:-1])



for team in team_table['School']:
    for year in year_cols:
        try:
            if int(year) > 2002:
                roster_changes[team][year] = len(list(set(rosters[team + '.' + year])- set(rosters[team + '.' + str(int(year) - 1)])))
            else:
                continue
        except KeyError:
            continue
            
            
#### need to do: finish roster comparison update conferences, lag games (record last 12 games)
####            lagged SOS, potential weekly ranking?


###clean games
#games_clean = games[['Winning','Winning H/A/N','Winning Conference','Losing',Year
#                    'Losing Conference','Winning YPPA','Winning YPRA','Winning TOP',
#                   'Winning Pen Yards','Winning TOP','Losing Points','Losing YPPA',
#                  'Losing YPRA','Losing TO','Losing Pen Yards','Losing TOP', Lagged_Something]]




#update conferences so that they reflect current years
all_conf = sorted(games['Winning Conference'].unique())


roster_changes.to_csv('./Data/wrangled-data/roster_changes.csv')

clean_coaches.to_csv('./Data/wrangled-data/clean_coaches.csv')
                     
rec_rank.to_csv('./Data/wrangled-data/rec_rank.csv')

expenses.to_csv('./Data/wrangled-data/expenses.csv')

cfb_win.to_csv('./Data/wrangled-data/cfb_win.csv')