from telethon import TelegramClient


class MyTelegramClient():
    def __init__(self,api_id:str,api_hash:str,phone_number:str):
        self.phone_number = phone_number
        self.api_id = api_id
        self.api_hash = api_hash
        self.client =  TelegramClient('session_name', self.api_id, self.api_hash)