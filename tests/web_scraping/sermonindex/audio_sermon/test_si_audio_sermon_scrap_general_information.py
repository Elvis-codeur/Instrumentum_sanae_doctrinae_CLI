import asyncio
import sys
from Instrumentum_sanae_doctrinae.my_tools import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import si_scrap_general_information


root_folder ='/home/elvis/Documents/ForGod/Scraping General/test_folder' 


# Test on one author 
def test_scrap_author_work():
    url = "https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=topicSermons&topic=Brainerd&page=0"
    name = "Brainerd"
    ob = si_scrap_general_information.SermonIndexScrapGeneralInformation(
        name=name,root_folder=root_folder,
        browse_by_type="topic",url_list=[url],
        material_root_folder=my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,intermdiate_folders=[],
    )
    #print(ob.__dict__)
    
    print(asyncio.run(ob.is_data_downloaded()))
    
    asyncio.run(ob.scrap_and_write())
    
    
def test_scrap_topic_work():
    url = "https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=topicSermons&topic=Brainerd&page=0"
    name = "Brainerd"
    ob = si_scrap_general_information.SermonIndexScrapGeneralInformation(
        name=name,root_folder=root_folder,
        browse_by_type="topic",url_list=[url],
        material_root_folder=my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,intermdiate_folders=[],
    )
    #print(ob.__dict__)
    
    print(asyncio.run(ob.is_data_downloaded()))
    
    asyncio.run(ob.scrap_and_write())
  
  
def test_scrap_scripture_work():
    url = "https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=bookSermons&book=Genesis&page=0"
    name = "Genesis"
    ob = si_scrap_general_information.SermonIndexScrapGeneralInformation(
        name=name,root_folder=root_folder,
        browse_by_type="scripture",url_list=[url],
        material_root_folder=my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,intermdiate_folders=[],
    )
    #print(ob.__dict__)
    
    print(asyncio.run(ob.is_data_downloaded()))
    
    asyncio.run(ob.scrap_and_write())  
    

# Get the main information for Audio sermons 
# This include the speakers, the topics, the podcasts and scriptures




###################################
###################################
###################################
###################################
###################################
###################################

# Audio sermon speakers
def test_scrap_all_audio_sermon_author_main_info_sermoindex():
    material_folder = my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
    browse_by_type = my_constants.SPEAKER_NAME
    ob = si_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=False
    )   
    asyncio.run(ob.update_downloaded_and_to_download_from_drive(True)) 
    asyncio.run(ob.download(2))
    ob.write_log_file()

# Audio sermon topics 
def test_scrap_all_audio_sermon_topic_main_info_sermoindex():
    material_folder = my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
    browse_by_type = my_constants.TOPIC_NAME
    ob = si_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    asyncio.run(ob.download(2))
    ob.write_log_file()
    

# Audio sermon scriptures 
def test_scrap_all_audio_sermon_scripture_main_info_sermoindex():
    material_folder = my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
    browse_by_type = my_constants.SCRIPTURE_NAME
    ob = si_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    #asyncio.run(ob.download(2))
    #ob.write_log_file()
    print(asyncio.run(ob.update_downloaded_and_to_download_from_drive(True)))


if __name__ == '__main__':
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    test_scrap_all_audio_sermon_scripture_main_info_sermoindex()