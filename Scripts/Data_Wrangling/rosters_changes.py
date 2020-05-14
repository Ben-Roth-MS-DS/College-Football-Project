#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:23:16 2020

@author: Broth
"""

## Rosters Scripts ###

## The purpose of this script is find the differences in 
## rosters for each team from year-to-year.

#import necessary modules
import pandas as pd
import numpy as np
import requests
import time
from bs4 import BeautifulSoup


#turn off warning
pd.options.mode.chained_assignment = None 

#select years of interest, convert to strings
year_cols = np.arange(2002, 2020)
year_cols = [str(x) for x in year_cols]


#scrape list of team names
team_url = "https://www.sports-reference.com/cfb/schools/"
team_page = requests.get(team_url)
soup = BeautifulSoup(team_page.content, 'html.parser')

#only keep team name and years active from websitet
team_table = pd.read_html(team_url)[0].iloc[:, [1,3]]

#rename columns
team_table.columns = ['School','To']

#remove nas
team_table = team_table.dropna(how = 'all')

#convert year to int
team_table['To'] = pd.to_numeric(team_table['To'], errors = 'coerce')

#boolean if is current team
is_current = team_table['To'] > min([int(year) for year in year_cols]) - 1
team_table = team_table[is_current]

#get team names into proper format
team_table['School'] = team_table['School'].str.replace(' ','-')
team_table['School'] = team_table['School'].str.lower()

#school names that need to be changed for url
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

start_time = time.time()

#initialize empty df  x
rosters = pd.DataFrame() 

#scrape rosters for each year from each year
for team in team_table['School']:
    for year in year_cols:
        #don't want to get blocked or banned or shut out of w/e
        time.sleep(0.5)
        
        #some schools don't have rosters on sports-reference, but try there first
        try:
            url = "https://www.sports-reference.com/cfb/schools/" + team + "/" + year + "-roster.html"
            page =requests.get(url)
            
            #if/else in case of redirect
            if page.url == url:
                #scrape players from that year/team, add to rosters df
                soup = BeautifulSoup(page.content, 'html.parser')
                team_rost = pd.DataFrame()
                team_rost[team + '.' + year] = pd.read_html(url)[0]['Player']
                rosters = pd.concat([rosters, team_rost], axis = 1)
            else:
                continue
            
        except:
            try:
                
                #texas state changed its website format for this year
                if team == 'texas-state' and int(year) < 2011 :
                    #get url for team specific roster site
                    url = team_pages[team] + year + '-' + str(int(year) + 1)
                    
                    page =requests.get(url)
                    
                    
                    #make sure page doesn't redirect
                    if page.url == url:
                        names = []
                        soup = BeautifulSoup(page.content, 'html.parser')
                        sidearm = soup.find_all('div',attrs={"class" : 'sidearm-roster-player-name'})

                        for a in sidearm:
                            all_names = a.find_all("a")
                            for name in all_names:
                                names.append(name.text)  
                
                        team_rost = pd.DataFrame()
                        team_rost[team + '.' + year] = names
                        rosters = pd.concat([rosters, team_rost], axis = 1)    
                    
                    else:
                        #know which team/year sites did not work
                        print(team, year)   
                
                    
                else:
                    #get url for team specific roster site
                    url = team_pages[team] + year
                
                    page = requests.get(url)
                    
                    #make sure page doesn't redirect
                    if page.url == url:
                        names = []
                        soup = BeautifulSoup(page.content, 'html.parser')
                        sidearm = soup.find_all('div',attrs={"class" : 'sidearm-roster-player-name'})

                        for a in sidearm:
                            all_names = a.find_all("a")
                            for name in all_names:
                                names.append(name.text)  
                
                        team_rost = pd.DataFrame()
                        team_rost[team + '.' + year] = names
                        rosters = pd.concat([rosters, team_rost], axis = 1)    
                    
                    else:
                        #know which team/year sites did not work
                        print(team, year)
                
            except:
                #know which team/year sites did not work
                print(team, year)
                
            continue
 


print("--- %s seconds ---" % (time.time() - start_time))


cols = rosters.columns


## match formatting of names in every columns

#if include regex = true, get 'nothing to repeat' error
rosters[cols] = rosters[cols].replace({'*':''})
rosters[cols] = rosters[cols].replace({',':'', '\.':''}, regex = True)

rosters[cols] = rosters[cols].apply(lambda x: x.astype(str).str.lower())

#create roster changes table
roster_changes = pd.DataFrame(columns = team_table['School'], index = year_cols[:-1])



for team in team_table['School']:
    for year in year_cols:
        try:
            if int(year) > 2001:
                roster_changes[team][year] = len(list(set(rosters[team + '.' + year])- set(rosters[team + '.' + str(int(year) - 1)])))
            else:
                continue
        except KeyError:
            continue
            
roster_changes['Year'] = roster_changes.index

roster_changes.index = range(len(roster_changes))

roster_changes.to_csv('../../Data/wrangled-data/roster_changes.csv')
