import os 
import sys 
import pathlib

import unittest

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import sermonindex_scrap_general_information
from Instrumentum_sanae_doctrinae.web_scraping import scrap_metadata
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import sermonindex_scrap_get_list 









def test_get_all_audio_sermon_speaker():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_get_list.GetAudioSermonSpeakerList(root_folder)
    ob.scrap_and_write()

def test_text_sermon_speaker():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_metadata.GetTextSermonSpeakerList(root_folder)
    ob.scrap_and_write()

def test_text_sermon_christian_book():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_metadata.GetTextSermonsChristianBook(root_folder)
    ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list)

def test_video_sermon_speaker():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_metadata.GetVideoSermonSpeakerList(root_folder)
    ob.scrap_and_write()

def test_vintage_image_sermon_speaker():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_metadata.GetVintageImageSpeakerList(root_folder)
    ob.scrap_and_write()



def test_scrap_author_work():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    url = "https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=1"
    name = "Leonard Ravenhill"
    ob = sermonindex_scrap_metadata.SermonIndexAudioSermonScrapAuthorMainInformation(
        name,root_folder,url
    )

    ob.scrap_and_write()















def test_scrap_all_audio_sermon_author_main_info_sermoindex():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    url = "https://www.sermonindex.net/modules/mydownloads/"
    material_folder = "audio_sermon"
    browse_by_type = "speaker"
    ob = sermonindex_scrap_metadata.SermonIndexScrapWebSiteAllAuthorTopicScripturesMainInformation(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    ob.download(100)
    ob.update_downloaded_and_to_download()
    ob.write_log_file()
    

def test_scrap_all_audio_sermon_topic_main_info_sermoindex():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    material_folder = "audio_sermon"
    browse_by_type = "topic"
    ob = sermonindex_scrap_metadata.SermonIndexScrapWebSiteAllAuthorTopicScripturesMainInformation(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    ob.download(100)
    ob.update_downloaded_and_to_download()
    ob.write_log_file()


def test_scrap_all_audio_sermon_scripture_main_info_sermoindex():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    material_folder = "audio_sermon"
    browse_by_type = "scripture"
    ob = sermonindex_scrap_metadata.SermonIndexScrapWebSiteAllAuthorTopicScripturesMainInformation(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    ob.download(30)
    ob.update_downloaded_and_to_download()
    ob.write_log_file()



def test_text_sermon_scrap_all_speaker_main_info_sermoindex():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    material_folder = "text_sermon"
    browse_by_type = "speaker"
    ob = sermonindex_scrap_metadata.SermonIndexScrapWebSiteAllAuthorTopicScripturesMainInformation(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    ob.download(100)
    ob.update_downloaded_and_to_download()
    ob.write_log_file()

def test_video_sermon_scrap_all_speaker_main_info_sermoindex():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    material_folder = "video_sermon"
    browse_by_type = "speaker"
    ob = sermonindex_scrap_metadata.SermonIndexScrapWebSiteAllAuthorTopicScripturesMainInformation(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    ob.download(100)
    ob.update_downloaded_and_to_download()
    ob.write_log_file()


def test_vintage_image_scrap_all_speaker_main_info_sermoindex():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    material_folder = "vintage_image"
    browse_by_type = "speaker"
    ob = sermonindex_scrap_metadata.SermonIndexScrapWebSiteAllAuthorTopicScripturesMainInformation(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    ob.download(100)
    ob.update_downloaded_and_to_download()
    ob.write_log_file()



def test_audio_sermon_get_scripture_work():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    material_folder = "audio_sermon"
    browse_by_type = "scripture"
    ob = sermonindex_scrap_metadata.SermonIndexScrapWebSiteAllAuthorTopicScripturesWork(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )
    
    ob.download(30)
    ob.update_downloaded_and_to_download()
    ob.write_log_file()
    

if __name__ == "__main__":
    #print("Elvs")
    
    #test_audio_sermon_topic()
    #test_audio_sermon_scripture()
    #test_audio_sermon_christian_book()
    #test_audio_sermon_podcast()

    #test_audio_sermon_speaker()
    #test_text_sermon_speaker()
    #test_text_sermon_christian_book()
    #test_video_sermon_speaker()
    #test_vintage_image_sermon_speaker()
    
    #test_scrap_all_audio_sermon_author_main_info_sermoindex()
    #test_scrap_all_audio_sermon_scripture_main_info_sermoindex()
    #test_scrap_all_audio_sermon_topic_main_info_sermoindex()
    #test_vintage_image_scrap_all_speaker_main_info_sermoindex()
    test_get_all_audio_sermon_speaker()