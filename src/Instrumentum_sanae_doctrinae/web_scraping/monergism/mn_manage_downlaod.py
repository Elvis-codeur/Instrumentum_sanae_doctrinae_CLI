import asyncio
import pathlib

from Instrumentum_sanae_doctrinae.my_tools.general_tools import read_json
from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_download
from Instrumentum_sanae_doctrinae.web_scraping.monergism.mn_tools import *


class ManageDownload():
    def __init__(self,root_folder,browse_by_type, *args, **kwds):
        self.root_folder = root_folder
        self.browse_by_type = browse_by_type
        
        self.input_root_folder = os.path.join(root_folder,
                                         my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.MONERGISM_NAME,
                                         my_constants.ELABORATED_DATA_FOLDER,
                                         browse_by_type,
                                         my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER,
                                           
                                         )
        
        self.input_files_content = []
        
    def load_input_file_content(self):
        input_filepath_list = [path for path in 
                             pathlib.Path(self.input_root_folder).rglob("*.json")]
        
        for filepath in input_filepath_list:
            file_content = read_json(filepath)
            
            self.input_files_content += file_content.get("data")
            
        
        
    def download(self,overwrite_log=False,update_log=True):
        for element in self.input_files_content:
            name = element.get("name")
            
            ob = mn_download.MN_Download_Work(name,self.root_folder,self.browse_by_type,
                                      overwrite_log = overwrite_log,update_log = update_log)

            print("\n\n Begin Downlaod ======= ",name, " ========")
            async def init_and_download():
                await ob.init_aiohttp_session()
                await ob.init_log_data()
            
                await ob.download(10)
                #await ob.update_downloaded_and_to_download()
                #await ob.update_log_data()
                await ob.close_aiohttp_session()
            
            asyncio.run(init_and_download())
                

        
        