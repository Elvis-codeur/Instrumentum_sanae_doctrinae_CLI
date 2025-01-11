import asyncio
import sys 


from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_download



def test_download():
    root_folder ='D:/projet_github/FOR GOD/Scraping general/test_folder'
    browse_by_type = "speaker"
    name = "Archibald Alexander"
    ob = mn_download.MN_Download_Work(name,root_folder,browse_by_type)
    #print("Elvis")
    async def init_and_download():
        await ob.init_aiohttp_session()
        await ob.init_log_data()
        await ob.download(10)
        #await ob.update_downloaded_and_to_download()
        #await ob.update_log_data()
        await ob.close_aiohttp_session()

        
    asyncio.run(init_and_download())
    


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    test_download()