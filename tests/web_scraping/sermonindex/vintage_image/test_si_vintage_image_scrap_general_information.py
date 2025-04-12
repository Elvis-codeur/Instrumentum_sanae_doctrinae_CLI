import asyncio
import sys
from Instrumentum_sanae_doctrinae.my_tools import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import si_scrap_general_information
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.text_sermon import si_text_sermon_scrap_general_information






###################################
###################################
###################################
###################################
###################################
###################################

root_folder ='/home/elvis/Documents/ForGod/Scraping General/test_folder' 


# Text sermon speakers 
def test_vintage_image_scrap_all_speaker_main_info_sermoindex():
    material_folder = my_constants.SERMONINDEX_VINTAGE_IMAGE_ROOT_FOLDER
    browse_by_type = my_constants.SPEAKER_NAME
    ob = si_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    #print(ob.__dict__)
    asyncio.run(ob.download(2))
    ob.write_log_file()
    

if __name__ == '__main__':
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    test_vintage_image_scrap_all_speaker_main_info_sermoindex()