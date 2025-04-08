

import asyncio
import time 
# This class works for the audio sermons 
from bs4 import NavigableString

from Instrumentum_sanae_doctrinae.web_scraping import http_connexion, my_constants
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_metadata import SermonIndexScrapAuthorTopicScripturePage
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_work import SI_ScrapWork_ALL


class SermonIndexScrapChristianBookTextSermonWork(SermonIndexScrapAuthorTopicScripturePage):
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
            
            book_text_div =  soup.find("div",class_ = "bookText")
            
            #print(book_text_div)
            
            for element in book_text_div.contents:
                
                if(isinstance(element, NavigableString)):
                    element_content = repr(element.string)  
                else:
                    element_content = element.get_text()
                
                if element_content:
                    result.append(element_content)
                    
            final_result[current_page_url] = result
            
        #await asyncio.sleep(0.3)
        
        return final_result

   
   
class SI_ScrapTextSermonChristianBookWork_ALL(SI_ScrapWork_ALL):
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
            ob = SermonIndexScrapChristianBookTextSermonWork(
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
        
        ob = SermonIndexScrapChristianBookTextSermonWork(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type =self.browse_by_type,
            url_list = element.get("url_list"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )
        return await ob.is_data_downloaded()
        
