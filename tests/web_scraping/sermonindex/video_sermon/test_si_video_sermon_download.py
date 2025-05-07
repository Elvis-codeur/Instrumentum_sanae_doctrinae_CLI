import asyncio
import sys
from Instrumentum_sanae_doctrinae.my_tools import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.video_sermon import si_video_sermon_download   


root_folder ='/media/elvis/Seagate Desktop Drive/Sanae_Doctrinae_Vault'

def test_video_sermon_download():
    
    async def d():
        
        browse_by_type = my_constants.SPEAKER_NAME
        material_type = my_constants.SERMONINDEX_VIDEO
        ob = si_video_sermon_download.SI_Download_ListOfVideoWork(
            "Carter Conlon",
            material_type,
            root_folder,
            browse_by_type,
            overwrite_log=False
        )
        await ob.init_aiohttp_session()
        await ob.init_log_data()
        await ob.update_downloaded_and_to_download_from_drive(True)
        print(len(ob.log_file_content["to_download"]))
        print(len(ob.log_file_content["downloaded"]))
        print(len(ob.log_file_content["not_found_404"]))
        await ob.download(1)
        await ob.close_aiohttp_session()
        
        
    asyncio.run(d())
    
    
    #print(ob.log_file_content.keys())
    #asyncio.run(ob.download_from_element_key_list([],1))
    #ob.update_downloaded_and_to_download()
    #ob.write_log_file()
    
if __name__ == "__main__":
    test_video_sermon_download()