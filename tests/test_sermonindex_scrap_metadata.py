import os 
import sys 
import pathlib

import unittest

from Instrumentum_sanae_doctrinae.scraping import sermonindex_scrap_metadata
from Instrumentum_sanae_doctrinae.scraping import scrap_metadata



        
        

def test_topic():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_metadata.GetTopicList(root_folder)
    ob.scrap_and_write()

def test_scripture():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_metadata.GetScriptureList(root_folder)
    ob.scrap_and_write()

def test_christian_book():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_metadata.GetChristianBookList(root_folder)
    ob.scrap_and_write()


def test_audio_sermon_speaker():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_metadata.GetAudioSermonSpeakerList(root_folder)
    ob.scrap_and_write()

def test_text_sermon_speaker():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_metadata.GetTextSermonSpeakerList(root_folder)
    ob.scrap_and_write()

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



def test_scrap_all_author_main_info_sermoindex():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    url = "https://www.sermonindex.net/modules/mydownloads/"
    material_folder = "audio_sermon"
    browse_by_type = "speaker"
    ob = sermonindex_scrap_metadata.SermonIndexAudioSermonAllAuthorMainInformation(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    ob.download(50)
    ob.update_downloaded_and_to_download()
    ob.write_log_file()
    

def test_scrap_all_topic_main_info_sermoindex():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    material_folder = "audio_sermon"
    browse_by_type = "topic"
    ob = sermonindex_scrap_metadata.SermonIndexAudioSermonAllTopicMainInformation(
        root_folder,
        material_folder,
        browse_by_type,
        overwrite_log=True
    )    
    ob.download(100)
    ob.update_downloaded_and_to_download()
    ob.write_log_file()


def test_scrap_all_scripture_main_info_sermoindex():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    material_folder = "audio_sermon"
    browse_by_type = "scripture"
    ob = sermonindex_scrap_metadata.SermonIndexAudioSermonAllScriptureMainInformation(
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
    ob = sermonindex_scrap_metadata.SermonIndexAudioSermonAllScriptureMainInformation(
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
    
    test_topic()
    test_scripture()
    test_audio_sermon_speaker()
    test_text_sermon_speaker()
    test_video_sermon_speaker()
    test_vintage_image_sermon_speaker()
    #test_scrap_all_topic_main_info_sermoindex()
    #test_scrap_all_scripture_main_info_sermoindex()
    
       