"""
This module is created for the scrapping of metadata from https://www.monergism.com/


"""

import os 
import pathlib
import re
import urllib
import urllib.parse
from urllib.parse import urlparse, parse_qs


from Instrumentum_sanae_doctrinae.web_scraping import http_connexion, my_constants,scrap_metadata
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools
from Instrumentum_sanae_doctrinae.web_scraping.monergism.mn_tools import *




    

class MonergismScrapAuthorTopicScripturePage(scrap_metadata.ScrapAuthorTopicScripturePage):
    def __init__(self, name,root_folder,url_list, browse_by_type,
                 information_type_root_folder,intermdiate_folders) -> None:
        
        self.root_folder = root_folder
        
        metadata_root_folder,log_root_folder = get_monergism_metadata_and_log_folder(root_folder)
        
        if not isinstance(url_list,list):
            url_list = [url_list]
     

        super().__init__(name, metadata_root_folder, log_root_folder,url_list,
                          browse_by_type,information_type_root_folder,intermdiate_folders)
        
        
    def prepare_intermdiate_folders(self,intermdiate_folders,browse_by_type,name,information_type_root_folder):
        return prepare_intermdiate_folders(intermdiate_folders,browse_by_type,name,information_type_root_folder)

       
    def next_page(self,main_url):
        main_div = self.url_informations[main_url].get("bs4_object").find("div",class_ = "region-inner region-content-inner")
        
        anchor_list = []

        if main_div:
            anchor_list = main_div.findAll("a")

        anchor_list = [anchor_element 
                       for anchor_element in anchor_list 
                       if anchor_element.get_text().strip() == "next ›"]
        #print(anchor_list) 


        if anchor_list:
            return urllib.parse.urljoin(main_url,anchor_list[0].get("href"))
        else:
            return None
        
        


    
