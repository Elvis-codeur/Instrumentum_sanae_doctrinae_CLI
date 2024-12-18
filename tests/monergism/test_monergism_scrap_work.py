import asyncio
import os 
import sys 
import pathlib

import time
import unittest

import logging
logging.basicConfig(level=logging.DEBUG)

from Instrumentum_sanae_doctrinae.scraping import monergism_scrap_works



def test_scrap_all_author_work():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "speaker"
     
    ob = monergism_scrap_works.MonergismScrapWebSiteAuthorTopicScripturesWork_All(
        root_folder=root_folder,
        browse_by_type=browse_by_type,
        overwrite_log=True,
    )
    #print(ob.__dict__)
    asyncio.run(ob.download(2))
    
    
def test_scrap_all_scripture_work():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "scripture"
     
    ob = monergism_scrap_works.MonergismScrapWebSiteAuthorTopicScripturesWork_All(
        root_folder=root_folder,
        browse_by_type=browse_by_type,
        overwrite_log=True,
    )
    #print(ob.__dict__)
    asyncio.run(ob.download(20))
    

def test_scrap_all_topic_work():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "topic"
     
    ob = monergism_scrap_works.MonergismScrapWebSiteAuthorTopicScripturesWork_All(
        root_folder=root_folder,
        browse_by_type=browse_by_type,
        overwrite_log=True,
    )
    #print(ob.__dict__)
    asyncio.run(ob.download(20))
    
    
def test_scrap_work():
    name = "Alfred  Edersheim"
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "speaker"
    url_list = ["https://www.monergism.com/search?f[0]=author:35298"]
    ob = monergism_scrap_works.MonergismScrapAuthorTopicScriptureWork(
        name=name,
        root_folder=root_folder,
        url_list=url_list,
        browse_by_type=browse_by_type
    )
    asyncio.run(ob.scrap_and_write())

if __name__ == "__main__":
    
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
     
    test_scrap_all_author_work()
    