

import asyncio

from Instrumentum_sanae_doctrinae.cli_interface.cli_tools import parse_argument
from Instrumentum_sanae_doctrinae.web_scraping import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import si_scrap_get_speaker_list
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.audio_sermon import si_audio_sermon_scrap_get_list
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.text_sermon import si_text_sermon_scrap_get_list
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
    


@click.command()
@click.argument("output_folder",type=str,required = True)
@click.pass_context
def sermonindex_scrap_list_command(context:click.Context,output_folder:str):
    root_folder = parse_argument(output_folder)
    sermonindex_scrap_list(root_folder)
    
