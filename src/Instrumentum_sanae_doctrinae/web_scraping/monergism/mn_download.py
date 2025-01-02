import datetime 
import aiofile 
import math 
import pathlib 
import aiohttp
import asyncio 
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
        
        async with self.aiohttp_session.get(self.url,allow_redirects=True) as response:
            content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
            self.prepare_the_output_file_path(content_type)
            
        #print(self.output_file_path,"----")
        return os.path.exists(self.output_file_path)
        
    def prepare_the_output_file_path(self,content_type):
            
            file_extension = self.get_file_extension_from_content_type(content_type)
            
            if self.separe_file_based_on_format:
                self.output_file_path = os.path.join(self.output_folder,
                                                        file_extension[1:].upper(),
                                                        self.output_file_name + file_extension)
            else:
                self.output_file_path = os.path.join(self.output_folder,
                                                        self.output_file_name + file_extension)
            
    async def download(self,):
        """
       
        """
        #print("Elvis")
        # The size of the file in Mb
        file_size_mega_byte = 0 
        
        # Chunck size 
        file_chunck_size_MB = 4*1024*1024 #Mega Byte # 
        
        result = {}
        request_datetime = None 
        
        async with self.aiohttp_session.get(self.url,allow_redirects=True) as response:
            request_datetime =  _my_tools.datetimeToGoogleFormat(datetime.datetime.now())
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
                content = await response.text()
                
                async with aiofile.async_open(self.output_file_path,mode = "w", encoding = "utf-8") as file:
                    await  file.write(content)
                    
                    
            result = {
                "success":1,
                "status_code":response.status,
                "download_data":{
                    "version": "0.0.1",
                    "url": self.url,
                    "filepath": self.output_file_path,
                    "request_datetime":request_datetime,
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
            self.element_dict[element.get("url")] =  {element.get("url"):None}
            
            self.element_dict[element.get("url")][element.get("url")] = {
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
        
        element_value =  list(element.values())[0]
        
        ob = MN_DownloadFromUrl(
            url = element_value.get("url"),
            output_folder = element_value.get('output_folder'),
            output_file_name = _my_tools.replace_forbiden_char_in_text(
                _my_tools.remove_consecutive_spaces(element_value.get("link_text"))),
            aiohttp_session= self.aiohttp_session
        )
        #print(element_value,"\n\n")
        result = await ob.download()
        return result 
        
        
        #print(element.get("data").get("name"),element.get("download_log").get("intermediate_folders"))
        
        

    def is_element_data_downloaded(self,element):
        
        element_value =  list(element.values())[0]
        
        ob = MN_DownloadFromUrl(
            url = element_value.get("url"),
            output_folder = element_value.get('output_folder'),
            output_file_name = _my_tools.replace_forbiden_char_in_text(
                _my_tools.remove_consecutive_spaces(element_value.get("link_text"))),
            aiohttp_session= self.aiohttp_session
        )
         
        return ob.is_downloaded()
    