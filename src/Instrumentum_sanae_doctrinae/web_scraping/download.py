"""
This module is meant to offer the base classes for the download of works(pdf, mp3, etc)
"""
import os 
import math 
import traceback
import aiofile 
import datetime
import asyncio


from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools
from Instrumentum_sanae_doctrinae.web_scraping import http_connexion 


class DownloadFromUrl():
    def __init__(self,url,output_file_path,aiohttp_session):
        self.url = url 
        self.output_file_path = output_file_path
        self.aiohttp_session = aiohttp_session
        
    
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
                    
                    async for chunck in response.content.iter_chunked(2 * 1024 * 1024):
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
                    
            download_end_time =  _my_tools.datetimeToGoogleFormat(datetime.datetime.now())
            
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
                **_my_tools.get_important_information_from_request_response(response)
            
            }}
            
            return result 

    
    
    def get_file_extension_from_content_type(self,content_type):
        """
        Get file extension based on the Content-Type in aiohttp  headers content type.

        Args:
            headers (dict): The headers dictionary from an aiohttp response.

        Returns:
            str: File extension (e.g., '.html', '.xml', '.txt', '.pdf').
        """
        # Mapping of content types to file extensions
        content_type_to_extension = {
            "text/html": ".html",
            "application/json": ".json",
            "text/plain": ".txt",
            "application/xml": ".xml",
            "text/xml": ".xml",
            "application/pdf": ".pdf",
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "application/javascript": ".js",
            "text/javascript": ".js",
            "text/css": ".css",
            "application/zip": ".zip",
            "application/x-tar": ".tar",
            "application/x-7z-compressed": ".7z",
            "application/vnd.rar": ".rar",
            "application/octet-stream": ".bin",
            "audio/mpeg": ".mp3",
            "audio/mp3":".mp3",
            "audio/ogg": ".ogg",
            "audio/wav": ".wav",
            "audio/flac": ".flac",
            "video/mp4": ".mp4",
            "video/webm": ".webm",
            "video/x-msvideo": ".avi",
            "application/vnd.ms-excel": ".xls",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
            "application/msword": ".doc",
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
            'application/vnd.ms-powerpoint': '.ppt',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
            'application/rtf': '.rtf',
            'application/x-shockwave-flash': '.flash',
            
            'audio/x-mp3': '.mp3',
            'audio/x-wav': '.wav', 
            'audio/x-aac': '.aac',
            'audio/x-flac': '.flac',
            'audio/x-ogg': '.ogg',
            'audio/x-midi': '.midi',
            'audio/x-ms-wma': '.wma',
            'audio/x-matroska': '.mka',
            
            
            'video/x-mp4': '.mp4',
            'video/x-msvideo': '.avi',
            'video/x-ms-wmv': '.wmv',
            'video/quicktime': '.mov',
            'video/x-flv': '.flv',
            'video/x-matroska': '.mkv',
            'video/x-mpeg': '.mpeg',
            'video/x-webm': '.webm',
            'video/x-ogv': '.ogv',
            
            'image/x-bmp': '.bmp',
            'image/x-tga': '.tga',
            'image/x-pcx': '.pcx',
            'image/x-icon': '.ico',
            'image/x-tiff': '.tiff',
            'image/x-webp': '.webp',
            'application/x-pdf': '.pdf',
            'application/x-msword': '.doc',
            'application/x-docx': '.docx',
            'application/x-excel': '.xls',
            'application/x-xlsx': '.xlsx',
            'application/x-powerpoint': '.ppt', 
            'application/x-pptx': '.pptx',
            'application/x-odt': '.odt', 
            'application/x-ods': '.ods',
            
            'text/x-html': '.html',
            'text/x-css': '.css', 
            'application/x-javascript': '.js',
            'application/x-json': '.json', 
            'application/x-xml': '.xml', 
            'text/x-csv': '.csv', 
            'application/x-zip-compressed': '.zip',
            'application/x-rar-compressed': '.rar', 
            'application/x-tar': '.tar', 
            'application/x-gzip': '.gz', 
            'application/x-7z-compressed': '.7z', 
            'application/x-font-ttf': '.ttf', 
            'application/x-font-otf': '.otf', 
            'application/x-font-woff': '.woff', 
            'application/x-font-woff2': '.woff2', 
            'application/x-msdownload': '.exe', 
            'application/x-msdos-program': '.dll', 
            'application/x-msdos-batch': '.bat', 
            'application/x-shellscript': '.sh', 
            'application/vnd.rn-realmedia': '.realmedia'

            }

        # Return the corresponding file extension or a default
        return content_type_to_extension.get(content_type, ".bin")  # Default to .bin for unknown types

    
    def is_binary_content(self,content_type):
        """
        Determine if a content type is binary or text-based.

        Args:
            content_type (str): The content type from a response header.

        Returns:
            bool: True if binary, False if text-based.
        """
        binary_content_types = [
            "application/octet-stream",
            "application/pdf",
            "application/zip",
            "application/x-tar",
            "application/x-7z-compressed",
            "application/vnd.rar",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "application/x-shockwave-flash",
            "image/png",
            "image/jpeg",
            "image/gif",
            "image/webp",
            "image/bmp",
            "image/x-icon",
            "audio/mpeg",
            "audio/ogg",
            "audio/wav",
            "audio/flac",
            "video/mp4",
            "video/webm",
            "video/x-msvideo",
            "application/vnd.apple.mpegurl",
            "application/x-mpegURL",
            "application/x-bittorrent",
            "font/woff",
            "font/woff2",
            "font/ttf",
            "font/otf",
        ]

        return content_type.lower() in binary_content_types
    
    
class DownloadWork(http_connexion.ParallelHttpConnexionWithLogManagement):
    def __init__(self,name,root_folder,browse_by_type, overwrite_log=False, update_log=True):
        
        # The name of the author, topic, scripture, etc 
        self.name = name
        self.browse_by_type = browse_by_type
        self.root_folder = root_folder
        
        root_folder = _my_tools.process_path_according_to_cwd(root_folder)
        
        
        # Get the path of log file, input file and download output folder 
        file_path_dict = self.prepare_log_metadata_input_files_path(root_folder)
        
        log_filepath = file_path_dict.get("log_filepath")
        input_root_folder = file_path_dict.get("input_root_folder")
        download_output_root_folder = file_path_dict.get("download_output_root_folder")
        
        
        
        self.download_output_root_folder = download_output_root_folder
        
        
        
        input_files = self.get_input_json_files(input_root_folder)
        #print(input_files)
        input_data = {}
        
        # Prepare the json files as input data 
        for filepath in input_files:
            try:
                file_content = _my_tools.read_json(filepath)
            except Exception as e :
                print(filepath)
                raise e 
            
            
            input_data[str(filepath)] = file_content
            
        super().__init__(log_filepath = log_filepath,
                         input_root_folder= input_root_folder,
                         input_data=input_data,
                         overwrite_log = overwrite_log)
        
       
        self.aiohttp_session = None 

        
    
    
    
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
        
        #print("len(element_to_download) = ",len(element_to_download))
       
        # Split it by size download_batch_size to download
        #  them in parralel 
        element_to_download_splitted = _my_tools.sample_list(element_to_download,
                                                      download_batch_size)

        print("Download to Begin",end=" ")
        await self.print_download_informations()

        # This is used to show a progress bar 
        for download_batch in element_to_download_splitted:
            tasks = [self.download_element_data(element) for element in download_batch]
            result_list = await asyncio.gather(*tasks)
            
            #await self.update_downloaded_and_to_download_from_download_result(result_list)
            
            
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
                    
                    # I comment this because it is too costly in time especially when there is hundreds 
                    # It is more constly on HDD drives 
                    #await self.update_log_data()
                    
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
                        
                        if url in self.log_file_content["to_download"]:
                            #print(url,404,"\n\n\n")
                            del self.log_file_content["to_download"][url]
                        
            await self.update_log_data()
            await self.print_download_informations()
            
            
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