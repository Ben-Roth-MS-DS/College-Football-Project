#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:58:13 2020

@author: Broth
"""
import pandas as pd
from recruiting_ranks import clean_cruits


expenses = pd.read_csv('../../Data/csv-data/cfb_expenses_2005-18.csv')


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

expenses = expenses.dropna(subset = ['Total Football Spending', 'Total Expenses'])


expenses['Total Football Spending Int'] = expenses['Total Football Spending'].str.replace('$','').str.replace(',','').astype(int)
expenses['Total Expenses Int'] = expenses['Total Expenses'].str.replace('$','').str.replace(',','').astype(int)


expenses['footall_expense_pct'] = expenses['Total Football Spending Int']/expenses['Total Expenses Int']


expenses.to_csv('../../Data/wrangled-data/expenses.csv')