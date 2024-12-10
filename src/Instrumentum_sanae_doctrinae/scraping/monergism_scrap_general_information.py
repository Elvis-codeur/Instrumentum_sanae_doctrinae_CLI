import re 
import aiohttp
import bs4
import requests 

from . import _my_tools
from .monergism_scrap_metadata import * 
from  . import http_connexion


class MonergismScrapAuthorTopicScriptureGeneralInformation(MonergismScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder, url, browse_by_type,) -> None:

        super().__init__(name, root_folder, url, browse_by_type,
                         information_type_root_folder = my_constants.MAIN_INFORMATION_ROOT_FOLDER,
                         intermdiate_folders= None)
        
        # This session object is created to be used to connect and Get the other pages 
        # Where the other information will be found 
        #self.other_page_request_session = aiohttp.ClientSession() 


    async def scrap_url_pages(self):
        """
        
        """

        def parse_filter_by_ul(bs4_soup,css_selector,url):
            result = {}

            filter_by_ul = bs4_soup.find("ul",class_= re.compile(css_selector))

            if not filter_by_ul:
                return []

            filter_by_lis = filter_by_ul.find_all("li")                       
                                        
            for li in filter_by_lis:
                link = li.find("a")
                link_text = link.get_text()

                topic_element_number = re.findall(r'\((\d+)\)',link_text)

                topic_element_number = int(topic_element_number[0]) if topic_element_number else None
                result[url] = {
                    "url":urllib.parse.urljoin(url,link.get("href")),
                    "link_text": link_text.split("(")[0].strip(),
                    "number":topic_element_number
                }   
            return result    


        def get_page_param(url):
            query_params = parse_qs(url.query)
            return int(query_params.get('page', [0])[0])

        def get_other_pages(old_url_list,soup,current_url):
            #print(current_url)
            
            pages_ul = soup.find(lambda tag :tag.name == "ul" and 
                                            tag.has_attr("class") and 
                                            'pager' in tag['class'] and
                                                  'clearfix' in tag['class']
                                            )
            
            if not pages_ul:
                return []

            next_page_li_list = pages_ul.find_all("li",attrs = {"class":"pager-item"})

            new_url_list = []

            for next_page_li in next_page_li_list:
                if next_page_li:
                    next_page_anchor = next_page_li.find("a")
                    if next_page_anchor:
                        next_page_url = urllib.parse.urljoin(url,
                                                            next_page_anchor.get("href"))
                        new_url_list.append(urllib.parse.urlparse(next_page_url))

            

            if not current_url in old_url_list:
                if isinstance(current_url,str):
                    old_url_list.append(urllib.parse.urlparse(current_url))
                else:
                    old_url_list.append(current_url)

            
            # To avoid the addition of the last page who will break the
            # loop using the method  
            old_url_list += new_url_list

            #print(current_url)
            
            # This li element exists only on the last page of 
            # an author, topic, scripture, etc
            last_page_li = pages_ul.find(lambda tag: tag.name == "li" and 
                                                tag.has_attr('class') and 
                                                'pager-current' in tag['class'] and
                                                  'last' in tag['class'])
            
            maximum_page_number = 0
            if last_page_li:
                maximum_page_number = int(last_page_li.get_text()) -1
                #print(current_url,"---",maximum_page_number) 
                if int(parse_qs(current_url.query).get("page",[0])[0]) == maximum_page_number:
                    return []

            #print(new_url_list)

            return new_url_list


        final_result = {}

        for url in self.url_informations:
           
            
            soup = self.url_informations[url].get("bs4_object")

            # Filter by topic
            filter_by_topic_data = parse_filter_by_ul(soup,"facetapi-facetapi-links*.facetapi-facet-field-link-topic",url)
            
            # Filter by format
            filter_by_format_data = parse_filter_by_ul(soup,"facetapi-facetapi-links*.facetapi-facet-field-link-format",url)
            
            # Filter by genre
            filter_by_genre_data = parse_filter_by_ul(soup,"facetapi-facetapi-links*.facetapi-facet-field-link-genres",url)
            
            # Filter by web site 
            filter_by_web_site_data = parse_filter_by_ul(soup,"facetapi-facetapi-links*.facetapi-facet-field-link-website",url)
            
            # Filter by author 
            filter_by_author_data = parse_filter_by_ul(soup,"facetapi-facetapi-links*.facetapi-facet-field-link-authors",url)

            pages_list = []
            new_pages_url = get_other_pages(pages_list,soup,url)

            if new_pages_url:
                pages_list += new_pages_url
            

                while(new_pages_url):
                    next_page_url = max(pages_list,key=get_page_param)
                    soup = await self.get_bs4soup_from_url(self.main_request_session,
                                                            urllib.parse.urlunparse(next_page_url))
                    new_pages_url = get_other_pages(pages_list,soup,next_page_url)
                    
                
            pages_list = list(set(pages_list))

            pages_list = sorted(pages_list,key = get_page_param)

            pages_list = [urllib.parse.urlunparse(url) for url in pages_list]
            
            
            name =  ""
            name_element = soup.find(lambda tag:tag.name == "li" and 
                                     tag.has_attr("class") and 
                                     
                                     ("active" in tag["class"] and
                                      "leaf" in tag["class"] and
                                      "first" in tag["class"])
                                     
                                     )
            
            
            
            if name_element:
                name =  "".join(name_element.find_all(text = True,recursive=False)).strip()

            if name:
                name = list(name)
                for indice in  range(len(name)-1):
                    if  name[indice] == " " and name[indice+1] == " ":
                        name[indice] = ""

            
            if not pages_list:
                pages_list = [url]
            else:
                pages_list = pages_list[1:]

            result = {
                "name": "".join(name),
                "pages":pages_list, # To avoid having the first url twice 
                "filter_by_topic": filter_by_topic_data,
                "filter_by_format":filter_by_format_data,
                "filter_by_genre":filter_by_genre_data,
                "filter_by_web_site":filter_by_web_site_data,
                "filter_by_author":filter_by_author_data,
            }


            final_result[url] = result

        return final_result 
    
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
            
            if not file_content.get("data").get("pages"):
                return False
            
        return True
    
    async def get_bs4soup_from_url(self,session_object,url):
        """
        Take an url and return a bs4 object. 
        """        
        async with session_object.get(url,
                                      timeout=my_constants.HTTP_REQUEST_TIMEOUT)  as response:
            html = await response.text()
            return bs4.BeautifulSoup(html,features="lxml") 

        



class MonergismScrapGeneralInformation(http_connexion.ParallelHttpConnexionWithLogManagement):
    def __init__(self,root_folder,browse_by_type, overwrite_log=False, update_log=True,intermdiate_folders=None):

        root_folder = _my_tools.process_path_according_to_cwd(root_folder)

        log_filepath = os.path.join(root_folder,my_constants.LOGS_ROOT_FOLDER,
                                       my_constants.MONERGISM_NAME,
                                       my_constants.ELABORATED_DATA_FOLDER,
                                       browse_by_type,
                                       my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER,
                                       my_constants.get_default_json_filename(0))
        
        input_root_folder = os.path.join(root_folder,
                                         my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.MONERGISM_NAME,
                                         my_constants.ELABORATED_DATA_FOLDER,
                                         browse_by_type,
                                        my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER,

                                         )
        
        
        input_json_files_content = {}

        for file in self.prepare_input_json_file(input_root_folder):
            input_json_files_content[str(file)] = _my_tools.read_json(file)

        
        #print(input_json_files_content)

        super().__init__(log_filepath = log_filepath,
                         element_list=input_json_files_content,
                         overwrite_log = overwrite_log,
                         update_log = update_log,
                         input_root_folder=input_root_folder)
        
        self.browse_by_type = browse_by_type
        self.root_folder = root_folder

    
    def prepare_input_json_file(self,input_root_folder):
        """
        :param input_root_folder: The folder from which to search for the json files to use as input
        """
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        input_json_files = []
        input_json_files = [i for i in pathlib.Path(input_root_folder).rglob("*.json") if i.is_file()]
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
        
        for element in element_list:

            self.element_dict[element.get("name")] = {
                **element,
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
        #print("\n",element.get("name"))
        ob = MonergismScrapAuthorTopicScriptureGeneralInformation(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type = self.browse_by_type,
            url = element.get("url_list"),
            )
        ob.scrap_and_write()
        
    def is_element_data_downloaded(self,element):
        #print(element)

        ob = MonergismScrapAuthorTopicScriptureGeneralInformation(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type = self.browse_by_type,
            url = element.get("url_list"),
            )
        
        return ob.is_data_downloaded()
        
