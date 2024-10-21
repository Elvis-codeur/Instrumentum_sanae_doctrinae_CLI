"""
Presentation of the supported websites
--------------------------------------

This module is meant to scrap the metadata from the web sites in the project. Actually 
The website supported are https://www.sermonindex.net/ and https://www.monergism.com/

Definition of of what a metadata is 
-----------------------------------

I define as metadata everything required to download the works of a speaker(author), 
topic, podcast, scripture, series, etc from a given web site. The metadata include
the list of all the authors,topics, series, etc  of a website. The metadata for me include
the html files where the information is scrapped from and the json file where the scrapped iformation 
is stored. 

See this file :ref:`Instrumentum_sanae_doctrinae.scraping` for more information about the scraping and download procedure 
"""


import os 
import pathlib

from . import http_connexion
from . import _my_tools
from . import my_constants





class GetAnyBrowseByListFromManyPages(http_connexion.ScrapDataFromURL):
    def __init__(self, metadata_root_folder, log_root_folder, url_list, browse_by_type, intermdiate_folders=None) -> None:
        
        if intermdiate_folders:
            intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER]\
                                     + intermdiate_folders
        else:
            intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER]
        
        super().__init__(metadata_root_folder, log_root_folder, url_list, browse_by_type, intermdiate_folders)

       
    def scrap_page_useful_links(self):

        """
        html_text : The text of the html page retrieved from the url. This method does the main work. 
        It get the list of the authors, topics or everthing else desired by the developper and and return 
        return it as a list. 

        Useful links are the links of the authors, topics, etc 

        For example here is the page of the authors of monergism https://www.monergism.com/authors. 
        Here is an example useful link **<a href="/search?f[0]=author:39115">H.B. Charles Jr.</a>**

        
        """
        self.connect_to_url()

    
    def scrap_and_write(self,save_html_file= True):
        """
        Connect to the url specified, scrap the right data, save the html content in a file and write the result in an json file 
        
        :param save_html_file: If true, the text of the request is saved as html. 

        """


        self.connect_to_url()

        if save_html_file:
            # Write the content of the html file get from the url
            self.write_html_page_content()


        # A list of dictionnaries containing the information of the HTML anchor element scrapped 
        
        for url,anchor_as_dict_list in self.scrap_page_useful_links():
            #print(url,anchor_as_dict_list)
            anchor_as_dict_list = self.anchor_object_list_to_dict_list(anchor_as_dict_list,url)
            self.prepare_json_data_for_saving(anchor_as_dict_list)


        # Write the json file of the data scrapped from the html file 
        self.write_json_data()




class ScrapAuthorTopicScripturePage(http_connexion.ScrapDataFromURL):
    def __init__(self,name, metadata_root_folder, log_root_folder, url_list, browse_by_type, intermdiate_folders=None) -> None:
        """
        :param name: The name of the author,topic, and more 
        """
        self.name = name 


        if intermdiate_folders:
            intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,]\
                                 + intermdiate_folders +[name,"main_information"] 
        else:
            intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER
                                   ,name,"main_information"]
    
        super().__init__(metadata_root_folder, log_root_folder, url_list, browse_by_type, intermdiate_folders)
    


    def is_data_downloaded(self):

        for url in self.url_informations:
            file_path = self.url_informations[url].get("json_filepath")
            if not os.path.exists(file_path):
                return False
            
            
            file_content = _my_tools.read_json(file_path)

            if not file_content:
                return False
            
            # Check mandatory information in the json file 

            if not file_content.get("url"):
                return False
            
            if not file_content.get("data").get("name"):
                return False
            
        return True

        

    def scrap_and_write(self,save_html_file= True,intermediate_folders = None):
        """
        Connect to the url specified, scrap the right data, save the html content in a file and write the result in an json file 
        
        :param save_html_file: If true, the text of the request is saved as html. 

        """
        print(self.__dict__)

        if intermediate_folders:
            for url in self.url_informations:
                json_filepath = pathlib.Path(self.url_informations[url]["json_filepath"])
                html_filepath = pathlib.Path(self.url_informations[url]["html_filepath"])
                
                # Insert the intermediate folders 
                json_filepath = json_filepath.parent / "/".join(intermediate_folders) / json_filepath.name
                html_filepath = html_filepath.parent / "/".join(intermediate_folders) / html_filepath.name

                self.url_informations[url]["json_filepath"] = json_filepath
                self.url_informations[url]["html_filepath"] = html_filepath


        # The data scrapped from each url 
        url_datascraped_list = self.scrap_url_pages()

        if save_html_file:
            # Write the content of the html file get from the url
            self.write_html_page_content()        

        for data in url_datascraped_list:
            self.prepare_json_data_for_saving(data)

        # Write the json file of the data scrapped from the html file 
        self.write_json_data()







      


class ScrapWebSiteAllAuthorTopicScriptures(http_connexion.ParallelHttpConnexionWithLogManagement):

    def __init__(self, log_filepath, input_root_folder, overwrite_log=False, update_log=True):

        self.input_json_root_folder = input_root_folder


        # Get all the files of the in the folder _list of the root folder in 
        # which we are 
        # The files in these folders are the list of the authors, topics, scriptures, etc
        
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        input_json_files = []
        
        pattern = f"*{my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER}"

        input_root_folder = pathlib.Path(input_root_folder)

        matching_subfolders = [i for i  in input_root_folder.rglob(pattern) if i.is_dir()]

        #print(input_root_folder)
        


        for folder in matching_subfolders:
            for files in [i for i in pathlib.Path(folder).rglob("*.json") if i.is_file()]:
                input_json_files.append(files)

        self.input_json_content_dict = {}

        input_json_files_content = {}

        
        for file in input_json_files:
            input_json_files_content[str(file)] = _my_tools.read_json(file)
       
        
        
        super().__init__(log_filepath,input_json_files_content,overwrite_log,update_log,input_root_folder)

    def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """


    def download(self,download_batch):
        """
        Download the content of the input files concurrently 
        by a batch of size :data:`download_batch` 
        """