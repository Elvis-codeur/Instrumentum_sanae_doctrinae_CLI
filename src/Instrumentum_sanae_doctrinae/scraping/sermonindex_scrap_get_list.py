
from concurrent.futures import ThreadPoolExecutor
import os 
import urllib
import urllib.parse
import pathlib
import traceback

from bs4 import BeautifulSoup
import requests



from ..scraping import scrap_metadata
from ..scraping import my_constants
from ..scraping import _my_tools

from ..scraping.sermonindex_scrap_metadata import GetSpeakerList, GetTopicOrScriptureOrPodcastOrChristianBooks


class GetAudioSermonTopicList(GetTopicOrScriptureOrPodcastOrChristianBooks):
    def __init__(self, root_folder, browse_by_type = "topic") -> None:
        super().__init__(root_folder,
                          url = "https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=topicsList",
                            browse_by_type = browse_by_type,
                            is_text=False)
        #print(self.__dict__) 

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



class GetAudioSermonPodcastList(GetTopicOrScriptureOrPodcastOrChristianBooks):
    def __init__(self, root_folder, browse_by_type = "podcast") -> None:
        super().__init__(root_folder,
                          url = "https://www.sermonindex.net/podcast.php",
                            browse_by_type = browse_by_type,
                            is_text=False)
        #print(self.__dict__) 

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


class GetAudioSermonScriptureList(GetTopicOrScriptureOrPodcastOrChristianBooks):
    """"""
    def __init__(self, root_folder, browse_by_type = "scripture") -> None:
        super().__init__(root_folder,
                          url = "https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=booksList",
                         browse_by_type = browse_by_type,
                         is_text=False)
        """"""
    

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

class GetAudioSermonChristianBookList(GetTopicOrScriptureOrPodcastOrChristianBooks):
    def __init__(self, root_folder, browse_by_type = "christian_book") -> None:
        super().__init__(root_folder,
                          url = "https://www.sermonindex.net/modules/bible_books/?view=books_list",
                         browse_by_type = browse_by_type,
                         is_text=True)
        

    def get_useful_anchor_object_list(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        """    

        container = bs4_container.find("table",
                                       attrs = {"width":"100%",
                                                "cellpadding":"2",
                                                "cellspacing":"2",
                                                "border":"0"})
        
        container = container.find("div")
        return container.find_all("a")






class GetSpeakerList():
    def __init__(self,root_folder,material_type,url) -> None:

        self.material_type = material_type
        
        if material_type == "audio":
            material_root_folder =  my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
        elif material_type == "video":
            material_root_folder =  my_constants.SERMONINDEX_VIDEO_SERMONS_ROOT_FOLDER
        elif material_type == "text":
            material_root_folder = my_constants.SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER
        elif material_type == "vintage_image":
            material_root_folder = my_constants.SERMONINDEX_VINTAGE_IMAGE_ROOT_FOLDER
        else:
            raise ValueError(f"The material type {material_type} is not allowed. The allowed are [audio, video,text,vintage_image]")
        

        root_folder = _my_tools.process_path_according_to_cwd(root_folder)


        self.metadata_root_folder = os.path.join(root_folder,
                            my_constants.SERMONINDEX_METADATA_ROOT_FOLDER,material_root_folder)


        self.log_root_folder = os.path.join(root_folder,
                            my_constants.SERMONINDEX_LOG_ROOT_FOLDER, material_root_folder)

        self.url = url

    def scrap_and_write(self):

        if self.material_type == "audio":
            ob_class = GetAudioSermonsSpeakerLinks
        elif self.material_type == "text":
            ob_class = GetTextSermonsSpeakerLinks
        elif self.material_type == "video":
            ob_class = GetVideoSermonsSpeakerLinks
        elif self.material_type == "vintage_image":
            ob_class = GetVintageImageSpeakerLinks
    
        ob = ob_class(self.metadata_root_folder,
                       self.log_root_folder,
                       self.url,
                       "speaker",)
        
        # The parent of the anchor object containing the 
        # url of author topic or scripture depends on the 
        # material type. The structure of the pages are not 
        # the same for all the type of material 
        # In the page of the of the text sermons ( https://www.sermonindex.net/modules/articles/)
        # The useful anchor objects are in <b> object 
        # while in the page of the audio sermons (https://www.sermonindex.net/modules/articles/)
        # The useful anchor object are in <td> object 
        
        
        ob.scrap_and_write(get_useful_link_method = 
                            ob.get_useful_anchor_object_list_on_main_page)
       
        #print(ob.other_page_links)
        for other_page_per_url in ob.other_page_links:
            for url,url_text in other_page_per_url:
                other_page_ob = ob_class(self.metadata_root_folder,
                            self.log_root_folder,
                            url,
                            "speaker",
                            intermdiate_folders = [url_text.strip()]
                                )
                
                other_page_ob.scrap_and_write(get_useful_link_method = 
                                                  ob.get_useful_anchor_object_list_on_other_page)

            
        



class GetAudioSermonSpeakerList(GetSpeakerList):
    def __init__(self, root_folder, material_type = "audio", url="https://www.sermonindex.net/modules/mydownloads/") -> None:
        """"""
        super().__init__(root_folder, material_type, url)


class GetTextSermonSpeakerList(GetSpeakerList):
    def __init__(self, root_folder, material_type = "text", url="https://www.sermonindex.net/modules/articles/") -> None:
        """"""
        super().__init__(root_folder, material_type, url)

class GetVideoSermonSpeakerList(GetSpeakerList):
    def __init__(self, root_folder, material_type = "video", url="https://www.sermonindex.net/modules/myvideo/") -> None:
        """"""
        super().__init__(root_folder, material_type, url)


class GetVintageImageSpeakerList(GetSpeakerList):
    def __init__(self, root_folder, material_type = "vintage_image", url="https://www.sermonindex.net/modules/myalbum/index.php") -> None:
        """"""
        super().__init__(root_folder, material_type, url)




