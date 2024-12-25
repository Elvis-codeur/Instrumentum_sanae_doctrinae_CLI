import asyncio
import sys
from Instrumentum_sanae_doctrinae.web_scraping import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.text_sermon import si_text_sermon_scrap_get_list


def test_get_text_sermons_speakers():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = si_text_sermon_scrap_get_list.GetTextSermonSpeakerList(root_folder)
    ob.scrap_and_write()
    
    
def test_get_text_sermons_christian_books():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = si_text_sermon_scrap_get_list.GetTextSermonsChristianBook(root_folder)
    ob.scrap_and_write()
    