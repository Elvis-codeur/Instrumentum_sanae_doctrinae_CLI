import os 
import sys 
import pathlib

import unittest

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import sermonindex_scrap_general_information
from Instrumentum_sanae_doctrinae.web_scraping import scrap_metadata
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import sermonindex_scrap_get_speaker_list 



    

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