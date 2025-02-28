import asyncio
import os 
import sys 
import pathlib

import time
import unittest

import logging
logging.basicConfig(level=logging.DEBUG)

from Instrumentum_sanae_doctrinae.web_scraping.monergism.mn_scrap_work_base import MN_ScrapSpeakerTopicScriptureWork_All


root_folder = os.path.join(os.getcwd(),'test_folder')

def test_scrap_all_author_work():
    browse_by_type = "speaker"
     
    ob = MN_ScrapSpeakerTopicScriptureWork_All(
        root_folder=root_folder,
        browse_by_type=browse_by_type,
        overwrite_log=False,
    )
    print(ob.element_dict.keys())
    
    #print(ob.__dict__)
    #asyncio.run(ob.download(4))

    
    

if __name__ == "__main__":
    
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
     
    test_scrap_all_author_work()
    