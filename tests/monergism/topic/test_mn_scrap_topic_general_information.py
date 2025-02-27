import asyncio
import os 
import sys 
import pathlib

import time
import unittest

import logging
logging.basicConfig(level=logging.DEBUG)

from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_scrap_general_information

        


    

root_folder = os.path.join(os.getcwd(),'test_folder')

    

def test_scrap_all_topic_general_information():
    browse_by_type = "topic"

    ob = mn_scrap_general_information.MonergismScrapGeneralInformation_ALL(
        root_folder = root_folder,
        browse_by_type = browse_by_type,
        overwrite_log=False,
    )
    #print(ob.__dict__)
    asyncio.run(ob.download(4))
      
    
if __name__ == '__main__':
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #test_scrap_all_author_general_information()
    
    
    test_scrap_all_topic_general_information()