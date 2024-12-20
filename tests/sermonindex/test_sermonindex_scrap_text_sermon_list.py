
import asyncio
import sys
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import sermonindex_text_sermon_scrap_get_list


def test_get_text_sermon_books():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder' 
    url = "https://www.sermonindex.net/modules/bible_books/?view=books_list"
    
    ob = sermonindex_text_sermon_scrap_get_list.GetTextSermonsChristianBook(
                                                    root_folder,
                                                    url)
    
    asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))


if __name__ == "__main__":
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    test_get_text_sermon_books()