import os 
import sys 
import pathlib

import unittest

from Instrumentum_sanae_doctrinae.scraping import monergism_scrap_metadata
        
        

def test_topic():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = monergism_scrap_metadata.GetTopicList(root_folder)
    ob.scrap_and_write()

def test_speakers():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = monergism_scrap_metadata.GetSpeakerList(root_folder)
    ob.scrap_and_write()


def test_scripture():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = monergism_scrap_metadata.GetScriptureList(root_folder)
    ob.scrap_and_write()


def test_scrap_author_main_information():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    url = "https://www.monergism.com/search?f[0]=author:38603" 
    ob = monergism_scrap_metadata.MonergismScrapAuthorTopicScriptureMainPage(
        name = "Tom Ascol",
        root_folder = root_folder,
        url = url,
        browse_by_type="speaker"
    )
    ob.scrap_and_write()

def test_get_author_all_work():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "speaker"
    ob = monergism_scrap_metadata.MonergismScrapWebSiteAllAuthorTopicScripturesWork(
        root_folder,
        browse_by_type,
        overwrite_log=True
    )
    ob.download(1)
    ob.update_downloaded_and_to_download()
    ob.write_log_file()
    





if __name__ == "__main__":
    #print("Elvs")
    url_topics = "https://www.monergism.com/topics"
    url_authors = "https://www.monergism.com/authors"
    #test_speakers()
    #test_topic()
    #test_scripture()
    #test_get_author_all_work()
    url_list = [
        "https://www.monergism.com/search?f[0]=author:38603",
        "https://www.monergism.com/search?f%5B0%5D=author%3A38603&page=1"
    ]
    # root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    # ob = monergism_scrap_metadata.MonergismScrapAuthorTopicScriptureWork(
    #     "Tom Ascol",
    #     root_folder,url_list,
    #     "speaker"
    # )
    # ob.scrap_and_write()
    #test_scrap_author_main_information()
    test_get_author_all_work()