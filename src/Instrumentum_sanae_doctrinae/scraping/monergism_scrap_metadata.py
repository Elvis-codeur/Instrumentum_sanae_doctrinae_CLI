"""
This module is created for the scrapping of metadata from https://www.monergism.com/


"""

import os 
import pathlib
import re
import urllib
import urllib.parse
from urllib.parse import urlparse, parse_qs


from ..scraping import scrap_metadata
from ..scraping import my_constants
from ..scraping import http_connexion
from ..scraping import _my_tools



def get_monergism_metadata_and_log_folder(root_folder):
    metadata_root_folder = os.path.join(root_folder,my_constants.MONERGISM_METADATA_ROOT_FOLDER)
    log_root_folder = os.path.join(root_folder,my_constants.MONERGISM_LOG_ROOT_FOLDER)
                           
    return metadata_root_folder,log_root_folder


class GetTopicOrAuthorOrScriptureList(scrap_metadata.GetAnyBrowseByListFromManyPages):
    """
    This class is created to get the list of all the authors, topics and scriptures  from monergism. 
    The topics and the author page has the same html structure for the presentation 
    of the authors and the topics 

    author page : https://www.monergism.com/topics
    topics page : https://www.monergism.com/authors
    scripture page : https://www.monergism.com/scripture
    """
    def __init__(self,root_folder,url,browse_by_type) -> None:
        """
        :param root_folder: The folder where the logs folder, metadata, download 
        folder will be created. It is the folder where everything will be placed. 
        If left empty,the current working directory will be used  
        :param url: The url of the web page to scrap 
        :param browse_by_type: The type of browse by used targeted. Either topics, speakers, or others
        """
        if not root_folder:
            root_folder = os.getcwd()


        metadata_root_folder,log_root_folder = get_monergism_metadata_and_log_folder(root_folder)

        super().__init__(metadata_root_folder,log_root_folder,
                          url_list = [url],
                            browse_by_type=browse_by_type)
        

    def scrap_page_useful_links(self):
        """
        This method return the useful links of the page. 

        For example for the page of the authors of monergism 
        https://www.monergism.com/authors The useful link are the <a> element
        of authors or topics as **<a href="/search?f[0]=author:39115">H.B. Charles Jr.</a>**
        """

        self.connect_to_all_url()

        result = []

        for url in self.url_informations:
            # Get the links (<a> </a>) which leads to the authors main page. 
            links = self.url_informations[url]["bs4_object"].find("div",{"id","region-content"}).findAll("a")#"section",{"id","block-views-36de325f9945b74b1c08af31b5376c02"}).find_all("a",{"class":None})
            links = [i for i in links if i.attrs.get("href")]
    
            authors_links = [[i] for i in links if self.useful_link_validation_function(i)]

            result.append((url,authors_links))

        return result
    
    def useful_link_validation_function(self,link):
        """
        :param link: A bs4 HTML anchor element
        Return true if the link is the link of a topic or an author
        """
        return (("/topics/" in link.attrs.get("href")) or ("=author:" in link.attrs.get("href")))
    
    

class GetScriptureList(GetTopicOrAuthorOrScriptureList):
    def __init__(self, root_folder,) -> None:
        super().__init__(root_folder,
                          "https://www.monergism.com/scripture",
                            "scripture")
        


    def scrap_page_useful_links(self):
        self.connect_to_all_url()

        result = []

        for url in self.url_informations:
            links_div_list = self.url_informations[url]['bs4_object'].findAll("div",{"class":"view-grouping"})
            url_links = []

            for link_div in links_div_list:

                # Take the anchor list and modify their string to correspond to the 
                # string of div containing them I do it because the anchor elements 
                # text do not correspond to leviticus, chronicles or any book in 
                # in the bible but to the type of the material (audio, book, etc)
                anchor_object_list = link_div.findAll("a")
                for anchor_object in anchor_object_list:
                    anchor_new_string = link_div.get_text().split("\n")
                    if anchor_new_string:
                        anchor_object.string = anchor_new_string[0]
                    else:
                        anchor_object.string = ""
                url_links.append(anchor_object_list)

            # Remove the duplicates
            final_url_links_url = []
            final_url_links = []
            for anchor_list in url_links:
                if anchor_list[0].get("href") not in final_url_links_url:
                    final_url_links.append(anchor_list)
            
            result.append((url,final_url_links))

        return result

class GetTopicList(GetTopicOrAuthorOrScriptureList):
    def __init__(self, root_folder) -> None:
        super().__init__(root_folder,
                          "https://www.monergism.com/topics",
                          "topic")


class GetSpeakerList(GetTopicOrAuthorOrScriptureList):
    def __init__(self, root_folder,) -> None:

        super().__init__(root_folder, 
                         "https://www.monergism.com/authors",
                         "speaker")


    

class MonergismScrapAuthorTopicScripturePage(scrap_metadata.ScrapAuthorTopicScripturePage):
    def __init__(self, name,root_folder,url_list, browse_by_type,
                 information_type_root_folder,intermdiate_folders) -> None:
        
        metadata_root_folder,log_root_folder = get_monergism_metadata_and_log_folder(root_folder)
        
        if not isinstance(url_list,list):
            url_list = [url_list]
     

        super().__init__(name, metadata_root_folder, log_root_folder,url_list,
                          browse_by_type,information_type_root_folder,intermdiate_folders)

    def scrap_url_pages(self):
        """
        
        """
        self.connect_to_all_url()
    


    

class MonergismScrapAuthorTopicScriptureWork(MonergismScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder, url_list, browse_by_type,intermdiate_folders = None):

        super().__init__(name, root_folder, url_list, browse_by_type,
                          information_type_root_folder = my_constants.WORK_INFORMATION_ROOT_FOLDER,
                          intermdiate_folders = intermdiate_folders)
        

    
    
    def scrap_url_pages(self):
        """
        Scrap the main links of the page. See this file (documentation/documentation.odt) for more info 
        """

        self.connect_to_all_url()

        final_result = {}

        for url in self.url_informations:
            
            # Take the div containing the links of the author 
            
            bs4_obect = self.url_informations[url].get("bs4_object")
            
            links_div = bs4_obect.find_all("div",
                                            class_=re.compile("view.*view-link-search.*view-id-link_search.*view-display-id-page.*view-dom-id-")) 
            
            if(len(links_div) != 0):
                links_div = links_div[0]

                # The header where this text isYour Search Yielded <n> Results
                # Displaying <a> Through <b> where <n> is the total number of links about the author and <a> and <b> the range of links displayed 
                header = links_div.find("div",{"class":"view-header"})

                header_text = header.get_text()
                header_text = header_text.split(" ")
                
                header_numbers = []

                for text in header_text:
                    if text.strip().isdigit():
                        header_numbers.append(int(text.strip()))

                # The number of element monergism has on the author
                self.num_result = header_numbers[0]

                # The index of element returned in this page. For exemple 1rst to 50th gives 1 and 50 in the two variables
                #display_index_begin = header_numbers[1]
                #display_index_end = header_numbers[2]


                # Get the main page links 
                main_content = links_div.find("div",{"class":"view-content"})
                main_links_li = main_content.find_all("li",{"class":"views-row"})
                main_links = []

                for li in main_links_li:
                    li = li.find("div").find("span")
                    link_type = li.get("class")[1]
                    link_href = li.find("a").get("href")
                    link_text = li.find("a").get_text()
                    main_links.append({
                        "link_type":link_type,
                        "url":link_href,
                        "link_text":link_text
                    })

                
                #print(main_links,url,"\n\n")

                final_result[url] = main_links

        return final_result




class MonergismScrapWebSiteAllAuthorTopicScripturesWork(http_connexion.ParallelHttpConnexionWithLogManagement):
    def __init__(self,root_folder,browse_by_type, overwrite_log=False, update_log=True,intermdiate_folders=None):

        root_folder = _my_tools.process_path_according_to_cwd(root_folder)

        log_filepath = os.path.join(root_folder,my_constants.LOGS_ROOT_FOLDER,
                                       my_constants.MONERGISM_NAME,
                                       browse_by_type,
                                       my_constants.ELABORATED_DATA_FOLDER,
                                       my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,
                                       my_constants.get_default_json_filename(0))
        
        input_root_folder = os.path.join(root_folder,
                                         my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.MONERGISM_NAME,
                                         my_constants.ELABORATED_DATA_FOLDER,
                                         browse_by_type)
        

        super().__init__(log_filepath = log_filepath,
                         input_root_folder = input_root_folder,
                         subfolder_pattern = my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,
                         overwrite_log = overwrite_log,
                         update_log = update_log)
        
        self.browse_by_type = browse_by_type
        self.root_folder = root_folder


    def prepare_input_json_file(self,input_root_folder):
        """
        :param input_root_folder: The folders from wich the json files will be searched out 
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
            **{
                "data":{
                    "name":element.get("name"),
                    "pages":element.get("pages")
                }
            },
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

        #print(element.get("data"))
        
        ob = MonergismScrapAuthorTopicScriptureWork(
            name = element.get("data").get("name"),
            root_folder = self.root_folder,
            browse_by_type = self.browse_by_type,
            url_list = element.get("data").get("pages"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders")
        )


        ob.scrap_and_write()

    def is_element_data_downloaded(self,element):
        ob = MonergismScrapAuthorTopicScriptureWork(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type =self.browse_by_type,
            url_list = element.get("url_list"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders")
        )
        return ob.is_data_downloaded()
        

