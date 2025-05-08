
import copy
import datetime
import os 
import urllib
from Instrumentum_sanae_doctrinae.my_tools.scraping_base_classes import ParallelConnexionWithLogManagement
import aiohttp
import requests

from bs4 import BeautifulSoup


from ..my_tools import my_constants
from . import my_errors
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools



class ScrapDataFromURL():
    """
    This class will be used to scrap the speakers, topics, series etc of the web site.
    This class is abstract and meant to be inherited of.  
        
    """
    
    def __init__(self,metadata_root_folder,log_root_folder,url_info_list,browse_by_type,intermdiate_folders,**kwargs) -> None:
        """
        :param metadata_root_folder: The folder where the metadata will be stored
        :param log_root_folder: The folder where the log of the download and scraping process will be stored
        :param url_info_list: The list of the dict containing url of the page and other information
        will be found. This class focus on the case where all the topics, authors, etc are 
        on a single page. What is the case on monergism and sermonindex in most of the situation. You an provide many url. Each url is scrapped  
        :param browse_by_type: The type of browse by used targeted. Either topics, speakers, or others
        :param intermdiate_folders: A list of string.It is used if the file must not be
        stored in the folder directly but in a subfolder. It is useful for web pages
        like the page of authors of sermonindex https://www.sermonindex.net/modules/mydownloads/
        There is some main links to be scrapped and somes links who leads to other authors listed from A to F, etc 
        This can be used to create a subfolder to this links 
        """
        
        self.metadata_root_folder = _my_tools.process_path_according_to_cwd(metadata_root_folder) #: The root folder where the metadata will be stored
        self.log_root_folder =  _my_tools.process_path_according_to_cwd(log_root_folder) #: The root folder where the logs of the download and scraping process will be stored

        
        # Ensure that url_info_list is a list of dict in the form {"url":"value",...}
        if not isinstance(url_info_list,list):
            self.url_info_list = [url_info_list]
        else:
            self.url_info_list = url_info_list
            
        for indice,url_info in enumerate(self.url_info_list):
            if not isinstance(url_info,dict):
                 self.url_info_list[indice] = {"url":url_info}
                 
        self.browse_by_type = browse_by_type
        
        self.intermdiate_folders = intermdiate_folders
        
        self.url_informations = {}
       
        
        
         # It contains the json filepath, html filepat, etc of each url  
        self.url_informations = {i.get("url"):{"json_filepath":None,
                                               "html_filepath":None,
                                               "connect_to_url":True,# If true, a connection is  made to the url otherwise it is not made
                                                                     # The goal here is to avoid for exemple to connect urls which data are already downloaded  
                                                "request":None,"bs4_object":None,
                                                "is_html_file_locally_saved":False,
                                                "is_json_file_locally_saved":False,
                                                "json_file_content":None} 
                                                    
                                                    for i in self.url_info_list} #: A dict for each url 

        # A dict for the url to which no connection will be made 
        # I set them appart to avoid any disturbance of the my code which already some pretty big 
        self.url_informations_not_connect = {}    
    
        self.prepare_url_informations()
        
    def prepare_url_informations(self,**kwargs):
        
        
        intermdiate_folders = [_my_tools.replace_forbiden_char_in_text(i) for i in self.intermdiate_folders]

        compteur = 0 
        
        for indice,element in enumerate(self.url_info_list):
            json_filepath = os.path.join(self.metadata_root_folder,
                                          my_constants.ELABORATED_DATA_FOLDER,
                                          *intermdiate_folders,
                                          my_constants.get_default_json_filename(indice))
            
            html_filepath =  os.path.join(self.metadata_root_folder,my_constants.RAW_DATA_FOLDER,
                                          *intermdiate_folders,
                                          my_constants.get_default_html_filename(indice))    
                
            self.url_informations[element.get("url")]['json_filepath'] =  json_filepath 
            
            self.url_informations[element.get("url")]['html_filepath']  = html_filepath
            
            # Mise à jour normal 
            compteur += 1
        
        self.main_request_session = None
        
        # The secondary is a non asynchronous http client 
        self.secondary_request_session = requests.Session() 
        
    
        
    async def close(self):
        if self.main_request_session:
            await self.main_request_session.close()
            
            
    
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
                async with self.main_request_session.get(url=url) as response:
                    
                    if response.status == 404:
                        raise my_errors.HTTP404Error(url)
                    
                    try:
                        html = await response.text()
                    except UnicodeDecodeError:
                        raw_data = await response.read()
                        html = raw_data.decode("utf-8",errors="replace")

                    #print(response.headers)            
                    
                    self.url_informations[url]["request"] = response
                    self.url_informations[url]["html_text"] = html
                    self.url_informations[url]["request_datetime"] = _my_tools.datetimeToGoogleFormat(datetime.datetime.now()),
                    # Create a bs4 object with the html text of the last request 
                    self.url_informations[url]["bs4_object"] = BeautifulSoup(html,features="html.parser") 
            else:
                # Add the url to which no connection is made to the list it belongs to 
                self.url_informations_not_connect[url] = copy.deepcopy(self.url_informations[url])
                
                # Remove it from the list of the standard url for download; 
                del self.url_informations[url]
                
                
    #print(self.url_informations)

    def next_page(self,**kwargs):
        """
        This method is meant to return the next page if there is an url to a next page. 
        For example this page of CH Spurgeon from  monergism ( https://www.monergism.com/search?f[0]=author:34468)
        has next page while this page from sermon index does not have one (https://www.monergism.com/search?f[0]=author:41188)
        """


    async def scrap_url_pages(self,**kwargs):

        """
        Scrap the web page 
        """
       
        
    def anchor_object_list_to_dict_list(self,anchor_dict_list,url,version = "0.0.1",**kwargs):
        """
        :param anchor_dict_list: The list of a dict containing the text to 
            associate to the anchor elements and the anchor elements 
        :param url: The url of the web page where the  anchor elements are taken of 
        :param version: The version of the data structure of the dict who contains the information taken 
        from the anchor object   
        """
        result = []
        for anchor_dict in anchor_dict_list:
            url_list = []
            
            #print(anchor_dict)

            for anchor_ob in anchor_dict.get("url_list"):
                
                link_text = anchor_ob.get_text().strip() 
                
                link_text = _my_tools.replace_forbiden_char_in_text(
                        _my_tools.remove_consecutive_spaces(link_text))
                
                url_list.append(
                    {
                        "url":urllib.parse.urljoin(url,anchor_ob.get("href")),
                        "link_text": link_text                 
                    }
                    )

            result.append({
                "version":version,
                "name" : _my_tools.replace_forbiden_char_in_text(
                        _my_tools.remove_consecutive_spaces(anchor_dict.get("name"))),
                "url_list" :url_list 
            })

        return result
    
    def prepare_json_data_for_saving(self,element_list,url,version = "0.0.1",**kwargs):
        """
        :param element_list: A list of the element to save in the json file as main elements. 
        For exemple, it can be a list of dictionnary like this [{'name': 'Worry, Fear & Anxiety', 'url': 'https://www.monergism.com/topics/worry-fear-anxiety'},
         {'name': 'Youth and Children', 'url': 'https://www.monergism.com/topics/youth-and-children'}]
        :param version: The version of the json data structure used to store the informations scrapped 
        """

        #print(element_list,"\n\n\n")
        #print(url)
    
        #print(self.url_informations[url]['html_filepath'],self.url_informations[url]['is_html_file_locally_saved'])
        self.url_informations[url]["json_file_content"] = {
            **{
            "version":version,
            "url":url,
            "local_json_filepath":self.url_informations[url]['json_filepath'],
            "local_html_filepath":self.url_informations[url]['html_filepath'] if self.url_informations[url]['is_html_file_locally_saved'] else "",
            "request_datetime":self.url_informations[url]["request_datetime"]
            },
            **_my_tools.get_important_information_from_request_response(self.url_informations[url]["request"]),
            "data":element_list
        }
        

    async def write_html_page_content(self,intermediate_folders = None,**kwargs):
        """
        Write the content of the html files 
        """

        for url in self.url_informations: 
                           
            html_text = self.url_informations[url]["html_text"]
            
            if html_text:
                await _my_tools.async_write_file(self.url_informations[url]["html_filepath"],
                                    html_text)
                self.url_informations[url]['is_html_file_locally_saved'] = True
                #print(url,"write html")



    async def write_json_data(self,**kwargs):
        """
        Write the json files 
        """
        
        #print(*[i.get("json_file_content") for i in self.url_informations.values()],sep="\n\n\n")

        for url in self.url_informations:
            
            
            
            #print("---ELVIS---",url)
            #print(self.url_informations[url]["json_filepath"])
            #print(self.url_informations[url]["json_file_content"])
            await _my_tools.async_write_json(self.url_informations[url]["json_filepath"],
                                 self.url_informations[url]["json_file_content"])
            self.url_informations[url]['is_json_file_locally_saved'] = True




    async def scrap_and_write(self,save_html_file= True,**kwargs):
        """
        Connect to the url specified, scrap the right data, save the html content in a file and write the result in an json file 
        
        :param save_html_file: If true, the text of the request is saved as html. 

        """
    

    def get_root_folder(self):
        return self.root_folder

    def set_root_folder(self, value):
        self.root_folder= value

    def get_url_list(self):
        return self.url_list

    def set_url_list(self, value):
        self.url_list = value




class ParallelHttpConnexionWithLogManagement(ParallelConnexionWithLogManagement):
    def __init__(self, log_filepath, input_data, overwrite_log=False, input_root_folder=""):
        super().__init__(log_filepath, input_data, overwrite_log, input_root_folder)
    