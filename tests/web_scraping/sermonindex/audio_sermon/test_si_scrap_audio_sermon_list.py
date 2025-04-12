import os 
import sys 
import pathlib
import asyncio

import unittest

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.audio_sermon import si_audio_sermon_scrap_get_list 
from Instrumentum_sanae_doctrinae.my_tools import my_constants

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import si_scrap_get_speaker_list 

        
root_folder ='/home/elvis/Documents/ForGod/Scraping General/test_folder' 

def test_get_text_sermons_speakers_list():
    ob = si_scrap_get_speaker_list.GetAudioSermonSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())


def test_get_audio_sermon_topic():
        
    ob = si_audio_sermon_scrap_get_list.GetAudioSermonTopicList(
                                                    root_folder,
                                                    browse_by_type=my_constants.TOPIC_NAME)
    
    
    
    asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))

def test_get_audio_sermon_scripture():
    ob = si_audio_sermon_scrap_get_list.GetAudioSermonScriptureList(
                                                    root_folder,
                                                    browse_by_type=my_constants.SCRIPTURE_NAME)
    asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))
    

def test_get_audio_sermon_podcast():
    ob = si_audio_sermon_scrap_get_list.GetAudioSermonPodcastList(
                                                    root_folder,
                                                    browse_by_type=my_constants.PODCAST_NAME)
    asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))






# Test for getting the list from drive method 

def test_get_audio_sermon_scripture_list_from_drive():
    ob = si_audio_sermon_scrap_get_list.GetAudioSermonScriptureList(
                                                    root_folder,
                                                    browse_by_type=my_constants.SCRIPTURE_NAME)
    #asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))
    
    print(ob.get_list_from_local_data())


def test_get_audio_sermon_topic_list_from_drive():
    ob = si_audio_sermon_scrap_get_list.GetAudioSermonTopicList(
                                                    root_folder,
                                                    browse_by_type=my_constants.TOPIC_NAME)
    #asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))
    
    print(ob.get_list_from_local_data())


def test_get_text_sermons_speakers_list_from_drive():
    ob = si_scrap_get_speaker_list.GetAudioSermonSpeakerList(root_folder)
    print(ob.get_list_from_local_data())
    

    

if __name__ == "__main__":
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
     
     
    test_get_audio_sermon_topic_list_from_drive()
    
    
    #test_get_audio_sermon_topic()
    #test_get_audio_sermon_scripture()
    #test_get_audio_sermon_podcast()