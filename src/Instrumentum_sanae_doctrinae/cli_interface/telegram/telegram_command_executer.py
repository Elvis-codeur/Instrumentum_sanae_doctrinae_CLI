import datetime
from Instrumentum_sanae_doctrinae.telegram_scraping.channel_scraper import ScrapTelegramGroup
from Instrumentum_sanae_doctrinae.telegram_scraping.telegram_tools import MyTelegramClient
import click 



@click.command()
@click.argument("api_id",type=str,required = True)
@click.argument("api_hash",type = str,required = True)
@click.argument("phone_number",type=str,required = True)
@click.argument("group_username",type = str, required = True)
@click.argument("date_begin",type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%S"]),required = True)
@click.argument("date_end",type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%S"]),required = True)
@click.argument("output_folder",type=str,required = True)
@click.option("-o","--overwrite",default = False)
@click.pass_context
def scrap_channel_text_message_from_date_to_date(context:click.Context,
                               api_id,api_hash,
                               phone_number,
                               date_begin,date_end,
                               group_username,
                               output_folder:str,
                               overwrite):
    
    
    telegram_client = MyTelegramClient(api_id,api_hash,phone_number)
    
    scraper =  ScrapTelegramGroup(group_username,telegram_client,output_folder)
    
    # Load the content of the file existing now 
    #scraper.load_file_content()
    
    #print(scraper.date_last_scraping)
    
    telegram_client.client.loop.run_until_complete(scraper.scrap_from_date_to_date(
        date_begin=date_begin,
        date_end=date_end
    ))
    
    if overwrite:
        scraper.overide_file_content()    
    else:
        scraper.update_file_content()

    
 
 
 


@click.command()
@click.argument("api_id",type=str,required = True)
@click.argument("api_hash",type = str,required = True)
@click.argument("phone_number",type=str,required = True)
@click.argument("group_username",type = str, required = True)
@click.argument("output_folder",type=str,required = True)
@click.pass_context
def scrap_channel_text_message_from_date_to_date(context:click.Context,
                               api_id,api_hash,
                               phone_number,
                               date_begin,date_end,
                               group_username,
                               output_folder:str,
                               overwrite):
    
    
    telegram_client = MyTelegramClient(api_id,api_hash,phone_number)
    
    scraper =  ScrapTelegramGroup(group_username,telegram_client,output_folder)
    
    # Load the content of the file existing now 
    #scraper.load_file_content()
    
    #print(scraper.date_last_scraping)
    
    telegram_client.client.loop.run_until_complete(scraper.scrap_from_last_scraping_date(
        date_begin=date_begin,
        date_end=date_end
    ))
    
    scraper.update_file_content()

    
 