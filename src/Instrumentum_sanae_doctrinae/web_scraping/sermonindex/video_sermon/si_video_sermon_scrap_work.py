


# This class works for the audio sermons 

import json
import os
import pathlib

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_work import SI_ScrapWork_ALL
import bs4 
from bs4 import BeautifulSoup
import urllib
from Instrumentum_sanae_doctrinae.web_scraping import http_connexion
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools, my_constants

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_metadata import SermonIndexScrapAuthorTopicScripturePage


class SI_ScrapVideoSermonWork(SermonIndexScrapAuthorTopicScripturePage):
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
            
            result = []
            
            table = soup.find("table",attrs = {
                "width":"100%",
                "cellspacing":"0",
                "cellpadding":"10",
                "border":"0"
                
            })
            
            for tr_element in table.find_all("tr",recursie = False):
                
                td_element = tr_element.find_all("td")[-1]
                
                anchor_element = td_element.find_all("a")[1]
                
                b_element_list = td_element.find_all("b",recursive = False)
                
                description_text = ""
                number_of_views = ""
                
                for b_element in b_element_list:
                    if "description:" in b_element.get_text().lower():
                        for next_element in b_element.next_siblings:
                            if next_element.name == "br":
                                break 
                            
                            if isinstance(next_element,bs4.NavigableString):    
                                description_text += next_element.get_text()
                    
                    if "views:" in b_element.get_text().lower():
                        for next_element in b_element.next_siblings:
                            if next_element.name == "br":
                                break 
                            
                            if isinstance(next_element,bs4.NavigableString):    
                                number_of_views += next_element.get_text()    
                
                
                link_text = anchor_element.get_text()
                
                url =   anchor_element.get("href")
                
                
                
                # Now connect to that url to get the precise download url 
                # and the youtube url if it is provided 
                intermediate_download_content = await self.parse_sermonindex_download_intermediate_page(current_page_url,
                                                                                                        url)
                #print(url,link_text)
                
                result.append(
                    {
                        **intermediate_download_content,
                        "url":url,
                        "link_text":link_text,
                        "description":description_text.strip(),
                        "views":number_of_views.strip(),
                    }
                )  
                        
            final_result[current_page_url] = result

        return final_result
    
    
    async def parse_sermonindex_download_intermediate_page(self,current_page_url,download_page_url):
        
        async with self.main_request_session.get(url=download_page_url) as response:
            
            html_code =  await response.text()
            
            parser = bs4.BeautifulSoup(html_code,features="html.parser")
            
            h2_list = parser.findAll("h2")
            
            
            
            embed_url = ""
            download_url = ""
            
            view_h2 = None
            for h2 in h2_list:
                if "view" in h2.get_text().lower():
                    view_h2 = h2
                    
            #print(view_h2)
            
            video_iframe = parser.find("iframe")
            video_embed = parser.find("embed")
            
            if view_h2:
                download_url = view_h2.parent.find("a").get("href")
                
            if video_iframe:
                embed_url = video_iframe.get("src")
            
            if video_embed:
                embed_url = video_embed.get("src")
                
                
            if not download_url:
                raise RuntimeError(f"The download url was not found. Info dowload_page_url = {download_page_url}"
                                   f" current_page_url = {current_page_url}")
            
            
            # Parse to get comments also
            
            comment_table_list = parser.find_all("table",attrs={"width":"95%"}) 
            comment_list = []
            for comment_table in comment_table_list:
                comment_title = ""
                comment_content = ""
                
                comment_title_strong = comment_table.find("strong")
                if comment_title_strong:
                    comment_title = comment_title_strong.get_text()
                
                #print(list(comment_table.children))
                
                content_td_list = comment_table.find_all("tr",recursive=False)
                
                if content_td_list:
                    content_td_list = content_td_list[-1].find_all("td")
                
                
                #print(content_td_list)
                
                for content_td in content_td_list:
                    content_td_text = content_td.get_text()
                    if content_td_text:
                        comment_content = content_td_text
                        break
                    
                
                comment_list.append(
                    {
                        "title":comment_title ,
                        "text":comment_content
                    }
                    )
                   

            return {
                "download_url":download_url,
                "embed_url":embed_url,
                "comments":comment_list
            }
            
                
            
                
                
                
                
                    



class SI_ScrapVideoSermonWork_ALL(SI_ScrapWork_ALL):
    def __init__(self, root_folder, material_root_folder, browse_by_type,
                 overwrite_log=False, update_log=True,
                 intermdiate_folders=None):
        super().__init__(root_folder, material_root_folder, browse_by_type,
                         overwrite_log, update_log, intermdiate_folders)
    
    
    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)
        #print(element)

        try:
            ob = SI_ScrapVideoSermonWork(
                name = element.get("name"),
                root_folder = self.root_folder,
                browse_by_type = self.browse_by_type,
                url_list = element.get("pages"),
                intermdiate_folders = element.get("download_log").get("intermediate_folders"),
                material_root_folder = self.material_root_folder
            )
            
            await ob.scrap_and_write()
            
            return {"success":True,"element":element}
        except:
            return {"success":False,"element":element}
            

        #print(element.get("name"))
        


    async def is_element_data_downloaded(self,element):
        ob = SI_ScrapVideoSermonWork(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type =self.browse_by_type,
            url_list = element.get("url_list"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )
        return await ob.is_data_downloaded()
        
