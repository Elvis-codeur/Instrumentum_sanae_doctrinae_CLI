import asyncio
import sys
from Instrumentum_sanae_doctrinae.web_scraping import my_constants

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.text_sermon import si_text_sermon_scrap_get_list
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import si_scrap_get_speaker_list


def test_get_text_sermons_speakers_list():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = si_scrap_get_speaker_list.GetTextSermonSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())
    
    
def test_get_text_sermons_christian_books_list():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = si_text_sermon_scrap_get_list.GetTextSermonsChristianBook(root_folder)
    asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))
    
    
if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    test_get_text_sermons_speakers_list()