




    

import os
import pathlib
import urllib

from Instrumentum_sanae_doctrinae.web_scraping import http_connexion, my_constants
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_metadata import SermonIndexScrapAuthorTopicScripturePage


class SermonIndexScrapGeneralInformation(SermonIndexScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder,browse_by_type, url_list,material_root_folder,intermdiate_folders=None):
        
        super().__init__(name, root_folder, url_list,browse_by_type,
                         information_type_root_folder = my_constants.MAIN_INFORMATION_ROOT_FOLDER,
                         material_root_folder = material_root_folder,
                         intermdiate_folders = intermdiate_folders)
        
        
    async def scrap_url_pages(self):
        """
        Scrap the main information of the web page. Here the description, the 
        urls of the author, topic, scripture work 
        """        

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
                    
                author_description_text = ""
                
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
class SermonIndexScrapSpeakerMainInformation_ALL(http_connexion.ParallelHttpConnexionWithLogManagement):
    def __init__(self,root_folder,material_root_folder,browse_by_type, overwrite_log=False, update_log=True,intermdiate_folders=None):
        
        root_folder = _my_tools.process_path_according_to_cwd(root_folder)

        log_filepath = os.path.join(root_folder,my_constants.LOGS_ROOT_FOLDER,
                                       my_constants.SERMONINDEX_NAME,
                                       material_root_folder,
                                       my_constants.ELABORATED_DATA_FOLDER,
                                       browse_by_type,
                                       my_constants.GENERAL_INFORMATION_NAME,
                                       my_constants.get_default_json_filename(0))
        
        input_root_folder = os.path.join(root_folder,
                                         my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.SERMONINDEX_NAME,
                                         material_root_folder,
                                         my_constants.ELABORATED_DATA_FOLDER,
                                         browse_by_type)

        input_json_files_content = {}
        
        for file in self.prepare_input_json_file(input_root_folder):
            input_json_files_content[file.as_posix()] = _my_tools.read_json(file)
        
        super().__init__(log_filepath = log_filepath,
                         input_data = input_json_files_content,
                         overwrite_log = overwrite_log,
                         input_root_folder=input_root_folder)
        
        self.material_root_folder = material_root_folder
        self.browse_by_type = browse_by_type
        self.root_folder = root_folder
    

    def prepare_input_json_file(self,input_root_folder):
        """
        :param input_root_folder: The folder from which to search for the json files to use as input
        """
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        
        folder =  os.path.join(input_root_folder,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER)
        
        input_json_files = []
        input_json_files = [i for i in pathlib.Path(folder).rglob("*.json") if i.is_file()]
        
        #print(folder,input_json_files)
        
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

        element_list = kwargs.get("file_content").get("data")
        
        # The path of the file from which the data is taken from 
        element_list_filepath = kwargs.get("file_path")
        
        for element in element_list:

            self.element_dict[element.get("name")] = {
                **element,
                **{"download_log":{
                    "input_file_index":self.meta_informations["input_files_information"]\
                                                            ["input_files"].index(kwargs.get("file_path")),
                    "intermediate_folders":kwargs.get("intermediate_folders")} 
                    }
                    }
    
    
    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(element.get("name"))
        ob = SermonIndexScrapGeneralInformation(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type = self.browse_by_type,
            url_list = element.get("url_list"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )

        await ob.scrap_and_write()

    def is_element_data_downloaded(self,element):
        ob = SermonIndexScrapGeneralInformation(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type =self.browse_by_type,
            url_list = element.get("url_list"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )
        return ob.is_data_downloaded()
        
