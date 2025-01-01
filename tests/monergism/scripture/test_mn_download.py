import asyncio
import sys 


from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_download



def test_download():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "scripture"
    name = "Genesis"
    ob = mn_download.MN_Download_Work(name,root_folder,browse_by_type)
    ob.update_downloaded_and_to_download()
    asyncio.run(ob.download(4))


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    test_download()