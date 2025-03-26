




    

import os
import pathlib
import json 
import urllib
import urllib.parse

from Instrumentum_sanae_doctrinae.web_scraping import http_connexion, my_constants
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_metadata import SermonIndexScrapAuthorTopicScripturePage


class SI_ChristianBookScrapGeneralInformation(SermonIndexScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder,browse_by_type, url_list,material_root_folder,intermdiate_folders=None):
        
        super().__init__(name, root_folder, url_list,browse_by_type,
                         information_type_root_folder = my_constants.MAIN_INFORMATION_ROOT_FOLDER,
                         material_root_folder = material_root_folder,
                         intermdiate_folders = intermdiate_folders)
        
        
    async def scrap_url_pages(self):
        """
        Scrap the main information of the web page. Here the description, the 
        urls of the author, topic, scripture work 
        """        

        final_result = {}

        for main_url in self.url_informations:
                
            soup = self.url_informations[main_url].get("bs4_object")

            result = {}
            pages = []

            book_content =  soup.find("div",class_ = 'bookContentsPage')
            
            h3_list =  book_content.findAll("h3",recursive = False)
            
            for h3_element in h3_list:
                anchor_object = h3_element.find("a")
                pages.append(
                    {
                        "link_text":anchor_object.get_text().strip(),
                        "url":urllib.parse.urljoin(main_url,anchor_object.get("href"))
                    }
                )
                
            
            # Author name 
            author_name = book_content.find_previous("i").get_text().strip()
            
            book_name = book_content.find_previous("b").get_text().strip()
            
            
            
            result['author_name'] = author_name
            result['book_name'] = book_name
            result['pages'] = pages
            
            #print(author_name,book_name)    

            final_result[main_url] = result

        #print(final_result,self.url_list)

        return final_result
    
    
    async def is_data_downloaded(self):

        for url in self.url_informations:
            file_path = self.url_informations[url].get("json_filepath")
            #print(file_path)
            if not os.path.exists(file_path):
                return False
            
            
            file_content = await _my_tools.async_read_file(file_path)
            

            if not file_content:
                return False
            
            file_content = json.loads(file_content)
            
            # Check mandatory information in the json file 

            if not file_content.get("url"):
                return False
            

            if not file_content.get("data").get("author_name"):
                return False
            
        return True
    


# Download the main information of each author, topic, etc 
class SI_ChristianBookScrapMainInformation_ALL(http_connexion.ParallelHttpConnexionWithLogManagement):
    def __init__(self,root_folder,material_root_folder,browse_by_type, overwrite_log=False, update_log=True,intermdiate_folders=None):
        
        root_folder = _my_tools.process_path_according_to_cwd(root_folder)

        log_filepath = os.path.join(root_folder,my_constants.LOGS_ROOT_FOLDER,
                                       my_constants.SERMONINDEX_NAME,
                                       material_root_folder,
                                       my_constants.ELABORATED_DATA_FOLDER,
                                       browse_by_type,
                                       my_constants.GENERAL_INFORMATION_NAME,
                                       my_constants.get_default_json_filename(0))
        
        input_root_folder = os.path.join(root_folder,
                                         my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.SERMONINDEX_NAME,
                                         material_root_folder,
                                         my_constants.ELABORATED_DATA_FOLDER,
                                         browse_by_type)

        input_json_files_content = {}
        
        for file in self.prepare_input_json_file(input_root_folder):
            input_json_files_content[file.as_posix()] = _my_tools.read_json(file)
        
        super().__init__(log_filepath = log_filepath,
                         input_data = input_json_files_content,
                         overwrite_log = overwrite_log,
                         input_root_folder=input_root_folder)
        
        self.material_root_folder = material_root_folder
        self.browse_by_type = browse_by_type
        self.root_folder = root_folder
    

    def prepare_input_json_file(self,input_root_folder):
        """
        :param input_root_folder: The folder from which to search for the json files to use as input
        """
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        
        folder =  os.path.join(input_root_folder,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER)
        
        input_json_files = []
        input_json_files = [i for i in pathlib.Path(folder).rglob("*.json") if i.is_file()]
        
        #print(folder,input_json_files)
        
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

        element_list = kwargs.get("file_content").get("data")
        
        # The path of the file from which the data is taken from 
        element_list_filepath = kwargs.get("file_path")
        
        for element in element_list:

            self.element_dict[element.get("name")] = {
                **element,
                **{"download_log":{
                    "input_file_index":self.meta_informations["input_files_information"]\
                                                            ["input_files"].index(kwargs.get("file_path")),
                    "intermediate_folders":kwargs.get("intermediate_folders")} 
                    }
                    }
    
    
    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        try:
            ob = SI_ChristianBookScrapGeneralInformation(
                name = element.get("name"),
                root_folder = self.root_folder,
                browse_by_type = self.browse_by_type,
                url_list = element.get("url_list"),
                intermdiate_folders = element.get("download_log").get("intermediate_folders"),
                material_root_folder = self.material_root_folder
            )

            await ob.scrap_and_write()
            return {"success":True,"element":element}
        except:
            return {"success":False,"element":element}
            

    async def is_element_data_downloaded(self,element):
        ob = SI_ChristianBookScrapGeneralInformation(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type =self.browse_by_type,
            url_list = element.get("url_list"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )
        return await ob.is_data_downloaded()
        
