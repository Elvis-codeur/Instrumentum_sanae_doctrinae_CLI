

import os
import pathlib
from Instrumentum_sanae_doctrinae.my_tools import general_tools
from Instrumentum_sanae_doctrinae.web_scraping import http_connexion, my_constants


class SI_ScrapWork_ALL(http_connexion.ParallelHttpConnexionWithLogManagement):
    def __init__(self,root_folder,material_root_folder,browse_by_type, overwrite_log=False, update_log=True,intermdiate_folders=None):
        
        root_folder = general_tools.process_path_according_to_cwd(root_folder)

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
            input_data[file.as_posix()] = general_tools.read_json(file)

        super().__init__(log_filepath = log_filepath,
                         input_root_folder = input_root_folder,
                         input_data=input_data,
                         overwrite_log = overwrite_log)
        
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
        
        intermediate_folders = kwargs.get("intermediate_folders")
        #print(intermediate_folders,name)
        
        self.element_dict[name] = {
            **{"pages":element.get("pages"),"name":name},
            
             **{
                "meta_data": {
                    "input_file_index":self.meta_informations["input_files_information"]\
                                                        ["input_files"].index(kwargs.get("file_path")),                
                }
             },
                        
            **{"download_log":{
                "intermediate_folders":intermediate_folders[:intermediate_folders.index(name)]} 
                }
            
                }
        
        