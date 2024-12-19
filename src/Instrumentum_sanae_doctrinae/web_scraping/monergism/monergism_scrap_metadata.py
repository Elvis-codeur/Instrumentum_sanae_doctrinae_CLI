"""
This module is created for the scrapping of metadata from https://www.monergism.com/


"""

import os 
import pathlib
import re
import urllib
import urllib.parse
from urllib.parse import urlparse, parse_qs


from ..scraping import scrap_metadata
from ..scraping import my_constants
from ..scraping import http_connexion
from ..scraping import _my_tools



def get_monergism_metadata_and_log_folder(root_folder):
    metadata_root_folder = os.path.join(root_folder,my_constants.MONERGISM_METADATA_ROOT_FOLDER)
    log_root_folder = os.path.join(root_folder,my_constants.MONERGISM_LOG_ROOT_FOLDER)
                           
    return metadata_root_folder,log_root_folder




    

class MonergismScrapAuthorTopicScripturePage(scrap_metadata.ScrapAuthorTopicScripturePage):
    def __init__(self, name,root_folder,url_list, browse_by_type,
                 information_type_root_folder,intermdiate_folders) -> None:
        
        metadata_root_folder,log_root_folder = get_monergism_metadata_and_log_folder(root_folder)
        
        if not isinstance(url_list,list):
            url_list = [url_list]
     

        super().__init__(name, metadata_root_folder, log_root_folder,url_list,
                          browse_by_type,information_type_root_folder,intermdiate_folders)

       
    


    
