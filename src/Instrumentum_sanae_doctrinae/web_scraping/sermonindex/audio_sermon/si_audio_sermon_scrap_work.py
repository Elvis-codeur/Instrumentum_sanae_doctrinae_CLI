


# This class works for the audio sermons 

import json
import os
import pathlib

from bs4 import BeautifulSoup
import urllib
from Instrumentum_sanae_doctrinae.web_scraping import _my_tools, http_connexion, my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_metadata import SermonIndexScrapAuthorTopicScripturePage


class SermonIndexAudioSermonWork(SermonIndexScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder,browse_by_type, url_list,material_root_folder,intermdiate_folders=None):
        
        super().__init__(name, root_folder, url_list,browse_by_type,
                         information_type_root_folder = my_constants.WORK_INFORMATION_ROOT_FOLDER,
                         material_root_folder = material_root_folder,
                         intermdiate_folders = intermdiate_folders)
        
        

    async def scrap_url_pages(self):
        """
        Scrap the main information of the web page. Here the description, the 
        urls of the author, topic, scripture work 
        """
       

        final_result = {}

        for current_page_url in self.url_informations:
                
            soup = self.url_informations[current_page_url].get("bs4_object")

            

            main_links_element = soup.find("table",{"border":0,"cellspacing":0,
                                            "cellpadding":10,"width":"100%"})
            
            if main_links_element:
                main_links_element = main_links_element.find_all("tr")
            else:
                return []
            

            #print(*main_links_element[:2],sep="\n\n\n")

            author_name = ""


            result = []

            compteur = 0
            for element in main_links_element:
            
                a_element = element.find("a")
                
                compteur += 1

                # There is some element in the main_links_element which are not a comment element

                if a_element:


                    url = a_element.get("href")
                    link_text  = a_element.get_text()

                    element_content = element.contents[-1].findAll("tr")[1:]


                    if (len(element_content) > 1):

                        add_element_to_topic = False
                        add_element_to_scriptures = False

                        topic_list = []
                        scripture_list = []

                        #print("\n\n\n",element_content[1].contents[0].contents[1:],compteur)
                        #print("\n\n\n",element_content[1],"\n",element_content)

                    
                        for comp in element_content[1].contents[0].contents[1:]:
                            if "by" in comp.get_text():
                                author_name = comp.get_text().split(" ")
                                if len(author_name) > 1:

                                    author_name = " ".join(author_name[1:])

                            if  "Topic:" in comp.get_text():
                                add_element_to_topic = True

                            if "Scripture" in comp.get_text():
                                add_element_to_scriptures = True
                                add_element_to_topic = False

                            if comp.name == 'i' and add_element_to_topic:
                                topic_list.append(comp.get_text())

                            if comp.name == 'i' and add_element_to_scriptures:
                                scripture_list.append(comp.get_text())

                        
                        link_description = "".join(element_content[2].find("td").find_all(string = True,recursive = False))


                        download_number = element_content[3].get_text().split("\xa0")
                        if len(download_number) >= 1:
                            download_number = download_number[0]


                        element_comment_a = element_content[-1].find("a")

                        element_comment_url = urllib.parse.urljoin(url,element_comment_a.get("href"))
                        
                        comment_number = int(element_comment_a.get_text().split("(")[1][:-1])
                        
                        comments = []

                        if comment_number > 0:
                            #print(self.url_informations[current_page_url].keys())
                            comments = await self.get_element_comments(element_comment_url,
                                                                 link_text,
                                                                 os.path.dirname(
                                                                     self.url_informations[current_page_url].get("html_filepath")))


                        # Take the number of download

                        download_number_element = element.find("td",{"colspan":"2","class":"bg3","align":"right"}) 

                        download_number = download_number_element.get_text()

                        download_number = download_number.split("\xa0")
                        if len(download_number) > 1:
                            download_number = download_number[0]
                        else:
                            download_number = -1

                        result.append({
                            "url":url,
                            "author_name":author_name,
                            "downlaod_number":download_number,
                            "topics":topic_list,
                            "scriptures":scripture_list,
                            "link_text":link_text,
                            "link_description":link_description,
                            "comments_url":element_comment_url,
                            "comments":comments,
                            "comments_number": comment_number
                        })

            final_result[current_page_url] = result

        return final_result


    async def get_element_comments(self,comment_url,link_text,raw_filefolder):
        """
        :param comment_url: The url of the comment. Here is an example of comment's  
        url on a sermon of Ravenhill https://www.sermonindex.net/modules/mydownloads/singlefile.php?lid=14469&commentView=itemComments
        :param link_text: The text content of the anchor object of the url
        :param raw_filefolder: The folder where the html files of this author or 
        topic are saved  
        """
        #print(raw_filefolder)
        comment_html_file_path =  os.path.join(
            os.path.dirname(raw_filefolder),
            "comments",
            _my_tools.replace_forbiden_char_in_text(link_text.strip()),"page.html")
        

        async with self.main_request_session.get(comment_url) as response:
            
            raw_data = await response.read()
            text = raw_data.decode(encoding="utf-8",errors="replace")
            
            # Write the comment file 
            await _my_tools.async_write_file(comment_html_file_path,text)

            soup = BeautifulSoup(text,features="lxml")

            comment_element = soup.find("table",{"width":"90%"})
            

            comments = [tr.find("td") for tr in  comment_element.contents if tr.name == "tr"]

            comments_list = []
            for i in range(2,len(comments),3):
                comments_list.append(
                    {
                        "title":comments[i-2].find("strong").get_text(),
                        "text":comments[i].get_text(),
                    }
                )

                    
        return {"local_html_filepath":comment_html_file_path,
                "request_headers":dict(response.headers),
                "comments":comments_list}
    

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

            #print(file_content,file_path)

            
            # Check mandatory information in the json file 

            if not file_content.get("url"):
                return False
            
        return True
    
    async def async_is_data_downloaded(self):

        for url in self.url_informations:
            file_path = self.url_informations[url].get("json_filepath")
            if not os.path.exists(file_path):
                return False
            
            
            file_content = _my_tools.async_read_file(file_path)
            
            if not file_content:
                return False
            
            try:
                file_content = json.loads(file_content)
            except:
                return False

            #print(file_content,file_path)

            
            # Check mandatory information in the json file 

            if not file_content.get("url"):
                return False
            
        return True


class SI_ScrapAudioSermonWork_ALL(http_connexion.ParallelHttpConnexionWithLogManagement):
    def __init__(self,root_folder,material_root_folder,browse_by_type, overwrite_log=False, update_log=True,intermdiate_folders=None):
        
        root_folder = _my_tools.process_path_according_to_cwd(root_folder)

        log_filepath = os.path.join(root_folder,my_constants.LOGS_ROOT_FOLDER,
                                       my_constants.SERMONINDEX_NAME,
                                       material_root_folder,
                                       my_constants.ELABORATED_DATA_FOLDER,
                                       browse_by_type,
                                       my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,
                                       my_constants.get_default_json_filename(0))
        
        input_root_folder = os.path.join(root_folder,
                                         my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.SERMONINDEX_NAME,
                                         material_root_folder,
                                         my_constants.ELABORATED_DATA_FOLDER,
                                         browse_by_type)
        
        input_data = {}
        
        self.input_root_folder = input_root_folder
        
        for file in self.prepare_input_json_file(input_root_folder):
            input_data[file.as_posix()] = _my_tools.read_json(file)

        super().__init__(log_filepath = log_filepath,
                         input_root_folder = input_root_folder,
                         input_data=input_data,
                         overwrite_log = overwrite_log,
                         update_log = update_log)
        
        self.material_root_folder = material_root_folder
        self.browse_by_type = browse_by_type
        self.root_folder = root_folder


    
    def prepare_input_json_file(self,input_root_folder):
        """
        :param matching_subfolders: The folders from wich the json files will be searched out 
        """
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        input_json_files = []

        folder = os.path.join(input_root_folder,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER)
    
        for file in [i for i in pathlib.Path(folder).rglob("*.json") if i.is_file()]:
            if str(file.parent).endswith(my_constants.MAIN_INFORMATION_ROOT_FOLDER):
                input_json_files.append(file)

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

        element = kwargs.get("file_content").get("data")
        
        name  = pathlib.Path(kwargs.get("file_path")).parent.parent.as_posix()
        
        name = name.split("/")[-1]
        
        self.element_dict[name] = {
            **{"pages":element.get("pages"),"name":name},
            
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

        
        ob = SermonIndexAudioSermonWork(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type = self.browse_by_type,
            url_list = element.get("pages"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )

        print(element.get("name"))
        

        await ob.scrap_and_write()

    def is_element_data_downloaded(self,element):
        ob = SermonIndexAudioSermonWork(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type =self.browse_by_type,
            url_list = element.get("url_list"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )
        return ob.is_data_downloaded()
        
