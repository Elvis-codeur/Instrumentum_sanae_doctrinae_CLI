import json
import os 
import pathlib
import urllib
import urllib.parse

from bs4 import BeautifulSoup

from Instrumentum_sanae_doctrinae.web_scraping import http_connexion, my_constants
from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_scrap_metadata
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools



def scrap_page_works(bs4_object):
    main_links = []
    
    for div_element in bs4_object.find_all("div"):
        div_class = div_element.get("class")
        
        if div_class:
            div_class = " ".join(div_class).strip()
            if div_class.startswith("views-row views-row-"):
            
                span_object = div_element.find("span")
                
                if span_object:
                
                    span_object_class = span_object.get("class")
                    
                    if len(span_object_class) >= 2:
                        #print(span_object)
                        
                        anchor_object = span_object.find('a')
                        author_em = div_element.find("em")
                    
                        link_type = span_object_class[1].strip()
                        link_href = anchor_object.get("href")
                        link_text = anchor_object.get_text()
                        
                        main_links.append(
                            {
                                "link_type":link_type,
                                "url":link_href,
                                "link_text":link_text,
                                "author":author_em.get_text().split("by")[-1].strip()
                            }
                        ) 
    return main_links   
        
    



class MN_ScriptureSubtopicWork(mn_scrap_metadata.MonergismScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder, url_list, browse_by_type,intermdiate_folders = None):

        super().__init__(name, root_folder, url_list, browse_by_type,
                          information_type_root_folder = my_constants.WORK_INFORMATION_ROOT_FOLDER,
                          intermdiate_folders = intermdiate_folders)
    
    async def scrap_url_pages(self):
        """
        Scrap the main links of the page. See this file (documentation/documentation.odt) for more info 
        """

        final_result = {}
        
    

        for main_url in self.url_informations:
            
            # Take the div containing the links of the author 
            
            bs4_object = self.url_informations[main_url].get("bs4_object")
            
            final_result[main_url] = {"main_links":scrap_page_works(bs4_object)}

        return final_result
    


class MN_ScriptureWork(mn_scrap_metadata.MonergismScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder, url_list, browse_by_type,intermdiate_folders = None):

        super().__init__(name, root_folder, url_list, browse_by_type,
                          information_type_root_folder = my_constants.WORK_INFORMATION_ROOT_FOLDER,
                          intermdiate_folders = intermdiate_folders)
        

    
    
    async def scrap_url_pages(self):
        """
        Scrap the main links of the page. See this file (documentation/documentation.odt) for more info 
        """

        final_result = {}    
        

        for main_url in self.url_informations:
            
            # Take the div containing the links of the author 
            
            bs4_object = self.url_informations[main_url].get("bs4_object")
            
            
            sub_url_topics_list = bs4_object.findAll("a")
            
            sub_url_topics_list = [anchor_object for anchor_object in sub_url_topics_list if anchor_object.get("href")]
            
            sub_url_topics_list = [
                i for i in sub_url_topics_list  
                if "/taxonomy/term/" in i.get("href") and i.get("href")[-1].isdigit()
            ]

            sub_url_topics_list = [
                {
                    "url": urllib.parse.urljoin(main_url,anchor_object.get("href")),
                    "link_text":anchor_object.get_text().strip()
                    
                } for anchor_object in sub_url_topics_list 
                               ]
            
            
            
            
            for url_info in sub_url_topics_list:
                #print(url_info,"\n\n\n")
                #print(self.intermdiate_folders)
                ob = MN_ScriptureSubtopicWork(name = self.name,root_folder=self.root_folder,
                                              url_list=[{"url":url_info.get("url")}],browse_by_type=self.browse_by_type,
                                              intermdiate_folders= 
                                              [self.intermdiate_folders[-1],"subtopics",url_info.get("link_text")])
                
                await ob.scrap_and_write(save_html_file=True)
                    
               
                
                
            
            
            final_result[main_url] = {
                        "main_links":scrap_page_works(bs4_object)
                    }

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




class MN_ScriptureWork_All(http_connexion.ParallelHttpConnexionWithLogManagement):
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
            filename = file.as_posix()
            if my_constants.MAIN_INFORMATION_ROOT_FOLDER in filename:
                input_json_files.append(file)

        #print(input_json_files)
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
        
        
        if not element.get("name") in self.element_dict.keys():
            self.element_dict[element.get("name")]  = []

                
        self.element_dict[element.get("name")].append({
            **{
                "data":{
                    "name":element.get("name"),
                    "pages":element.get("pages")
                }
            },
            **{
                "meta_data": {
                    "input_file_index":self.meta_informations["input_files_information"]\
                                                        ["input_files"].index(kwargs.get("file_path")),                
            },
            
            **{"download_log":{
                "intermediate_folders":kwargs.get("intermediate_folders")[2:]}
                }}}
        )
        
        

    async def download_element_data(self,element_list):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)

        #print(element.get("data"))
        
        #print(element)
        
        #print(element.get("data").get("name"),element.get("download_log").get("intermediate_folders"))
        
        for element in element_list:
            ob = MN_ScriptureWork(
                name = element.get("data").get("name"),
                root_folder = self.root_folder,
                browse_by_type = self.browse_by_type,
                url_list = [{"url":i} for i in element.get("data").get("pages")],
                intermdiate_folders = element.get("download_log").get("intermediate_folders")
            )

            await ob.scrap_and_write()

    async def is_element_data_downloaded(self,element_list):
        
        #print(element)
        #print(element.get("data").get("name"),element.get("download_log").get("intermediate_folders"))
        
        for element in element_list:
            ob = MN_ScriptureWork(
                name = element.get("data").get("name"),
                root_folder = self.root_folder,
                browse_by_type = self.browse_by_type,
                url_list = [{"url":i} for i in element.get("data").get("pages")],
                intermdiate_folders = element.get("download_log").get("intermediate_folders")
            )
            if not ob.is_data_downloaded():
                return False 
        
        return True 
        

