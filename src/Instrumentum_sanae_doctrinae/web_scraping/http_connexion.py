import asyncio
from concurrent.futures import ThreadPoolExecutor
import io
import threading
import datetime
import os 
import urllib
import pathlib
import aiohttp
from tqdm import tqdm


import requests
from bs4 import BeautifulSoup


from ..web_scraping import my_constants
from . import my_errors
from ..web_scraping import _my_tools


class ScrapDataFromURL():
    """
    This class will be used to scrap the speakers, topics, series etc of the web site.
    This class is abstract and meant to be inherited of.  
        
    """
    
    def __init__(self,metadata_root_folder,log_root_folder,url_info_list,browse_by_type,intermdiate_folders) -> None:
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

        
        self.url_info_list = url_info_list
        
        self.browse_by_type = browse_by_type
        
        self.intermdiate_folders = intermdiate_folders
        

        # It contains the json filepath, html filepat, etc of each url  
        self.url_informations = {i.get("url"):{"json_filepath":None,"html_filepath":None,
                                    "request":None,"bs4_object":None,
                                    "is_html_file_locally_saved":False,
                                    "is_json_file_locally_saved":False,
                                    "json_file_content":None} for i in self.url_info_list} #: A dict for each url 

        
        
        
        self.prepare_url_informations()
        
    def prepare_url_informations(self):
    
        intermdiate_folders = [_my_tools.replace_forbiden_char_in_text(i) for i in self.intermdiate_folders]
    
        for indice,element in enumerate(self.url_info_list):
            print(element)
            self.url_informations[element.get("url")]['json_filepath'] =  os.path.join(self.metadata_root_folder,
                                                                                my_constants.ELABORATED_DATA_FOLDER,
                                                                                *intermdiate_folders,
                                                                                my_constants.get_default_json_filename(indice))
            
            self.url_informations[element.get("url")]['html_filepath']  = os.path.join(self.metadata_root_folder,
                                                                                my_constants.RAW_DATA_FOLDER,
                                                                                *intermdiate_folders,
                                                                                my_constants.get_default_html_filename(indice))
    

        
        self.main_request_session = None
        
    
        
    async def close(self):
        if self.main_request_session:
            await self.main_request_session.close()
            
            

    async def connect_to_all_url(self,**kwargs):
        """
        Connect to an html page whose url has been given 
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "close",
        }
        
        self.main_request_session = aiohttp.ClientSession()
    
        for url_dict in self.url_info_list:
            url = url_dict.get("url")
            #timeout = aiohttp.ClientTimeout(total=15)
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
            name_list = []
            
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





class ParallelHttpConnexionWithLogManagement():
    def __init__(self,log_filepath,input_data,overwrite_log = False,update_log = True,input_root_folder = ""):
        """
        :param log_filepath: The path of the log file used to store and manage the downloaded, undownloaded, not found etc 
        :param input_data: A dictionnary where the keys are the file path and the value the content of the file
        :param input_root_folder: The folder from which all the json files are searched from to be used as input files 
        """
        self.log_filepath = log_filepath
        self.element_dict = {}

        if not input_root_folder:
            raise ValueError("The value of variable input_root_folder must be given")


        self.input_root_folder = input_root_folder

        self.meta_informations = {}
        
        # The information of the json input files 
        self.meta_informations["input_files_information"] = {}

        self.meta_informations["input_files_information"]["input_files"] = list(input_data.keys())


        # Add download log the element each element 
        for file_path in input_data:
            
            file_path_from_root_folder = _my_tools.get_uncommon_part_of_two_path(
                                                    self.input_root_folder,file_path)[1]
            
            file_path_from_root_folder = pathlib.Path(file_path_from_root_folder).parent
            
            # The subfolder from the root folder where the scraped data must be stored
            #  (the information of the author, topic, scripture, etc)
            intermediate_folders = list(file_path_from_root_folder.parts[1:])

            file_content  =  input_data[file_path]

            #print(self.meta_informations)

            self.prepare_input_data(file_content = file_content,
                                    intermediate_folders = intermediate_folders,
                                    file_path = file_path)
            


        self.log_file_content = {}

        

        if overwrite_log:
            self.log_file_content = self.create_default_log_file_content()
            _my_tools.write_json(self.log_filepath,self.log_file_content)
        else:
            if not os.path.exists(self.log_filepath):
                _my_tools.write_json(self.log_filepath,self.create_default_log_file_content())
            else:
                
                self.log_file_content = self.create_default_log_file_content()

                 # A list of the url of of the link object which have been already downloaded 
                downloaded_link_url_list = [i for i in self.log_file_content.get("downloaded")] if self.log_file_content.get("downloaded") else []
                to_downlaod_link_url_list = [i for i in self.log_file_content.get("to_download")] if self.log_file_content.get("to_download") else []

                # We take "element_list" variable because it contains the link of the author, scripture or topic
                for url in self.element_dict:
                    if url not in downloaded_link_url_list: # If it is not already downloaded 
                        if url not in to_downlaod_link_url_list: # It is not in the link prepared to for download. 
                            self.log_file_content["to_download"][url] = self.element_dict[url]
                        else: # If the element is already in the "to_download" list, there is no need to add it 
                            pass 
                    else: # If the link is already downlaed. There is no need of modification of anything 
                        pass 
    

    def update_downloaded_and_to_download(self):
        """
        This function verify if the data of the links in "downloaded" list are truly downloaded. 
        If not this link is put back in the "to_download" list. 
        If a link data is downloaded but is in to_download list, it is put in the downloaded list
        """

        # Remove from link_list the link whoes data are already downloaded 
        downloaded = {}
        to_download = {}

        element_dict = {**self.log_file_content["to_download"],
                     ** self.log_file_content["downloaded"]}

        for key in element_dict:
            if self.is_element_data_downloaded(element_dict[key]):
                #print(key,True)
                downloaded[key] = element_dict[key]
            else:
                #print(key,False)
                to_download[key] = element_dict[key]
        
        
        self.log_file_content["to_download"] = to_download
        self.log_file_content["downloaded"] = downloaded


    def prepare_input_data(self,**kwargs):
        """
        This method take a json file content and create input data for download 
        that are put int dict self.element_dict

        """



    def write_log_file(self):
        return _my_tools.write_json(self.log_filepath,self.log_file_content)
        
    def is_element_data_downloaded(self,element):
        """
        Check if the element data was downloaded 
        """
            

    def create_default_log_file_content(self):

        return {
                "meta_info":self.meta_informations,
                "to_download":self.element_dict,
                "downloaded":{},
                "not_found_404":{}
                }

    def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """


    async def download(self,download_batch_size):
        """
        Download the content of the input files concurrently 
        by a batch of size :data:`download_batch` 
        """
        result = []

        # Update before the begining of downloads
        self.update_downloaded_and_to_download() 
         
        element_to_download = list(self.log_file_content["to_download"].values())
        
       
        # Split it by size download_batch_size to download
        #  them in parralel 
        element_to_download_splitted = _my_tools.sample_list(element_to_download,
                                                      download_batch_size)

        
        # This is used to show a progress bar 
        for download_batch in element_to_download_splitted:
            tasks = [self.download_element_data(element) for element in download_batch]
            result = await asyncio.gather(*tasks)
            self.update_downloaded_and_to_download()
            break 
               
                
      
        


