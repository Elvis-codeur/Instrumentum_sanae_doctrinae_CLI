import datetime 
import aiofile 
import math 
import pathlib 
import aiohttp
import asyncio 
import traceback 
from charset_normalizer import detect as detect_encoding
import os 
from Instrumentum_sanae_doctrinae.web_scraping import download
from Instrumentum_sanae_doctrinae.web_scraping import _my_tools,my_constants,http_connexion


class MN_DownloadFromUrl(download.DownloadFromUrl):
    
    def __init__(self, url, output_folder,output_file_name,aiohttp_session,separe_file_based_on_format = True):
        """
        :param output_file_name: The name of the file without its extension .html or .pdf, etc
        :param separe_file_based_on_format: If true, the pdf files are saved in the subfolder PDF, the html files 
        in the subfolder HTML, etc. If false, all the files are downloaded in the same folder not matter what 
        their format is 
        """
        self.output_folder = output_folder
        self.output_file_name = output_file_name
        self.separe_file_based_on_format = separe_file_based_on_format
        
                     
        
        super().__init__(url, "",aiohttp_session)
        
        
    def __repr__(self):
        return f"{self.__class__.__name__}({str(self.__dict__)})"
        
    
    async def is_downloaded(self):
        
        # Check if there is a file with the same name as the name given to the object
        
        files = pathlib.Path(self.output_folder).rglob("*")
        files = [file for file in files if file.is_file()]
        
        for file in files:
            file_basename = os.path.basename(file)
            if file_basename.startswith(self.output_file_name):
                #print(file_basename,self.output_file_name)
                return True 
        
        return False 
    
        """
        async with self.aiohttp_session.get(self.url,allow_redirects=True) as response:
            content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
            self.prepare_the_output_file_path(content_type)
        """ 
        #print(self.output_file_path,"----")
        #return os.path.exists(self.output_file_path)
        
    def prepare_the_output_file_path(self,content_type):
            
            file_extension = self.get_file_extension_from_content_type(content_type)
            
            if self.separe_file_based_on_format:
                self.output_file_path = os.path.join(self.output_folder,
                                                        file_extension[1:].upper(),
                                                        self.output_file_name + file_extension)
            else:
                self.output_file_path = os.path.join(self.output_folder,
                                                        self.output_file_name + file_extension)
    
    async def download(self):
        try:
            result = await self.download_internal_version()
            return result
        except Exception as e:
            result = {"success":0,"error":"" .join(traceback.format_exception(e))}
            return result 
            
    async def download_internal_version(self):
        """
       
        """
        #print("Elvis")
        # The size of the file in Mb
        file_size_mega_byte = 0 
        
        # Chunck size 
        file_chunck_size_MB = 4*1024*1024 #Mega Byte # 
        
        result = {}
        download_begin_time = None 
        
        async with self.aiohttp_session.get(self.url,allow_redirects=True) as response:
            download_begin_time =  _my_tools.datetimeToGoogleFormat(datetime.datetime.now())
            content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
            
            # Prepare the output file path so that the file downloaded 
            # can be saved 
            self.prepare_the_output_file_path(content_type)
            
            if response.status  == 404:
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
                    
                    # Big file 
                    if file_size_mega_byte > file_chunck_size_MB:
                        async for chunck in response.content.iter_chunked(file_chunck_size_MB):
                            await file.write(chunck)
                            
                    # Small file 
                    else:
                        content = await response.read()
                        await file.write(content)
                
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
                    
               
                
                
                    
            download_end_time =  _my_tools.datetimeToGoogleFormat(datetime.datetime.now())
            
            result = {
                "success":1,
                "status_code":response.status,
                "download_data":{
                    "version": "0.0.1",
                    "url": self.url,
                    "filepath": self.output_file_path,
                    "download_begin_time":download_begin_time,
                    "download_end_time":download_end_time,
                **_my_tools.get_important_information_from_request_response(response)
            
            }}
            
            return result 
                    
            
                
                                                                    

class MN_Download_Work(http_connexion.ParallelHttpConnexionWithLogManagement):
    def __init__(self,name,root_folder,browse_by_type, overwrite_log=False, update_log=True):
        
        # The name of the author, topic, scripture, etc 
        self.name = name 
        
        root_folder = _my_tools.process_path_according_to_cwd(root_folder)

        log_filepath = os.path.join(root_folder,
                                    my_constants.LOGS_ROOT_FOLDER,
                                    my_constants.MONERGISM_NAME,
                                    my_constants.ELABORATED_DATA_FOLDER,
                                    browse_by_type, 
                                    my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_DOWNLOAD_FOLDER,
                                    self.name,
                                    my_constants.get_default_json_filename(0)
                                    )
        
        input_root_folder = os.path.join(root_folder,
                                         my_constants.METADATA_ROOT_FOLDER,
                                         my_constants.MONERGISM_NAME,
                                         my_constants.ELABORATED_DATA_FOLDER,
                                         browse_by_type, 
                                         my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,
                                         self.name
                                         )
        
        download_output_root_folder = os.path.join(root_folder,
                                         my_constants.DOWNLOAD_ROOT_FOLDER,
                                         my_constants.MONERGISM_NAME,
                                         browse_by_type, 
                                         self.name,
                                         my_constants.DOWNLOAD_ROOT_FOLDER,                             
                                         )
        
        
        input_files = self.get_input_json_files(input_root_folder)
        
        input_data = {}
        
        # Prepare the json files as input data 
        for filepath in input_files:
            file_content = _my_tools.read_json(filepath)
            input_data[str(filepath)] = file_content
            
        
        self.browse_by_type = browse_by_type
        self.root_folder = root_folder
        self.download_output_root_folder = download_output_root_folder
        
        
        
        super().__init__(log_filepath = log_filepath,
                         input_root_folder= input_root_folder,
                         input_data=input_data,
                         overwrite_log = overwrite_log,
                         update_log = update_log)
        
       
        self.aiohttp_session = None 


    def get_input_json_files(self,input_root_folder):
        """
        :param input_root_folder: The folders from wich the json files will be searched out 
        """
        # List of folder in which name  :data:`my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_LISTING_FOLDER`
        input_json_files = []

        # The folder where the works of the author are 
        folder_path = os.path.join(input_root_folder,my_constants.WORK_INFORMATION_ROOT_FOLDER)
                
        # List to store paths to all JSON files
        json_files = [i for i in pathlib.Path(folder_path).rglob("*.json") if i.is_file()]

        #print("kaka",json_files,input_root_folder)
        
        for file in json_files:
            filename = file.as_posix()
            if my_constants.WORK_INFORMATION_ROOT_FOLDER in filename:
                input_json_files.append(file)
                

        #print(input_json_files)
        return input_json_files
    
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
        
       
        
        for element in element_list:        
            self.element_dict[element.get("url")] = {
                **{
                    "link_text":element.get("link_text"),
                    "url":element.get("url"),
                    "output_folder":self.download_output_root_folder,
                } 
                ,
                **{"download_log":{
                    "input_file_index":self.meta_informations["input_files_information"]\
                                                            ["input_files"].index(kwargs.get("file_path")),
                    "intermediate_folders":kwargs.get("intermediate_folders")[2:]}
                    }
            }
    
        #print(self.element_dict)
        
        
    async def init_aiohttp_session(self):
        if self.aiohttp_session == None:
            self.aiohttp_session = aiohttp.ClientSession()
            
    async def close_aiohttp_session(self):
        if self.aiohttp_session != None:
            await self.aiohttp_session.close()
    

    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)

        #print(element.get("data"))
        
        ob = MN_DownloadFromUrl(
            url = element.get("url"),
            output_folder = element.get('output_folder'),
            output_file_name = _my_tools.replace_forbiden_char_in_text(
                _my_tools.remove_consecutive_spaces(element.get("link_text"))),
            aiohttp_session= self.aiohttp_session
        )
        #print(element_value,"\n\n")
        result = await ob.download()
        return result 
        
      

    async def is_element_data_downloaded(self,element):
        #print(element)
        ob = MN_DownloadFromUrl(
            url = element.get("url"),
            output_folder = element.get('output_folder'),
            output_file_name = _my_tools.replace_forbiden_char_in_text(
                _my_tools.remove_consecutive_spaces(element.get("link_text"))),
            aiohttp_session= self.aiohttp_session
        )
        is_downloaded = await ob.is_downloaded()
        
        result =  is_downloaded and element.get("download_log").get("download_data") != None
        #print(result,element,"\n\n\n")
        return result 
        
    
    async def download(self,download_batch_size):
        """
        Download the content of the input files concurrently 
        by a batch of size :data:`download_batch` 
        """
        result = []

        # Init the log informations 
        await self.init_log_data()
        
        # Update before the begining of downloads
        await self.update_log_data()
         
        element_to_download = list(self.log_file_content["to_download"].values())
        
       
        # Split it by size download_batch_size to download
        #  them in parralel 
        element_to_download_splitted = _my_tools.sample_list(element_to_download,
                                                      download_batch_size)

        
        # This is used to show a progress bar 
        for download_batch in element_to_download_splitted:
            tasks = [self.download_element_data(element) for element in download_batch]
            result_list = await asyncio.gather(*tasks)
            
            for result,element in zip(result_list,download_batch):
                succes = result.get("success")
                status_code = result.get("status_code")
                url = element.get("url")
                
                element_for_log =  element.copy()
                
                if succes:
                    # Update the download log informations 
                
                    #print(element,element_for_log["download_log"],result.get("download_data"),"\n\n\n")
                    
                    element_for_log["download_log"]["download_data"] = result.get("download_data")
                    
                    self.log_file_content["downloaded"][url] = element_for_log
                    
                    # Delete the element from the to download list 
                    if url in self.log_file_content["to_download"]:
                        del self.log_file_content["to_download"][url]
                    
                    await self.update_log_data()
                    
                else:
                    
                    # If the error is caused by a 404 error
                    if status_code == 404:
                        self.log_file_content["not_found_404"][url] = element_for_log

                        if url in self.log_file_content["to_download"]:
                            #print(url,404,"\n\n\n")
                            del self.log_file_content["to_download"][url]
                    else:
                        element_for_log["download_log"]["error_data"] = result.get("error")
                        self.log_file_content["to_download"][url] = element_for_log
                        # Delete the element from the to download list 
                        
            await self.update_log_data()
            
    async def update_to_download_list(self):
        # A list of the url of of the link object which have been already downloaded 
        downloaded_link_url_list = [i for i in self.log_file_content.get("downloaded")] if self.log_file_content.get("downloaded") else []
        to_downlaod_link_url_list = [i for i in self.log_file_content.get("to_download")] if self.log_file_content.get("to_download") else []

        # We take "element_list" variable because it contains the link of the author, scripture or topic
        
        for url in self.element_dict:
            if url not in downloaded_link_url_list: # If it is not already downloaded 
                if url not in to_downlaod_link_url_list: # It is not in the link prepared to for download. 
                    #print("\n\n\n\n\n",self.log_file_content["to_download"].keys(),"\n\n\n",self.element_dict.keys(),"\n\n\n\n",url,element_name)
                    
                    self.log_file_content["to_download"][url] = self.element_dict[url]
                else: # If the element is already in the "to_download" list, there is no need to add it 
                    pass 
            else: # If the link is already downlaed. There is no need of modification of anything 
                pass 