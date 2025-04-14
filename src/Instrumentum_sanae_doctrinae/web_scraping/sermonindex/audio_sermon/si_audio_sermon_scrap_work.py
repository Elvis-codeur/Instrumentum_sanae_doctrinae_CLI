


# This class works for the audio sermons 

import json
import os
import pathlib

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_work import SI_ScrapWork_ALL
from bs4 import BeautifulSoup
import urllib
from Instrumentum_sanae_doctrinae.web_scraping import http_connexion
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools, my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_metadata import SermonIndexScrapAuthorTopicScripturePage


class SI_AudioSermonWork(SermonIndexScrapAuthorTopicScripturePage):
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
                main_links_element = main_links_element.find_all("tr",recursive = False)
            else:
                return []
            

            #print(*main_links_element[:2],sep="\n\n\n")

            name = ""


            result = []

            compteur = 0
            for element in main_links_element:
            
                a_element = element.find("a")
                
                compteur += 1

                # There is some element in the main_links_element which are not a comment element

                if a_element:


                    url = a_element.get("href")
                    link_text  = a_element.get_text().strip()

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
                                name = comp.get_text().split(" ")
                                if len(name) > 1:

                                    name = " ".join(name[1:]).strip()

                            if  "topic" in comp.get_text().lower():
                                add_element_to_topic = True

                            if "scripture" in comp.get_text().lower():
                                add_element_to_scriptures = True
                                add_element_to_topic = False

                            if comp.name == 'i' and add_element_to_topic:
                                topic_list.append(comp.get_text().strip())

                            if comp.name == 'i' and add_element_to_scriptures:
                                scripture_list.append(comp.get_text().strip())

                        
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
                            "name":name,
                            "downlaod_number":download_number,
                            "topics":topic_list,
                            "scriptures":scripture_list,
                            "link_text":link_text,
                            "link_description":link_description.strip(),
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
                        "title":comments[i-2].find("strong").get_text().strip(),
                        "text":comments[i].get_text().strip(),
                    }
                )

                    
        return {"local_html_filepath":comment_html_file_path,
                "request_headers":dict(response.headers),
                "comments":comments_list}
    


class SI_ScrapAudioSermonWork_ALL(SI_ScrapWork_ALL):
    def __init__(self, root_folder, material_root_folder, browse_by_type,
                 overwrite_log=False, update_log=True,
                 intermdiate_folders=None):
        super().__init__(root_folder, material_root_folder, browse_by_type, 
                         overwrite_log, update_log, intermdiate_folders)
          
    
    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)
        #print(element.get("name"))

        try:
            ob = SI_AudioSermonWork(
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
        ob = SI_AudioSermonWork(
            name = element.get("name"),
            root_folder = self.root_folder,
            browse_by_type =self.browse_by_type,
            url_list = element.get("url_list"),
            intermdiate_folders = element.get("download_log").get("intermediate_folders"),
            material_root_folder = self.material_root_folder
        )
        return await ob.is_data_downloaded()
        
