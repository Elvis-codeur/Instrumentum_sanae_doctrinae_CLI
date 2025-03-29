


# This class works for the audio sermons 

import json
import os
import pathlib

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_work import SI_ScrapWork_ALL
import bs4 
from Instrumentum_sanae_doctrinae.web_scraping import http_connexion, my_constants
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_metadata import SermonIndexScrapAuthorTopicScripturePage


class SI_ScrapVintageImageWork(SermonIndexScrapAuthorTopicScripturePage):
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
            
            for tr_object in table.find_all("tr",recursive = False):
                
                td_objects = tr_object.find_all("td")
                
                image_td_object = td_objects[0]
                
                description_td_object = td_objects[1]
                
                img_url = image_td_object.find("img").get("src")
                
                # img_url is actually the url of thumnail. I convert it the url of a jpg image url 
                img_url = img_url.replace("thumbs/","")
                
                
                decription_anchor_object = description_td_object.find_all("a",recursive = False)[-1]
                
                
                description = "".join((i.strip() for i in description_td_object.contents 
                                       if isinstance(i,bs4.NavigableString))).strip()
                
                result.append(
                    {
                        "img_url":img_url,
                        "url":decription_anchor_object.get("href"),
                        "link_text":decription_anchor_object.get_text(),
                        "description":description,
                    }
                )
                
                
            final_result[current_page_url] = result

        return final_result


class SI_ScrapVintageImageWork_ALL(SI_ScrapWork_ALL):
    def __init__(self, root_folder, material_root_folder, browse_by_type,
                 overwrite_log=False, update_log=True,
                 intermdiate_folders=None):
        super().__init__(root_folder, material_root_folder, browse_by_type,
                         overwrite_log, update_log, intermdiate_folders)
          
    
    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)
        try:
            ob = SI_ScrapVintageImageWork(
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
            

    async def is_element_data_downloaded(self,element):
        ob = SI_ScrapVintageImageWork(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type =self.browse_by_type,
            url_list = element.get("url_list"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )
        return await ob.is_data_downloaded() 