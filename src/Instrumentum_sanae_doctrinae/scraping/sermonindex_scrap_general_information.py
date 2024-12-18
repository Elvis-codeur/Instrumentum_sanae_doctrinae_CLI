
from ..scraping import scrap_metadata


class GetSpeakerLinks(scrap_metadata.GetAnyBrowseByListFromManyPages):
    def __init__(self, metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders=None) -> None:
        super().__init__(metadata_root_folder, log_root_folder, [url], browse_by_type, intermdiate_folders)

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
           
            for i in anchor_list:
                
                if "~" not in i.get_text():
                    if i.get_text():
                        links.append([i])
                else:
                    other_page_list.append((urllib.parse.urljoin(url, i.attrs.get("href")),i.get_text().strip()))
            self.other_page_links.append(other_page_list)
            result.append((url,links))
        return result
    


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
    


class GetTextSermonsChristianBook(GetTopicOrScriptureOrPodcastOrChristianBooks):
    def __init__(self, root_folder, 
                 url = "https://www.sermonindex.net/modules/bible_books/?view=books_list",
                  browse_by_type = "Christian Book", is_text= True):
        
        super().__init__(root_folder, url, browse_by_type, is_text)


    def get_useful_anchor_object_list(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        """    

        container = bs4_container.find("div",
                                       attrs = {"class":"bookContentsPage"})
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
    