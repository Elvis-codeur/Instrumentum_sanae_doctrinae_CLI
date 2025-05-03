import asyncio
import os 
import pathlib

from Instrumentum_sanae_doctrinae.my_tools import general_tools
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_download import SI_Download_Work


def get_old_log_root_folder(root_folder,browse_by):
    return os.path.join(root_folder,f"download/logs/by {browse_by}")

def get_old_log_file_path(root_folder,browse_by,name):
    return os.path.join(get_old_log_root_folder(root_folder,browse_by),f"{name}.json")


def get_name_of_all_elements(root_folder,browse_by):
    file_list = list(pathlib.Path(os.path.join(root_folder,f"download/logs/by {browse_by}")).rglob("*.json"))
    result = ["".join(os.path.basename(file).split(".")[:-1]) for file in file_list]
    return result
    

def convert_old_topic_download_log_to_new_log(data,old_root_folder):
    result = {}
    result["link_text"] = data["link_text"]
    result["url"] = data["url"]
    result["output_folder"] = pathlib.Path(data["output_filepath"]).as_posix()
    
    result["download_log"] = {}
    
    #print(os.path.join(old_root_folder,data.get("output_filepath")))
    
    result["download_log"]["download_data"] = {
        "version":"0.0.1",
        "url":data["url"],
        "other_params":{},
        "filepath": os.path.join(old_root_folder,pathlib.Path(data.get("output_filepath")).as_posix()),
        "download_begin_time": data.get("download_log").get("time_begin"),
        "download_end_time": data.get("download_log").get("time_end"),
        "request_header":data.get("download_log").get("first_level_request_header"),
        "request_status_code": data.get("download_log").get("first_level_request_status_code"),
        "request_cookies": [],
        "request_history":[data.get("download_log").get("second_level_request_header")],
        "second_level_url": data.get("download_log").get("second_level_url"),
    }
  
    return result



class SI_ImportOldDownload(SI_Download_Work):
    def __init__(self, name,material_type, new_root_folder,old_root_folder, browse_by_type,
                 overwrite_log=False, update_log=True):
        super().__init__(name,material_type, new_root_folder, browse_by_type,
                         overwrite_log, update_log)
        
        self.old_root_folder = old_root_folder
        
        self.old_log_filepath = get_old_log_file_path(old_root_folder,self.browse_by_type,self.name)
        
        if not os.path.exists(self.old_log_filepath):
            raise ValueError(f"Le fichier de l'ancien log {self.old_log_filepath} n'existe pas")
        
        self.old_log_filecontent = general_tools.read_json(self.old_log_filepath)
        
    def import_old_log_data(self):
        
        for key in self.element_dict.keys():
            for old_element in self.old_log_filecontent["downloaded"]:
                if old_element.get("url") == key:
                    self.log_file_content["downloaded"][key] = convert_old_topic_download_log_to_new_log(old_element,self.old_root_folder)
                    
                    # Je modifie certaines données du dictionnaire nouvellement crée 
                    self.log_file_content["downloaded"][key]["link_text"] = self.element_dict[key].get("link_text")
                    self.log_file_content["downloaded"][key]["metadata"] = self.element_dict[key].get("metadata") 
                    
                    break
        
                
        
        
        
        
        
        
if __name__ =="__main__":
    new_root_folder ='/media/elvis/Seagate Desktop Drive/Sanae_Doctrinae_Vault' 
    old_root_folder = "/media/elvis/Seagate Desktop Drive/Github_project_for_God/Sermon_index_scrapping"
    
    
    ob = SI_ImportOldDownload("1 Corinthians","audio",new_root_folder,old_root_folder,"topic",False)
    
    async def f():    
        await ob.init_log_data()
        ob.import_old_log_data()
        ob.write_log_file()
        
    
    asyncio.run(f())
            
