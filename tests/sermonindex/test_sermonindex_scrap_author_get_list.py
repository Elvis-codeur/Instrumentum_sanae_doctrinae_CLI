import asyncio
import sys


from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import sermonindex_scrap_get_speaker_list


def test_audio_sermon_get_all_speaker():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_get_speaker_list.GetAudioSermonSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())

def test_text_sermon_get_all_speaker():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_get_speaker_list.GetTextSermonSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())
    

def test_video_sermon_get_all_speaker():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_get_speaker_list.GetVideoSermonSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())
    

def test_vintage_image_sermon_get_all_speaker():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = sermonindex_scrap_get_speaker_list.GetVintageImageSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())
    


if __name__ == "__main__":
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    test_vintage_image_sermon_get_all_speaker()