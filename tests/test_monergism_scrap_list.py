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
    
    
if __name__ == "__main__":
    
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    test_speakers()