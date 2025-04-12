import datetime
from pathlib import Path
import os
import re 
import asyncio

from Instrumentum_sanae_doctrinae.telegram_scraping.telegram_tools import *
from dotenv import load_dotenv
from telethon.tl.functions.messages import GetHistoryRequest
from Instrumentum_sanae_doctrinae.my_tools import general_tools








class ScrapTelegramGroup():
    def __init__(self,group_username:str,client:MyTelegramClient,output_folder):
        """This class scrap the text messages in a telegram group posts. 

        Args:
            group_username (str): The user name of the group. The name in it telegram link 
            for exemple for the url t.me/ChristianSermonsAndAudioBooks, the group_username is ChristianSermonsAndAudioBooks
        """
        
        self.group_username = group_username
        self.date_last_scraping:datetime.datetime = None  
        self.client = client  
        self.output_filepath =  get_telegram_channel_text_message_filepath(output_folder,self.group_username)
        self.file_content = {}
        self.newly_scraped_data = []
        
    
    def load_file_content(self):
        
        self.file_content = general_tools.read_json(self.output_filepath)
    
        self.group_username = self.file_content.get("group_username")
        
        self.date_last_scraping = general_tools.datetimeFromGoogleFormat(self.file_content.get("date_last_scraping"))
        
        self.data = getattr(self.file_content,"data",[])
        
    
        
    async def scrap_from_date_to_date(self,date_begin:datetime.datetime,
                                      date_end:datetime.datetime):
        
        result = []
        
        await self.client.client.start(phone=self.client.phone_number)
    
        entity = await self.client.client.get_entity(self.group_username)
        
        # GetHistoryRequest return publication up to the date offset_date
        # with a limit of 100 publications 
        
        last_message_date = date_begin
        
        message_retrieved = []
        
        #print(date_begin,date_end)
        
        while last_message_date < date_end + datetime.timedelta(30):
            print(last_message_date)
            message_retrieved = await self.client.client(GetHistoryRequest(
                peer=entity,
                limit=500,  # change to what you need
                offset_date=last_message_date,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0
            ))

            for message in message_retrieved.messages:
                #print(type(message))
                text = getattr(message, 'message', None)  # message.message is the actual text field
                if text and isinstance(text, str):
                    result.append(TelegramTextMessage(
                        text=text,
                        datetime = message.date
                    ))
            
            if message_retrieved.messages and getattr(message_retrieved.messages[-1].message,"date",None):
                #print(message_retrieved.messages[-1].message,type(message_retrieved.messages[-1].message))
                last_message_date = message_retrieved.messages[-1].message.date + datetime.timedelta(30)
            else:
                last_message_date = last_message_date + datetime.timedelta(30)
        
        #result = list(set(result)) # I used set to remove any duplicate 
        
        # Store it in the newly scraped data 
        self.newly_scraped_data = result 
        
        #Update the date of the last scraping 
        self.date_last_scraping = date_end
        
        return result.sort(key=lambda message: message.datetime_object) 
    
    def update_file_content(self):
        """ 
        This function update the content of the actual filepath with 
        """
      
        
        self.file_content = {
            "date_last_scraping" : general_tools.datetimeToGoogleFormat(self.date_last_scraping),
            "group_username" : self.group_username,
            "data":getattr(self.file_content,"data",[]) + self.newly_scraped_data
        }
        
        general_tools.write_json(self.output_filepath,self.file_content)
    
    def overide_file_content(self):
        self.file_content = {
            "date_last_scraping" : general_tools.datetimeToGoogleFormat(self.date_last_scraping),
            "group_username" : self.group_username,
            "data": self.newly_scraped_data
        }
        
        general_tools.write_json(self.output_filepath,self.file_content)
    
        
        
                
                        
    async def scrap_from_last_scraping_date(self):
        datetime_now = datetime.datetime.now()
        
        result = await self.scrap_from_date_to_date(self.date_last_scraping,datetime_now)
                 
        return result
