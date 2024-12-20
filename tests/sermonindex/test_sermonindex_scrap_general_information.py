import asyncio
import sys
from Instrumentum_sanae_doctrinae.web_scraping import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import sermonindex_scrap_general_information

def test_scrap_author_work():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    url = "https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=1"
    name = "Leonard Ravenhill"
    ob = sermonindex_scrap_general_information.SermonIndexScrapGeneralInformation(
        name=name,root_folder=root_folder,
        browse_by_type="speaker",url_list=[url],
        material_root_folder=my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,intermdiate_folders=[],
    )
    print(ob.__dict__)
    
    asyncio.run(ob.scrap_and_write())
    


def test_scrap_all_audio_sermon_author_main_info_sermoindex():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    material_folder = my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
    browse_by_type = my_constants.SPEAKER_NAME
    ob = sermonindex_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    asyncio.run(ob.download(100))
    ob.update_downloaded_and_to_download()
    ob.write_log_file()
    

def test_text_sermon_scrap_all_speaker_main_info_sermoindex():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    material_folder = my_constants.SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER
    browse_by_type = my_constants.SPEAKER_NAME
    ob = sermonindex_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    asyncio.run(ob.download(100))
    ob.update_downloaded_and_to_download()
    ob.write_log_file()

def test_video_sermon_scrap_all_speaker_main_info_sermoindex():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    material_folder = my_constants.SERMONINDEX_VIDEO_SERMONS_ROOT_FOLDER
    browse_by_type = my_constants.SPEAKER_NAME
    ob = sermonindex_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    asyncio.run(ob.download(100))
    ob.update_downloaded_and_to_download()
    ob.write_log_file()


def test_vintage_image_scrap_all_speaker_main_info_sermoindex():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    material_folder = my_constants.SERMONINDEX_VINTAGE_IMAGE_ROOT_FOLDER
    browse_by_type = my_constants.SPEAKER_NAME
    ob = sermonindex_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    asyncio.run(ob.download(100))
    ob.update_downloaded_and_to_download()
    ob.write_log_file()

if __name__ == '__main__':
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    test_video_sermon_scrap_all_speaker_main_info_sermoindex()