"""
This module is created for the scrapping of metadata from https://www.monergism.com/


"""

import os 
import re
import urllib
import urllib.parse
from urllib.parse import urlparse, parse_qs


from ..scraping import scrap_metadata
from ..scraping import my_constants
from ..scraping import _my_tools



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
        

    def scrap_page_useful_links(self):
        """
        This method return the useful links of the page. 

        For example for the page of the authors of monergism 
        https://www.monergism.com/authors The useful link are the <a> element
        of authors or topics as **<a href="/search?f[0]=author:39115">H.B. Charles Jr.</a>**
        """

        self.connect_to_url()

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
        


    def scrap_page_useful_links(self):
        self.connect_to_url()

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


    

class MonergismScrapAuthorTopicScripturePage(scrap_metadata.ScrapAuthorTopicScripturePage):
    def __init__(self, name,root_folder,url, browse_by_type) -> None:
        
        metadata_root_folder,log_root_folder = get_monergism_metadata_and_log_folder(root_folder)
        
        super().__init__(name, metadata_root_folder, log_root_folder,[url], browse_by_type,None)

    def scrap_url_pages(self):
        """
        
        """
        self.connect_to_url()
    


class MonergismScrapAuthorTopicScriptureMainPage(MonergismScrapAuthorTopicScripturePage):
    def __init__(self, name, root_folder, url, browse_by_type) -> None:
        super().__init__(name, root_folder, url, browse_by_type)


    def scrap_url_pages(self):
        """
        
        """
        super().scrap_url_pages()

        def parse_filter_by_ul(bs4_soup,css_selector,url):
            result = []

            filter_by_ul = bs4_soup.find("ul",class_= re.compile(css_selector))

            if not filter_by_ul:
                return []

            filter_by_lis = filter_by_ul.find_all("li")                       
                                        
            for li in filter_by_lis:
                link = li.find("a")
                link_text = link.get_text()

                topic_element_number = re.findall(r'\((\d+)\)',link_text)

                topic_element_number = int(topic_element_number[0]) if topic_element_number else None
                result.append({
                    "url":urllib.parse.urljoin(url,link.get("href")),
                    "link_text": link_text.split("(")[0].strip(),
                    "number":topic_element_number
                })   
            return result    


        def get_other_pages(old_url_list,soup):
            
            pages_ul = soup.find(lambda tag :tag.name == "ul" and 
                                            tag.has_attr("class") and 
                                            'pager' in tag['class'] and
                                                  'clearfix' in tag['class']
                                            )
            next_page_li_list = pages_ul.find_all("li")

            new_url_list = []

            for next_page_li in next_page_li_list:
                if next_page_li:
                    next_page_anchor = next_page_li.find("a")
                    if next_page_anchor:
                        next_page_url = urllib.parse.urljoin(url,
                                                            next_page_anchor.get("href"))
                        new_url_list.append(next_page_url)

            for new_url in new_url_list:
                if not new_url in old_url_list:
                    old_url_list.append(new_url)
            
            # This li element exists only on the last page of 
            # an author, topic, scripture, etc
            last_page_li = soup.find(lambda tag: tag.name == "li" and 
                                                tag.has_attr('class') and 
                                                'pager-current' in tag['class'] and
                                                  'last' in tag['class'])
            if last_page_li:
                return []

            return new_url_list





        final_result = []

        for url in self.url_informations:
            
            soup = self.url_informations[url].get("bs4_object")

            # Filter by topic
            filter_by_topic_data = parse_filter_by_ul(soup,"facetapi-facetapi-links*.facetapi-facet-field-link-topic",url)
            
            # Filter by format
            filter_by_format_data = parse_filter_by_ul(soup,"facetapi-facetapi-links*.facetapi-facet-field-link-format",url)
            
            # Filter by genre
            filter_by_genre_data = parse_filter_by_ul(soup,"facetapi-facetapi-links*.facetapi-facet-field-link-genres",url)
            
            # Filter by web site 
            filter_by_web_site_data = parse_filter_by_ul(soup,"facetapi-facetapi-links*.facetapi-facet-field-link-website",url)
            
            # Filter by author 
            filter_by_author_data = parse_filter_by_ul(soup,"facetapi-facetapi-links*.facetapi-facet-field-link-authors",url)

            pages_list = []
            next_page_url = get_other_pages(pages_list,soup)

            if next_page_url:
               pages_list += next_page_url

               while(next_page_url):
                   soup = _my_tools.get_bs4soup_from_url(next_page_url[-1])
                   next_page_url = get_other_pages(pages_list,soup)
                   pages_list += next_page_url
            
            pages_list = list(set(pages_list))

            
            
            pages_list = sorted(pages_list,
                                key= lambda url: int(parse_qs(urlparse(url).query).get("page",[0])[0]))

                    
            result = {
                "pages":pages_list,
                "filter_by_topic": filter_by_topic_data,
                "filter_by_format":filter_by_format_data,
                "filter_by_genre":filter_by_genre_data,
                "filter_by_web_site":filter_by_web_site_data,
                "filter_by_author":filter_by_author_data,
            }


            final_result.append(result)




        return final_result 
