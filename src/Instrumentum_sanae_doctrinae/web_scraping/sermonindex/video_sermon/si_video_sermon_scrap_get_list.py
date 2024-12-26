
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import si_scrap_get_speaker_list


class GetVideoSermonSpeakerList(si_scrap_get_speaker_list.GetSpeakerList):
    def __init__(self, root_folder, material_type = "video", url="https://www.sermonindex.net/modules/myvideo/") -> None:
        """"""
        super().__init__(root_folder, material_type, url)