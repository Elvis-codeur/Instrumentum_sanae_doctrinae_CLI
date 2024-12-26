


# This class works for the audio sermons 

import json
import os
import pathlib

from bs4 import BeautifulSoup
import urllib
from Instrumentum_sanae_doctrinae.web_scraping import _my_tools, http_connexion, my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_metadata import SermonIndexScrapAuthorTopicScripturePage


class SI_ScrapVideoSermonWork(SermonIndexScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder,browse_by_type, url_list,material_root_folder,intermdiate_folders=None):
        
        super().__init__(name, root_folder, url_list,browse_by_type,
                         information_type_root_folder = my_constants.WORK_INFORMATION_ROOT_FOLDER,
                         material_root_folder = material_root_folder,
                         intermdiate_folders = intermdiate_folders)
        
        

    async def scrap_url_pages(self):
        """
        Scrap the main information of the web page. Here the description, the 
        urls of the author, topic, scripture work 
        """
       

        final_result = {}

        for current_page_url in self.url_informations:
                
            soup = self.url_informations[current_page_url].get("bs4_object")
            
            result = []
            
            table = soup.find("table",attrs = {
                "width":"100%",
                "cellspacing":"0",
                "cellpadding":"10",
                "border":"0"
                
            })
            
            for tr_element in table.find_all("tr",recursie = False):
                
                td_element = tr_element.find_all("td")[-1]
                
                anchor_element = td_element.find_all("a")[1]
                
                b_elements = td_element.find_all("b",recursive = False)
                
                result.append(
                    {
                        "url":anchor_element.get("href"),
                        "link_text":anchor_element.get_text(),
                        "description":b_elements[0].get_text(),
                        "views":b_elements[1].get_text(),
                        
                    }
                )
                
                        
            final_result[current_page_url] = result

        return final_result


    

    def is_data_downloaded(self):

        for url in self.url_informations:
            file_path = self.url_informations[url].get("json_filepath")
            if not os.path.exists(file_path):
                return False
            
            file_content = _my_tools.read_file(file_path)
            
            if not file_content:
                return False
            
            try:
                file_content = json.loads(file_content)
            except:
                return False

            if not file_content.get("url"):
                return False
            
        return True
    
    async def async_is_data_downloaded(self):

        for url in self.url_informations:
            file_path = self.url_informations[url].get("json_filepath")
            if not os.path.exists(file_path):
                return False
            
            
            file_content = _my_tools.async_read_file(file_path)
            
            if not file_content:
                return False
            
            try:
                file_content = json.loads(file_content)
            except:
                return False

            if not file_content.get("url"):
                return False
            
        return True


class SI_ScrapVideoSermonWork_ALL(http_connexion.ParallelHttpConnexionWithLogManagement):
    def __init__(self,root_folder,material_root_folder,browse_by_type, overwrite_log=False, update_log=True,intermdiate_folders=None):
        
        root_folder = _my_tools.process_path_according_to_cwd(root_folder)

        log_filepath = os.path.join(root_folder,my_constants.LOGS_ROOT_FOLDER,
                                       my_constants.SERMONINDEX_NAME,
                                       material_root_folder,
                                       my_constants.ELABORATED_DATA_FOLDER,
                                       browse_by_type,
                                       my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,
                                       my_constants.get_default_json_filename(0))
        
        input_root_folder = os.path.join(root_folder,
                                         my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.SERMONINDEX_NAME,
                                         material_root_folder,
                                         my_constants.ELABORATED_DATA_FOLDER,
                                         browse_by_type)
        
        input_data = {}
        
        self.input_root_folder = input_root_folder
        
        for file in self.prepare_input_json_file(input_root_folder):
            input_data[file.as_posix()] = _my_tools.read_json(file)

        super().__init__(log_filepath = log_filepath,
                         input_root_folder = input_root_folder,
                         input_data=input_data,
                         overwrite_log = overwrite_log,
                         update_log = update_log)
        
        self.material_root_folder = material_root_folder
        self.browse_by_type = browse_by_type
        self.root_folder = root_folder


    
    def prepare_input_json_file(self,input_root_folder):
        """
        :param matching_subfolders: The folders from wich the json files will be searched out 
        """
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        input_json_files = []

        folder = os.path.join(input_root_folder,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER)
    
        for file in [i for i in pathlib.Path(folder).rglob("*.json") if i.is_file()]:
            if str(file.parent).endswith(my_constants.MAIN_INFORMATION_ROOT_FOLDER):
                input_json_files.append(file)

        return input_json_files

    

    def prepare_input_data(self,**kwargs):
        """
        This method take a json file content and create input data for download 
        that are put int dict self.element_dict

        :param file_content: the content of a json file where input data will be taken 
        :param intermediate_folders: The intermediate folders from the root folder to 
        the json file 
        :param file_path: The path of the json file 
        """

        element = kwargs.get("file_content").get("data")
        
        name  = pathlib.Path(kwargs.get("file_path")).parent.parent.as_posix()
        
        name = name.split("/")[-1]
        
        self.element_dict[name] = {
            **{"pages":element.get("pages"),"name":name},
            
            **{"download_log":{
                "input_file_index":self.meta_informations["input_files_information"]\
                                                        ["input_files"].index(kwargs.get("file_path")),
                "intermediate_folders":[]} #kwargs.get("intermediate_folders")
                }
                }
        
    
    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)

        
        ob = SI_ScrapVideoSermonWork(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type = self.browse_by_type,
            url_list = element.get("pages"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )

        print(element.get("name"))
        

        await ob.scrap_and_write()

    def is_element_data_downloaded(self,element):
        ob = SI_ScrapVideoSermonWork(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type =self.browse_by_type,
            url_list = element.get("url_list"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )
        return ob.is_data_downloaded()
        
