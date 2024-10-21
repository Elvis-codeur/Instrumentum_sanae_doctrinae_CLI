
from concurrent.futures import ThreadPoolExecutor
import os 
import urllib
import urllib.parse
import pathlib
import traceback



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
        

     

    def scrap_page_useful_links(self):
        """
        This method return the useful links of the page. 

        For example for the page of the topics of sermonindex https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=topicsList
        The useful link are the <a> element
        of topics as <a href="scr_index.php?act=topicSermons&amp;topic=1%20Corinthians&amp;page=0">1 Corinthians</a>

        """


        self.connect_to_url()

        result = []

        for url in self.url_informations:
            # Get the links (<a> </a>) which leads to the authors main page. 
            links = self.url_informations[url]['bs4_object'].findAll("a")
            
            # Get all the links of the document
            links = [i for i in links if i.attrs.get("href")]

            links = self.page_useful_links_validation_method(links)

            links = [[i] for i in links]

            result.append((url,links))

        return result

    def page_useful_links_validation_method(self,anchor_list):
        pass 

    
    def useful_link_validation_function(self,link):
        """
        :param link: A bs4 HTML anchor element

        Return true if the link is an usefull link 
        """
        

class GetTopicList(GetTopicOrScriptureOrPodcastOrChristianBooks):
    def __init__(self, root_folder, browse_by_type = "topic") -> None:
        super().__init__(root_folder,
                          url = "https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=topicsList",
                            browse_by_type = browse_by_type,
                            is_text=False)
        #print(self.__dict__)     

    def page_useful_links_validation_method(self,anchor_list):
        # Keep the links which have topic in their url
        anchor_list = [i for i in anchor_list if ("topic" in i.attrs.get("href") and "page" in i.attrs.get("href"))]

        return anchor_list


class GetScriptureList(GetTopicOrScriptureOrPodcastOrChristianBooks):
    """"""
    def __init__(self, root_folder, browse_by_type = "scripture") -> None:
        super().__init__(root_folder,
                          url = "https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=booksList",
                         browse_by_type = browse_by_type,
                         is_text=False)
        """"""

    def page_useful_links_validation_method(self,anchor_list):
        # Keep the links which have boook in their url
        anchor_list = [i for i in anchor_list if ("act=bookSermons" in i.attrs.get("href") and "page" in i.attrs.get("href"))]
       
        return anchor_list
    



class GetChristianBookList(GetTopicOrScriptureOrPodcastOrChristianBooks):
    def __init__(self, root_folder, browse_by_type = "christian_book") -> None:
        super().__init__(root_folder,
                          url = "https://www.sermonindex.net/modules/bible_books/?view=books_list",
                         browse_by_type = browse_by_type,
                         is_text=True)
    
    def page_useful_links_validation_method(self,anchor_list):
        # Keep the links which have boook in their url
        anchor_list = [i for i in anchor_list if ("view=book&book" in i.attrs.get("href"))]

        return anchor_list
    


class GetSpeakerLinks(scrap_metadata.GetAnyBrowseByListFromManyPages):
    def __init__(self, metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders=None) -> None:
        super().__init__(metadata_root_folder, log_root_folder, [url], browse_by_type, intermdiate_folders)

        # A list of the other pages. For sermonindex, it is the links who's text begin with ~
        # See this pages for more 
        # https://www.sermonindex.net/modules/mydownloads/
        # https://www.sermonindex.net/modules/articles/

        self.other_page_page_list = []


    def page_useful_links_validation_method(self,anchor_list):

        pass 

    def scrap_page_useful_links_and_other_page_links(self):
        
        
        # Connect to the url and create a beautiful soup object with the html for scraping 
        self.connect_to_url()

        result = [] 

        for url in self.url_informations:

            other_page_links = []

            links = []

            anchor_list = self.url_informations[url]['bs4_object'].findAll("a")

            # A method to filter the useful links. All the subclasses has to reimplement 
            # this method to their needs
            anchor_list = [i  for i in anchor_list if i.attrs.get("href")]
            anchor_list = self.page_useful_links_validation_method(anchor_list)
        
            for i in anchor_list:
                if "~" not in i.get_text():
                    if i.get_text():
                        links.append([i])
                else:
                    other_page_links.append((urllib.parse.urljoin(url, i.attrs.get("href")),i.get_text().strip()))

            result.append(((url,links),other_page_links))
            #print((url,links),other_page_links)
        return result
    
       
    def scrap_page_useful_links(self):
        result = self.scrap_page_useful_links_and_other_page_links()
        self.other_page_page_list = [i[1] for i in result]
        links = [i[0] for i in result]

        return links



class GetAudioSermonsSpeakerLinks(GetSpeakerLinks):
    def __init__(self, metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders=None) -> None:
        super().__init__(metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders)

    def page_useful_links_validation_method(self, anchor_list):

        result = []
        for  anchor_object in anchor_list:
            next_sibling = anchor_object.next_sibling
            if next_sibling:
                if next_sibling:
                    if "(" in next_sibling and ")" in next_sibling:
                        result.append(anchor_object)
        return result

   
class GetTextSermonsSpeakerLinks(GetSpeakerLinks):
    def __init__(self, metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders=None) -> None:
        super().__init__(metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders)

    def page_useful_links_validation_method(self,anchor_list):
        result = [i for i  in anchor_list if "view=category&cid="  in i.attrs.get("href")]
        return result

class GetVideoSermonsSpeakerLinks(GetSpeakerLinks):
    def __init__(self, metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders=None) -> None:
        super().__init__(metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders)

    def page_useful_links_validation_method(self, anchor_list):
        result = [i for i  in anchor_list if "/myvideo/viewcat.php?cid="  in i.attrs.get("href")]
        return result

class GetVintageImageSpeakerLinks(GetSpeakerLinks):
    def __init__(self, metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders=None) -> None:
        super().__init__(metadata_root_folder, log_root_folder, url, browse_by_type, intermdiate_folders)

    def page_useful_links_validation_method(self, anchor_list):
        result = [i for i  in anchor_list if "/myalbum/viewcat.php?cid="  in i.attrs.get("href")]
        return result

    
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
        
        ob.scrap_and_write()

        #print(ob.other_page_page_list)

        for other_page_per_url in ob.other_page_page_list:
            for url,url_text in other_page_per_url:
                other_page_ob = ob_class(self.metadata_root_folder,
                            self.log_root_folder,
                            url,
                            "speaker",
                            intermdiate_folders = [url_text.strip()]
                                )
                other_page_ob.scrap_and_write()

            
        

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
    def __init__(self,name, root_folder,url,browse_by_type,material_root_folder,intermdiate_folders=None) -> None:
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
        super().__init__(name,metadata_root_folder,log_root_folder,url,browse_by_type,intermdiate_folders)


class SermonIndexAudioSermonScrapAuthorTopicScripturePage(SermonIndexScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder, url):
        
        super().__init__(name, root_folder, url,browse_by_type = "speaker",
                        material_root_folder =  my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER)
        
    def scrap_page(self):
        """
        
        """


class SermonIndexAudioSermonScrapAuthorTopicScriptureMainInformation(SermonIndexScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder,browse_by_type, url_list,intermdiate_folders=None):
        
        super().__init__(name, root_folder, url_list,browse_by_type,
                        material_root_folder =  my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER,intermdiate_folders = intermdiate_folders)
        
    def scrap_url_pages(self):
        """
        Scrap the main information of the web page. Here the description, the 
        urls of the author, topic, scripture work 
        """
        super().scrap_url_pages()

        

        final_result = []

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

            result["pages"] = other_page_url_list

            if not result.get("name"):
                result["name"] = self.name 

            final_result.append(result)

        #print(final_result,self.url_list)

        return final_result
    

class SermonIndexAudioSermonScrapAuthorMainInformation(SermonIndexAudioSermonScrapAuthorTopicScriptureMainInformation):
    def __init__(self, name, root_folder, url_list,intermdiate_folders):
        super().__init__(name, root_folder, "speaker", url_list,intermdiate_folders)




class SermonIndexScrapWebSiteAllAuthorTopicScripturesMainInformation(scrap_metadata.ScrapWebSiteAllAuthorTopicScriptures):
    def __init__(self,root_folder,material_root_folder,browse_by_type, overwrite_log=False, update_log=True,intermdiate_folders=None):
        
        root_folder = _my_tools.process_path_according_to_cwd(root_folder)

        log_root_folder = os.path.join(root_folder,my_constants.LOGS_ROOT_FOLDER,
                                       my_constants.SERMONINDEX_NAME,
                                       material_root_folder,browse_by_type,
                                       my_constants.ELABORATED_DATA_FOLDER,
                                       my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER,
                                       my_constants.get_default_json_filename(0))
        
        input_root_folder = os.path.join(root_folder,my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.SERMONINDEX_NAME,
                                         material_root_folder,my_constants.ELABORATED_DATA_FOLDER,
                                         browse_by_type)

        super().__init__(log_root_folder,
                         input_root_folder,
                         overwrite_log,update_log)
        
        self.root_folder = root_folder

    
    def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """
        

        try: 
            ob = SermonIndexAudioSermonScrapAuthorMainInformation(
            element.get("name"),self.root_folder,element.get("url_list"),
            element.get("download_log").get("intermediate_folders"))
            ob.scrap_and_write()
            
            return {"success":True}
        except Exception as e:
            return {"success":False,"error":"".join(traceback.format_exception(e))}


    def download(self,download_batch_size):
        """
        Download the content of the input files concurrently 
        by a batch of size :data:`download_batch` 
        """
        result = []

        # Update before the begining of downloads
        self.update_downloaded_and_to_download() 
        to_download_len = len(self.log_file_content["to_download"].values())

        for key in self.log_file_content["to_download"]:
            element = self.log_file_content["to_download"][key]
            
            element["download_log"]["intermediate_folders"] = ["Elvis est un enfant de Dieu"]
            print(self.is_element_data_downloaded(element))

            self.download_element_data(element)
            break
      



     

class SermonIndexScrapWebSiteAudioSermonAllAuthorMainInformation(SermonIndexScrapWebSiteAllAuthorTopicScripturesMainInformation):
    def __init__(self, root_folder, material_root_folder, browse_by_type, overwrite_log=False, update_log=True,intermdiate_folders=None):
        super().__init__(root_folder, material_root_folder, browse_by_type, overwrite_log, update_log,intermdiate_folders)


    def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        ob = SermonIndexAudioSermonScrapAuthorMainInformation(
            element.get("name"),self.root_folder,element.get("url_list"),
            element.get("download_log").get("intermediate_folders")
        )

        ob.scrap_and_write()

    def is_element_data_downloaded(self,element):
        ob = SermonIndexAudioSermonScrapAuthorMainInformation(
            element.get("name"),self.root_folder,element.get("url_list"),
            element.get("download_log").get("intermediate_folders")
        )
        #print(ob)
        return ob.is_data_downloaded()
        