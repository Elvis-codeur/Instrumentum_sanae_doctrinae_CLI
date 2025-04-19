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

See this file :ref:`Instrumentum_sanae_doctrinae.web_scraping_documentation` for more information about the scraping and download procedure 

"""


import os 
import pathlib
import asyncio
import json 

from ..web_scraping import http_connexion
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools
from ..my_tools import my_constants





class GetAnyBrowseByListFromManyPages(http_connexion.ScrapDataFromURL):
    def __init__(self, metadata_root_folder, log_root_folder, url_list, browse_by_type, intermdiate_folders=None) -> None:
        
        if intermdiate_folders:
            intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER]\
                                     + intermdiate_folders
        else:
            intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER]
        
        super().__init__(metadata_root_folder, log_root_folder, url_list, browse_by_type, intermdiate_folders)

    
    def anchor_list_to_dict_list(self,anchor_object_list):
        result = []
        for anchor_object in anchor_object_list:
            link_text = _my_tools.replace_forbiden_char_in_text(
                        _my_tools.remove_consecutive_spaces(anchor_object.get_text()))
            result.append(
                {
                    "name": link_text,
                    "url_list":[anchor_object]
                }
            )
        return result 

    async def scrap_page_useful_links(self,**kwargs):
        """
        This method return the useful links of the page. 

        For example for the page of the topics of sermonindex https://www.sermonindex.net/modules/mydownloads/scr_index.php?act=topicsList
        The useful link are the <a> element
        of topics as <a href="scr_index.php?act=topicSermons&amp;topic=1%20Corinthians&amp;page=0">1 Corinthians</a>

        :param parent_name_for_selection: if element.parent.name == parent_name_for_selection,
          element is added to the list returned


        """
        

        result = []

        #print(kwargs.keys(),"get_useful_link_method")

        for url in self.url_informations:
            # Get the links (<a> </a>) which leads to the authors main page. 
            bs4_object = self.url_informations[url]['bs4_object']
            
            links = kwargs.get("get_useful_link_method")(bs4_object)
           
            links = self.anchor_list_to_dict_list(links)

            result.append((url,links))

        return result


    def page_useful_links_validation_method(self,anchor_list,parent_name_for_selection):
        """"
        if element.parent.name == parent_name_for_selection, element is added to the list returned 
        
        """

        result = [] 

        for  anchor_object in anchor_list:
            if anchor_object.parent.name == parent_name_for_selection:
                result.append(anchor_object)
        
        return result
        
    async def scrap_and_write(self,save_html_file= True,**kwargs):
        """
        Connect to the url specified, scrap the right data, save the html content in a file and write the result in an json file 
        
        :param save_html_file: If true, the text of the request is saved as html. 

        """


        await self.connect_to_all_url()

        if save_html_file:
            # Write the content of the html file get from the url
            await self.write_html_page_content()


        # A list of dictionnaries containing the information of the HTML anchor element scrapped 
        
        useful_links = await self.scrap_page_useful_links(**kwargs)
        
        for url,anchor_as_dict_list in useful_links:
            #print(url,anchor_as_dict_list)
            anchor_as_dict_list = self.anchor_object_list_to_dict_list(anchor_as_dict_list,url)
            self.prepare_json_data_for_saving(
                                            element_list=anchor_as_dict_list,
                                            url=url)


        # Write the json file of the data scrapped from the html file 
        await self.write_json_data()
        
        if self.main_request_session:
            await self.main_request_session.close()




class ScrapAuthorTopicScripturePage(http_connexion.ScrapDataFromURL):
    def __init__(self,name, metadata_root_folder, log_root_folder, url_list, browse_by_type,information_type_root_folder, intermdiate_folders=None) -> None:
        """
        :param name: The name of the author,topic, and more 
        """
        self.name = name 
        self.information_type_root_folder = information_type_root_folder
        intermdiate_folders = self.prepare_intermdiate_folders(intermdiate_folders,browse_by_type,name,information_type_root_folder)
        
        super().__init__(metadata_root_folder, log_root_folder, url_list, browse_by_type, intermdiate_folders)
    

    def prepare_intermdiate_folders(self,intermdiate_folders,browse_by_type,name,information_type_root_folder):
        if intermdiate_folders:
            intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,]\
                                 + intermdiate_folders +[name,information_type_root_folder] 
            return intermdiate_folders
        else:
            intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER
                                   ,name,information_type_root_folder]
            return intermdiate_folders
        


    async def is_data_downloaded(self):

        for url in self.url_informations:
            file_path = self.url_informations[url].get("json_filepath")
            #print(file_path)
            if not os.path.exists(file_path):
                return False
            
            
            file_content = await _my_tools.async_read_file(file_path)
            

            if not file_content:
                return False
            
            file_content = json.loads(file_content)
            
            # Check mandatory information in the json file 

            if not file_content.get("url"):
                return False
            

            if not file_content.get("data").get("name"):
                return False
            
        return True

        

    async def scrap_and_write(self,save_html_file= True,intermediate_folders = None):
        """
        Connect to the url specified, scrap the right data, save the html content in a file and write the result in an json file 
        
        :param save_html_file: If true, the text of the request is saved as html. 

        """
        #print(self.__dict__)

        if intermediate_folders:
            for url in self.url_informations:
                json_filepath = pathlib.Path(self.url_informations[url]["json_filepath"])
                html_filepath = pathlib.Path(self.url_informations[url]["html_filepath"])
                
                # Insert the intermediate folders 
                json_filepath = json_filepath.parent / "/".join(intermediate_folders) / json_filepath.name
                html_filepath = html_filepath.parent / "/".join(intermediate_folders) / html_filepath.name

                self.url_informations[url]["json_filepath"] = json_filepath
                self.url_informations[url]["html_filepath"] = html_filepath


        await self.connect_to_all_url()
        
        #print(self.url_informations)
        
        
        # The data scrapped from each url 
        # This step can contain http connections 
        url_datascraped_list = await self.scrap_url_pages()
        #print(url_datascraped_list)
        if url_datascraped_list:
            
            #raise RuntimeError("The method scrap_url_pages() is not defined by the class or return None")
        

            if save_html_file:
                # Write the content of the html file get from the url
                await self.write_html_page_content()  


            #print(url_datascraped_list,sep="\n\n\n")      

            for url in url_datascraped_list:
                self.prepare_json_data_for_saving(element_list=url_datascraped_list[url],
                                                url=url)

            # Write the json file of the data scrapped from the html file 
            await self.write_json_data()
            
            await self.main_request_session.close()

