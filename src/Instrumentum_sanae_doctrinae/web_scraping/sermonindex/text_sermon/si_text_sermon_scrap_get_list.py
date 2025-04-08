


import os
from Instrumentum_sanae_doctrinae.web_scraping import my_constants, scrap_metadata
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_metadata import  get_sermonindex_metadata_and_log_folder
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools


        



class GetTextSermonsChristianBook(scrap_metadata.GetAnyBrowseByListFromManyPages):
    
    def __init__(self, root_folder,
                 url = "https://www.sermonindex.net/modules/bible_books/?view=books_list"):
        
        if not root_folder:
            root_folder = os.getcwd()
            
        material_root_folder = my_constants.SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER
            
        metadata_root_folder,log_root_folder = get_sermonindex_metadata_and_log_folder(root_folder,material_root_folder)        

        super().__init__(metadata_root_folder, log_root_folder,
                         url_list = [url],
                         browse_by_type = my_constants.SERMONINDEX_CHRISTIAN_BOOKS_ROOT_FOLDER,
                         intermdiate_folders = [])
        
    
    def get_list_from_local_data(self):
       
        file_path = list(self.url_informations.values())[0].get("json_filepath")
        
        file_content = _my_tools.read_json(file_path)
        
        return [i.get("name") for i in file_content.get("data")]


    def get_useful_anchor_object_list(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        """    

        container = bs4_container.find("div",
                                       attrs = {"class":"bookContentsPage"})
        return container.find_all("a")
    