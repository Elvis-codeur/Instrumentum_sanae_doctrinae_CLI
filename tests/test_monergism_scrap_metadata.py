import asyncio
import os 
import sys 
import pathlib

import time
import unittest

import logging
logging.basicConfig(level=logging.DEBUG)

from Instrumentum_sanae_doctrinae.scraping import monergism_scrap_metadata
from Instrumentum_sanae_doctrinae.scraping import monergism_scrap_general_information
from Instrumentum_sanae_doctrinae.scraping import monergism_scrap_get_list  
from Instrumentum_sanae_doctrinae.scraping import monergism_scrap_works
      
        

def test_topic():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = monergism_scrap_get_list.GetTopicList(root_folder)
    asyncio.run(ob.scrap_and_write())

def test_speakers():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = monergism_scrap_get_list.GetSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())


def test_scripture():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = monergism_scrap_get_list.GetScriptureList(root_folder)
    asyncio.run(ob.scrap_and_write())


def test_scrap_author_main_information():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    url = "https://www.monergism.com/search?f[0]=author:38603" 
    ob = monergism_scrap_metadata.MonergismScrapAuthorTopicScriptureWork(
        name = "Tom Ascol",
        root_folder = root_folder,
        url_list= [url],
        browse_by_type="speaker"
    )
    ob.scrap_and_write()


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
    asyncio.run(ob.download(2))


def test_get_author_all_work():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "speaker"
    ob = monergism_scrap_works.MonergismScrapWebSiteAllAuthorTopicScripturesWork(
        root_folder,
        browse_by_type,
        overwrite_log=True
    )
    asyncio.run(ob.download(60))
    ob.update_downloaded_and_to_download()
    ob.write_log_file()

if __name__ == "__main__":
    
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  
    
    #print("Elvs")
    url_topics = "https://www.monergism.com/topics"
    url_authors = "https://www.monergism.com/authors"
    
    begin_time = time.time()
    
    #test_speakers()
    #test_topic()
    #test_scripture()
    #test_scrap_author_general_information()
    
    test_scrap_all_topic_general_information()
    
    
    end_time = time.time()
    print("time used = ",end_time - begin_time)   
    
    
    
    
   
   