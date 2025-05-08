

import copy
import datetime
from Instrumentum_sanae_doctrinae.my_tools.scraping_using_selenium import async_connect_to_url_with_selenium, connect_to_url_with_selenium
from Instrumentum_sanae_doctrinae.web_scraping import my_errors
from Instrumentum_sanae_doctrinae.web_scraping.http_connexion import ScrapDataFromURL
import aiohttp
from bs4 import BeautifulSoup
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools



class MonergismScrapDataFromURL(ScrapDataFromURL):
    def __init__(self, metadata_root_folder, log_root_folder, url_info_list, browse_by_type, intermdiate_folders, **kwargs):
        super().__init__(metadata_root_folder, log_root_folder, url_info_list, browse_by_type, intermdiate_folders, **kwargs)
        
        
    
    async def connect_to_all_url(self,**kwargs):
        """
        Connect to an html page whose url has been given 
        """

        
        self.main_request_session = aiohttp.ClientSession()
        
        #print(self.url_informations)
        
        # I use a deepcopy here becaus the potential deletions will change
        # The size of the dict during the iteration 
        for url,value in copy.deepcopy(self.url_informations).items():
            
            
            # This value must be True by default 
            # It can be set to false if data of this url is already downloaded             
            connect_to_url = value.get('connect_to_url')
            
            #print(url_dict,connect_to_url)
            
            # Connect to the url if and only if authorised 
            if connect_to_url:
                #print(url)
                
                #timeout = aiohttp.ClientTimeout(total=15)
                #print(url_dict)
            
                async with self.main_request_session.get(url=url) as response:
                    
                    if response.status == 404:
                        raise my_errors.HTTP404Error(url)
                    elif response.status == 403:
                        html = await async_connect_to_url_with_selenium(url)
                        
                        try:
                            html = await response.text()
                        except UnicodeDecodeError:
                            raw_data = await response.read()
                            html = raw_data.decode("utf-8",errors="replace")

                        #print(response.headers)            
                        
                        self.url_informations[url]["request"] = None
                        self.url_informations[url]["html_text"] = html
                        self.url_informations[url]["request_datetime"] = _my_tools.datetimeToGoogleFormat(datetime.datetime.now()),
                        # Create a bs4 object with the html text of the last request 
                        self.url_informations[url]["bs4_object"] = BeautifulSoup(html,features="html.parser") 
            
                    else:
                        try:
                            html = await response.text()
                        except UnicodeDecodeError:
                            raw_data = await response.read()
                            html = raw_data.decode("utf-8",errors="replace")

                        #print(response.headers)            
                        
                        self.url_informations[url]["request"] = response
                        self.url_informations[url]["html_text"] = html
                        self.url_informations[url]["request_datetime"] = _my_tools.datetimeToGoogleFormat(datetime.datetime.now()),
                        # Create a bs4 object with the html text of the last request 
                        self.url_informations[url]["bs4_object"] = BeautifulSoup(html,features="html.parser") 
            else:
                # Add the url to which no connection is made to the list it belongs to 
                self.url_informations_not_connect[url] = copy.deepcopy(self.url_informations[url])
                
                # Remove it from the list of the standard url for download; 
                del self.url_informations[url]
