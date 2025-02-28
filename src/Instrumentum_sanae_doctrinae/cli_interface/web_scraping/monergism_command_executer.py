

import asyncio
from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_scrap_general_information, mn_scrap_get_list
from Instrumentum_sanae_doctrinae.web_scraping import my_constants
import click


def monergism_scrap_list(root_folder):
    # Get the list of the topics 
    ob = mn_scrap_get_list.GetTopicList(root_folder)
    asyncio.run(ob.scrap_and_write())
    
    # Get the list of speakers
    ob = mn_scrap_get_list.GetSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())
    #print(ob.__dict__.keys(),root_folder)
    
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
    #print(root_folder,browse_by_type,overwrite_log)
    if browse_by_type in [my_constants.SPEAKER_NAME,my_constants.SCRIPTURE_NAME,my_constants.TOPIC_NAME]:
        
        ob = mn_scrap_general_information.MonergismScrapGeneralInformation_ALL(
            root_folder = root_folder,
            browse_by_type = browse_by_type,
            overwrite_log = overwrite_log
        )
        #print(ob.__dict__)
        asyncio.run(ob.print_download_informations(True))
        asyncio.run(ob.download(download_batch_size=download_batch_size))
        
        
    else:
        a = 0



# Scrap the  list of all the authors, scriptures and topics 
@click.command()
@click.argument("output_folder",required = True)
@click.pass_context
def scrap_list_command(context:click.Context,output_folder:str):
    if "=" in output_folder:
        output_folder = output_folder.split("=")[1]
    print(output_folder)
    monergism_scrap_list(output_folder)



# Scrap the general information of all the authors, topics or scriptures
@click.command()
@click.argument("browse_by_type",required = True)
@click.argument("output_folder",required = True)
@click.option('-u', '--overwrite-log',"overwrite_log",
              default = False,required =  False)
@click.option("-bs","--download_batch_size","download_batch_size",
              default = 10,type = int,required = False)

@click.pass_context
def scrap_general_information_command(context:click.Context,browse_by_type,output_folder,
                                  overwrite_log,download_batch_size):
    
    if output_folder:
        if browse_by_type:
            monegism_scrap_general_information(root_folder = output_folder,
                                           browse_by_type=browse_by_type,
                                           download_batch_size = download_batch_size,
                                           overwrite_log = overwrite_log)
        else:
            raise ValueError("The argument <browse_by_type> must be given if the action parameter is <scrap_general_info>")
        
    
   


