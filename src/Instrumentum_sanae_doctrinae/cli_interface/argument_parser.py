import asyncio
import os
from Instrumentum_sanae_doctrinae.cli_interface.web_scraping.monergism_command_executer import *
from Instrumentum_sanae_doctrinae.cli_interface.web_scraping.sermonindex_command_executer import sermonindex_scrap_general_information_command, sermonindex_scrap_list_command, sermonindex_scrap_work_command,sermonindex_download_command
import click
from Instrumentum_sanae_doctrinae.web_scraping.my_constants import SCRIPTURE_NAME, SPEAKER_NAME, TOPIC_NAME


"""
    The different possible values are :
-scrap_list :  to get the list of all the authors, topics and scriptures.
    An example of author is John Calvin (https://www.monergism.com/search?f[0]=author:34198).
    An example of topic is Abraham (https://www.monergism.com/topics/abraham)
    An example of scripture is Matthew 
-scrap_general_information :
    
"""


# The general group. It is the basis group 
@click.group()
def entry_point():
    pass 





    
 
# The group for monergism commands
@entry_point.group(name = "monergism")
def monergism_group():
    pass 


# The group for sermonindex commands
@entry_point.group(name = "sermonindex")
def sermon_index_group():
    pass 


# Add command for monergism
monergism_group.add_command(monergism_scrap_list_command,name="scrap_list")
monergism_group.add_command(monergism_scrap_general_information_command,name="scrap_general_information")
monergism_group.add_command(monergism_scrap_work_command,name="scrap_work")



# Add command for sermoinedex 
sermon_index_group.add_command(sermonindex_scrap_list_command,name = "scrap_list")
sermon_index_group.add_command(sermonindex_scrap_general_information_command,name = "scrap_general_information")
sermon_index_group.add_command(sermonindex_scrap_work_command,name = "scrap_work")
sermon_index_group.add_command(sermonindex_download_command,name = "download")

if __name__ == "__main__":
    entry_point()
    