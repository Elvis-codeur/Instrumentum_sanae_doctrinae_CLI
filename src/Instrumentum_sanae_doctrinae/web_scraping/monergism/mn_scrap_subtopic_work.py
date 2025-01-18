import json
import os 
import pathlib
import urllib
import urllib.parse

from bs4 import BeautifulSoup

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
                print(self.intermdiate_folders,"In subtopic scraper")
                ob = MN_ScriptureSubtopicWork(name = self.name,root_folder=self.root_folder,
                                              url_list=[{"url":url_info.get("url")}],browse_by_type=self.browse_by_type,
                                              intermdiate_folders= 
                                              self.intermdiate_folders[-3:] + ["subtopics",url_info.get("link_text")])
                
                await ob.scrap_and_write(save_html_file=True)
            
            final_result[main_url] = scrap_page_works(bs4_object)

        return final_result
    