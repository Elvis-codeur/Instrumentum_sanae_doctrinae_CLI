


import copy
import datetime
import math
import os
import requests
import traceback
from Instrumentum_sanae_doctrinae.my_tools import general_tools

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_download import SI_Download_Work, SI_DownloadFromUrl
import aiofile
import bs4


class SI_DownloadVideo(SI_DownloadFromUrl):
    def __init__(self, url, output_folder, output_file_name,
                 aiohttp_session, separe_file_based_on_format=True):
        
        super().__init__(url, output_folder, output_file_name,
                         aiohttp_session, separe_file_based_on_format)
    
    
    
    async def download(self,input_file_path):
        
        #print(input_file_path)
        
        """
        Args:
            input_file_path (str): The path of the file where the work input url and 
            information have been taken from . It is important because I will open
            the file and I will add the comments and data scraped from 
            the intermediate page to the data scraped about the work 

        Returns:
            _type_: _description_
        """
        try:
            intermediate_page_content =  await self.parse_sermonindex_download_intermediate_page(self.url)
            
            #print(intermediate_page_content)
            
            # I pass the dict as **kwargs to the function 
            result = await self.download_internal_version(
                **{
                 "download_url":intermediate_page_content.get("download_url"),
                 "embed_url":intermediate_page_content.get("embed_url"),   
                }   
            )
            
            
            file_content = await general_tools.async_read_json(input_file_path)
            
            new_file_content = copy.deepcopy(file_content)
            
            #print(result)
            
            for indice,element in enumerate(file_content.get("data")):
                if element.get("url") == self.url:
                    new_element = {**element,**intermediate_page_content}
                    #print(new_element)
                    new_file_content["data"][indice] = new_element
                    
                    await general_tools.async_write_json(input_file_path,new_file_content)
            
            return result
        
        
        except Exception as e:
            result = {"success":0,"error":"" .join(traceback.format_exception(e))}
            return result 
    
    
            
    async def download_internal_version(self,**parameters_to_add_result):
        """
       
        """
        #print("Elvis")
        # The size of the file in Mb
        file_size_mega_byte = 0 
        
        # Chunck size 
        file_chunck_size_byte = 4*1024*1024 #Mega Byte # 
        
        result = {}
        download_begin_time = None 
        
        #print(parameters_to_add_result)
        
        #print("in downlaod",parameters_to_add_result)
        
        async with self.aiohttp_session.get(parameters_to_add_result.get("download_url"),allow_redirects=True) as response:
            download_begin_time =  general_tools.datetimeToGoogleFormat(datetime.datetime.now())
            content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
            
            # Prepare the output file path so that the file downloaded 
            # can be saved 
            self.prepare_the_output_file_path(content_type)
            
            if response.status  == 404:
                print(parameters_to_add_result.get("download_url"))
                result = {"success":0,"status_code":404}
                return result 
            
            
            if "content-Length" in response.headers:
                file_size_mega_byte = math.ceil(int(response.headers.get("content-Length"))) # File size in byte (octet)
                
            # Extract the Content-Type from headers
            
            if not self.output_file_path:
                raise ValueError(f"The parameters given are wrong. {self.__class__.__name__}({self.__dict__})")
            
            # Create file folder it does not exists 
            file_folder = os.path.dirname(self.output_file_path)
            if not os.path.exists(file_folder):
                os.makedirs(file_folder)
                
            
            
            if self.is_binary_content(content_type):
                
                async with aiofile.async_open(self.output_file_path,mode = "wb") as file:
                    
                    async for chunck in response.content.iter_chunked(2 * 1014 * 1024):
                        await file.write(chunck)
                            
            else:
                
                # Read body as binary       
                content = await response.read()
                
                try:
                    content = content.decode(encoding = "utf-8")
                except:
                    pass 
                
                
                if type(content) == str:
                    async with aiofile.async_open(self.output_file_path,mode = "w", encoding = "utf-8") as file:
                        # Decode the body with the enconding 
                        await  file.write(content)
                elif type(content) == bytes:
                    async with aiofile.async_open(self.output_file_path,mode = "wb") as file:
                        await  file.write(content)
                    
            download_end_time =  general_tools.datetimeToGoogleFormat(datetime.datetime.now())
            
            result = {
                "success":1,
                "status_code":response.status,
                "download_data":{
                    "version": "0.0.1",
                    "url": self.url,
                    "other_params":parameters_to_add_result,
                    "filepath": self.output_file_path,
                    "download_begin_time":download_begin_time,
                    "download_end_time":download_end_time,
                **general_tools.get_important_information_from_request_response(response)
            
            }}
            
            return result 


    
    async def parse_sermonindex_download_intermediate_page(self,download_page_url):
        
        async with self.aiohttp_session.get(url=download_page_url) as response:
            
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
                                   f" current_page_url = {download_page_url}")
            
            
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
                   
            #print(download_page_url,comment_list)

            return {
                "download_url":download_url,
                "embed_url":embed_url,
                "comments":comment_list
            }
            
                

    


class SI_Download_ListOfVideoWork(SI_Download_Work):
    def __init__(self, name,material_type, root_folder,intermediate_folders, browse_by_type,
                 overwrite_log=False, update_log=True):
        super().__init__(name,material_type, root_folder,intermediate_folders, browse_by_type,
                         overwrite_log, update_log)
        
        
        
    def prepare_input_data(self,**kwargs):
        """
        This method take a json file content and create input data for download 
        that are put into the dict self.element_dict

        :param file_content: the content of a json file where input data will be taken 
        :param intermediate_folders: The intermediate folders from the root folder to 
        the json file 
        :param file_path: The path of the json file 
        """

        element_list = kwargs.get("file_content").get("data")
        
        if element_list:
            name = element_list[0].get("author_name")
            
        intermediate_folders = kwargs.get("intermediate_folders")
        
        local_intermediate_folders = []
        
        if intermediate_folders:
            if name in intermediate_folders:
                local_intermediate_folders = intermediate_folders[:intermediate_folders.index(name)].copy()
        
        for element in element_list:    
            url = element.get("url")  
            #print(url)
            self.element_dict[url] = {
                **{
                    "link_text":element.get("link_text"),
                    "url":url,
                    "output_folder":self.download_output_root_folder,
                },
                 
                **{"metadata": {"input_file_index":self.meta_informations["input_files_information"]\
                                                            ["input_files"].index(kwargs.get("file_path")),
                    "intermediate_folders":local_intermediate_folders,
                    }
                   },
                
                **{"download_log":{}}
            }

            #print(self.element_dict[url])

        
        
    
    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)
        #print(element)
        
        ob = SI_DownloadVideo(
            url = element.get("url"),
            output_folder = element.get('output_folder'),
            output_file_name = general_tools.replace_forbiden_char_in_text(
                general_tools.remove_consecutive_spaces(element.get("link_text"))),
            aiohttp_session= self.aiohttp_session
        )
        #print(element_value,"\n\n")
        
        input_file_index = element["metadata"]["input_file_index"]
        input_file_path = self.meta_informations["input_files_information"]\
                                                            ["input_files"][input_file_index]
                                                            
        result = await ob.download(input_file_path)
        
        
        #print(result)
        return result 
        
      

    async def is_element_data_downloaded(self,element):
        #print(element)
        ob = SI_DownloadVideo(
            url = element.get("url"),
            output_folder = element.get('output_folder'),
            output_file_name = general_tools.replace_forbiden_char_in_text(
                general_tools.remove_consecutive_spaces(element.get("link_text"))),
            aiohttp_session= self.aiohttp_session
        )
        is_downloaded = await ob.is_downloaded()
        
        result =  is_downloaded #and element.get("download_log").get("download_data") != None
        #print(element,result,"\n\n\n")
        return result 
        
