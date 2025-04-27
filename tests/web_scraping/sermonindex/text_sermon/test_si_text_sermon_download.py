import asyncio
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.text_sermon import si_text_sermon_christianbook_download  
import aiohttp
import sys
from Instrumentum_sanae_doctrinae.my_tools import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.text_sermon import si_text_sermon_speaker_download     


root_folder ='/media/elvis/Seagate Desktop Drive/Sanae_Doctrinae_Vault' 

def test_text_sermon_speaker_download():
    
    async def d():
        
        browse_by_type = my_constants.SPEAKER_NAME
        material_type = my_constants.SERMONINDEX_TEXT
        ob = si_text_sermon_speaker_download.SI_Download_Speaker_ListOfTextWork(
            "A Collection of Hymns",
            material_type,
            root_folder,
            browse_by_type,
            overwrite_log=False
        )
        await ob.init_aiohttp_session()
        await ob.init_log_data()
        await ob.update_downloaded_and_to_download_from_drive(add_not_found_404_elements=True)
        #print("Elvis",len(ob.log_file_content["to_download"].keys()))
        await ob.download(10)
    
    asyncio.run(d())
    

def test_text_sermon_christiabook_download():
    
    async def d():
        
        browse_by_type = my_constants.SERMONINDEX_CHRISTIAN_BOOKS_NAME
        material_type = my_constants.SERMONINDEX_TEXT
        ob = si_text_sermon_christianbook_download.SI_Download_ChristianBooks_ListOfTextWork(
            "Albert Barnes - Barnes New Testament Notes",
            material_type,
            root_folder,
            browse_by_type,
            overwrite_log=False
        )
        #print(ob.__dict__)
        await ob.init_aiohttp_session()
        await ob.init_log_data()
        await ob.update_downloaded_and_to_download_from_drive(True)
        await ob.print_download_informations()
        await ob.download(50)
        
        ob.write_log_file()
        await ob.close_aiohttp_session()
    
    asyncio.run(d())


    
if __name__ == "__main__":
    test_text_sermon_speaker_download()