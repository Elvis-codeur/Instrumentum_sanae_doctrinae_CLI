


from Instrumentum_sanae_doctrinae.my_tools import general_tools
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_download import SI_Download_Work, SI_DownloadFromUrl


class SI_DownloadAudio(SI_DownloadFromUrl):
    def __init__(self, url, output_folder, output_file_name,
                 aiohttp_session, separe_file_based_on_format=True):
        
        super().__init__(url, output_folder, output_file_name,
                         aiohttp_session, separe_file_based_on_format)
    
    
class SI_Download_ListOfAudioWork(SI_Download_Work):
    def __init__(self, name,material_type, root_folder, browse_by_type,
                 overwrite_log=False, update_log=True):
        super().__init__(name,material_type, root_folder, browse_by_type,
                         overwrite_log, update_log)
        
        
    
    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """

        #print(self.root_folder,self.browse_by_type)

        
        ob = SI_DownloadAudio(
            url = element.get("url"),
            output_folder = element.get('output_folder'),
            output_file_name = general_tools.replace_forbiden_char_in_text(
                general_tools.remove_consecutive_spaces(element.get("link_text"))),
            aiohttp_session= self.aiohttp_session
        )
        #print(element_value,"\n\n")
        result = await ob.download()
        print(result)
        return result 
        
      

    async def is_element_data_downloaded(self,element):
        #print(element)
        ob = SI_DownloadAudio(
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
        
