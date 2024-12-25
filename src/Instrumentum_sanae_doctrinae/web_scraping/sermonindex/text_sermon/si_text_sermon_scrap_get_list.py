


import os
from Instrumentum_sanae_doctrinae.web_scraping import my_constants, scrap_metadata
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_metadata import  get_sermonindex_metadata_and_log_folder


from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import si_scrap_get_speaker_list

class GetTextSermonSpeakerList(si_scrap_get_speaker_list.GetSpeakerList):
    def __init__(self, root_folder, material_type = "text", url="https://www.sermonindex.net/modules/articles/") -> None:
        """"""
        super().__init__(root_folder, material_type, url)
        
        



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
        
        


    def get_useful_anchor_object_list(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        """    

        container = bs4_container.find("div",
                                       attrs = {"class":"bookContentsPage"})
        return container.find_all("a")
    