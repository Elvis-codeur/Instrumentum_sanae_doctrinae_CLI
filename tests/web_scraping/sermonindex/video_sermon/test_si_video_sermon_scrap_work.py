import asyncio
import sys
from Instrumentum_sanae_doctrinae.my_tools import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.video_sermon import  si_video_sermon_scrap_work

root_folder ='/home/elvis/Documents/ForGod/Scraping General/test_folder' 

def test_video_sermon_get_speaker_work():
    material_folder = my_constants.SERMONINDEX_VIDEO_SERMONS_ROOT_FOLDER
    browse_by_type = my_constants.SPEAKER_NAME
    ob = si_video_sermon_scrap_work.SI_ScrapVideoSermonWork_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )
    #print(ob.__dict__)
    asyncio.run(ob.download_from_element_key_list(["Zac Poonen"],1))
    
    #ob.update_downloaded_and_to_download()
    #ob.write_log_file()
    


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    test_video_sermon_get_speaker_work()