import json
import os 
import pathlib
import re

import urllib

from Instrumentum_sanae_doctrinae.web_scraping import http_connexion
from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_scrap_metadata
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools, my_constants
from Instrumentum_sanae_doctrinae.web_scraping.monergism.mn_scrap_subtopic_work import MN_ScrapScriptureOrTopicWork, get_subtopics
from Instrumentum_sanae_doctrinae.web_scraping.monergism.mn_scrap_work_base import MN_ScrapSpeakerTopicScriptureWork_All


class MN_ScrapTopicWork_All(http_connexion.ParallelHttpConnexionWithLogManagement):
    def __init__(self,root_folder,browse_by_type, overwrite_log=False, update_log=True,intermdiate_folders=None):

        root_folder = _my_tools.process_path_according_to_cwd(root_folder)

        log_filepath = os.path.join(root_folder,
                                    my_constants.LOGS_ROOT_FOLDER,
                                    my_constants.MONERGISM_NAME,
                                    my_constants.ELABORATED_DATA_FOLDER,
                                    browse_by_type,
                                    my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,
                                    my_constants.get_default_json_filename(0))
        
        input_root_folder = os.path.join(root_folder,
                                         my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.MONERGISM_NAME,
                                         my_constants.ELABORATED_DATA_FOLDER,
                                         browse_by_type
                                         )
        

        #print(input_root_folder)
        
        input_files = self.get_input_json_files(input_root_folder)
        
        input_data = {}
        
        # Prepare the json files as input data 
        for filepath in input_files:
            file_content = _my_tools.read_json(filepath)
            input_data[str(filepath)] = file_content
        
        
        super().__init__(log_filepath = log_filepath,
                         input_root_folder= input_root_folder,
                         input_data=input_data,
                         overwrite_log = overwrite_log)
        
        self.browse_by_type = browse_by_type
        self.root_folder = root_folder


    def get_input_json_files(self,input_root_folder):
        """
        :param input_root_folder: The folders from wich the json files will be searched out 
        """
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        input_json_files = []

        # The folder where the works of the author are 
        folder_path = os.path.join(input_root_folder,
                                my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER)
        
        
        # List to store paths to all JSON files
        json_files = [i for i in pathlib.Path(folder_path).rglob("*.json") if i.is_file()]

                
        for file in json_files:
            #print(file)
            if str(file.parent).endswith(my_constants.MAIN_INFORMATION_ROOT_FOLDER):
                input_json_files.append(file)

        

        return input_json_files
            

    async def download_element_data(self,element_list):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)

        #print(element.get("data"))
        for element in element_list:
            
            #print(element.get("data").get("name"))
    
            ob = MN_ScrapSpeakerTopicScriptureWork_All(
                name = element.get("data").get("name"),
                root_folder = self.root_folder,
                browse_by_type = self.browse_by_type,
                url_list = [{'url':i} for i in element.get("data").get("pages")],
                intermdiate_folders = element.get("download_log").get("intermediate_folders")
            )
            await ob.scrap_and_write()

    async def is_element_data_downloaded(self,element_list):
        
        for element in element_list:
            
            ob = MN_ScrapSpeakerTopicScriptureWork_All(
                name = element.get("data").get("name"),
                root_folder = self.root_folder,
                browse_by_type = self.browse_by_type,
                url_list = [{'url':i} for i in element.get("data").get("pages")],
                intermdiate_folders = element.get("download_log").get("intermediate_folders")
            )
            if not await ob.is_data_downloaded():
                return False 
            
        return True 
        

