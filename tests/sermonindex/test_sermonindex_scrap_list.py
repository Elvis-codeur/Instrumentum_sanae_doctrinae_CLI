import os 
import sys 
import pathlib
import asyncio

import unittest

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import sermonindex_audio_sermon_scrap_get_list 
from Instrumentum_sanae_doctrinae.web_scraping import my_constants 

        

def test_get_audio_sermon_topic():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
        
    ob = sermonindex_audio_sermon_scrap_get_list.GetAudioSermonTopicList(
                                                    root_folder,
                                                    browse_by_type=my_constants.TOPIC_NAME)
    
    asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))

def test_get_audio_sermon_scripture():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_audio_sermon_scrap_get_list.GetAudioSermonScriptureList(
                                                    root_folder,
                                                    browse_by_type=my_constants.SCRIPTURE_NAME)
    asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))


def test_get_audio_sermon_podcast():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_audio_sermon_scrap_get_list.GetAudioSermonPodcastList(
                                                    root_folder,
                                                    browse_by_type=my_constants.PODCAST_NAME)
    asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))

if __name__ == "__main__":
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
     
    test_get_audio_sermon_topic()
    test_get_audio_sermon_scripture()
    test_get_audio_sermon_podcast()