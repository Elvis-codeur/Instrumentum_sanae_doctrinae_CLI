
from concurrent.futures import ThreadPoolExecutor
import os 
import urllib
import urllib.parse
import pathlib
import traceback

from bs4 import BeautifulSoup
import requests


from .. import scrap_metadata
from ...my_tools import my_constants
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools



"""
This file contains the class that get the list of all the authors. This include 

    - The authors of audio sermon https://www.sermonindex.net/modules/mydownloads/
    - The authors of text sermon https://www.sermonindex.net/modules/articles/
    - The authors of video sermon https://www.sermonindex.net/modules/myvideo/
    - The authors of vintage https://www.sermonindex.net/modules/myalbum/index.php
"""





class GetSpeakerLinks(scrap_metadata.GetAnyBrowseByListFromManyPages):
    def __init__(self, metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders=None) -> None:
        
        url_list = []
        if not isinstance(url,list):
            url_list = [url]
        else:
            url_list = url.copy()
            
        for indice,url in enumerate(url_list):
            if not isinstance(url,dict):
                url_list[indice] = {"url":url}
                
        super().__init__(metadata_root_folder, log_root_folder, url_list, browse_by_type, intermdiate_folders)

        # A list of the other pages. For sermonindex, it is the links who's text begin with ~
        # See this pages for more 
        # https://www.sermonindex.net/modules/mydownloads/
        # https://www.sermonindex.net/modules/articles/

        
        # A list to store the link ot the other pages 
        # For example 
        self.other_page_links = []

    async def scrap_page_useful_links(self,**kwargs):
        
        # Connect to the url and create a beautiful soup object with the html for scraping 
    

        result = [] 

        for url in self.url_informations:
            links = []
            other_page_list = []

            bs4_object = self.url_informations[url]['bs4_object']
            anchor_list =  kwargs.get("get_useful_link_method")(bs4_object)
           
            for anchor_object in anchor_list:
                link_text = _my_tools.replace_forbiden_char_in_text(
                        _my_tools.remove_consecutive_spaces(anchor_object.get_text()))
                
                if "~" not in link_text:
                    if link_text:
                        links.append(
                            {
                                "name": link_text,
                                "url_list":[anchor_object]
                            }
                        )
                        
                else:
                    other_page_list.append((urllib.parse.urljoin(url, anchor_object.attrs.get("href")),anchor_object.get_text().strip()))
            
            self.other_page_links.append(other_page_list)
            
            result.append((url,links))
            
            #print(links)
        return result
    
    
    def get_list_from_local_data(self):
        print(self.__dict__)
    


class GetAudioSermonsSpeakerLinks(GetSpeakerLinks):
    def __init__(self, metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders=None) -> None:
        super().__init__(metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders)

    def get_useful_anchor_object_list_on_main_page(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        This function work on this page https://www.sermonindex.net/modules/mydownloads/
        """    

        container = bs4_container.find("table",
                                       attrs = {"width":"90%",
                                                "cellpadding":"0",
                                                "cellspacing":"5",
                                                "border":"0"})
        
        result = []

        tr_container_list = container.find_all("tr")

        for tr_container in tr_container_list:
            td_container_list = tr_container.find_all("td")
            if len(td_container_list) >= 4:
                anchor_element1 = td_container_list[1].find("a")
                anchor_element2 = td_container_list[3].find("a")

                if anchor_element1:
                    result.append(anchor_element1)

                if anchor_element2:
                    result.append(anchor_element2)


        return result
    
    def get_useful_anchor_object_list_on_other_page(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        This function work on this pages 
            - https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=670
            - https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=168
            - https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=58
            - https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=59
            - https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=60
            - https://www.sermonindex.net/modules/mydownloads/viewcat.php?cid=61

        """    

        container = bs4_container.find("table",
                                       attrs = {"width":"95%"})
        
        return container.find_all("a")
    
   
class GetTextSermonsSpeakerLinks(GetSpeakerLinks):
    def __init__(self, metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders=None) -> None:
        super().__init__(metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders)


    def get_useful_anchor_object_list_on_main_page(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        This function work on this page https://www.sermonindex.net/modules/articles/
        """    

        container = bs4_container.find("table",
                                       attrs = {"width":"100%",
                                                "cellpadding":"2",
                                                "cellspacing":"2",
                                                "border":"0"})
        
        container = container.find("tr").find("td")
        
        container = [i for i in container.find_all("table") if not i.attrs][0]
        
        containers = container.find_all("table")
        containers = [i for i in containers if not i.attrs]


        result = [i.find_all("a")[1] for i in containers]
        result = [i for i in result if i]
        result = [i for i in result if "index.php?view=category" in i.get("href")]
        
        return result
    
    def get_useful_anchor_object_list_on_other_page(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        This function work on this pages 
            - https://www.sermonindex.net/modules/articles/index.php?view=category&cid=115
            - https://www.sermonindex.net/modules/articles/index.php?view=category&cid=116
            - https://www.sermonindex.net/modules/articles/index.php?view=category&cid=117
            - https://www.sermonindex.net/modules/articles/index.php?view=category&cid=118
            
        """    
        
        container = bs4_container.find("table",
                                       attrs = {"width":"100%",
                                                "cellpadding":"3",
                                                "cellspacing":"0",
                                                "border":"0"})
        
        container = container.find("tr").find("td")
        
        container = container.find_all("table",recursive = False)[1]
        return container.find_all("a")
    
    
    
class GetVideoSermonsSpeakerLinks(GetSpeakerLinks):
    def __init__(self, metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders=None) -> None:
        super().__init__(metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders)


    def get_useful_anchor_object_list_on_main_page(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        This function work on this page https://www.sermonindex.net/modules/myvideo/
        """    

        
        container = bs4_container.find("table",
                                       attrs = {"width":"90%",
                                                "cellpadding":"0",
                                                "cellspacing":"5",
                                                "border":"0"})
        
        result = []

        tr_container_list = container.find_all("tr")

        for tr_container in tr_container_list:
            td_container_list = tr_container.find_all("td")
            if len(td_container_list) >= 4:
                anchor_element1 = td_container_list[1].find("a")
                anchor_element2 = td_container_list[3].find("a")

                if anchor_element1:
                    result.append(anchor_element1)

                if anchor_element2:
                    result.append(anchor_element2)



        return result
    
    def get_useful_anchor_object_list_on_other_page(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        This function work on this pages 
            - https://www.sermonindex.net/modules/myvideo/viewcat.php?cid=21
            - https://www.sermonindex.net/modules/myvideo/viewcat.php?cid=22
            - https://www.sermonindex.net/modules/myvideo/viewcat.php?cid=23
            - https://www.sermonindex.net/modules/myvideo/viewcat.php?cid=24
        """    

        container = bs4_container.find("table",
                                       attrs = {"width":"100%",
                                                "cellpadding":"3",
                                                "cellspacing":"0",
                                                "border":"0"})

        container = container.find_all("tr",recursive = False)[-1]
        
        container = container.find("td").find("table")
        
        return container.find_all("a")



class GetVintageImageSpeakerLinks(GetSpeakerLinks):
    def __init__(self, metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders=None) -> None:
        super().__init__(metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders)


    def get_useful_anchor_object_list_on_main_page(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        This function work on this page https://www.sermonindex.net/modules/myalbum/index.php
        """    

        
        container = bs4_container.find("table",
                                       attrs = {"width":"90%",
                                                "cellpadding":"0",
                                                "cellspacing":"5",
                                                "border":"0"})
        
        result = []

        tr_container_list = container.find_all("tr")

        for tr_container in tr_container_list:
            td_container_list = tr_container.find_all("td")
            if len(td_container_list) >= 4:
                anchor_element1 = td_container_list[1].find("a")
                anchor_element2 = td_container_list[3].find("a")

                if anchor_element1:
                    result.append(anchor_element1)

                if anchor_element2:
                    result.append(anchor_element2)



        return result
    
    def get_useful_anchor_object_list_on_other_page(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        This function work on this pages 
            - https://www.sermonindex.net/modules/myalbum/viewcat.php?cid=7
            - https://www.sermonindex.net/modules/myalbum/viewcat.php?cid=8
            - https://www.sermonindex.net/modules/myalbum/viewcat.php?cid=9
            - https://www.sermonindex.net/modules/myalbum/viewcat.php?cid=10
            
        """    

        container = bs4_container.find("table",
                                       attrs = {"width":"95%",})
        
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

    async def scrap_and_write(self):

        ob_class = None
        
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
        
        
        await ob.scrap_and_write(get_useful_link_method = 
                            ob.get_useful_anchor_object_list_on_main_page)
        
        await ob.close()
       
        #print(ob.other_page_links)
        for other_page_per_url in ob.other_page_links:
            for url,url_text in other_page_per_url:
                other_page_ob = ob_class(self.metadata_root_folder,
                            self.log_root_folder,
                            url,
                            "speaker",
                            intermdiate_folders = [url_text.strip()]
                                )
                
                await other_page_ob.scrap_and_write(get_useful_link_method = 
                                                  ob.get_useful_anchor_object_list_on_other_page)

                await other_page_ob.close()
                
                
    def get_list_from_local_data(self):
        speaker_list_json_file_root_folder = os.path.join(self.metadata_root_folder,
                                                          my_constants.ELABORATED_DATA_FOLDER,
                                                          my_constants.SPEAKER_NAME,
                                                          my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER,
                                                          )
        
        
        filepath_list = pathlib.Path(speaker_list_json_file_root_folder).rglob("*.json")
        
        #print(speaker_list_json_file_root_folder,[i for i in filepath_list])
        
        result = []
        
        for file_path in filepath_list:
            file_content = _my_tools.read_json(file_path)
            result += [i.get("name") for i in file_content.get("data")]   
            
        return result     
        
        
        

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