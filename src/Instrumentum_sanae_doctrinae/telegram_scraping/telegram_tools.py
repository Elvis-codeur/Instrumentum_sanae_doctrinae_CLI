import datetime
import json
import os
from telethon import TelegramClient
from dataclasses import dataclass, asdict 

from Instrumentum_sanae_doctrinae.my_tools import general_tools
from Instrumentum_sanae_doctrinae.my_tools import my_constants



def get_telegram_root_folder(root_folder):
    return os.path.join(root_folder,my_constants.TELEGRAM_METADATA_ROOT_FOLDER)    


def get_telegram_channel_root_folder(root_folder,channel_username):
    return os.path.join(get_telegram_root_folder(root_folder),
                        my_constants.TELEGRAM_CHANNEL_ROOT_FOLDER,
                        channel_username)
    
def get_telegram_channel_text_message_filepath(root_folder,channel_username):
    return os.path.join(
        get_telegram_channel_root_folder(root_folder,channel_username),
        my_constants.TELEGRAM_CHANNEL_TEXT_MESSAGE_ROOT_FOLDER,
        my_constants.get_default_json_filename(0))
        


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
    print(get_telegram_channel_text_message_filepath("/home/elvis/Documents/ForGod/Scraping General/test_folder",
                                           "ChristianSermonsAndAudioBooks"))