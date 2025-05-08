import asyncio
import copy
import datetime
import os
import re 



from Instrumentum_sanae_doctrinae.my_tools.scraping_using_selenium import connect_to_url_with_selenium
from Instrumentum_sanae_doctrinae.web_scraping import  http_connexion, my_errors, scrap_metadata
from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_scrap_metadata
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools

from Instrumentum_sanae_doctrinae.web_scraping.monergism.mn_tools import *
import aiohttp
from bs4 import BeautifulSoup





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
                          url_list = [{"url":url}],
                            browse_by_type=browse_by_type)
    
    
    

    async def scrap_page_useful_links(self):
        """
        This method return the useful links of the page. 

        For example for the page of the authors of monergism 
        https://www.monergism.com/authors The useful link are the <a> element
        of authors or topics as **<a href="/search?f[0]=author:39115">H.B. Charles Jr.</a>**
        """
        
        final_result = []

        for url in self.url_informations:
            #print(url)
            # Get the links (<a> </a>) which leads to the authors main page. 
            #print(self.url_informations[url]["bs4_object"].find("div",attrs = {"class":}))
            #print(type(self.url_informations[url]["bs4_object"]))
            
            
            links = self.url_informations[url]["bs4_object"].find_all("a")
            
            links = [i for i in links if i.attrs.get("href")]
            
            #print(self.url_informations[url]["bs4_object"])
    
            authors_links = [i for i in links if self.useful_link_validation_function(i)]

            result = []
            for anchor_object in authors_links:
                link_text = _my_tools.replace_forbiden_char_in_text(
                        _my_tools.remove_consecutive_spaces(anchor_object.get_text()))
                result.append(
                    {
                        "name": link_text,
                        "url_list":[anchor_object]
                    }
                )
                
            final_result.append((url,result))

        return final_result
    
    def useful_link_validation_function(self,link):
        """
        :param link: A bs4 HTML anchor element
        Return true if the link is the link of a topic or an author
        """
        
        return (("/topics/" in link.attrs.get("href")) or ("=author:" in link.attrs.get("href")))
    
    
    
    async def get_list_of_downloadable_element(self,update_from_internet = False):
        """
        :param update_from_internet: If true, the json file containing the name of the downloadable element are updated from internet. 
        This function return the list of all the element that can be downloaded. 
        For the authors, it the name of the authors. 
        For the scriptures, it is the name of the bible books. 
        For topics, it is the name of the topics 
        """
        
        if update_from_internet:
            await self.scrap_and_write()
    
        result = {}
        for url in self.url_informations:
            url_information = self.url_informations[url]
            json_filepath = url_information.get("json_filepath")
            
            if json_filepath:
                url = url_information.get("url")
                
                json_filecontent = await _my_tools.async_read_json(json_filepath)
                
                result[url] = json_filecontent.get("data")
        
        return result
    
    
     
    async def connect_to_all_url(self,**kwargs):
        """
        Connect to an html page whose url has been given 
        """

        
        self.main_request_session = aiohttp.ClientSession()
        
        #print(self.url_informations)
        
        # I use a deepcopy here becaus the potential deletions will change
        # The size of the dict during the iteration 
        for url,value in copy.deepcopy(self.url_informations).items():
            
            
            # This value must be True by default 
            # It can be set to false if data of this url is already downloaded             
            connect_to_url = value.get('connect_to_url')
            
            #print(url_dict,connect_to_url)
            
            # Connect to the url if and only if authorised 
            if connect_to_url:
                #print(url)
                
                #timeout = aiohttp.ClientTimeout(total=15)
                #print(url_dict)
            
                html = connect_to_url_with_selenium(url)
                #print(html)
        
                #print(response.headers)            
                
                self.url_informations[url]["request"] = None
                self.url_informations[url]["html_text"] = html
                self.url_informations[url]["request_datetime"] = _my_tools.datetimeToGoogleFormat(datetime.datetime.now()),
                # Create a bs4 object with the html text of the last request 
                self.url_informations[url]["bs4_object"] = BeautifulSoup(html,features="html.parser") 
    
        
            else:
                # Add the url to which no connection is made to the list it belongs to 
                self.url_informations_not_connect[url] = copy.deepcopy(self.url_informations[url])
                
                # Remove it from the list of the standard url for download; 
                del self.url_informations[url]

        

class GetScriptureList(GetTopicOrAuthorOrScriptureList):
    def __init__(self, root_folder,) -> None:
        super().__init__(root_folder,
                          "https://www.monergism.com/scripture",
                            "scripture")
        


    async def scrap_page_useful_links(self):
        
        result = []

        for url in self.url_informations:
            links_div_list = self.url_informations[url]['bs4_object'].findAll("div",{"class":"view-grouping"})
            url_links = []
            
            # The bible book to which the links refer to
            

            for link_div in links_div_list:
                name = link_div.find("div",class_="view-grouping-header").get_text().strip()
                

                # Take the anchor list and modify their string to correspond to the 
                # string of div containing them I do it because the anchor elements 
                # text do not correspond to leviticus, chronicles or any book in 
                # in the bible but to the type of the material (audio, book, etc)
                anchor_object_list = link_div.findAll("a")
                    
                url_links.append({"name":name,"url_list": anchor_object_list})

            
            result.append((url,url_links))

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
        
        
