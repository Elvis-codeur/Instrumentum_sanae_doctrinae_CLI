
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.sermonindex_scrap_metadata import GetTopicOrScriptureOrPodcastOrChristianBooks


class GetAudioSermonChristianBookList(GetTopicOrScriptureOrPodcastOrChristianBooks):
    def __init__(self, root_folder, browse_by_type = "christian_book") -> None:
        super().__init__(root_folder,
                          url = "https://www.sermonindex.net/modules/bible_books/?view=books_list",
                         browse_by_type = browse_by_type,
                         is_text=True)
        

    def get_useful_anchor_object_list(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        """    

        container = bs4_container.find("table",
                                       attrs = {"width":"100%",
                                                "cellpadding":"2",
                                                "cellspacing":"2",
                                                "border":"0"})
        
        container = container.find("div")
        return container.find_all("a")



class GetTextSermonsChristianBook(GetTopicOrScriptureOrPodcastOrChristianBooks):
    def __init__(self, root_folder, 
                 url = "https://www.sermonindex.net/modules/bible_books/?view=books_list",
                  browse_by_type = "Christian Book", is_text= True):
        
        super().__init__(root_folder, url, browse_by_type, is_text)


    def get_useful_anchor_object_list(self,bs4_container):
        """
        :param bs4_container: a <div>,<center> or anithing that contain the anchor elements 
        """    

        container = bs4_container.find("div",
                                       attrs = {"class":"bookContentsPage"})
        return container.find_all("a")
    