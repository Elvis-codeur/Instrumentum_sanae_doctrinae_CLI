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
    url = "https://www.monergism.com/search?f[0]=author:34468" 
    ob = monergism_scrap_metadata.MonergismScrapAuthorTopicScriptureMainPage(
        name = "C H Spurgeon",
        root_folder = root_folder,
        url = url,
        browse_by_type="speaker"
    )
    ob.scrap_and_write()


def test_scrap_topic_main_information():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    url = "https://www.monergism.com/topics/abraham" 
    ob = monergism_scrap_metadata.MonergismScrapAuthorTopicScriptureMainPage(
        "Abraham",root_folder,url
    )
    ob.scrap_and_write()


def test_scrap_scriptures_main_information():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    url = "https://www.monergism.com/topics/abraham" 
    ob = monergism_scrap_metadata.MonergismScrapAuthorTopicScriptureMainPage(
        name = "Abraham",
        root_folder = root_folder,
        url = url,
        browse_by_type="s"
    )
    ob.scrap_and_write()


if __name__ == "__main__":
    #print("Elvs")
    url_topics = "https://www.monergism.com/topics"
    url_authors = "https://www.monergism.com/authors"
    #test_speakers()
    #test_topic()
    #test_scripture()
    test_scrap_author_main_information()
