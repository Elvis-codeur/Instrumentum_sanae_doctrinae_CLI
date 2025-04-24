

import os
import pathlib
from Instrumentum_sanae_doctrinae.my_tools import general_tools
from Instrumentum_sanae_doctrinae.my_tools import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_download import SI_Download_Work, SI_DownloadFromUrl
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_metadata import SermonIndexScrapAuthorTopicScripturePage


class DownloadTextSermonChristianBooks(SI_DownloadFromUrl):
    def __init__(self, url, output_folder, output_file_name, aiohttp_session,
                 separe_file_based_on_format=True):
        super().__init__(url, output_folder, output_file_name, aiohttp_session,
                         separe_file_based_on_format)
        


class SI_Download_ChristianBooks_ListOfTextWork(SI_Download_Work):
    def __init__(self, name,material_type, root_folder, browse_by_type,
                 overwrite_log=False, update_log=True):
        super().__init__(name,material_type, root_folder, browse_by_type,
                         overwrite_log, update_log)
        
        
    
    
    
    def get_input_json_files(self,input_root_folder):
        """
        :param input_root_folder: The folders from wich the json files will be searched out 
        """
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        input_json_files = []

        # The folder where the works of the author are 
        
        
        # Pay attention to this line 
        # Things are different here 
        # I take my data from the subfolder MAIN_INFORMATION_ROOT_FOLDER and no more from 
        # WORK_INFORMATION_ROOT_FOLDER
        
        folder_path = os.path.join(input_root_folder,my_constants.MAIN_INFORMATION_ROOT_FOLDER)
        
        
        #print(folder_path)
        # List to store paths to all JSON files
        json_files = [i for i in pathlib.Path(folder_path).rglob("*.json") if i.is_file()]

        #print(folder_path,json_files)
        
        #print("kaka",json_files,input_root_folder)
        
        for file in json_files:
            filename = file.as_posix()
            if my_constants.MAIN_INFORMATION_ROOT_FOLDER in filename:
                input_json_files.append(file)
                

        #print(input_root_folder,input_json_files)
        return input_json_files
    
    def prepare_input_data(self,**kwargs):
        """
        This method take a json file content and create input data for download 
        that are put into the dict self.element_dict

        :param file_content: the content of a json file where input data will be taken 
        :param intermediate_folders: The intermediate folders from the root folder to 
        the json file 
        :param file_path: The path of the json file 
        """

        element_list = kwargs.get("file_content").get("data")
        
        #print(element_list)
        
        if element_list:
            name = element_list.get("author_name")
            
        intermediate_folders = kwargs.get("intermediate_folders")
        
        local_intermediate_folders = []
        if intermediate_folders:
            if name in intermediate_folders:
                local_intermediate_folders = intermediate_folders[:intermediate_folders.index(name)].copy()
        
        #print(element_list)
        
        for element in element_list.get("pages"): 
            #print(element)  
            
            link_text = element.get("link_text")
            
            if link_text.endswith("."):
                link_text = link_text[:-1]
                 
            self.element_dict[element.get("url")] = {
                **{
                    "link_text":link_text,
                    "url":element.get("url"),
                    "output_folder":self.download_output_root_folder,
                },
                 
                **{"metadata": {"input_file_index":self.meta_informations["input_files_information"]\
                                                            ["input_files"].index(kwargs.get("file_path")),
                    "intermediate_folders":local_intermediate_folders,
                    }
                   },
                
                **{"download_log":{}}
            }
    
        #print(self.element_dict)
        


       
    
    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)

        #print(element)
        
        ob = DownloadTextSermonChristianBooks(
            url = element.get("url"),
            output_folder = element.get('output_folder'),
            output_file_name = general_tools.replace_forbiden_char_in_text(
                general_tools.remove_consecutive_spaces(element.get("link_text"))),
            aiohttp_session= self.aiohttp_session
        )
        #print(element_value,"\n\n")
        result = await ob.download()
        #print(result)
        return result 
        
      

    async def is_element_data_downloaded(self,element):
        #print(element)
        ob = DownloadTextSermonChristianBooks(
            url = element.get("url"),
            output_folder = element.get('output_folder'),
            output_file_name = general_tools.replace_forbiden_char_in_text(
                general_tools.remove_consecutive_spaces(element.get("link_text"))),
            aiohttp_session= self.aiohttp_session
        )
        is_downloaded = await ob.is_downloaded()
        
        result =  is_downloaded #and element.get("download_log").get("download_data") != None
        #print(result,element,"\n\n\n")
        #print(result,element.get("url"))
        return result 
        
