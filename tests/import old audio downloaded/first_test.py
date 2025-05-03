import os 
import pathlib
from Instrumentum_sanae_doctrinae.my_tools import general_tools

if __name__ == "__main__":
    root_folder = "/media/elvis/Seagate Desktop Drive/Github_project_for_God/Sermon_index_scrapping"
    
    topic_list = get_name_of_all_elements(root_folder,"topic")
    
    speaker_log = general_tools.read_json(get_old_log_file_path(root_folder,"topic","1 Corinthians"))
    
    
    data = speaker_log["downloaded"][0]
    new_version_data = convert_old_topic_download_log_to_new_log(data)
    print(new_version_data)
    
    
