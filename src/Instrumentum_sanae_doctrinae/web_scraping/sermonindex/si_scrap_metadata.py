
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
from Instrumentum_sanae_doctrinae.web_scraping import my_constants
from Instrumentum_sanae_doctrinae.web_scraping import _my_tools




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

        if not isinstance(url,list):
            url_list = [url]
            for indice,url in enumerate(url_list):
                if not isinstance(url,dict):
                    url_list[indice] = {"url":url}
                    

        metadata_root_folder,log_root_folder = get_sermonindex_metadata_and_log_folder(root_folder,material_root_folder)
        super().__init__(name,metadata_root_folder,log_root_folder,url_list,
                         browse_by_type,information_type_root_folder,
                         intermdiate_folders)
