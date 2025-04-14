import asyncio
import sys
from Instrumentum_sanae_doctrinae.my_tools import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.audio_sermon import si_audio_sermon_download 


root_folder ='/home/elvis/Documents/ForGod/Scraping General/test_folder' 

def test_audio_sermon_get_speaker_work():
    
    async def d():
        
        browse_by_type = my_constants.SPEAKER_NAME
        material_type = my_constants.SERMONINDEX_AUDIO
        ob =si_audio_sermon_download.SI_Download_ListOfAudioWork(
            "A.W. Tozer",
            material_type,
            root_folder,
            browse_by_type,
            overwrite_log=True
        )
        await ob.init_aiohttp_session()
        await ob.init_log_data()
        await ob.download(1)
        
    asyncio.run(d())
    
    
    #print(ob.log_file_content.keys())
    #asyncio.run(ob.download_from_element_key_list([],1))
    #ob.update_downloaded_and_to_download()
    #ob.write_log_file()
    
if __name__ == "__main__":
    test_audio_sermon_get_speaker_work()