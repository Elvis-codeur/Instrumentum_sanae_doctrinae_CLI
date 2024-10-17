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
        if intermdiate_folders:
            intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,
                                   name,"main_information"] + intermdiate_folders
        else:
            intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER
                                   ,name,"main_information"]
    
        super().__init__(metadata_root_folder, log_root_folder, url_list, browse_by_type, intermdiate_folders)
    


    def scrap_and_write(self,save_html_file= True):
        """
        Connect to the url specified, scrap the right data, save the html content in a file and write the result in an json file 
        
        :param save_html_file: If true, the text of the request is saved as html. 

        """


        # The data scrapped from each url 
        url_datascraped_list = self.scrap_url_pages()


        if save_html_file:
            # Write the content of the html file get from the url
            self.write_html_page_content()        

        for data in url_datascraped_list:
            self.prepare_json_data_for_saving(data)

        # Write the json file of the data scrapped from the html file 
        self.write_json_data()







      
class ParralelScrapingManyUrl(http_connexion.ParallelHttpConnexionWithLogManagement):
    def __init__(self, log_filepath, element_list, overwrite_log=False, update_log=True):
        super().__init__(log_filepath, element_list, overwrite_log, update_log)


    def update_downloaded_and_to_download(self):
        """
        This function verify if the data of the links in "downloaded" list are truly downloaded. 
        If not this link is put back in the "to_download" list. 
        If a link data is downloaded but is in to_download list, it is put in the downloaded list
        """

        # Remove from link_list the link whoes data are already downloaded 
        downloaded = []
        to_download = []

        for link in {**self.log_file_content["to_download"],
                     ** self.log_file_content["downloaded"]}:
            
            if self.is_element_data_downloaded(link):
                downloaded.append(link)
            else:
                to_download.append(link)
        
        
        self.log_file_content["to_download"] = to_download.copy()
        self.log_file_content["downloaded"] = downloaded.copy()
        
    def is_element_data_downloaded(self,link):
            link_local_file_path = link.get("output_filepath")

            # If the link has an output file path
            if not link_local_file_path:

                return False
            

            # If the file exists and is not deleted 
            if not os.path.exists(link_local_file_path):
                return False    
                
            # If there is a download log in the link object. There is no download log 
            # in link object when they are first get from the folder of the works of the author 
            # topic or scripture
            if link.get("download_log"):
                # If there is no error in download log 
                # The download log of a true download does not contain the key "error"
                if not link.get("download_log").get("error"):
                    return True
                else:
                    return False
            else:
                return False
               

class ScrapWebSiteAllAuthorTopicScriptures(ParralelScrapingManyUrl):

    def __init__(self, log_filepath, input_root_folder, overwrite_log=False, update_log=True):

        self.input_json_root_folder = input_root_folder


        # Get all the files of the in the folder _list of the root folder in 
        # which we are 
        # The files in these folders are the list of the authors, topics, scriptures, etc
        
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        input_json_files = []
        
        pattern = f"*{my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER}"

        path = pathlib.Path(input_root_folder)

        matching_subfolders = [i for i  in path.rglob(pattern) if i.is_dir()]

        #print(input_root_folder)

        for folder in matching_subfolders:
            for files in [i for i in pathlib.Path(folder).rglob("*.json") if i.is_file()]:
                input_json_files.append(files)

        self.input_json_content_dict = {}

        input_json_files_content = {}

        for file in input_json_files:
            input_json_files_content[str(file)] = _my_tools.read_json(file)
       
        #print(input_json_files)
        
        super().__init__(log_filepath,input_json_files_content,overwrite_log,update_log)


    def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """


    def download(self,download_batch):
        """
        Download the content of the input files concurrently 
        by a batch of size :data:`download_batch` 
        """