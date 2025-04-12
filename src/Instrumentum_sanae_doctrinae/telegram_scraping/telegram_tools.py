import datetime
import json
from telethon import TelegramClient
from dataclasses import dataclass, asdict 

from Instrumentum_sanae_doctrinae.my_tools import general_tools



def get_telegram_root_folder(root_folder):
    


class MyTelegramClient():
    def __init__(self,api_id:str,api_hash:str,phone_number:str):
        self.phone_number = phone_number
        self.api_id = api_id
        self.api_hash = api_hash
        self.client =  TelegramClient('session_name', self.api_id, self.api_hash)
        


class TelegramTextMessage(dict):
    def __init__(self,text:str,datetime:datetime.datetime):
        self.datetime_object = datetime
        super().__init__(text = text,datetime = general_tools.datetimeToGoogleFormat(datetime))
        
        
    def __eq__(self, value):
        return super().__eq__(value)
        
        
if __name__ == "__main__":
    ob = TelegramTextMessage("Elvis",datetime=datetime.datetime.now())
    print(json.dumps(ob))