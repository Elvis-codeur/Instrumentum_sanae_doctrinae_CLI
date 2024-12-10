import os 

from  ..scraping import my_constants
from ..scraping import scrap_metadata




def get_monergism_metadata_and_log_folder(root_folder):
    metadata_root_folder = os.path.join(root_folder,my_constants.MONERGISM_METADATA_ROOT_FOLDER)
    log_root_folder = os.path.join(root_folder,my_constants.MONERGISM_LOG_ROOT_FOLDER)
                           
    return metadata_root_folder,log_root_folder


class GetTopicOrAuthorOrScriptureList(scrap_metadata.GetAnyBrowseByListFromManyPages):
    """
    This class is created to get the list of all the authors, topics and scriptures  from monergism. 
    The topics and the author page has the same html structure for the presentation 
    of the authors and the topics 

    author page : https://www.monergism.com/topics
    topics page : https://www.monergism.com/authors
    scripture page : https://www.monergism.com/scripture
    """
    def __init__(self,root_folder,url,browse_by_type) -> None:
        """
        :param root_folder: The folder where the logs folder, metadata, download 
        folder will be created. It is the folder where everything will be placed. 
        If left empty,the current working directory will be used  
        :param url: The url of the web page to scrap 
        :param browse_by_type: The type of browse by used targeted. Either topics, speakers, or others
        """
        if not root_folder:
            root_folder = os.getcwd()


        metadata_root_folder,log_root_folder = get_monergism_metadata_and_log_folder(root_folder)

        super().__init__(metadata_root_folder,log_root_folder,
                          url_list = [url],
                            browse_by_type=browse_by_type)
        

    async def scrap_page_useful_links(self):
        """
        This method return the useful links of the page. 

        For example for the page of the authors of monergism 
        https://www.monergism.com/authors The useful link are the <a> element
        of authors or topics as **<a href="/search?f[0]=author:39115">H.B. Charles Jr.</a>**
        """

        

        result = []

        for url in self.url_informations:
            # Get the links (<a> </a>) which leads to the authors main page. 
            links = self.url_informations[url]["bs4_object"].find("div",{"id","region-content"}).findAll("a")#"section",{"id","block-views-36de325f9945b74b1c08af31b5376c02"}).find_all("a",{"class":None})
            links = [i for i in links if i.attrs.get("href")]
    
            authors_links = [[i] for i in links if self.useful_link_validation_function(i)]

            result.append((url,authors_links))

        return result
    
    def useful_link_validation_function(self,link):
        """
        :param link: A bs4 HTML anchor element
        Return true if the link is the link of a topic or an author
        """
        return (("/topics/" in link.attrs.get("href")) or ("=author:" in link.attrs.get("href")))
    
    

class GetScriptureList(GetTopicOrAuthorOrScriptureList):
    def __init__(self, root_folder,) -> None:
        super().__init__(root_folder,
                          "https://www.monergism.com/scripture",
                            "scripture")
        


    async def scrap_page_useful_links(self):
        
        result = []

        for url in self.url_informations:
            links_div_list = self.url_informations[url]['bs4_object'].findAll("div",{"class":"view-grouping"})
            url_links = []

            for link_div in links_div_list:

                # Take the anchor list and modify their string to correspond to the 
                # string of div containing them I do it because the anchor elements 
                # text do not correspond to leviticus, chronicles or any book in 
                # in the bible but to the type of the material (audio, book, etc)
                anchor_object_list = link_div.findAll("a")
                for anchor_object in anchor_object_list:
                    anchor_new_string = link_div.get_text().split("\n")
                    if anchor_new_string:
                        anchor_object.string = anchor_new_string[0]
                    else:
                        anchor_object.string = ""
                url_links.append(anchor_object_list)

            # Remove the duplicates
            final_url_links_url = []
            final_url_links = []
            for anchor_list in url_links:
                if anchor_list[0].get("href") not in final_url_links_url:
                    final_url_links.append(anchor_list)
            
            result.append((url,final_url_links))

        return result

class GetTopicList(GetTopicOrAuthorOrScriptureList):
    def __init__(self, root_folder) -> None:
        super().__init__(root_folder,
                          "https://www.monergism.com/topics",
                          "topic")


class GetSpeakerList(GetTopicOrAuthorOrScriptureList):
    def __init__(self, root_folder,) -> None:

        super().__init__(root_folder, 
                         "https://www.monergism.com/authors",
                         "speaker")