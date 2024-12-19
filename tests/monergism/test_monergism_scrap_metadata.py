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
    
    #test_scrap_all_topic_general_information()
    #test_scrap_all_scripture_general_information()
    test_scrap_series_general_information()
    
    end_time = time.time()
    print("time used = ",end_time - begin_time)   
    
    
    
    
   
   