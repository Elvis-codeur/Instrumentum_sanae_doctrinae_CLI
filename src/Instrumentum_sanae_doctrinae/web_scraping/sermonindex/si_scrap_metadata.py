
from concurrent.futures import ThreadPoolExecutor
import json
import os 
import urllib
import urllib.parse
import pathlib
import traceback

from bs4 import BeautifulSoup
import requests

from Instrumentum_sanae_doctrinae.web_scraping import http_connexion



from Instrumentum_sanae_doctrinae.web_scraping import scrap_metadata
from Instrumentum_sanae_doctrinae.my_tools import my_constants
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools




def get_sermonindex_metadata_and_log_folder(root_folder,material_root_folder):
    metadata_root_folder = os.path.join(root_folder,
                            my_constants.SERMONINDEX_METADATA_ROOT_FOLDER,
                            material_root_folder)
    
    log_root_folder = os.path.join(root_folder,
                            my_constants.SERMONINDEX_LOG_ROOT_FOLDER,
                            material_root_folder)
    
    return metadata_root_folder,log_root_folder


def get_sermonindex_auth_top_scrip_list_json_filepath(root_folder,material_root_folder,browse_by_type):
    metadata_root_folder,_ = get_sermonindex_metadata_and_log_folder(root_folder,material_root_folder)
    
    return os.path.join(metadata_root_folder,my_constants.ELABORATED_DATA_FOLDER,browse_by_type,
                        f"{browse_by_type}_list",my_constants.get_default_json_filename(0))




# The classes here are not intended to scrap the list of the authors, or the list of topics. They 
# intended to scrap the work of a given author, topic, or the podcasts

class SermonIndexScrapAuthorTopicScripturePage(scrap_metadata.ScrapAuthorTopicScripturePage):
    def __init__(self,name, root_folder,url,browse_by_type,material_root_folder,information_type_root_folder,intermdiate_folders=None) -> None:
        """
        :param name: The name of the author, topic, ...
        :param root_folder: The folder where the logs, metadata download and more will be stored 
        :url: The url of the page to connect to and scrap the information 
        :browse_by_type: On sermonindex, the audio sermons are browseable by speaker, topic, scripture. It is \
        the mean  by which the browsing is made that is required here 
        :param material_root_folder: On sermonindex, there are audio sermons, text sermons, video sermons and \
        vintage image. Each material has his own root folder. See here for more \
        """
        #print(intermdiate_folders)            

        metadata_root_folder,log_root_folder = get_sermonindex_metadata_and_log_folder(root_folder,material_root_folder)
        super().__init__(name,metadata_root_folder,log_root_folder,url,
                         browse_by_type,information_type_root_folder,
                         intermdiate_folders)



    async def is_data_downloaded(self):
        result = True 
        for url in self.url_informations:
            
            is_this_url_data_downloaded = True 
            
            file_path = self.url_informations[url].get("json_filepath")
            #print(url,os.path.exists(file_path))
                        
            if not os.path.exists(file_path):
                result =  False
                is_this_url_data_downloaded = False
            else:
                
                # Here the file_content is a text 
                # I load the file content as text first because some times, there are interruption
                # and the json file is not well written. 
                # Loading it cause error. So I load it as text first and then 
                # I can try to convert it to json later 
                file_content = await _my_tools.async_read_file(file_path)
                
                #print(file_content)
                
                if file_content == "":
                    result =  False
                    is_this_url_data_downloaded = False
                
                try:
                    file_content = json.loads(file_content)

                    if not file_content.get("url"):
                        result =  False
                        is_this_url_data_downloaded = False

                except:
                    result =  False
                    is_this_url_data_downloaded = False
                    
                # If the data of this url is already downloaded, mark so that it may not 
                # be downloaded again
                if is_this_url_data_downloaded == True:
                    self.url_informations[url]["connect_to_url"] = False 
        
        # I make the return outside of the loop to make sure that every url data is checked 
        return result
   
