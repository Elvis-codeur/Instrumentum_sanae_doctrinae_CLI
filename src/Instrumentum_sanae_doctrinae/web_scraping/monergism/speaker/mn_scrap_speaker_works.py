import json
import os 
import pathlib
import re

from Instrumentum_sanae_doctrinae.web_scraping import http_connexion, my_constants
from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_scrap_metadata
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools
from Instrumentum_sanae_doctrinae.web_scraping.monergism.mn_scrap_work_base import MN_ScrapSpeakerTopicScriptureWork_All




class MN_SpeakerWork_All(MN_ScrapSpeakerTopicScriptureWork_All):
    def __init__(self, root_folder, browse_by_type, overwrite_log=False, intermdiate_folders=None):
        super().__init__(root_folder, browse_by_type, overwrite_log, intermdiate_folders)

