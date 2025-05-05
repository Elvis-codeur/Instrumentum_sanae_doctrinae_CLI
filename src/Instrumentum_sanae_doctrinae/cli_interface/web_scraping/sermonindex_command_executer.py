

import asyncio

from Instrumentum_sanae_doctrinae.cli_interface.cli_tools import parse_argument
from Instrumentum_sanae_doctrinae.my_tools import general_tools
from Instrumentum_sanae_doctrinae.my_tools import my_constants
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex import si_scrap_general_information, si_scrap_get_speaker_list
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.audio_sermon import si_audio_sermon_scrap_get_list, si_audio_sermon_scrap_work
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.text_sermon import si_text_sermon_christianbook_download, si_text_sermon_scrap_general_information, si_text_sermon_scrap_get_list, si_text_sermon_speaker_download, si_text_sermon_speaker_scrap_work
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.text_sermon import si_text_sermon_christianbook_scrap_work
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.video_sermon import si_video_sermon_scrap_work
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.vintage_image import si_vin_im_scrap_work
import click

from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.video_sermon import si_video_sermon_download
from Instrumentum_sanae_doctrinae.web_scraping.sermonindex.audio_sermon import si_audio_sermon_download


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
    
    if material_type == my_constants.SERMONINDEX_AUDIO:
        
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
            
        
        
    elif material_type == my_constants.SERMONINDEX_TEXT:
        material_folder = my_constants.SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER
        
        if browse_by_type == my_constants.SPEAKER_NAME:
            # The general information of the speakers 
            speaker_text_ob = si_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
                    output_folder,
                    material_folder,
                    browse_by_type,
                    overwrite_log=overwrite_log
                )    
            
            if target == "all":
                asyncio.run(speaker_text_ob.download(download_batch_size))
                speaker_text_ob.write_log_file()
            else: 
                asyncio.run(speaker_text_ob.download_from_element_key_list([target_name],1))
                
            
        if browse_by_type == my_constants.SERMONINDEX_CHRISTIAN_BOOKS_NAME:
            # The general information the books 
            
            book_text_ob = si_text_sermon_scrap_general_information.SI_ChristianBookScrapMainInformation_ALL(
                    output_folder,
                    material_folder,
                    browse_by_type,
                    overwrite_log=overwrite_log
                )    
            if target == "all":
                asyncio.run(book_text_ob.download(download_batch_size))
                book_text_ob.write_log_file()
            else:
                #print(book_text_ob.log_file_content["downloaded"].keys())
                
                asyncio.run(book_text_ob.download_from_element_key_list([target_name],1))
            
        
    elif material_type == my_constants.SERMONINDEX_VIDEO:
        material_folder = my_constants.SERMONINDEX_VIDEO_SERMONS_ROOT_FOLDER
        
        ob = si_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
            output_folder,
            material_folder,
            browse_by_type,
            overwrite_log=overwrite_log
            )    
        if target == "all":
            #print(ob.__dict__)
            asyncio.run(ob.download(download_batch_size))
            ob.write_log_file()
        else:
            asyncio.run(ob.download_from_element_key_list([target_name],1))
            ob.write_log_file()
    
    elif material_type == my_constants.SERMONINDEX_VINTAGE_IMAGE:
        material_folder = my_constants.SERMONINDEX_VINTAGE_IMAGE_ROOT_FOLDER
    
        ob = si_scrap_general_information.SermonIndexScrapSpeakerMainInformation_ALL(
            output_folder,
            material_folder,
            browse_by_type,
            overwrite_log=overwrite_log
            )
        
        if target == "all":
            #print(ob.__dict__)
            asyncio.run(ob.download(download_batch_size))
            ob.write_log_file()
        else:
            asyncio.run(ob.download_from_element_key_list([target_name],1))
            ob.write_log_file()    
        
        

def sermonindex_scrap_work(browse_by_type:str,material_type:str,
                            target:str,output_folder,
                            overwrite_log,download_batch_size:int):
    
    target_name = general_tools.remove_forbiden_char_in_text(target)

    if material_type == my_constants.SERMONINDEX_AUDIO:
        material_folder = my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
        
        ob = si_audio_sermon_scrap_work.SI_ScrapAudioSermonWork_ALL(
                root_folder=output_folder,
                material_root_folder=material_folder,
                browse_by_type = browse_by_type,
                overwrite_log=overwrite_log
        )
        
        if target == "all":
            asyncio.run(ob.download(download_batch_size=download_batch_size))
            ob.write_log_file()
        else:
            asyncio.run(ob.download_from_element_key_list([target_name],1))
            ob.write_log_file()
            
    elif material_type == my_constants.SERMONINDEX_TEXT:
        material_folder = my_constants.SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER
        
        # Download work of a speaker 
        if browse_by_type == my_constants.SPEAKER_NAME:
            ob = si_text_sermon_speaker_scrap_work.SI_ScrapTextSermonSpeakerWork_ALL(
                    root_folder=output_folder,
                    material_root_folder=material_folder,
                    browse_by_type = browse_by_type,
                    overwrite_log=overwrite_log
            )
            
            if target == "all":
                asyncio.run(ob.download(download_batch_size=download_batch_size))
                ob.write_log_file()
            else:
                asyncio.run(ob.download_from_element_key_list([target_name],1))
                ob.write_log_file()
        else:
            ob = si_text_sermon_christianbook_scrap_work.SI_ScrapTextSermonChristianBookWork_ALL(
                    root_folder=output_folder,
                    material_root_folder=material_folder,
                    browse_by_type = browse_by_type,
                    overwrite_log=overwrite_log
            )
            
            if target == "all":
                asyncio.run(ob.download(download_batch_size=download_batch_size))
                ob.write_log_file()
            else:
                asyncio.run(ob.download_from_element_key_list([target_name],1))
                ob.write_log_file()
            
           
    
    elif material_type == my_constants.SERMONINDEX_VIDEO:
        material_folder = my_constants.SERMONINDEX_VIDEO_SERMONS_ROOT_FOLDER
        
        ob = si_vin_im_scrap_work.SI_ScrapVintageImageWork_ALL(
                root_folder=output_folder,
                material_root_folder=material_folder,
                browse_by_type = browse_by_type,
                overwrite_log=overwrite_log
        )
        
        if target == "all":
            asyncio.run(ob.download(download_batch_size=download_batch_size))
            ob.write_log_file()
        else:
            asyncio.run(ob.download_from_element_key_list([target_name],1))
            ob.write_log_file()
            
    elif material_type == my_constants.SERMONINDEX_VINTAGE_IMAGE:
        material_folder = my_constants.SERMONINDEX_VINTAGE_IMAGE_ROOT_FOLDER
        
        ob = si_vin_im_scrap_work.SI_ScrapVintageImageWork_ALL(
                root_folder=output_folder,
                material_root_folder=material_folder,
                browse_by_type = browse_by_type,
                overwrite_log=overwrite_log
        )
        
        if target == "all":
            asyncio.run(ob.download(download_batch_size=download_batch_size))
            ob.write_log_file()
        else:
            asyncio.run(ob.download_from_element_key_list([target_name],1))
            ob.write_log_file() 
    
    
def sermonindex_donwload(browse_by_type:str,material_type:str,
                                       target:str,output_folder,
                                       overwrite_log,download_batch_size:int):
    
    
    target_name = general_tools.remove_forbiden_char_in_text(target)

    if material_type == my_constants.SERMONINDEX_AUDIO:
        material_folder = my_constants.SERMONINDEX_AUDIO_SERMONS_ROOT_FOLDER
        
        if browse_by_type == my_constants.SPEAKER_NAME:
            
            list_ob = si_scrap_get_speaker_list.GetAudioSermonSpeakerList(root_folder=output_folder)
            
            speaker_list = list_ob.get_list_from_local_data()
            
            
            if target == "all":
                # Make the download for each spaker
                for element in speaker_list:
                    name,intermediate_folders = element.get("name"),element.get("intermediate_folders")
                    
                    ob =si_audio_sermon_download.SI_Download_ListOfAudioWork(
                        name,
                        material_type,
                        output_folder,
                        intermediate_folders,
                        browse_by_type,
                        overwrite_log=True
                    )
                    
                    async def  f():
                        await ob.init_aiohttp_session()
                        await ob.download(download_batch_size=download_batch_size)
                        ob.write_log_file()
                        
                    asyncio.run(f())
                
            else:
                
                ob = si_audio_sermon_download.SI_Download_ListOfAudioWork(
                        target_name,
                        material_type,
                        output_folder,
                        browse_by_type,
                        overwrite_log=True
                    )
                
                    
                async def f():
                    await ob.init_aiohttp_session()
                    await ob.download(download_batch_size=download_batch_size)
                    ob.write_log_file()
                    await ob.close_aiohttp_session()
                    
                asyncio.run(f())
                
        elif browse_by_type == my_constants.TOPIC_NAME:
            list_ob = si_audio_sermon_scrap_get_list.GetAudioSermonTopicList(root_folder=output_folder)
            
            speaker_list = list_ob.get_list_from_local_data()
            
            
            if target == "all":
                # Make the download for each spaker
                for element in speaker_list:
                    name,intermediate_folders = element.get("name"),element.get("intermediate_folders")
                    
                    ob =si_audio_sermon_download.SI_Download_ListOfAudioWork(
                        name,
                        material_type,
                        output_folder,
                        intermediate_folders,
                        browse_by_type,
                        overwrite_log=overwrite_log
                    )
                    
                    async def  f():
                        await ob.init_aiohttp_session()
                        await ob.download(download_batch_size=download_batch_size)
                        ob.write_log_file()
                        await ob.close_aiohttp_session()
                        
                        
                    asyncio.run(f())
                
            else:
                
                ob = si_audio_sermon_download.SI_Download_ListOfAudioWork(
                        target_name,
                        material_type,
                        output_folder,
                        browse_by_type,
                        overwrite_log=True
                    )
                
                async def f():
                    await ob.init_aiohttp_session()
                    await ob.download(download_batch_size=download_batch_size)
                    ob.write_log_file()
                    
                asyncio.run(f())
                
            
            
            
            
    elif material_type == my_constants.SERMONINDEX_TEXT:
        material_folder = my_constants.SERMONINDEX_TEXT_SERMONS_ROOT_FOLDER
        
        # Download work of a speaker 
        if browse_by_type == my_constants.SPEAKER_NAME:
            
            if target == "all":
                
                # Get the list of speakers 
                list_ob = si_scrap_get_speaker_list.GetTextSermonSpeakerList(root_folder=output_folder,
                                                                     material_type=material_type)
                speaker_list = list_ob.get_list_from_local_data()
                
                for element in speaker_list:
                    name,intermediate_folders = element.get("name"),element.get("intermediate_folders")
                    
                    ob = si_text_sermon_speaker_download.SI_Download_Speaker_ListOfTextWork(
                        name,
                        material_type,
                        output_folder,
                        intermediate_folders,
                        browse_by_type,
                        overwrite_log=overwrite_log
                    ) 
                    async def f():
                        await ob.init_aiohttp_session()               
                        await ob.download(download_batch_size=download_batch_size)
                        ob.write_log_file()
                
                    asyncio.run(f())
                    
            else:
                
                ob = si_text_sermon_speaker_download.SI_Download_Speaker_ListOfTextWork(
                        target_name,
                        material_type,
                        output_folder,
                        browse_by_type,
                        overwrite_log=overwrite_log
                ) 
                async def f():
                    await ob.init_aiohttp_session()               
                    await ob.download(download_batch_size=download_batch_size)
                    ob.write_log_file()
            
                asyncio.run(f())
                
                
        # Download Christian books        
        else:
            
            if target == "all":
                list_ob = si_text_sermon_scrap_get_list.GetTextSermonsChristianBook(root_folder=output_folder)
                book_list = list_ob.get_list_from_local_data()
                
                for book_name in book_list:
                    print(book_name)
                    ob = si_text_sermon_christianbook_download.SI_Download_ChristianBooks_ListOfTextWork(
                        book_name,
                        material_type,
                        output_folder,
                        browse_by_type,
                        overwrite_log=True
                    )
                    async def f():
                        await ob.init_aiohttp_session()
                        await ob.init_log_data()
                        #print(ob.__dict__)
                        await ob.download(download_batch_size=download_batch_size)
                        await ob.close_aiohttp_session()
                        
                    asyncio.run(f())
                
                
            else:
                ob = si_text_sermon_christianbook_download.SI_Download_ChristianBooks_ListOfTextWork(
                    target_name,
                    material_type,
                    output_folder,
                    browse_by_type,
                    overwrite_log=True
                )
                async def f():
                    await ob.init_aiohttp_session()
                    await ob.init_log_data()
                    #print(ob.__dict__)
                    await ob.download(download_batch_size=download_batch_size)
                    await ob.close_aiohttp_session()
                    
                asyncio.run(f())
            
           
    
    elif material_type == my_constants.SERMONINDEX_VIDEO:
        material_folder = my_constants.SERMONINDEX_VIDEO_SERMONS_ROOT_FOLDER
        
        if target == "all":
            list_ob = si_scrap_get_speaker_list.GetVideoSermonSpeakerList(root_folder=output_folder)
            speaker_list = list_ob.get_list_from_local_data()
            
            for element in speaker_list:
                name,intermediate_folders = element.get("name"),element.get("intermediate_folders")
               
                ob = si_video_sermon_download.SI_Download_ListOfVideoWork(
                    name,
                    material_type,
                    output_folder,
                    intermediate_folders,
                    browse_by_type,
                    overwrite_log=True
                )
                async def f():
                    await ob.init_aiohttp_session()
                    await ob.init_log_data()
                    #print(ob.__dict__)
                    await ob.download(download_batch_size=download_batch_size)
                    await ob.close_aiohttp_session()
                    
                asyncio.run(f())
            
            
        else:
            ob = si_video_sermon_download.SI_Download_ListOfVideoWork(
                target_name,
                material_type,
                output_folder,
                browse_by_type,
                overwrite_log=True
            )
            async def f():
                await ob.init_aiohttp_session()
                await ob.init_log_data()
                #print(ob.__dict__)
                await ob.download(download_batch_size=download_batch_size)
                await ob.close_aiohttp_session()
                
            asyncio.run(f())
        
    

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
    #print(browse_by_type,material_type,target)
    sermonindex_scrap_general_information(browse_by_type=browse_by_type,material_type=material_type,
                                          target=target,output_folder=output_folder,
                                          overwrite_log=overwrite_log,download_batch_size=download_batch_size)
    
    
@click.command()
@click.argument("browse_by_type",required = True,type = str)
@click.argument("material_type",required = True,type=str)
@click.argument("target",required = True,type = str)
@click.argument("output_folder",required = True,type=str)
@click.option('-u', '--overwrite-log',"overwrite_log",
              default = False,required =  False)
@click.option("-bs","--download_batch_size","download_batch_size",
              default = 10,type = int,required = False)

@click.pass_context
def sermonindex_scrap_work_command(context:click.Context,browse_by_type:str,
                                                  material_type:str,target:str,output_folder,
                                                  overwrite_log,download_batch_size:int):
    
    output_folder = parse_argument(output_folder)
    
    sermonindex_scrap_work(browse_by_type=browse_by_type,material_type=material_type,
                           target=target,overwrite_log=overwrite_log,
                           download_batch_size=download_batch_size,
                           output_folder=output_folder)
    

@click.command()
@click.argument("browse_by_type",required = True,type = str)
@click.argument("material_type",required = True,type=str)
@click.argument("target",required = True,type = str)
@click.argument("output_folder",required = True,type=str)
@click.option('-u', '--overwrite-log',"overwrite_log",
              default = False,required =  False)
@click.option("-bs","--download_batch_size","download_batch_size",
              default = 10,type = int,required = False)

@click.pass_context
def sermonindex_download_command(context:click.Context,browse_by_type:str,
                                                  material_type:str,target:str,output_folder,
                                                  overwrite_log,download_batch_size:int):
    
    output_folder = parse_argument(output_folder)
    
    sermonindex_donwload(browse_by_type=browse_by_type,material_type=material_type,
                           target=target,overwrite_log=overwrite_log,
                           download_batch_size=download_batch_size,
                           output_folder=output_folder)