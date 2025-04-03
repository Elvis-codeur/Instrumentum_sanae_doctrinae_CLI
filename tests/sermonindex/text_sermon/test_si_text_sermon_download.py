import asyncio
import aiohttp
import sys
from Instrumentum_sanae_doctrinae.web_scraping import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.text_sermon import si_text_sermon_speaker_download     


root_folder ='/home/elvis/Documents/ForGod/Scraping General/test_folder' 

def test_audio_sermon_get_speaker_work():
    
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

    """
    data = {
        "url": "https://www.sermonindex.net/modules/articles/index.php?view=article&aid=1340",
        "link_text": "\"Alas For Us, If Thou Wert All, and Nought Beyond, O Earth\""
    }
    
    async with aiohttp.ClientSession() as session:
        ob = si_text_sermon_speaker_download.DownloadTextSermonSpeaker(
            url=data.get("url"),
            output_folder=root_folder,
            output_file_name=data.get("link_text"),
            separe_file_based_on_format=True,
            aiohttp_session=session
        )
        await ob.download()
        print(ob.__dict__)
    """
    
    
    #print(ob.log_file_content.keys())
    #asyncio.run(ob.download_from_element_key_list([],1))
    #ob.update_downloaded_and_to_download()
    #ob.write_log_file()
    
if __name__ == "__main__":
    test_audio_sermon_get_speaker_work()