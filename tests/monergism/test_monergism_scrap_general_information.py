import asyncio
import os 
import sys 
import pathlib

import time
import unittest

import logging
logging.basicConfig(level=logging.DEBUG)

from Instrumentum_sanae_doctrinae.web_scraping import monergism_scrap_metadata
from Instrumentum_sanae_doctrinae.web_scraping import monergism_scrap_general_information
from Instrumentum_sanae_doctrinae.web_scraping import monergism_scrap_get_list  
from Instrumentum_sanae_doctrinae.web_scraping import monergism_scrap_works
      
        

def test_scrap_author_general_information():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "speaker"
    url = "https://www.monergism.com/search?f[0]=author:34468" 

    ob = monergism_scrap_general_information.MonergismScrapAuthorTopicScriptureGeneralInformation(
        name = "C H Spurgeon",
        root_folder = root_folder,
        url = url,
        browse_by_type = browse_by_type,
    )
    asyncio.run(ob.scrap_and_write())
    
    
def test_scrap_all_author_general_information():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "speaker"

    ob = monergism_scrap_general_information.MonergismScrapGeneralInformation_ALL(
        root_folder = root_folder,
        browse_by_type = browse_by_type,
        overwrite_log=True,
    )
    #print(ob.__dict__)
    asyncio.run(ob.download(4))
    
    

def test_scrap_all_topic_general_information():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "topic"

    ob = monergism_scrap_general_information.MonergismScrapGeneralInformation_ALL(
        root_folder = root_folder,
        browse_by_type = browse_by_type,
        overwrite_log=True,
    )
    #print(ob.__dict__)
    asyncio.run(ob.download(20))
    

def test_scrap_all_scripture_general_information():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "scripture"

    ob = monergism_scrap_general_information.MonergismScrapGeneralInformation_ALL(
        root_folder = root_folder,
        browse_by_type = browse_by_type,
        overwrite_log=True,
    )
    #print(ob.__dict__)
    asyncio.run(ob.download(20))


def test_scrap_series_general_information():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "serie"
    url = "https://www.monergism.com/search?keywords=%22MP3+Series%22&format=All"

    ob = monergism_scrap_general_information.MonergismScrapSeriesGeneralInformation(
        name = "",
        root_folder = root_folder,
        url = url,
        browse_by_type = browse_by_type,
    )
    asyncio.run(ob.scrap_and_write())
    
    
def test_scrap_rc_sproul_page():
    
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    url = "https://www.monergism.com/r-c-sproul"
    ob = monergism_scrap_general_information.MonergismScrapRCSproulGeneralInformation(
        root_folder=root_folder,
        url= url
    )
    asyncio.run(ob.scrap_and_write())
  
    
if __name__ == '__main__':
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #test_scrap_all_author_general_information()
    
    
    test_scrap_rc_sproul_page()