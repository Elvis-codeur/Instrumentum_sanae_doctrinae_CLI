import os

from Instrumentum_sanae_doctrinae.web_scraping import my_constants


def get_monergism_metadata_and_log_folder(root_folder):
    metadata_root_folder = os.path.join(root_folder,my_constants.MONERGISM_METADATA_ROOT_FOLDER)
    log_root_folder = os.path.join(root_folder,my_constants.MONERGISM_LOG_ROOT_FOLDER)
                           
    return metadata_root_folder,log_root_folder


def prepare_intermdiate_folders(intermdiate_folders,browse_by_type,name,information_type_root_folder):
    if intermdiate_folders:
        intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER,]\
                                + [name,information_type_root_folder] + intermdiate_folders 
        return intermdiate_folders
    else:
        intermdiate_folders = [browse_by_type,my_constants.SPEAKER_TOPIC_OR_SCRIPTURE_WORK_FOLDER
                                ,name,information_type_root_folder]
        return intermdiate_folders