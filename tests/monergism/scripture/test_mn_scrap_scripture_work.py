import asyncio
import os 
import sys 
import pathlib

import time
import unittest

import logging
logging.basicConfig(level=logging.DEBUG)

from Instrumentum_sanae_doctrinae.web_scraping.monergism.scripture import mn_scrap_scripture_works


def test_scrap_all_scripture_work():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "scripture"
     
    ob = mn_scrap_scripture_works.MN_ScriptureWork_All(
        root_folder=root_folder,
        browse_by_type=browse_by_type,
        overwrite_log=True,
    )
    #print(ob.__dict__)
    asyncio.run(ob.download(4))
    

if __name__ == "__main__":
    
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
     
    test_scrap_all_scripture_work()
    