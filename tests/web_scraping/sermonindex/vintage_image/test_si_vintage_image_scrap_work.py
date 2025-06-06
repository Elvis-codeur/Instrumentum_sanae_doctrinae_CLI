import asyncio
import sys
from Instrumentum_sanae_doctrinae.my_tools import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.vintage_image import  si_vin_im_scrap_work


root_folder ='/home/elvis/Documents/ForGod/Scraping General/test_folder' 

def test_vintage_image_get_speaker_work():
    material_folder = my_constants.SERMONINDEX_VINTAGE_IMAGE_ROOT_FOLDER
    browse_by_type = my_constants.SPEAKER_NAME
    ob = si_vin_im_scrap_work.SI_ScrapVintageImageWork_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )
    #print(ob.meta_informations["input_files_information"]["input_files"])
    #print(ob.__dict__)
    asyncio.run(ob.download(2))
    #ob.update_downloaded_and_to_download()
    #ob.write_log_file()
    


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    test_vintage_image_get_speaker_work()