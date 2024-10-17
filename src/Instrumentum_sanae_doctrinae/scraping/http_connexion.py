import datetime
import os 
import urllib

import requests
from bs4 import BeautifulSoup

from ..scraping import my_constants
from ..scraping import _my_tools


class ScrapDataFromURL():
    """
    This class will be used to scrap the speakers, topics, series etc of the web site.
    This class is abstract and meant to be inherited of.  
        
    """
    def __init__(self,metadata_root_folder,log_root_folder,url_list,browse_by_type,intermdiate_folders) -> None:
        """
        :param metadata_root_folder: The folder where the metadata will be stored
        :param log_root_folder: The folder where the log of the download and scraping process will be stored
        :param url_list: The list of  url of the page where the list of the authors, topics, etc
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


        # It contains the json filepath, html filepat, etc of each url  
        self.url_informations = {i:{"json_filepath":None,"html_filepath":None,
                                    "request":None,"bs4_object":None,
                                    "is_html_file_locally_saved":False,
                                    "is_json_file_locally_saved":False,
                                    "json_file_content":None} for i in url_list} #: A dict for each url 


        intermdiate_folders = [_my_tools.replace_forbiden_char_in_text(i) for i in intermdiate_folders]
    
        for i in range(len(url_list)):
            self.url_informations[url_list[i]]['json_filepath'] =  os.path.join(self.metadata_root_folder,
                                                                                my_constants.ELABORATED_DATA_FOLDER,
                                                                                *intermdiate_folders,
                                                                                my_constants.get_default_json_filename(i))
            
            self.url_informations[url_list[i]]['html_filepath']  = os.path.join(self.metadata_root_folder,
                                                                                my_constants.RAW_DATA_FOLDER,
                                                                                *intermdiate_folders,
                                                                                my_constants.get_default_html_filename(i))
    
        self.url_list = url_list #: A list of all the urls of the web pages accross which the list of the speakers, topic, etc are spreaded


        

    def connect_to_url(self):
        """
        Connect to an html page whose url has been given 
        """

        for url in self.url_list:
            response = requests.get(url=url,timeout=my_constants.HTTP_REQUEST_TIMEOUT)
            self.url_informations[url]["request"] = response
            self.url_informations[url]["request_datetime"] = _my_tools.datetimeToGoogleFormat(datetime.datetime.now()),
            # Create a bs4 object with the html text of the last request 
            self.url_informations[url]["bs4_object"] = BeautifulSoup(response.text,features="html.parser") 

        #print(self.url_informations)

    def next_page(self):
        """
        This method is meant to return the next page if there is an url to a next page. 
        For example this page of CH Spurgeon from  monergism ( https://www.monergism.com/search?f[0]=author:34468)
        has next page while this page from sermon index does not have one (https://www.monergism.com/search?f[0]=author:41188)
        """



    def scrap_url_pages(self):

        """
        Scrap the web page 
        """
        self.connect_to_url()
        
    


    def anchor_object_list_to_dict_list(self,anchor_object_list,url,version = "0.0.1"):
        """
        :param anchor_object_list: The list of a the bs4 HTML anchor objects
        :param url: The url of the web page where the  anchor elements are taken of 
        :param version: The version of the data structure of the dict who contains the information taken 
        from the anchor object   
        """
        result = []
        for anchor_object in anchor_object_list:
            url_list = []
            name_list = []

            for anchor_ob in anchor_object:
                url_list.append(urllib.parse.urljoin(url,anchor_ob.get("href")))
                name_list.append(anchor_ob.get_text().strip())

            # Ensure that all the string in name list are the same 
            # All the anchor objects must have the same text
            # The href parameters can be different 
            if len(name_list) > 1:
                first_name = name_list[0]
                for i in name_list[1:]:
                    if i != first_name:
                        raise ValueError(f"The string in name list {name_list} must be the same not different")

            result.append({
                "version":version,
                "name" : name_list[0],
                "url_list" :url_list 
            })

        return result
    
    def prepare_json_data_for_saving(self,element_list,version = "0.0.1"):
        """
        :param element_list: A list of the element to save in the json file as main elements. 
        For exemple, it can be a list of dictionnary like this [{'name': 'Worry, Fear & Anxiety', 'url': 'https://www.monergism.com/topics/worry-fear-anxiety'},
         {'name': 'Youth and Children', 'url': 'https://www.monergism.com/topics/youth-and-children'}]
        :param version: The version of the json data structure used to store the informations scrapped 
        """


        for url in self.url_informations:
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
        

    def write_html_page_content(self):
        """
        Write the content of the html files 
        """

        for url in self.url_informations:
            _my_tools.write_file(self.url_informations[url]["html_filepath"],
                                 self.url_informations[url]["request"].text)
            self.url_informations[url]['is_html_file_locally_saved'] = True
            #print(url,self.url_informations[url]['is_html_file_locally_saved'])



    def write_json_data(self):
        """
        Write the json files 
        """
        for url in self.url_informations:
            print(self.url_informations[url]["json_filepath"])
            _my_tools.write_json(self.url_informations[url]["json_filepath"],
                                 self.url_informations[url]["json_file_content"])
            self.url_informations[url]['is_json_file_locally_saved'] = True




    def scrap_and_write(self,save_html_file= True):
        """
        Connect to the url specified, scrap the right data, save the html content in a file and write the result in an json file 
        
        :param save_html_file: If true, the text of the request is saved as html. 

        """


        self.connect_to_url()
    

    


    def get_root_folder(self):
        return self.root_folder

    def set_root_folder(self, value):
        self.root_folder= value

    def get_url_list(self):
        return self.url_list

    def set_url_list(self, value):
        self.url_list = value





class ParallelHttpConnexionWithLogManagement():
    def __init__(self,log_filepath,element_list,overwrite_log = False,update_log = True):
        """
        :param log_filepath: The path of the log file used to store and manage the downloaded, undownloaded, not found etc 
        :element_list: The list of the element to download 
        """
        self.log_filepath = log_filepath
        self.element_dict = {}

        self.meta_informations = {}
        self.meta_informations["input_files"] = list(element_list.keys())

        for file_path in element_list:
            file_content  =  element_list[file_path]
            for element in file_content.get("data"):
                self.element_dict[element.get("name")] = {**element,
                                                         **{"download_log":{
                                                             "input_file_index":self.meta_informations["input_files"].index(file_path)}}}

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


    def create_default_log_file_content(self):

        return {
                "meta_info":self.meta_informations,
                "to_download":self.element_dict,
                "downloaded":{},
                "not_found_404":{}
                }


    def update_downloaded_and_to_download(self):
        """
        Update the downloaded and to_download in the log file  
        """
    

    def is_element_data_downloaded(self):
        """
        This method must be implemented by the child class to  check if the element data was downloaded 
        """


    def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """


    def download(self,download_batch):
        """
        Download the content of the input files concurrently 
        by a batch of size :data:`download_batch` 
        """
        

