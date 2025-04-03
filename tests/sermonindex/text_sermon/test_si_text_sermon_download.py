import asyncio
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.text_sermon import si_text_sermon_christianbook_download  
import aiohttp
import sys
from Instrumentum_sanae_doctrinae.web_scraping import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.text_sermon import si_text_sermon_speaker_download     


root_folder ='/home/elvis/Documents/ForGod/Scraping General/test_folder' 

def test_text_sermon_speaker_download():
    
    async def d():
        
        browse_by_type = my_constants.SPEAKER_NAME
        material_type = my_constants.SERMONINDEX_TEXT
        ob = si_text_sermon_speaker_download.SI_Download_Speaker_ListOfTextWork(
            "C.H. Spurgeon",
            material_type,
            root_folder,
            browse_by_type,
            overwrite_log=True
        )
        await ob.init_aiohttp_session()
        await ob.init_log_data()
        print(ob.__dict__)
        await ob.download(1)
    
    asyncio.run(d())
    

def test_text_sermon_christiabook_download():
    
    async def d():
        
        browse_by_type = my_constants.SERMONINDEX_CHRISTIAN_BOOKS_NAME
        material_type = my_constants.SERMONINDEX_TEXT
        ob = si_text_sermon_christianbook_download.SI_Download_ChristianBooks_ListOfTextWork(
            "Albert Taylor Bledsoe - A Theodicy Or Vindication Of The Divine Glory",
            material_type,
            root_folder,
            browse_by_type,
            overwrite_log=True
        )
        await ob.init_aiohttp_session()
        await ob.init_log_data()
        #print(ob.__dict__)
        await ob.download(1)
    
    asyncio.run(d())


    
if __name__ == "__main__":
    test_text_sermon_christiabook_download()