import pathlib 
import aiohttp 
from charset_normalizer import detect as detect_encoding
import os 
from Instrumentum_sanae_doctrinae.web_scraping import download
from Instrumentum_sanae_doctrinae.web_scraping import http_connexion
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools, my_constants


class SI_DownloadFromUrl(download.DownloadFromUrl):
    
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
        
    
    async def is_downloaded(self,files_list = None):
        
        # Check if there is a file with the same name as the name given to the object
        
        if not files_list:
            files_list = pathlib.Path(self.output_folder).rglob("*")
            files_list = [file for file in files_list if file.is_file()]
            
            
        for file in files_list:
            file_basename = os.path.basename(file)
            #print(file_basename)
            if file_basename.startswith(self.output_file_name):
                #print(file_basename,self.output_file_name)
                #print(True)
                return True 
            
        #print(self.output_file_name)
        
        return False 
    
                                               

class SI_Download_Work(download.DownloadWork):
    def __init__(self,name,material_type, root_folder,intermediate_folders, browse_by_type, overwrite_log=False, update_log=True):
        
        self.material_type = material_type
        if self.material_type == my_constants.SERMONINDEX_AUDIO:
            self.material_type_root_folder = my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
        elif self.material_type == my_constants.SERMONINDEX_VIDEO:
            self.material_type_root_folder = my_constants.SERMONINDEX_VIDEO_SERMONS_ROOT_FOLDER
        elif self.material_type == my_constants.SERMONINDEX_TEXT:
                    self.material_type_root_folder = my_constants.SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER
        elif self.material_type == my_constants.SERMONINDEX_VINTAGE_IMAGE:
                    self.material_type_root_folder = my_constants.SERMONINDEX_VINTAGE_IMAGE_ROOT_FOLDER
                    
        self.intermediate_folders = intermediate_folders
        
        super().__init__(name,root_folder, browse_by_type, overwrite_log, update_log)
        
       
    def prepare_log_metadata_input_files_path(self, root_folder):
        
        
       
        log_filepath = pathlib.Path(os.path.join(root_folder,my_constants.SERMONINDEX_LOG_ROOT_FOLDER,
                                    self.material_type_root_folder,
                                    my_constants.ELABORATED_DATA_FOLDER,
                                    self.browse_by_type, 
                                    my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_DOWNLOAD_FOLDER,
                                    *self.intermediate_folders,
                                    self.name,
                                    my_constants.get_default_json_filename(0)
                                    )).resolve().as_posix()
        
        input_root_folder = pathlib.Path(os.path.join(root_folder,my_constants.SERMONINDEX_METADATA_ROOT_FOLDER,
                                         self.material_type_root_folder,
                                         my_constants.ELABORATED_DATA_FOLDER,
                                         self.browse_by_type, 
                                         my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,
                                         *self.intermediate_folders,
                                         self.name
                                         )).resolve().as_posix()
        
        download_output_root_folder = pathlib.Path(os.path.join(root_folder,my_constants.SERMONINDEX_DOWNLOAD_ROOT_FOLDER,
                                         self.material_type_root_folder,
                                         self.browse_by_type, 
                                         *self.intermediate_folders,
                                         self.name,
                                         my_constants.DOWNLOAD_ROOT_FOLDER,                             
                                         )).resolve().as_posix()
        
        return locals()
        
        

    def get_input_json_files(self,input_root_folder):
        """
        :param input_root_folder: The folders from wich the json files will be searched out 
        """
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        input_json_files = []

        # The folder where the works of the author are 
        folder_path = os.path.join(input_root_folder,my_constants.WORK_INFORMATION_ROOT_FOLDER)
        
        #print(folder_path)
        
        #print(folder_path)
        # List to store paths to all JSON files
        json_files = [i for i in pathlib.Path(folder_path).rglob("*.json") if i.is_file()]

        #print(json_files)
        #print("kaka",json_files,input_root_folder)
        
        for file in json_files:
            filename = file.as_posix()
            if my_constants.WORK_INFORMATION_ROOT_FOLDER in filename:
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
        
        if element_list:
            name = element_list[0].get("author_name")
            
        intermediate_folders = kwargs.get("intermediate_folders")
        
        local_intermediate_folders = []
        if intermediate_folders:
            if name in intermediate_folders:
                local_intermediate_folders = intermediate_folders[:intermediate_folders.index(name)].copy()
        
        for element in element_list:        
            self.element_dict[element.get("url")] = {
                **{
                    "link_text":element.get("link_text"),
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
        
        
    async def init_aiohttp_session(self):
        if self.aiohttp_session == None:
            self.aiohttp_session = aiohttp.ClientSession()
            
    async def close_aiohttp_session(self):
        if self.aiohttp_session != None:
            await self.aiohttp_session.close()
    

    async def download_element_data(self,element):
       pass 
        
      

    async def is_element_data_downloaded(self,element):
       pass 
        
