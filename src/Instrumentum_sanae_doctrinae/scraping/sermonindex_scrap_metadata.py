
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




def get_sermonindex_metadata_and_log_folder(root_folder,material_root_folder):
    metadata_root_folder = os.path.join(root_folder,
                            my_constants.SERMONINDEX_METADATA_ROOT_FOLDER,
                            material_root_folder)
    
    log_root_folder = os.path.join(root_folder,
                            my_constants.SERMONINDEX_LOG_ROOT_FOLDER,
                            material_root_folder)
    
    return metadata_root_folder,log_root_folder


def get_sermonindex_auth_top_scrip_list_json_filepath(root_folder,material_root_folder,browse_by_type):
    metadata_root_folder,_ = get_sermonindex_metadata_and_log_folder(root_folder,material_root_folder)
    
    return os.path.join(metadata_root_folder,my_constants.ELABORATED_DATA_FOLDER,browse_by_type,
                        f"{browse_by_type}_list",my_constants.get_default_json_filename(0))

    

class GetTopicOrScriptureOrPodcastOrChristianBooks(scrap_metadata.GetAnyBrowseByListFromManyPages):
    """
    This class is created to get the list of all the scriptures, podcasts, christian books
      and topics from sermonindex. \n

    topic page : https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=topicsList
    scripture page : https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=booksList
    podcast page : https://www.sermonindex.net/podcast.php
    christian book page : https://www.sermonindex.net/modules/bible_books/?view=books_list
    """
    def __init__(self,root_folder,url,browse_by_type,is_text) -> None:
        """
        :param root_folder: The folder where the logs folder, metadata, download 
        folder will be created. It is the folder where everything will be placed. 
        If left empty,the current working directory will be used  
        :param url: The url of the web page to scrap 
        :param browse_by_type: The type of browse by used targeted. Either topics, speakers, or others
        :param is_text: If the data to be scrapped has to deal with audio sermons or text sermons
        """
        if not root_folder:
            root_folder = os.getcwd()
        
        material_root_folder = my_constants.SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER if is_text else my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
    
        metadata_root_folder,log_root_folder = get_sermonindex_metadata_and_log_folder(root_folder,material_root_folder)        

        super().__init__(metadata_root_folder,log_root_folder,
                            url_list = [url],
                            browse_by_type=browse_by_type)
        

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

    def scrap_page_useful_links(self,**kwargs):
        
        # Connect to the url and create a beautiful soup object with the html for scraping 
        self.connect_to_all_url()

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



# The classes here are not intended to scrap the list of the authors, or the list of topics. They 
# intended to scrap the work of a given author, topic, or the podcasts

class SermonIndexScrapAuthorTopicScripturePage(scrap_metadata.ScrapAuthorTopicScripturePage):
    def __init__(self,name, root_folder,url,browse_by_type,material_root_folder,information_type_root_folder,intermdiate_folders=None) -> None:
        """
        :param name: The name of the author, topic, ...
        :param root_folder: The folder where the logs, metadata download and more will be stored 
        :url: The url of the page to connect to and scrap the information 
        :browse_by_type: On sermonindex, the audio sermons are browseable by speaker, topic, scripture. It is \
        the mean  by which the browsing is made that is required here 
        :param material_root_folder: On sermonindex, there are audio sermons, text sermons, video sermons and \
        vintage image. Each material has his own root folder. See here for more \
        """
        #print(intermdiate_folders)

        if not isinstance(url,list):
            url = [url]

        metadata_root_folder,log_root_folder = get_sermonindex_metadata_and_log_folder(root_folder,material_root_folder)
        super().__init__(name,metadata_root_folder,log_root_folder,url,
                         browse_by_type,information_type_root_folder,
                         intermdiate_folders)




class SermonIndexAudioSermonScrapAuthorTopicScripturePage(SermonIndexScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder, url):
        
        super().__init__(name, root_folder, url,browse_by_type = "speaker",
                        material_root_folder =  my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,
                        information_type_root_folder = my_constants.MAIN_INFORMATION_ROOT_FOLDER)
        
    def scrap_page(self):
        """
        
        """


class SermonIndexScrapAuthorTopicScriptureMainInformation(SermonIndexScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder,browse_by_type, url_list,material_root_folder,intermdiate_folders=None):
        
        super().__init__(name, root_folder, url_list,browse_by_type,
                         information_type_root_folder = my_constants.MAIN_INFORMATION_ROOT_FOLDER,
                         material_root_folder = material_root_folder,
                         intermdiate_folders = intermdiate_folders)
        
        
    def scrap_url_pages(self):
        """
        Scrap the main information of the web page. Here the description, the 
        urls of the author, topic, scripture work 
        """
        super().scrap_url_pages()

        

        final_result = {}

        for url in self.url_informations:
                
            soup = self.url_informations[url].get("bs4_object")

            result = {}

            # The author presentation 
            author_presentation_element = soup.find("table",{"cellspacing":"0",
                                                            "cellpadding":"20",
                                                            "width":"550",
                                                            "bgcolor": "#f7f7e0"})
            

            if  author_presentation_element:

                author_img = author_presentation_element.find("img")
                #print(author_img)
                if author_img:
                    result["img_url"] =  author_img.get("src")
                
                author_name = author_presentation_element.find("h1")
                if author_name:
                    result['name'] = author_name.get_text()

                author_description = author_presentation_element.find_all("tr")[1]

                if author_description:
                    author_description = author_description.find("td")
                
                if author_description:
                    author_description_text = "".join(author_description.find_all(string = True,recursive = False))

                author_description_text2 = ""

                if author_description.find("p"):
                    author_description_text2 = "".join(author_description.find("p").find_all(string = True,recursive = False))

                result["description"] = [author_description_text,author_description_text2] 

                result["recomandation"] = []

                author_recomandations =  author_description.find("p")

                if author_recomandations:
                    author_recomandations = author_recomandations.find_all("a")
                else:
                    author_recomandations = []

                if author_recomandations:
                    for link in author_recomandations:
                        result["recomandation"].append({"url":link.get("href"),"text":link.get_text()})
                

            # Get the list of the pages of the works of the author, topic, scripture ... 
            other_page_url_list = soup.findAll("a")
            # The link to the other page text are digits
            other_page_url_list = [i.get("href") for i in other_page_url_list 
                                            if i.get_text().isdigit()]
            
            other_page_url_list = [url] + [urllib.parse.urljoin(url,i) for i in other_page_url_list]

            #print(other_page_url_list)

            result["pages"] = other_page_url_list

            if not result.get("name"):
                result["name"] = self.name 

            final_result[url] = result

        #print(final_result,self.url_list)

        return final_result
    

# Download the main information of each author, topic, etc 
class SermonIndexScrapWebSiteAllAuthorTopicScripturesMainInformation(scrap_metadata.ScrapWebSiteAllAuthorTopicScriptures):
    def __init__(self,root_folder,material_root_folder,browse_by_type, overwrite_log=False, update_log=True,intermdiate_folders=None):
        
        root_folder = _my_tools.process_path_according_to_cwd(root_folder)

        log_filepath = os.path.join(root_folder,my_constants.LOGS_ROOT_FOLDER,
                                       my_constants.SERMONINDEX_NAME,
                                       material_root_folder,browse_by_type,
                                       my_constants.ELABORATED_DATA_FOLDER,
                                       my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER,
                                       my_constants.get_default_json_filename(0))
        
        input_root_folder = os.path.join(root_folder,my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.SERMONINDEX_NAME,
                                         material_root_folder,my_constants.ELABORATED_DATA_FOLDER,
                                         browse_by_type)

        super().__init__(log_filepath = log_filepath,
                         input_root_folder = input_root_folder,
                         subfolder_pattern = my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER,
                         overwrite_log = overwrite_log,
                         update_log = update_log)
        
        self.material_root_folder = material_root_folder
        self.browse_by_type = browse_by_type
        self.root_folder = root_folder
    

    def prepare_input_json_file(self,matching_subfolders):
        """
        :param matching_subfolders: The folders from wich the json files will be searched out 
        """
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        input_json_files = []
        for folder in matching_subfolders:
            for file in [i for i in pathlib.Path(folder).rglob("*.json") if i.is_file()]:
                input_json_files.append(file)

        #print(input_json_files,"\n\n\n")

        return input_json_files
    
    
    def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """


        ob = SermonIndexScrapAuthorTopicScriptureMainInformation(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type = self.browse_by_type,
            url_list = element.get("url_list"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )

        ob.scrap_and_write()

    def is_element_data_downloaded(self,element):
        ob = SermonIndexScrapAuthorTopicScriptureMainInformation(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type =self.browse_by_type,
            url_list = element.get("url_list"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )
        return ob.is_data_downloaded()
        


# Scrap the works on the page of each author, topic, etc
# This class works for the audio sermons 


class SermonIndexAudioSermonScrapAuthorTopicScriptureWork(SermonIndexScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder,browse_by_type, url_list,material_root_folder,intermdiate_folders=None):
        
        super().__init__(name, root_folder, url_list,browse_by_type,
                         information_type_root_folder = my_constants.WORK_INFORMATION_ROOT_FOLDER,
                         material_root_folder = material_root_folder,
                         intermdiate_folders = intermdiate_folders)
        
        

    def scrap_url_pages(self):
        """
        Scrap the main information of the web page. Here the description, the 
        urls of the author, topic, scripture work 
        """
        super().scrap_url_pages()

        final_result = {}

        for current_page_url in self.url_informations:
                
            soup = self.url_informations[current_page_url].get("bs4_object")

            

            main_links_element = soup.find("table",{"border":0,"cellspacing":0,
                                            "cellpadding":10,"width":"100%"})
            
            if main_links_element:
                main_links_element = main_links_element.find_all("tr")
            else:
                return []
            

            #print(*main_links_element[:2],sep="\n\n\n")

            author_name = ""


            result = []

            compteur = 0
            for element in main_links_element:
            
                a_element = element.find("a")
                
                compteur += 1

                # There is some element in the main_links_element which are not a comment element

                if a_element:


                    url = a_element.get("href")
                    link_text  = a_element.get_text()

                    element_content = element.contents[-1].findAll("tr")[1:]


                    if (len(element_content) > 1):

                        add_element_to_topic = False
                        add_element_to_scriptures = False

                        topic_list = []
                        scripture_list = []

                        #print("\n\n\n",element_content[1].contents[0].contents[1:],compteur)
                        #print("\n\n\n",element_content[1],"\n",element_content)

                    
                        for comp in element_content[1].contents[0].contents[1:]:
                            if "by" in comp.get_text():
                                author_name = comp.get_text().split(" ")
                                if len(author_name) > 1:

                                    author_name = " ".join(author_name[1:])

                            if  "Topic:" in comp.get_text():
                                add_element_to_topic = True

                            if "Scripture" in comp.get_text():
                                add_element_to_scriptures = True
                                add_element_to_topic = False

                            if comp.name == 'i' and add_element_to_topic:
                                topic_list.append(comp.get_text())

                            if comp.name == 'i' and add_element_to_scriptures:
                                scripture_list.append(comp.get_text())

                        
                        link_description = "".join(element_content[2].find("td").find_all(string = True,recursive = False))


                        download_number = element_content[3].get_text().split("\xa0")
                        if len(download_number) >= 1:
                            download_number = download_number[0]


                        element_comment_a = element_content[-1].find("a")

                        element_comment_url = urllib.parse.urljoin(url,element_comment_a.get("href"))
                        
                        comment_number = int(element_comment_a.get_text().split("(")[1][:-1])
                        
                        comments = []

                        if comment_number > 0:
                            #print(self.url_informations[current_page_url].keys())
                            comments = self.get_element_comments(element_comment_url,
                                                                 link_text,
                                                                 os.path.dirname(
                                                                     self.url_informations[current_page_url].get("html_filepath")))


                        # Take the number of download

                        download_number_element = element.find("td",{"colspan":"2","class":"bg3","align":"right"}) 

                        download_number = download_number_element.get_text()

                        download_number = download_number.split("\xa0")
                        if len(download_number) > 1:
                            download_number = download_number[0]
                        else:
                            download_number = -1

                        result.append({
                            "url":url,
                            "author_name":author_name,
                            "downlaod_number":download_number,
                            "topics":topic_list,
                            "scriptures":scripture_list,
                            "link_text":link_text,
                            "link_description":link_description,
                            "comments_url":element_comment_url,
                            "comments":comments,
                            "comments_number": comment_number
                        })

            final_result[url] = result

        return final_result


    def get_element_comments(self,comment_url,link_text,raw_filefolder):
        """
        :param comment_url: The url of the comment. Here is an example of comment's  
        url on a sermon of Ravenhill https://www.sermonindex.net/modules/mydownloads/singlefile.php?lid=14469&commentView=itemComments
        :param link_text: The text content of the anchor object of the url
        :param raw_filefolder: The folder where the html files of this author or 
        topic are saved  
        """
        #print(raw_filefolder)
        comment_html_file_path =  os.path.join(
            os.path.dirname(raw_filefolder),
            "comments",
            _my_tools.remove_forbiden_char_in_text(link_text.strip()).replace("...",""),"page.html")
        

        response = requests.get(comment_url,timeout=20)

        # Write the comment file 
        _my_tools.write_file(comment_html_file_path,response.text)

        soup = BeautifulSoup(response.text,features="lxml")

        comment_element = soup.find("table",{"width":"90%"})
        

        comments = [tr.find("td") for tr in  comment_element.contents if tr.name == "tr"]

        comments_list = []
        for i in range(2,len(comments),3):
            comments_list.append(
                {
                    "title":comments[i-2].find("strong").get_text(),
                    "text":comments[i].get_text(),
                }
            )

                    
        return {"local_html_filepath":comment_html_file_path,
                "request_headers":dict(response.headers),
                "comments":comments_list}
    

    def is_data_downloaded(self):

        for url in self.url_informations:
            file_path = self.url_informations[url].get("json_filepath")
            if not os.path.exists(file_path):
                return False
            
            
            file_content = _my_tools.read_json(file_path)

            #print(file_content,file_path)


            if not file_content:
                return False
            
            # Check mandatory information in the json file 

            if not file_content.get("url"):
                return False
            
        return True

    


class SermonIndexScrapWebSiteAllAuthorTopicScripturesWork(scrap_metadata.ScrapWebSiteAllAuthorTopicScriptures):
    def __init__(self,root_folder,material_root_folder,browse_by_type, overwrite_log=False, update_log=True,intermdiate_folders=None):
        
        root_folder = _my_tools.process_path_according_to_cwd(root_folder)

        log_filepath = os.path.join(root_folder,my_constants.LOGS_ROOT_FOLDER,
                                       my_constants.SERMONINDEX_NAME,
                                       material_root_folder,browse_by_type,
                                       my_constants.ELABORATED_DATA_FOLDER,
                                       my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,
                                       my_constants.get_default_json_filename(0))
        
        input_root_folder = os.path.join(root_folder,
                                         my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.SERMONINDEX_NAME,
                                         material_root_folder,my_constants.ELABORATED_DATA_FOLDER,
                                         browse_by_type)
        

        super().__init__(log_filepath = log_filepath,
                         input_root_folder = input_root_folder,
                         subfolder_pattern = my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,
                         overwrite_log = overwrite_log,
                         update_log = update_log)
        
        self.material_root_folder = material_root_folder
        self.browse_by_type = browse_by_type
        self.root_folder = root_folder


    
    def prepare_input_json_file(self,matching_subfolders):
        """
        :param matching_subfolders: The folders from wich the json files will be searched out 
        """
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        input_json_files = []
    
        for folder in matching_subfolders:
            for file in [i for i in pathlib.Path(folder).rglob("*.json") if i.is_file()]:
                if str(file.parent).endswith(my_constants.MAIN_INFORMATION_ROOT_FOLDER):
                    input_json_files.append(file)

        #print(input_json_files)

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
        
        
        self.element_dict[element.get("name")] = {
            **element,
            **{"download_log":{
                "input_file_index":self.meta_informations["input_files_information"]\
                                                        ["input_files"].index(kwargs.get("file_path")),
                "intermediate_folders":[]} #kwargs.get("intermediate_folders")
                }
                }
        
    
    def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)

        print(element.get("name"))
        
        ob = SermonIndexAudioSermonScrapAuthorTopicScriptureWork(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type = self.browse_by_type,
            url_list = element.get("pages"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )


        ob.scrap_and_write()

    def is_element_data_downloaded(self,element):
        ob = SermonIndexAudioSermonScrapAuthorTopicScriptureWork(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type =self.browse_by_type,
            url_list = element.get("url_list"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )
        return ob.is_data_downloaded()
        

