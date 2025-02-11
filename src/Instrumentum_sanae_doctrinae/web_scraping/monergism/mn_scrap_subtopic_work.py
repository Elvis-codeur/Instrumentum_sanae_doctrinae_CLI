import json
import os 
import sys 

import urllib
import urllib.parse

sys.setrecursionlimit(2000)

from Instrumentum_sanae_doctrinae.web_scraping import http_connexion, my_constants
from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_scrap_metadata
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools



"""
This class is used to scrap the subtopic of scripture and topic pages. It go their pages 
and scrap them. 

"""


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
                    
                    if span_object_class:
                        
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



def get_description_text(bs4_object):
    result = []
    
    div = bs4_object.find("div",class_ = "views-row views-row-1 views-row-odd views-row-first views-row-last")
    if div:
        div = div.find("div",class_ = "views-field views-field-description")
        if div:
            div = div.find("div",class_ = "field-content")
            
            p_list = div.find_all("p")
            
            for p_element in p_list:
                result.append(p_element.get_text().strip())
                
    return result

    
def get_subtopics(bs4_soup,main_url):
        
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
        


class MN_ScrapScriptureOrTopicWork(mn_scrap_metadata.MonergismScrapAuthorTopicScripturePage):
    
    url_already_consulted = []
    
    def __init__(self, name, root_folder, url_list, browse_by_type,intermdiate_folders = None):

        super().__init__(name, root_folder, url_list, browse_by_type,
                          information_type_root_folder = my_constants.WORK_INFORMATION_ROOT_FOLDER,
                          intermdiate_folders = intermdiate_folders)
        #print(self.url_info_list)
    
    async def scrap_url_pages(self):
        """
        Scrap the main links of the page. See this file (documentation/documentation.odt) for more info 
        """

        final_result = {}
        
        for main_url in self.url_informations:
            
            
            # Take the div containing the links of the author 
            
            bs4_object = self.url_informations[main_url].get("bs4_object")
            
            sub_url_topics_list = get_subtopics(bs4_object,main_url)
            
            # Download substopics 
            for url_info in sub_url_topics_list:
                #print(url_info,"\n\n\n")
                
                intermediate_folders = self.intermdiate_folders[
                self.intermdiate_folders.index(my_constants.WORK_INFORMATION_ROOT_FOLDER) + 1:]
                
                url = url_info.get("url")
                
                if url not in MN_ScrapScriptureOrTopicWork.url_already_consulted:
                    MN_ScrapScriptureOrTopicWork.url_already_consulted.append(url)
                                        
                    #print(self.intermdiate_folders,intermediate_folders)
                    ob = MN_ScrapScriptureOrTopicWork(name = self.name,root_folder=self.root_folder,
                                                url_list=[{"url":url}],browse_by_type=self.browse_by_type,
                                                intermdiate_folders= 
                                                    intermediate_folders + ["subtopics",url_info.get("name")])
                    
                    await ob.scrap_and_write(save_html_file=True)
                    
                    
                    f = open(os.path.join(self.root_folder,"trr.json"),mode = "w",encoding = "utf-8")
                    f.write(json.dumps(MN_ScrapScriptureOrTopicWork.url_already_consulted))
                    f.close()
                    
                
                

            # If there is other page to download in this level 
            # The next page 
            next_url = self.next_page(main_url)

            #print("next url found",next_url)

            #print("next url ",next_url)
            intermediate_folders = self.intermdiate_folders[
                self.intermdiate_folders.index(my_constants.WORK_INFORMATION_ROOT_FOLDER) + 1:]
                
            if next_url and (next_url not in MN_ScrapScriptureOrTopicWork.url_already_consulted):
                MN_ScrapScriptureOrTopicWork.url_already_consulted.append(next_url)
                
                #print("next url to download",next_url)
                #print(self.intermdiate_folders,intermediate_folders)
                ob = MN_ScrapScriptureOrTopicWork(name = self.name,root_folder=self.root_folder,
                                            url_list=[{"url":next_url}],browse_by_type=self.browse_by_type,
                                            # It is a page next to the page level so it is the same intermediate folders path
                                            intermdiate_folders= intermediate_folders)
                
                ob.prepare_url_informations(use_page_index_in_url=True)
                
                
                await ob.scrap_and_write(save_html_file=True)
                


                f = open(os.path.join(self.root_folder,"trr.json"),mode = "w",encoding = "utf-8")
                f.write(json.dumps(MN_ScrapScriptureOrTopicWork.url_already_consulted))
                f.close()

            final_result[main_url] = {
                "description_text":get_description_text(bs4_object),
                "main_links":scrap_page_works(bs4_object)
                
                }

        return final_result
    
    def prepare_url_informations(self,use_page_index_in_url = True):
        
        intermdiate_folders = [_my_tools.replace_forbiden_char_in_text(i) for i in self.intermdiate_folders]
        
        compteur = 0 
        
        if use_page_index_in_url:
            for indice,element in enumerate(self.url_info_list):
                
                url = element.get("url")
                
                parsed_url = urllib.parse.urlparse(url)
                
                url_params = urllib.parse.parse_qs(parsed_url.query)
                
                page_number = url_params.get("page",[0])[0]
                    
                json_filepath = os.path.join(self.metadata_root_folder,
                                            my_constants.ELABORATED_DATA_FOLDER,
                                            *intermdiate_folders,
                                            my_constants.get_default_json_filename(page_number))
                
                html_filepath =  os.path.join(self.metadata_root_folder,my_constants.RAW_DATA_FOLDER,
                                            *intermdiate_folders,
                                            my_constants.get_default_html_filename(page_number))    
                    
                self.url_informations[url]['json_filepath'] =  json_filepath 
                
                self.url_informations[url]['html_filepath']  = html_filepath
                
                # Mise à jour normal 
                compteur += 1
            
        else:
            
            for indice,element in enumerate(self.url_info_list):
                json_filepath = os.path.join(self.metadata_root_folder,
                                            my_constants.ELABORATED_DATA_FOLDER,
                                            *intermdiate_folders,
                                            my_constants.get_default_json_filename(indice))
                
                html_filepath =  os.path.join(self.metadata_root_folder,my_constants.RAW_DATA_FOLDER,
                                            *intermdiate_folders,
                                            my_constants.get_default_html_filename(indice))    
                    
                self.url_informations[element.get("url")]['json_filepath'] =  json_filepath 
                
                self.url_informations[element.get("url")]['html_filepath']  = html_filepath
                
                # Mise à jour normal 
                compteur += 1
            
        self.main_request_session = None
    
    async def is_data_downloaded(self):

        for url in self.url_informations:
            file_path = self.url_informations[url].get("json_filepath")
            
            if not os.path.exists(file_path):
                return False
                        
            file_content = await _my_tools.async_read_file(file_path)
            
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
