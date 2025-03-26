

import asyncio

from Instrumentum_sanae_doctrinae.cli_interface.cli_tools import parse_argument
from Instrumentum_sanae_doctrinae.my_tools import general_tools
from Instrumentum_sanae_doctrinae.web_scraping import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import si_scrap_general_information, si_scrap_get_speaker_list
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.audio_sermon import si_audio_sermon_scrap_get_list
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.text_sermon import si_text_sermon_scrap_general_information, si_text_sermon_scrap_get_list
import click


def sermonindex_scrap_list(root_folder):
    # Audio sermon 
    
    ob = si_scrap_get_speaker_list.GetAudioSermonSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())
    
    # The list of topics
    ob = si_audio_sermon_scrap_get_list.GetAudioSermonTopicList(
                                                    root_folder,
                                                    browse_by_type=my_constants.TOPIC_NAME)
    
    asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))
    # The list of scriptures 
    ob = si_audio_sermon_scrap_get_list.GetAudioSermonScriptureList(
                                                    root_folder,
                                                    browse_by_type=my_constants.SCRIPTURE_NAME)
    asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))
    # The list of podcasts 
    ob = si_audio_sermon_scrap_get_list.GetAudioSermonPodcastList(
                                                    root_folder,
                                                    browse_by_type=my_constants.PODCAST_NAME)
    asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))



    # Text sermons 
    # Text sermon list 
    ob = si_scrap_get_speaker_list.GetTextSermonSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())
    # The list of christian books s
    ob = si_text_sermon_scrap_get_list.GetTextSermonsChristianBook(root_folder)
    asyncio.run(ob.scrap_and_write(get_useful_link_method = ob.get_useful_anchor_object_list))
    
    
    # Video sermons    
    ob = si_scrap_get_speaker_list.GetVideoSermonSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())
    
    # Vintage image 
    ob = si_scrap_get_speaker_list.GetVintageImageSpeakerList(root_folder)
    asyncio.run(ob.scrap_and_write())
    


def sermonindex_scrap_general_information(browse_by_type:str,material_type:str,
                                       target:str,output_folder,
                                       overwrite_log,download_batch_size:int):
    
    target_name = general_tools.replace_forbiden_char_in_text(target)
    
    if material_type == "audio":
        
        material_folder = my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
        
        ob = si_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
            output_folder,
            material_folder,
            browse_by_type,
            overwrite_log=overwrite_log
            )
         
        if target == "all":   
            asyncio.run(ob.download(download_batch_size))
            ob.write_log_file()
        else:
            asyncio.run(ob.download_from_element_key_list([target_name],1))
            
        
        
    elif material_type == "text":
        material_folder = my_constants.SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER
        
        if target == "all":
            
            # The general information of the speakers 
            ob = si_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
                    output_folder,
                    material_folder,
                    browse_by_type,
                    overwrite_log=True
                )    
            #print(ob.__dict__)
            asyncio.run(ob.download(download_batch_size))
            
            ob.write_log_file()
        
            # The general information the books 
            ob = si_text_sermon_scrap_general_information.SI_ChristianBookScrapMainInformation_ALL(
                    output_folder,
                    material_folder,
                    browse_by_type,
                    overwrite_log=True
                )    
            asyncio.run(ob.download(download_batch_size))
            ob.write_log_file()
        
    elif material_type == "video":
        material_folder = my_constants.SERMONINDEX_VIDEO_SERMONS_ROOT_FOLDER
        
        ob = si_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
            output_folder,
            material_folder,
            browse_by_type,
            overwrite_log=True
            )    
        if target == "all":
            #print(ob.__dict__)
            asyncio.run(ob.download(download_batch_size))
            ob.write_log_file()
        else:
            asyncio.run(ob.download_from_element_key_list([target_name],1))
            ob.write_log_file()
    
    elif material_type == "vintage_image":
        material_folder = my_constants.SERMONINDEX_VINTAGE_IMAGE_ROOT_FOLDER
    
        ob = si_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
            output_folder,
            material_folder,
            browse_by_type,
            overwrite_log=True
            )
        
        if target == "all":
                
            #print(ob.__dict__)
            asyncio.run(ob.download(download_batch_size))
            ob.write_log_file()
        else:
            asyncio.run(ob.download_from_element_key_list([target_name],1))
            ob.write_log_file()    
        
        
   
    
    
    
    

@click.command()
@click.argument("output_folder",type=str,required = True)
@click.pass_context
def sermonindex_scrap_list_command(context:click.Context,output_folder:str):
    root_folder = parse_argument(output_folder)
    sermonindex_scrap_list(root_folder)
    



# Scrap the general information of all the authors, topics or scriptures
@click.command()
@click.argument("browse_by_type",required = True,type=str)
@click.argument("material_type",required = True,type=str)
@click.argument("target",required = True,type = str)
@click.argument("output_folder",required = True,type=str)
@click.option('-u', '--overwrite-log',"overwrite_log",
              default = False,required =  False)
@click.option("-bs","--download_batch_size","download_batch_size",
              default = 10,type = int,required = False)

@click.pass_context
def sermonindex_scrap_general_information_command(context:click.Context,browse_by_type:str,
                                                  material_type:str,target:str,output_folder,
                                                  overwrite_log,download_batch_size:int):
    
    output_folder = parse_argument(output_folder)
    sermonindex_scrap_general_information(browse_by_type=browse_by_type,material_type=material_type,
                                          target=target,output_folder=output_folder,
                                          overwrite_log=overwrite_log,download_batch_size=download_batch_size)