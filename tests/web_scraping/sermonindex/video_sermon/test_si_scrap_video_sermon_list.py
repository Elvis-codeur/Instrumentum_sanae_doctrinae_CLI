import asyncio
import sys
from Instrumentum_sanae_doctrinae.my_tools import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import si_scrap_get_speaker_list

root_folder ='/home/elvis/Documents/ForGod/Scraping General/test_folder' 


def test_get_video_sermons_speakers_list():
    ob = si_scrap_get_speaker_list.GetVideoSermonSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())
    
def test_get_video_sermons_speakers_list_from_drive():
    ob = si_scrap_get_speaker_list.GetVideoSermonSpeakerList(root_folder)
    print(ob.get_list_from_local_data())
      
    
if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    test_get_video_sermons_speakers_list_from_drive()