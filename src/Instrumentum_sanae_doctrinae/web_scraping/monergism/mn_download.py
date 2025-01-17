import pathlib 
import aiohttp 
from charset_normalizer import detect as detect_encoding
import os 
from Instrumentum_sanae_doctrinae.web_scraping import download
from Instrumentum_sanae_doctrinae.web_scraping import my_constants,http_connexion
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools


class MN_DownloadFromUrl(download.DownloadFromUrl):
    
    def __init__(self, url, output_folder,output_file_name,aiohttp_session,separe_file_based_on_format = True):
        """
        :param output_file_name: The name of the file without its extension .html or .pdf, etc
        :param separe_file_based_on_format: If true, the pdf files are saved in the subfolder PDF, the html files 
        in the subfolder HTML, etc. If false, all the files are downloaded in the same folder not matter what 
        their format is 
        """
        self.output_folder = output_folder
        self.output_file_name = output_file_name
        self.separe_file_based_on_format = separe_file_based_on_format
        
                     
        
        super().__init__(url, "",aiohttp_session)
        
        
    def __repr__(self):
        return f"{self.__class__.__name__}({str(self.__dict__)})"
        
    
    async def is_downloaded(self):
        
        # Check if there is a file with the same name as the name given to the object
        
        files = pathlib.Path(self.output_folder).rglob("*")
        files = [file for file in files if file.is_file()]
        
        for file in files:
            file_basename = os.path.basename(file)
            if file_basename.startswith(self.output_file_name):
                #print(file_basename,self.output_file_name)
                return True 
        
        return False 
    
        
                    
            
                
                                                                    

class MN_Download_Work(download.DownloadWork):
    def __init__(self,name, root_folder, browse_by_type, overwrite_log=False, update_log=True):
        super().__init__(name,root_folder, browse_by_type, overwrite_log, update_log)
        


    def prepare_log_metadata_input_files_path(self, root_folder):
       
        log_filepath = os.path.join(root_folder,
                                    my_constants.LOGS_ROOT_FOLDER,
                                    my_constants.MONERGISM_NAME,
                                    my_constants.ELABORATED_DATA_FOLDER,
                                    self.browse_by_type, 
                                    my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_DOWNLOAD_FOLDER,
                                    self.name,
                                    my_constants.get_default_json_filename(0)
                                    )
        
        input_root_folder = os.path.join(root_folder,
                                         my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.MONERGISM_NAME,
                                         my_constants.ELABORATED_DATA_FOLDER,
                                         self.browse_by_type, 
                                         my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,
                                         self.name
                                         )
        
        download_output_root_folder = os.path.join(root_folder,
                                         my_constants.DOWNLOAD_ROOT_FOLDER,
                                         my_constants.MONERGISM_NAME,
                                         self.browse_by_type, 
                                         self.name,
                                         my_constants.DOWNLOAD_ROOT_FOLDER,                             
                                         )
        
        return locals()
        
        

    def get_input_json_files(self,input_root_folder):
        """
        :param input_root_folder: The folders from wich the json files will be searched out 
        """
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        input_json_files = []

        # The folder where the works of the author are 
        folder_path = os.path.join(input_root_folder,my_constants.WORK_INFORMATION_ROOT_FOLDER)
                
        # List to store paths to all JSON files
        json_files = [i for i in pathlib.Path(folder_path).rglob("*.json") if i.is_file()]

        #print("kaka",json_files,input_root_folder)
        
        for file in json_files:
            filename = file.as_posix()
            if my_constants.WORK_INFORMATION_ROOT_FOLDER in filename:
                input_json_files.append(file)
                

        #print(input_json_files)
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
        
        for element in element_list:        
            self.element_dict[element.get("url")] = {
                **{
                    "link_text":element.get("link_text"),
                    "url":element.get("url"),
                    "output_folder":self.download_output_root_folder,
                },
                 
                **{"metadata": {"input_file_index":self.meta_informations["input_files_information"]\
                                                            ["input_files"].index(kwargs.get("file_path")),
                    "intermediate_folders":kwargs.get("intermediate_folders")[2:]
                    }
                   },
                
                **{"download_log":{}}
            }
    
        #print(self.element_dict)
        
        
    async def init_aiohttp_session(self):
        if self.aiohttp_session == None:
            self.aiohttp_session = aiohttp.ClientSession()
            
    async def close_aiohttp_session(self):
        if self.aiohttp_session != None:
            await self.aiohttp_session.close()
    

    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)

        #print(element.get("data"))
        
        ob = MN_DownloadFromUrl(
            url = element.get("url"),
            output_folder = element.get('output_folder'),
            output_file_name = _my_tools.replace_forbiden_char_in_text(
                _my_tools.remove_consecutive_spaces(element.get("link_text"))),
            aiohttp_session= self.aiohttp_session
        )
        #print(element_value,"\n\n")
        result = await ob.download()
        return result 
        
      

    async def is_element_data_downloaded(self,element):
        #print(element)
        ob = MN_DownloadFromUrl(
            url = element.get("url"),
            output_folder = element.get('output_folder'),
            output_file_name = _my_tools.replace_forbiden_char_in_text(
                _my_tools.remove_consecutive_spaces(element.get("link_text"))),
            aiohttp_session= self.aiohttp_session
        )
        is_downloaded = await ob.is_downloaded()
        
        result =  is_downloaded and element.get("download_log").get("download_data") != None
        #print(result,element,"\n\n\n")
        return result 
        
