

import datetime
from Instrumentum_sanae_doctrinae.telegram_scraping.telegram_tools import TelegramTextMessage, get_telegram_channel_speaker_filepath, get_telegram_channel_text_message_filepath
from  Instrumentum_sanae_doctrinae.my_tools import general_tools

class ParseChannelTextMessages():
    def __init__(self,group_username,output_folder):
        self.output_folder = output_folder 
        self.group_username = group_username
        self.output_filepath =  get_telegram_channel_text_message_filepath(output_folder,self.group_username)

    
    def load_file_content(self):
        
        #print(self.output_filepath)
        
        self.file_content = general_tools.read_json(self.output_filepath)
        
    
        self.group_username = self.file_content.get("group_username")
        
        self.date_last_scraping = general_tools.datetimeFromGoogleFormat(self.file_content.get("date_last_scraping"))
        
        self.data = [TelegramTextMessage(i.get("text"),general_tools.datetimeFromGoogleFormat(i.get("datetime")))
                     for i in self.file_content.get("data")]

    def is_contained_list(self,small_list,big_list,condition = "or"):
        if condition == "or":
            return any(item in big_list for item in small_list)
        else:
            return all(item in big_list for item in small_list)
        
    
    def is_contained_str(self,keyword_list,text,condition = "or"):
        if condition == "or":
            return any(item.lower() in text.lower() for item in keyword_list)
        else:
            return all(item.lower() in text.lower() for item in keyword_list)
        
        
            
    def filter_message_by_hashtag(self,hashtag_list,condition = "or"):
        prepared_hash_list = []
        for hashtag in hashtag_list:
            if hashtag[0] != "#":
                prepared_hash_list.append("#" + hashtag)
            else:
                prepared_hash_list.append(hashtag)
                
        result = [message for message in self.data if self.is_contained_list(prepared_hash_list,
                                                                        message.hashtag_list,
                                                                        condition=condition)]
        
        return result
    
    def filter_message_by_keyword(self,keyword_list,condition = "or"):
        result = [message for message in self.data if self.is_contained_str(keyword_list,message.text,
                                                                            condition=condition)]
        return result 
    
    
    def save_speaker_parsed_data(self,data,name,filename):
    
        output_filepath = get_telegram_channel_speaker_filepath(self.output_folder,self.group_username,
                                              name,filename)
        
        general_tools.write_json(output_filepath,{"datetime":general_tools.datetimeToGoogleFormat(datetime.datetime.now()),
                                                  "data":data})
        
if __name__ == "__main__":
    output_folder = "/home/elvis/Documents/ForGod/Scraping General/test_folder"
    ob = ParseChannelTextMessages("ChristianSermonsAndAudioBooks",output_folder)
    ob.load_file_content()
    
    spurgeon_hashtag_list = ["#CharlesSpurgeon", "#Spurgeon", "#SpurgeonSermons", "#CHSpurgeon"]
    
    ob.save_speaker_parsed_data(ob.filter_message_by_hashtag(spurgeon_hashtag_list),"CH_Spurgeon","all_messages.json")