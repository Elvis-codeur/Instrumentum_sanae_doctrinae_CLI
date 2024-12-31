import math 
import os 
from Instrumentum_sanae_doctrinae.web_scraping import download

class MN_Download(download.DownloadFromUrl):
    
    def __init__(self, url, output_folder,output_file_name,aiohttp_session):
        self.output_folder = output_folder
        self.output_file_name = output_file_name
        
        super().__init__(url, "",aiohttp_session)
        
        
        
    async def download(self,separe_file_based_on_format = True):
        """
        :param separe_file_based_on_format: If true, the pdf files are saved in the subfolder PDF, the html files 
        in the subfolder HTML, etc. If false, all the files are downloaded in the same folder not matter what 
        their format is 
        """
        async with self.aiohttp_session.get(self.url,stream=True,allow_redirects=True) as response:
            if "content-Length" in response.headers:
                    file_size_mega_byte = math.ceil(int(response.headers.get("content-Length"))/10**6) # File size in MB
                
                
                # Extract the Content-Type from headers
                content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
                
                file_extension = self.get_file_extension_from_header(content_type)
                
                if separe_file_based_on_format:
                    self.output_file_path = os.path.join(self.output_folder,
                                                         file_extension[1:].upper(),
                                                         self.output_file_name + file_extension)
                                                         
                
                if self.is_binary_content(content_type)
                                                                     

        