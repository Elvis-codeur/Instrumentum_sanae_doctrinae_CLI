import os 
import sys 
import pathlib

import unittest

from Instrumentum_sanae_doctrinae.scraping import sermonindex_scrap_get_list

        

def test_audio_sermon_topic():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_get_list.GetAudioSermonTopicList(root_folder)
    ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list)

def test_audio_sermon_scripture():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_get_list.GetAudioSermonScriptureList(root_folder)
    ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list)

def test_audio_sermon_christian_book():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_get_list.GetAudioSermonChristianBookList(root_folder)
    ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list)

def test_audio_sermon_podcast():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_get_list.GetAudioSermonPodcastList(root_folder)
    ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list)

