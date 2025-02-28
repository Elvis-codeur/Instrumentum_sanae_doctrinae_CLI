import json
import re 
import aiohttp
import urllib
import bs4
import os 
import pathlib
from urllib.parse import parse_qs
import requests 


from Instrumentum_sanae_doctrinae.web_scraping import  http_connexion, my_constants
from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_scrap_metadata
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools


class MonergismScrapAuthorTopicScriptureGeneralInformation(mn_scrap_metadata.MonergismScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder, url_list, browse_by_type,) -> None:
        
        
        
        super().__init__(name, root_folder, url_list, browse_by_type,
                         information_type_root_folder = my_constants.MAIN_INFORMATION_ROOT_FOLDER,
                         intermdiate_folders= None)
        
        # This session object is created to be used to connect and Get the other pages 
        # Where the other information will be found 
        #self.other_page_request_session = aiohttp.ClientSession() 
        
    
         
    def prepare_url_informations(self):
        
        intermdiate_folders = [_my_tools.replace_forbiden_char_in_text(i) for i in self.intermdiate_folders]
    
        for indice,url_dict in enumerate(self.url_info_list):
            url_intermediate_folders = url_dict.get("intermediate_folders")                
            
            #print("Elvis",self.name,url_intermediate_folders)
            
            self.url_informations[url_dict.get("url")]['json_filepath'] =  os.path.join(self.metadata_root_folder,
                                                                                my_constants.ELABORATED_DATA_FOLDER,
                                                                                *intermdiate_folders,
                                                                                *url_intermediate_folders,
                                                                                my_constants.get_default_json_filename(indice))
            
            self.url_informations[url_dict.get("url")]['html_filepath']  = os.path.join(self.metadata_root_folder,
                                                                                my_constants.RAW_DATA_FOLDER,
                                                                                *intermdiate_folders,
                                                                                *url_intermediate_folders,
                                                                                my_constants.get_default_html_filename(indice))
        
        self.main_request_session = None


    def parse_filter_by_ul(self,section_object,url):
       
        result = {}
        
        if not section_object:
            return {}

        filter_by_lis = section_object.find_all("li")                       
                                    
        for li in filter_by_lis:
            link = li.find("a")
            link_text = link.get_text()

            topic_element_number = re.findall(r'\((\d+)\)',link_text)

            topic_element_number = int(topic_element_number[0]) if topic_element_number else None
            
            link_text = link_text.split("(")[0].strip()
            
            result[link_text] = {
                "url":urllib.parse.urljoin(url,link.get("href")),
                "link_text": link_text,
                "number":topic_element_number
            }   
        return result    
    
    
    def get_page_param(self,url):
        query_params = parse_qs(url.query)
        return int(query_params.get('page', [0])[0])

    def get_other_pages_in_the_current_page(self,main_url,old_url_list,soup,current_url):
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
                      
                    next_page_url = urllib.parse.urljoin(main_url,
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
    
    
    async def get_all_the_other_pages(self,main_url,bs4_soup):
        """
        This method get the other pages of the author. 
        For example. If on the firt web page of the pages of Calvin https://www.monergism.com/search?f[0]=author:34198
        This method will get the other pages also. In my case until the 
        thirtheenth page https://www.monergism.com/search?f%5B0%5D=author%3A34198&page=13 (at the date I wrote this code) 
        """
        pages_list = []
        new_pages_url = self.get_other_pages_in_the_current_page(main_url,pages_list,bs4_soup,main_url)

        if new_pages_url:
            pages_list += new_pages_url
        

            while(new_pages_url):
                next_page_url = max(pages_list,key=self.get_page_param)
                soup = await self.get_bs4soup_from_url(self.main_request_session,
                                                        urllib.parse.urlunparse(next_page_url))
                new_pages_url = self.get_other_pages_in_the_current_page(main_url,pages_list,soup,next_page_url)
                
            
        pages_list = list(set(pages_list))

        pages_list = sorted(pages_list,key = self.get_page_param)

        pages_list = [urllib.parse.urlunparse(url) for url in pages_list]
        
        if not pages_list:
            pages_list = [main_url]
        else:
            if main_url not in pages_list[1:]:
                pages_list = [main_url] + pages_list[1:]
            else:
                pages_list = pages_list[1:]
                
        
        return pages_list
        
    
    
    
    def scrap_filters(self,bs4_soup,main_url):
        """
        This method scrap the topics, the authors, etc 
        """
        
        filter_by_sections = bs4_soup.find("div",class_ ="region-inner region-sidebar-first-inner")
            
        
        filter_by_topic_data = {}
        filter_by_format_data = {}
        filter_by_genre_data = {} 
        filter_by_web_site_data = {}
        filter_by_author_data = {}
        filter_by_serie_data = {}
        
        
        if filter_by_sections:
            
            filter_by_sections = filter_by_sections.find_all("section")

            # Filter by topic
            filter_by_topic_data = self.parse_filter_by_ul(filter_by_sections[1],main_url)
            
            # Filter by author
            filter_by_author_data =  self.parse_filter_by_ul(filter_by_sections[2],main_url)
            
            # Filter by series
            filter_by_serie_data =  self.parse_filter_by_ul(filter_by_sections[3],main_url)
            
            # Filter by genre
            filter_by_genre_data =  self.parse_filter_by_ul(filter_by_sections[4],main_url)
            
            # Filter by format 
            filter_by_format_data =  self.parse_filter_by_ul(filter_by_sections[5],main_url)

            # Filter by web site 
            filter_by_web_site_data =  self.parse_filter_by_ul(filter_by_sections[6],main_url)


        result = {
            "filter_by_topic": filter_by_topic_data,
            "filter_by_format":filter_by_format_data,
            "filter_by_genre":filter_by_genre_data,
            "filter_by_web_site":filter_by_web_site_data,
            "filter_by_author":filter_by_author_data,
            "filter_by_serie_data":filter_by_serie_data,
        }

        return result 

        
        
            

    async def scrap_url_pages(self):
        """
        
        """


    def is_data_downloaded(self):
        #print(self.name)
        
        if not self.url_informations:
            return False

        for url in self.url_informations:
            file_path = self.url_informations[url].get("json_filepath")
            if not os.path.exists(file_path):
                return False
            
            #print(file_path)
            
            file_content = _my_tools.read_file(file_path)
            
            if not file_content:
                return False
            
            file_content = json.loads(file_content)
            

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
        
        
        
class MonergismScrapAuthorGeneralInformation(MonergismScrapAuthorTopicScriptureGeneralInformation):
    def __init__(self, name, root_folder, url_list, browse_by_type):
        super().__init__(name, root_folder, url_list, browse_by_type)
        
        
    
    def get_the_name_of_the_author(self,bs4_soup):
        name =  ""
        name_element = bs4_soup.find(lambda tag:tag.name == "li" and 
                                    tag.has_attr("class") and 
                                    
                                    ("active" in tag["class"] and
                                    "leaf" in tag["class"] and
                                    "first" in tag["class"])
                                    
                                    )
        
        
        
        if name_element:
            name =  "".join(name_element.find_all(text = True,recursive=False)).strip()

        # Remove any consecutive space like "   " from the name of the author 
        if name:
            return _my_tools.remove_consecutive_spaces(name)
            
    
        
        
    async def scrap_url_pages(self):
        final_result = {}

        for main_url in self.url_informations:
           
            bs4_soup = self.url_informations[main_url].get("bs4_object")
             
            pages_list = await self.get_all_the_other_pages(main_url,bs4_soup)
        
            author_name = self.get_the_name_of_the_author(bs4_soup)
            
            result = {
                "pages":pages_list,
                "name":author_name,
                **self.scrap_filters(bs4_soup,main_url),
                
            }

            final_result[main_url] = result

        return final_result 
    
    
class MonergismScrapTopicOrScriptureGeneralInformation(MonergismScrapAuthorTopicScriptureGeneralInformation):
    def __init__(self, name, root_folder, url_list, browse_by_type):
        super().__init__(name, root_folder, url_list, browse_by_type)
        
        
    
    def get_subtopics(self,bs4_soup,main_url):
        
        h3_list = [i for i in bs4_soup.find_all("h3")]
        
        subtopic_h3 = [h3_object for h3_object in h3_list if h3_object.get_text() == "Subtopics"]
        
        if not subtopic_h3:
            return []
        
        subtopic_h3 = subtopic_h3[0]
        
        #print(subtopic_h3.parent.next)
        
        content = subtopic_h3.parent.find_next_sibling("div")
        #print(content,"\n\n\n")
        
        result = []

        if content:
            links = content.find_all("a")
            for i in links:
                anchor_text = i.get_text()
                if anchor_text:
                    result.append(
                        {
                            "name":anchor_text,
                            "url":urllib.parse.urljoin(main_url,i.get("href")),
                        }
                    )
                
        return result
        
        
            
           
        
        
    def get_topic_description(self,bs4_soup):
        result = []
        
        div = bs4_soup.find("div",class_ = 'views-field views-field-description')
        
        if div:    
            div = div.find("div","field-content")
            for paragraph in div.find_all("p"):
                result.append(paragraph.get_text())

        return result        
        
    def get_recommanded_reading(self,bs4_soup):
        result = []
        
        recommanded_h2 = bs4_soup.find_all("h2")

        recommanded_h2 = [i for i in recommanded_h2 if i.get_text().lower() ==  "recommended reading"]

        if not recommanded_h2:
            return []
        recommanded_h2 = recommanded_h2[0]
        
        recomandation_div = recommanded_h2.find_next_sibling("div")

        
        if not recomandation_div:
            return []
        
        divs = recomandation_div.find("div",class_ = "view-content").find_all("div",recursive = False)
        
        for div in divs:
            
            #print(div,"\n\n\n")
        

            # The title of the book
            title = div.find("div",class_ = "views-field views-field-title")
            
            title_span = title.find("span")
            title = title_span.get_text()
            
            # The author of the document
            author_name = div.find("div",class_ = "views-field views-field-field-author")
            author_name = author_name.find("div").get_text()
            
            result.append(
                {
                    "url": title_span.find("a").get("href"),
                    #"cover_image_url":field_cover_anchor.find("img").get("src"),
                    "title":title,
                    "author_name":author_name,
                    
                }
            )
        return result 
    
    async def scrap_url_pages(self):
        final_result = {}

        for main_url in self.url_informations:
            
            #print(main_url)
           
            bs4_soup = self.url_informations[main_url].get("bs4_object")

            # The pages of the topic 
            pages_list = await self.get_all_the_other_pages(main_url,bs4_soup)
            
            # The subtopics of the topic
            subtopics = self.get_subtopics(bs4_soup,main_url)
            
            # The text describing the topic 
            description = self.get_topic_description(bs4_soup)
            
            # The books recommanded
            recommanded_books =  self.get_recommanded_reading(bs4_soup)
            
            
            # The name of the topic or the bible book 
            title_h1 = bs4_soup.find("h1",id = "page-title")
            name =  title_h1.get_text().strip()
            if "-" in name:
                name = name.split("-")[-1].strip()
                
            if "by" in name:
                name = name.split("by")[0].strip()
                
            name = _my_tools.remove_consecutive_spaces(name)
            name = _my_tools.replace_forbiden_char_in_text(name)
            
            
            result = {
                "name":name,
                "pages":pages_list,
                "subtopics":subtopics,
                "recommanded_reading":recommanded_books,
                "description":description,
            }

            final_result[main_url] = result
        
        return final_result
        

        
class MonergismScrapSeriesGeneralInformation(MonergismScrapAuthorTopicScriptureGeneralInformation):
    
    def __init__(self, name, root_folder, url, browse_by_type):
        super().__init__(name, root_folder, url, browse_by_type)
        
        
    
    def prepare_intermdiate_folders(self,intermdiate_folders,browse_by_type,name,information_type_root_folder):
        if intermdiate_folders:
            intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER,]\
                                 + intermdiate_folders +[name] 
            return intermdiate_folders
        else:
            intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER
                                   ,name]
            return intermdiate_folders
        
        
    
    async def scrap_url_pages(self):
        final_result = {}

        for main_url in self.url_informations:
           
            bs4_soup = self.url_informations[main_url].get("bs4_object")
             
            result = {
                **self.scrap_filters(bs4_soup,main_url),
            }

            final_result[main_url] = result

        return final_result 
    
    
    
class MonergismScrapRCSproulGeneralInformation(MonergismScrapAuthorTopicScriptureGeneralInformation):
    def __init__(self,root_folder, url, browse_by_type = my_constants.SPEAKER_NAME, name = 'R C Sproul'):
        super().__init__(name, root_folder, url, browse_by_type)
        

    
    def get_main_quote(self,article_object):
        quote = article_object.find("blockquote")
        return quote.get_text()
    
    def get_tributes(self,tributes_p):
        result = []
        
    
        for anchor_element in tributes_p.find_all("a"):
            result.append(
                {
                    "name":_my_tools.remove_consecutive_spaces(anchor_element.get_text()),
                    "url":anchor_element.get("href")
                }
            )
        return result
    

    
    def anchor_object_to_dict(self,anchor_object):
        return {
                "name":anchor_object.get_text(),
                "url":anchor_object.get("href")
            }
        
        
    async def scrap_url_pages(self):
        final_result = {}
        for main_url in self.url_informations:
            
            bs4_soup = self.url_informations[main_url].get("bs4_object")
            
            main_article_class_name = "node node-page node-published node-not-promoted node-not-sticky author-john-hendryx odd clearfix"
            
            main_article = bs4_soup.find("article",class_ = main_article_class_name)
            
            main_div = main_article.find("div",class_ = "field field-name-field-body field-type-text-long field-label-hidden")
            
            main_div = main_article.find("div",class_ = "field-item even")
            
            main_div_direct_children = main_div.contents 
            
            main_div_direct_children = [i for i in main_div_direct_children if i.name]
            
            
            quote = self.get_main_quote(main_div)
            tributes = self.get_tributes(main_div_direct_children[1])
            theology = main_div_direct_children[2].get_text()
            bibliography_paragraph =  []
            selected_lectures = []
            sermon_by_scripture = []
            sermon_by_topic = []
            selected_essay = []
            
            actual_h3_text = ''
            for child in main_div_direct_children[2:]:
                if child.name =="h3":
                    actual_h3_text = child.get_text().strip()
                    
                if child.name == "p":
                    if actual_h3_text == "Biographical Sketch":
                        bibliography_paragraph.append(child)
                        
                    elif actual_h3_text == "Selected Lecture Series (MP3 Format)":
                        anchor_object = child.find("a")
                        selected_lectures.append(self.anchor_object_to_dict(anchor_object))
                        
                    elif actual_h3_text == "Sermon Series by Scripture":
                        for li in child.find_all("li"):
                            anchor_object = li.find("a")
                            sermon_by_scripture.append(self.anchor_object_to_dict(anchor_object))
                    
                    elif actual_h3_text == "Sermon Series by Topic":
                        for li in child.find_all("li"):
                            anchor_object = li.find("a")
                            sermon_by_topic.append(self.anchor_object_to_dict(anchor_object))
                    
                    elif actual_h3_text == "Selected Essays":
                        anchor_object = child.find("a")
                        if anchor_object:
                            selected_essay.append(self.anchor_object_to_dict(anchor_object))
                            
                        



class MonergismScrapGeneralInformation_ALL(http_connexion.ParallelHttpConnexionWithLogManagement):
    def __init__(self,root_folder,browse_by_type, overwrite_log=False,intermdiate_folders=None):

        root_folder = _my_tools.process_path_according_to_cwd(root_folder)

        log_filepath = os.path.join(root_folder,my_constants.LOGS_ROOT_FOLDER,
                                       my_constants.MONERGISM_NAME,
                                       my_constants.ELABORATED_DATA_FOLDER,
                                       browse_by_type,
                                       my_constants.GENERAL_INFORMATION_NAME,
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
                         input_data=input_json_files_content,
                         overwrite_log = overwrite_log,
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
        
        intermediate_folders = self.get_element_intermidiate_folders(element)
        result = {}
        
        try:
            if self.browse_by_type == my_constants.SPEAKER_NAME:
                ob = MonergismScrapAuthorGeneralInformation(
                    name = element.get("name"),
                    root_folder = self.root_folder,
                    browse_by_type = self.browse_by_type,
                    url_list = [{**i,**u} for i,u in zip(element.get("url_list"),intermediate_folders)],
                    )
                await ob.scrap_and_write()
                
                result = {"success":True,"element":element}
                
            elif self.browse_by_type == my_constants.TOPIC_NAME or \
                    self.browse_by_type == my_constants.SCRIPTURE_NAME:
                ob = MonergismScrapTopicOrScriptureGeneralInformation(
                    name = element.get("name"),
                    root_folder = self.root_folder,
                    browse_by_type = self.browse_by_type,
                    url_list = [{**i,**u} for i,u in zip(element.get("url_list"),intermediate_folders)],
                    )
                await ob.scrap_and_write()
                
                result = {"success":True,"element":element}
                
            return result
                
        except:
            result = {"success":False,"element":element}
            
            return result
    
            
    
    def get_element_intermidiate_folders(self,element):
        element_url_list = element.get("url_list")
        element_name = element.get("name")
        
        result = []
        
        for url_object in element_url_list:
            if element_name != url_object.get("link_text"):
                result.append({"intermediate_folders":[url_object.get("link_text")]})
            else:
                result.append({"intermediate_folders":[]})
                
        return result 
        
    async def is_element_data_downloaded(self,element):
        
        intermediate_folders = self.get_element_intermidiate_folders(element)
        
        #print(element)
        
        if self.browse_by_type == my_constants.SPEAKER_NAME:
            ob = MonergismScrapAuthorGeneralInformation(
                name = element.get("name"),
                root_folder = self.root_folder,
                browse_by_type = self.browse_by_type,
                url_list = [{**i,**u} for i,u in zip(element.get("url_list"),intermediate_folders)],
                )
            
            #if element.get("name") in ["K. Scott Oliphint","H.B. Charles Jr.",]:
            #    print(element.get("name"),ob.is_data_downloaded(),ob.__dict__,"\n\n")
            
            
            return ob.is_data_downloaded()
        
        elif self.browse_by_type == my_constants.TOPIC_NAME or \
                self.browse_by_type == my_constants.SCRIPTURE_NAME:
            
            
            ob = MonergismScrapTopicOrScriptureGeneralInformation(
                name = element.get("name"),
                root_folder = self.root_folder,
                browse_by_type = self.browse_by_type,
                url_list = [{**i,**u} for i,u in zip(element.get("url_list"),intermediate_folders)],
                )
            
            
            return ob.is_data_downloaded()
        
        
        
    async def update_to_download_list(self):
        """
        This function take the element in the self.element_dict and take care that if there 
        is an element in the self.element_dict that is not downloaded and is not in the yet in 
        the to_download list. That happen if after the last scraping, new elements have been scrapped 
        and not yet downloaded
        """
        # A list of the url of of the link object which have been already downloaded 
        downloaded_list = [i for i in self.log_file_content.get("downloaded")] if self.log_file_content.get("downloaded") else []
        to_downlaod_list = [i for i in self.log_file_content.get("to_download")] if self.log_file_content.get("to_download") else []

        
        # We take "element_list" variable because it contains the link of the author, scripture or topic
        for element_name in self.element_dict:
            if element_name not in downloaded_list: # If it is not already downloaded 
                if element_name not in to_downlaod_list: # It is not in the link prepared to for download. 
                    #print("\n\n\n\n\n",self.log_file_content["to_download"].keys(),"\n\n\n",self.element_dict.keys(),"\n\n\n\n",url,element_name)
                    print(element_name)
                    self.log_file_content["to_download"][element_name] = self.element_dict[element_name]
                else: # If the element is already in the "to_download" list, there is no need to add it 
                    pass 
            else: # If the link is already downlaed. There is no need of modification of anything 
                pass 
               






