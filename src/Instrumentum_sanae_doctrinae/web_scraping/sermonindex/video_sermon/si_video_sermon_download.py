


from Instrumentum_sanae_doctrinae.my_tools import general_tools
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_download import SI_Download_Work, SI_DownloadFromUrl


class SI_DownloadVideo(SI_DownloadFromUrl):
    def __init__(self, url, output_folder, output_file_name,
                 aiohttp_session, separe_file_based_on_format=True):
        
        super().__init__(url, output_folder, output_file_name,
                         aiohttp_session, separe_file_based_on_format)
    
    


class SI_Download_ListOfVideoWork(SI_Download_Work):
    def __init__(self, name,material_type, root_folder, browse_by_type,
                 overwrite_log=False, update_log=True):
        super().__init__(name,material_type, root_folder, browse_by_type,
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
            self.element_dict[element.get("url")] = {
                **{
                    "link_text":element.get("link_text"),
                    "url":element.get("download_url"),
                    "output_folder":self.download_output_root_folder,
                },
                 
                **{"metadata": {"input_file_index":self.meta_informations["input_files_information"]\
                                                            ["input_files"].index(kwargs.get("file_path")),
                    "intermediate_folders":local_intermediate_folders,
                    }
                   },
                
                **{"download_log":{}}
            }
    

        
        
    
    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)

        
        ob = SI_DownloadVideo(
            url = element.get("url"),
            output_folder = element.get('output_folder'),
            output_file_name = general_tools.replace_forbiden_char_in_text(
                general_tools.remove_consecutive_spaces(element.get("link_text"))),
            aiohttp_session= self.aiohttp_session
        )
        #print(element_value,"\n\n")
        result = await ob.download()
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
        
        result =  is_downloaded and element.get("download_log").get("download_data") != None
        #print(result,element,"\n\n\n")
        return result 
        
