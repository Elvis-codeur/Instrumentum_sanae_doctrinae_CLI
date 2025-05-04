

import os
from Instrumentum_sanae_doctrinae.web_scraping import scrap_metadata
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools, my_constants

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_metadata import get_sermonindex_metadata_and_log_folder



#####################################
#####################################
#####################################
#####################################
#####################################
#####################################
#####################################
#####################################
#####################################
#####################################

class GetAudioSermonList(scrap_metadata.GetAnyBrowseByListFromManyPages):
    
    def __init__(self, root_folder,url,browse_by_type):
        
        if not root_folder:
            root_folder = os.getcwd()
            
        material_root_folder = my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
            
        metadata_root_folder,log_root_folder = get_sermonindex_metadata_and_log_folder(root_folder,material_root_folder)        

        super().__init__(metadata_root_folder, log_root_folder,
                         url_list = [url],
                         browse_by_type = browse_by_type,
                         intermdiate_folders = [])
        
        
    def get_list_from_local_data(self):
       
        file_path = list(self.url_informations.values())[0].get("json_filepath")
        
        file_content = _my_tools.read_json(file_path)
        
        return [i.get("name") for i in file_content.get("data")]
        
        
        
        

class GetAudioSermonTopicList(GetAudioSermonList):
    def __init__(self, root_folder, browse_by_type = my_constants.TOPIC_NAME,
                 url = "https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=topicsList"):
        
        super().__init__(root_folder, url, browse_by_type)
    
    

    def get_useful_anchor_object_list(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        """    

        container = bs4_container.find("table",
                                       attrs = {"width":"100%",
                                                "cellspacing":"0",
                                                "border":"0"})
        container = container.find("div")

        return container.find_all("a")



class GetAudioSermonPodcastList(GetAudioSermonList):
    def __init__(self, root_folder, browse_by_type = my_constants.PODCAST_NAME,
                 url = "https://www.sermonindex.net/podcast.php"):
        super().__init__(root_folder, url, browse_by_type)

    def get_useful_anchor_object_list(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        """    

        container = bs4_container.find("table",
                                       attrs = {"width":"100%",
                                                "cellspacing":"0",
                                                "cellpadding":"1",
                                                "width":"571",
                                                "border":"0"})
        
        result = container.find("tr").find("td").\
                find_all("a")

        #print(result)

        #result = [i for i in result if 
        #          urllib.parse.urlparse(i.get("href")).netloc == "archive.org"]

        return result


class GetAudioSermonScriptureList(GetAudioSermonList):
    def __init__(self, root_folder, browse_by_type = my_constants.SCRIPTURE_NAME,
                 url = "https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=booksList"):
        super().__init__(root_folder, url,browse_by_type)

    def get_useful_anchor_object_list(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        """    
        #print(bs4_container)
        container = bs4_container.find("table",
                                       attrs = {"width":"90%",
                                                "cellpadding":"0",
                                                "cellspacing":"0",
                                                "border":"0"})
        return container.find_all("a")
