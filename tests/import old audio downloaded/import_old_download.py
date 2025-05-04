import asyncio
import os 
import pathlib
import shutil

from Instrumentum_sanae_doctrinae.my_tools import general_tools
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.audio_sermon.si_audio_sermon_download import SI_Download_ListOfAudioWork
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.audio_sermon.si_audio_sermon_scrap_get_list import GetAudioSermonScriptureList, GetAudioSermonTopicList
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_get_speaker_list import GetAudioSermonSpeakerList

import argparse



def get_old_log_root_folder(root_folder,browse_by):
    return os.path.join(root_folder,f"download/logs/by {browse_by}")

def get_old_log_file_path(root_folder,browse_by,name):
    return os.path.join(get_old_log_root_folder(root_folder,browse_by),f"{name}.json")


def get_name_of_all_elements(root_folder,browse_by):
    file_list = list(pathlib.Path(os.path.join(root_folder,f"download/logs/by {browse_by}")).rglob("*.json"))
    result = ["".join(os.path.basename(file).split(".")[:-1]) for file in file_list]
    return result
    

def convert_old_download_log_to_new_log(data):
    
    file_path = data.get("output_filepath").replace("\\","/")
    
    
    result = {}
    result["link_text"] = data["link_text"]
    result["url"] = data["url"]
    # It will be set later 
    #result["output_folder"] = pathlib.Path(file_path).parent.parent.as_posix()
    
    result["download_log"] = {}
    
    
    #print(file_path,os.path.exists(file_path))
    
    result["download_log"]["download_data"] = {
        "version":"0.0.1",
        "url":data["url"],
        "other_params":{},
        "filepath": file_path,
        "download_begin_time": data.get("download_log").get("time_begin"),
        "download_end_time": data.get("download_log").get("time_end"),
        "request_header":data.get("download_log").get("first_level_request_header"),
        "request_status_code": data.get("download_log").get("first_level_request_status_code"),
        "request_cookies": [],
        "request_history":[data.get("download_log").get("second_level_request_header")],
        "second_level_url": data.get("download_log").get("second_level_url"),
    }
  
    return result




class SI_ImportOldDownload(SI_Download_ListOfAudioWork):
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
                    
                    
                    old_data_converted_to_new_standard = convert_old_download_log_to_new_log(old_element)
                    
                    # La partie principale 
                    old_relative_filepath = old_data_converted_to_new_standard["download_log"]["download_data"]["filepath"]
                    
                    old_file_path = os.path.join(self.old_root_folder,old_relative_filepath)
                    
                    new_file_path = os.path.join(self.element_dict[key]["output_folder"],"MP3" + "/" + pathlib.Path(old_file_path).name)
                    
                    if os.path.exists(old_file_path):
                        # Create the folder of our new file 
                        if not os.path.exists(os.path.dirname(new_file_path)):
                            os.makedirs(os.path.dirname(new_file_path))
                        
                        shutil.copyfile(old_file_path,new_file_path)
                        
                        
                        # Créeer les données pour
                        self.log_file_content["downloaded"][key] = old_data_converted_to_new_standard
                         
                        # Je modifie certaines données du dictionnaire nouvellement crée 
                        self.log_file_content["downloaded"][key]["link_text"] = self.element_dict[key].get("link_text")
                        self.log_file_content["downloaded"][key]["metadata"] = self.element_dict[key].get("metadata")
                        self.log_file_content["downloaded"][key]["output_folder"] = self.element_dict[key].get("output_folder")
                    
                                            
                        self.log_file_content["downloaded"][key]["download_log"]["download_data"]["filepath"] = new_file_path
                        
                        # Supprimer l'élément de la liste des éléments à télécharge 
                        if key in self.log_file_content["to_download"].keys():
                            self.log_file_content["to_download"][key] 
                                    
                    break
        
                
def import_topic_audio_files():

    list_ob = GetAudioSermonTopicList(root_folder=new_root_folder,)
    topic_list = list_ob.get_list_from_local_data()

    list_len = len(topic_list)
    
    for indice,element in enumerate(topic_list):
        ob = SI_ImportOldDownload(element,"audio",new_root_folder,old_root_folder,"topic",False)
        async def f():    
            await ob.init_log_data()
            ob.import_old_log_data()
            await ob.update_downloaded_and_to_download_from_drive(True)
            ob.write_log_file()
            
        asyncio.run(f())
        print(f"{element} {indice} / {list_len}")


             
def import_scripture_audio_files():

    list_ob = GetAudioSermonScriptureList(root_folder=new_root_folder,)
    topic_list = list_ob.get_list_from_local_data()

    list_len = len(topic_list)
    
    for indice,element in enumerate(topic_list):
        ob = SI_ImportOldDownload(element,"audio",new_root_folder,old_root_folder,"scripture",False)
        async def f():    
            await ob.init_log_data()
            ob.import_old_log_data()
            await ob.update_downloaded_and_to_download_from_drive(True)
            ob.write_log_file()
            
        asyncio.run(f())
        print(f"{element} {indice} / {list_len}")




            
def import_speaker_audio_files():

    list_ob = GetAudioSermonSpeakerList(root_folder=new_root_folder,)
    topic_list = list_ob.get_list_from_local_data()

    list_len = len(topic_list)
    
    for indice,element in enumerate(topic_list):
        ob = SI_ImportOldDownload(element,"audio",new_root_folder,old_root_folder,"speaker",False)
        async def f():    
            await ob.init_log_data()
            ob.import_old_log_data()
            await ob.update_downloaded_and_to_download_from_drive(True)
            ob.write_log_file()
            
        asyncio.run(f())
        print(f"{element} {indice} / {list_len}")






def main():
    parser = argparse.ArgumentParser(description="Script multi-fonction.")
    parser.add_argument(
        "action",
        choices=["speaker", "topic", "scripture"],
        help="Action à exécuter"
    )

    args = parser.parse_args()

    if args.action == "speaker":
        import_speaker_audio_files()
    elif args.action == "topic":
        import_topic_audio_files()
    elif args.action == "scripture":
        import_scripture_audio_files()

if __name__ == "__main__":
    new_root_folder ='/media/elvis/Seagate Desktop Drive/Sanae_Doctrinae_Vault' 
    old_root_folder = "/media/elvis/Seagate Desktop Drive/Github_project_for_God/Sermon_index_scrapping"
    
    main()
                
