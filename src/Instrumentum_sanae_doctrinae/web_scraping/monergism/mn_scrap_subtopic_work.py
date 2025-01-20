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
        


class MN_ScriptureSubtopicWork(mn_scrap_metadata.MonergismScrapAuthorTopicScripturePage):
    
    url_already_consulted = []
    
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
            
            sub_url_topics_list = get_subtopics(bs4_object,main_url)
            
            for url_info in sub_url_topics_list:
                #print(url_info,"\n\n\n")
                
                intermediate_folders = self.intermdiate_folders[
                self.intermdiate_folders.index(my_constants.WORK_INFORMATION_ROOT_FOLDER) + 1:]
                
                url = url_info.get("url")
                
                if url not in MN_ScriptureSubtopicWork.url_already_consulted:
                    
                    
                    #print(url," not consulted yet. total = ",len(MN_ScriptureSubtopicWork.url_already_consulted))
                    #f = open(os.path.join(self.root_folder,"trr.json"),"w")
                    #f.write(json.dumps(MN_ScriptureSubtopicWork.url_already_consulted))
                    #f.close()
                    
                    #print(self.intermdiate_folders,intermediate_folders)
                    ob = MN_ScriptureSubtopicWork(name = self.name,root_folder=self.root_folder,
                                                url_list=[{"url":url}],browse_by_type=self.browse_by_type,
                                                intermdiate_folders= 
                                                    intermediate_folders + ["subtopics",url_info.get("name")])
                    
                    await ob.scrap_and_write(save_html_file=True)
                    
                    MN_ScriptureSubtopicWork.url_already_consulted.append(url)
                    
                    next_url = self.next_page(main_url)
                    
                    # If there is other page to download in this level 
                    if next_url:
                        #print(self.intermdiate_folders,intermediate_folders)
                        ob = MN_ScriptureSubtopicWork(name = self.name,root_folder=self.root_folder,
                                                    url_list=[{"url":next_url}],browse_by_type=self.browse_by_type,
                                                    intermdiate_folders= 
                                                        intermediate_folders + ["subtopics",url_info.get("name")])
                        
                        await ob.scrap_and_write(save_html_file=True)
                        
                    MN_ScriptureSubtopicWork.url_already_consulted.append(next_url)
                    
                        
                    
                else:
                    final_result[main_url] = scrap_page_works(bs4_object)

                    return final_result
    
            final_result[main_url] = {
                "description_text":get_description_text(bs4_object),
                "main_links":scrap_page_works(bs4_object)
                
                }

        return final_result
    
