import asyncio
import os
import sys 


from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_download


root_folder = os.path.join(os.getcwd(),'test_folder')



def test_download():
    browse_by_type = "scripture"
    name = "1 Samuel"
    ob = mn_download.MN_Download_Work(name,root_folder,browse_by_type,
                                      overwrite_log=False,update_log=True)
    #asyncio.run(ob.init_log_data())
    #print(ob.log_file_content["downloaded"])
    
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