import datetime
from pathlib import Path
import os
import re 

from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from Instrumentum_sanae_doctrinae.my_tools import general_tools





class ScrapTelegramGroup():
    def __init__(self,group_username:str,client:TelegramClient):
        """This class scrap the text messages in a telegram group posts. 

        Args:
            group_username (str): The user name of the group. The name in it telegram link 
            for exemple for the url t.me/ChristianSermonsAndAudioBooks, the group_username is ChristianSermonsAndAudioBooks
        """
        self.group_username = group_username
        self.date_last_scraping:datetime.datetime = None  
        self.client = client  
        
        
    async def laod_data_from_json(self,filepath):
        data = general_tools.async_read_json(filepath)
        
        self.group_username = data.get("group_username")
        self.date_last_scraping = data.get("date_last_scraping")
        
        
    async def scrap_from_date_to_date(self,date_begin:datetime.datetime,
                                      date_end:datetime.datetime,
                                      outpout_filepath):
        
        result = []
        
        await self.client.client.start(phone=phone_number)
    
        entity = await self.client.client.get_entity(group_username)
        
        # GetHistoryRequest return publication up to the date offset_date
        # with a limit of 100 publications 
        
        last_message_date = date_begin
        
        message_retrieved = []
        
        #print(date_begin,date_end)
        
        while last_message_date < date_end + datetime.timedelta(30) or message_retrieved:
            
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
                text = getattr(message, 'message', None)  # message.message is the actual text field
                if text and isinstance(text, str):
                    result.append({
                        "text":text,
                        "datetime":message.date.strftime('%Y-%m-%d %H:%M:%S')
                    })
                    last_message_date = message_retrieved.messages[-1].message.date + datetime.timedelta(30)
                    
        
        result = list(set(result)) # I used set to remove any duplicate 
        
        if outpout_filepath:
            general_tools.async_write_json(outpout_filepath,result)        
            
        return result 
                
                        
    async def scrap_from_last_scraping_date(self):
        pass 
    
        


load_dotenv(dotenv_path=Path("telegram.env"))

if __name__ == "__main__":
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    phone_number = os.getenv("MY_PHONE_NUMBER")
    
    

    group_username = 'ChristianSermonsAndAudioBooks'
    # Regex for YouTube URLs (handles youtu.be and youtube.com links)
    youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/[^\s]+')
    
    telegram_client = MyTelegramClient(api_id,api_hash,phone_number)
    scraper =  ScrapTelegramGroup(group_username,telegram_client)
    print(telegram_client.client.loop.run_until_complete(scraper.scrap_from_date_to_date(date_begin=datetime.datetime(2021,1,1),
                                                                                                    date_end=datetime.datetime.now())))
    
    
