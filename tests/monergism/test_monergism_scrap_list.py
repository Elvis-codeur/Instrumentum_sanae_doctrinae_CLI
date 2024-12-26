import asyncio
import sys 


from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_scrap_get_list


def test_get_topic_list():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = mn_scrap_get_list.GetTopicList(root_folder)
    asyncio.run(ob.scrap_and_write())

def test_get_speakers_list():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = mn_scrap_get_list.GetSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())


def test_get_scripture_list():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    ob = mn_scrap_get_list.GetScriptureList(root_folder)
    asyncio.run(ob.scrap_and_write())
    
    
if __name__ == "__main__":
    
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    test_get_scripture_list()