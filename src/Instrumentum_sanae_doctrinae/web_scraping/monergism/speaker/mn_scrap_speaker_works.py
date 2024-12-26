import json
import os 
import pathlib
import re

from Instrumentum_sanae_doctrinae.web_scraping import _my_tools, http_connexion, my_constants
from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_scrap_metadata



class MN_ScrapAuthorWork(mn_scrap_metadata.MonergismScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder, url_list, browse_by_type,intermdiate_folders = None):

        super().__init__(name, root_folder, url_list, browse_by_type,
                          information_type_root_folder = my_constants.WORK_INFORMATION_ROOT_FOLDER,
                          intermdiate_folders = intermdiate_folders)
        

    
    
    async def scrap_url_pages(self):
        """
        Scrap the main links of the page. See this file (documentation/documentation.odt) for more info 
        """

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
    
    def is_data_downloaded(self):

        for url in self.url_informations:
            file_path = self.url_informations[url].get("json_filepath")
            
            if not os.path.exists(file_path):
                return False
            
            
            
            file_content = _my_tools.read_file(file_path)
            
            if not file_content:
                return False 
            
            try:
                file_content = json.loads(file_content)
            except:
                return False
            
            
            if not file_content:
                return False
            
            # Check mandatory information in the json file 
            if not file_content.get("url"):
                return False
            

            if not file_content.get("data"):
                return False
            
        return True




class MN_ScrapAuthorWork_All(http_connexion.ParallelHttpConnexionWithLogManagement):
    def __init__(self,root_folder,browse_by_type, overwrite_log=False, update_log=True,intermdiate_folders=None):

        root_folder = _my_tools.process_path_according_to_cwd(root_folder)

        log_filepath = os.path.join(root_folder,
                                    my_constants.LOGS_ROOT_FOLDER,
                                    my_constants.MONERGISM_NAME,
                                    my_constants.ELABORATED_DATA_FOLDER,
                                    browse_by_type,
                                    my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,
                                    my_constants.get_default_json_filename(0))
        
        input_root_folder = os.path.join(root_folder,
                                         my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.MONERGISM_NAME,
                                         my_constants.ELABORATED_DATA_FOLDER,
                                         browse_by_type
                                         )
        

        #print(input_root_folder)
        
        input_files = self.get_input_json_files(input_root_folder)
        
        input_data = {}
        
        # Prepare the json files as input data 
        for filepath in input_files:
            file_content = _my_tools.read_json(filepath)
            input_data[str(filepath)] = file_content
        
        
        super().__init__(log_filepath = log_filepath,
                         input_root_folder= input_root_folder,
                         input_data=input_data,
                         overwrite_log = overwrite_log,
                         update_log = update_log)
        
        self.browse_by_type = browse_by_type
        self.root_folder = root_folder


    def get_input_json_files(self,input_root_folder):
        """
        :param input_root_folder: The folders from wich the json files will be searched out 
        """
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        input_json_files = []

        # The folder where the works of the author are 
        folder_path = os.path.join(input_root_folder,
                                my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER)
        
        
        # List to store paths to all JSON files
        json_files = [i for i in pathlib.Path(folder_path).rglob("*.json") if i.is_file()]

                
        for file in json_files:
            #print(file)
            if str(file.parent).endswith(my_constants.MAIN_INFORMATION_ROOT_FOLDER):
                input_json_files.append(file)

        

        return input_json_files
    
    def prepare_input_data(self,**kwargs):
        """
        This method take a json file content and create input data for download 
        that are put into the dict self.element_dict

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
        

    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)

        #print(element.get("data"))
        print(element.get("data").get("name"))
        
        ob = MN_ScrapAuthorWork(
            name = element.get("data").get("name"),
            root_folder = self.root_folder,
            browse_by_type = self.browse_by_type,
            url_list = element.get("data").get("pages"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders")
        )

        await ob.scrap_and_write()

    def is_element_data_downloaded(self,element):
        ob = MN_ScrapAuthorWork(
            name = element.get("data").get("name"),
            root_folder = self.root_folder,
            browse_by_type = self.browse_by_type,
            url_list = element.get("data").get("pages"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders")
        )
        return ob.is_data_downloaded()
        

