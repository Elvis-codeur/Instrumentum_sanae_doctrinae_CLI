


import os
from Instrumentum_sanae_doctrinae.web_scraping import my_constants, scrap_metadata
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.si_scrap_metadata import  get_sermonindex_metadata_and_log_folder


from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import si_scrap_get_speaker_list

class GetVintageImageSpeakerList(si_scrap_get_speaker_list.GetSpeakerList):
    def __init__(self, root_folder, material_type = "vintage_image", url="https://www.sermonindex.net/modules/myalbum/index.php") -> None:
        """"""
        super().__init__(root_folder, material_type, url)
        
