import asyncio
import sys
from Instrumentum_sanae_doctrinae.my_tools import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.audio_sermon import si_audio_sermon_scrap_work 


root_folder ='/home/elvis/Documents/ForGod/Scraping General/test_folder' 

def test_audio_sermon_get_speaker_work():
    material_folder = my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
    browse_by_type = my_constants.SPEAKER_NAME
    ob = si_audio_sermon_scrap_work.SI_ScrapAudioSermonWork_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )
 
    
    #print(ob.log_file_content.keys())
    asyncio.run(ob.download_from_element_key_list(["Leonard Ravenhill"],1))
    #ob.update_downloaded_and_to_download()
    #ob.write_log_file()
    
    
def test_is_downloaded_scrap_work():
    url_list = [
            "https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=1",
            "https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=1&min=20&orderby=titleA&show=20",
            "https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=1&min=40&orderby=titleA&show=20",
            "https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=1&min=60&orderby=titleA&show=20",
            "https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=1&min=80&orderby=titleA&show=20",
            "https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=1&min=100&orderby=titleA&show=20",
    ]
    
    ob = si_audio_sermon_scrap_work.SI_AudioSermonWork(
            name = "Leonard Ravenhill",
            root_folder = root_folder,
            browse_by_type ="speaker",
            url_list = url_list,
            intermdiate_folders = [],
            material_root_folder = "audio_sermon"
        )
    
    async def f():
        print([i.get("connect_to_url") for i in  ob.url_informations.values()])
        print (await ob.is_data_downloaded())
        print([i.get("connect_to_url") for i in  ob.url_informations.values()])
        await ob.scrap_and_write()
        
    asyncio.run(f())
    

def test_audio_sermon_get_topic_work():
    material_folder = my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
    browse_by_type = my_constants.TOPIC_NAME
    ob = si_audio_sermon_scrap_work.SI_ScrapAudioSermonWork_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )
    #print(ob.__dict__)
    asyncio.run(ob.download(2))
    #ob.update_downloaded_and_to_download()
    #ob.write_log_file()
    

def test_audio_sermon_get_scripture_work():
    material_folder = my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
    browse_by_type = my_constants.SCRIPTURE_NAME
    ob = si_audio_sermon_scrap_work.SI_ScrapAudioSermonWork_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )
    #print(ob.__dict__)
    asyncio.run(ob.download(2))
    #ob.update_downloaded_and_to_download()
    #ob.write_log_file()

def test_audio_sermon_get_podcast_work():
    material_folder = my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
    browse_by_type = my_constants.PODCAST_NAME
    ob = si_audio_sermon_scrap_work.SI_ScrapAudioSermonWork_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )
    #print(ob.__dict__)
    asyncio.run(ob.download(2))
    #ob.update_downloaded_and_to_download()
    #ob.write_log_file()
    
if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    test_is_downloaded_scrap_work()