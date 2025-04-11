import asyncio
import sys 
import os 

from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_scrap_general_information

root_folder = os.path.join(os.getcwd(),'test_folder')

def test_scrap_all_scripture_general_information():
    browse_by_type = "scripture"

    ob = mn_scrap_general_information.MonergismScrapGeneralInformation_ALL(
        root_folder = root_folder,
        browse_by_type = browse_by_type,
        overwrite_log= True,
    )
    print(ob.log_filepath)
    asyncio.run(ob.print_download_informations(True))
    #print(ob.__dict__)
    asyncio.run(ob.download(1))
    

  
    
if __name__ == '__main__':
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #test_scrap_all_author_general_information()
    
    test_scrap_all_scripture_general_information()