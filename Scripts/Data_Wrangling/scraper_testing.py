#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 06:59:34 2020

@author: Broth
"""

from functions.scraping import azcapitoltimes as azcap
from functions.scraping import foxphoenix as f10
from functions.scraping import googlenews as gn
from functions.scraping import azcentral as azcen
from functions.scraping import phoenixnewtimes as pnt
from functions.scraping import cronkitepbs as pbsaz
from functions.scraping import azdailynews as tucson

#az capital times
climate_urls = azcap.url_getter(key_words = ['climate change'],
                                         date_upper = '04/15/2019',
                                         date_lower = '05/15/2018')



climate_df = azcap.article_scraper_compiler(url_list = climate_urls)


#fox10
climate_urls2 = f10.url_getter(key_words = ['climate change'],
                                         date_upper = '04/15/2019',
                                         date_lower = '05/15/2018')



climate_df2 = f10.article_scraper_compiler(url_list = climate_urls2)

#az central
climate_urls3 = gn.google_scraper(key_words = ['climate change'],
                                  date_upper = '04/15/2019',
                                  date_lower = '05/15/2018',
                                  site = 'azcentral.com')

climate_df3 = azcen.article_scraper_compiler(url_list = climate_urls3)

#phoenix new times
climate_urls4 = gn.google_scraper(key_words = ['climate change'],
                                  date_upper = '04/15/2019',
                                  date_lower = '05/15/2018',
                                  site = 'phoenixnewtimes.com')

climate_df4 = pnt.article_scraper_compiler(url_list = climate_urls4)


#cronkite news
climate_urls5 = gn.google_scraper(key_words = ['climate change'],
                                  date_upper = '04/15/2019',
                                  date_lower = '05/15/2018',
                                  site = 'cronkitenews.azpbs.org/')


climate_df5 = pbsaz.article_scraper_compiler(url_list = climate_urls5)


#tucson news
climate_urls6 = gn.google_scraper(key_words = ['climate change'],
                                  date_upper = '04/15/2019',
                                  date_lower = '05/15/2018',
                                  site = 'tucson.com')

climate_df6 = tucson.article_scraper_compiler(url_list = climate_urls6)
