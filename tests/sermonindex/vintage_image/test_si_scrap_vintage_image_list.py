import asyncio
import sys
from Instrumentum_sanae_doctrinae.web_scraping import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.vintage_image import si_vin_im_scrap_get_list


def test_get_vintage_image_sermons_speakers_list():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = si_vin_im_scrap_get_list.GetVintageImageSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())
      
    
if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    test_get_vintage_image_sermons_speakers_list()