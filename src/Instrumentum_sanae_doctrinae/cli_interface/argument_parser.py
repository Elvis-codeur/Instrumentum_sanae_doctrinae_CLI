import asyncio
import os
import click
from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_scrap_general_information, mn_scrap_get_list
from Instrumentum_sanae_doctrinae.web_scraping.my_constants import SCRIPTURE_NAME, SPEAKER_NAME, TOPIC_NAME


"""
    The different possible values are :
-scrap_list :  to get the list of all the authors, topics and scriptures.
    An example of author is John Calvin (https://www.monergism.com/search?f[0]=author:34198).
    An example of topic is Abraham (https://www.monergism.com/topics/abraham)
    An example of scripture is Matthew 
-scrap_general_information :
    
"""


#root_folder = os.path.join(os.getcwd(),'test_folder')

#print(root_folder)

def monergism_scrap_list(root_folder):
    # Get the list of the topics 
    ob = mn_scrap_get_list.GetTopicList(root_folder)
    asyncio.run(ob.scrap_and_write())
    
    # Get the list of speakers
    ob = mn_scrap_get_list.GetSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())
    
    # Get the list of the scriptures 
    ob = mn_scrap_get_list.GetScriptureList(root_folder)
    asyncio.run(ob.scrap_and_write())
    
    
    
def monegism_scrap_general_information(root_folder,browse_by_type,
                                       download_batch_size,
                                       overwrite_log):
    """_summary_

    Args:
        root_folder (_type_): The root folder where the download and metadata, logs data are stored 
        browse_by_type (_type_): the browse by type (either scripture, topic or speaker)
        subject (_type_): optionnal. 
    """
    print(root_folder,browse_by_type,overwrite_log)
    if browse_by_type in [SPEAKER_NAME,SCRIPTURE_NAME,TOPIC_NAME]:
        
        ob = mn_scrap_general_information.MonergismScrapGeneralInformation_ALL(
            root_folder = root_folder,
            browse_by_type = browse_by_type,
            overwrite_log = overwrite_log
        )
        print(ob.__dict__)
        asyncio.run(ob.print_download_informations(True))
        asyncio.run(ob.download(download_batch_size=download_batch_size))
        
        
    else:
        a = 0

@click.group()
def cli():
    pass 


@cli.command(name = "monergism",help = """Interact with monergism.com""")
@click.argument("action",required = True)
@click.argument("browse_by_type",required = False)
@click.argument("output_folder",required = True)
@click.option('-u', '--overwrite-log',"overwrite_log",
              default = False,required =  False)
@click.option("-bs","--download_batch_size","download_batch_size",
              default = 10,type = int,required = False)

def configure_monergism_arguments(action,output_folder,browse_by_type,
                                  overwrite_log,download_batch_size):
    
    if "=" in output_folder:
        output_folder = output_folder.split("=")[1]
    if action == "scrap_list":
        a = 0
        #monergism_scrap_list(output_folder)
    elif action == "scrap_general_info":
        if browse_by_type:
            monegism_scrap_general_information(root_folder = output_folder,
                                           browse_by_type=browse_by_type,
                                           download_batch_size = download_batch_size,
                                           overwrite_log = overwrite_log)
        else:
            raise ValueError("The argument <browse_by_type> must be given if the action parameter is <scrap_general_info>")
        
    
   



        

if __name__ == "__main__":
    cli()
    