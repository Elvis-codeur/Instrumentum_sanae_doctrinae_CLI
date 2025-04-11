import asyncio
import os
import sys 

import logging
logging.basicConfig(level=logging.DEBUG)

from Instrumentum_sanae_doctrinae.web_scraping.monergism.mn_scrap_work_base import MN_ScrapSpeakerTopicScriptureWork_All
from Instrumentum_sanae_doctrinae.web_scraping.monergism.scripture import mn_scrap_scripture_works

root_folder = os.path.join(os.getcwd(),'test_folder')

def test_scrap_all_scripture_work():
    
    browse_by_type = "scripture"
     
    ob = MN_ScrapSpeakerTopicScriptureWork_All(
        root_folder=root_folder,
        browse_by_type=browse_by_type,
        overwrite_log=False,
    )
       
    
    
    async def run_ob():
        # Init the log informations 
        await ob.init_log_data() 
        
        # Update before the begining of downloads
        #await ob.update_downloaded_and_to_download_from_drive(add_not_found_404_elements = True) 
        
        await ob.print_download_informations(check_from_file=True)
        #await ob.download(1)
        await ob.download_from_element_key_list(["Daniel"],1)
    
    asyncio.run(run_ob())
    

if __name__ == "__main__":
    
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
     
    test_scrap_all_scripture_work()
    