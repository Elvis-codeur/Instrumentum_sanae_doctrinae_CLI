import asyncio
import json
import os 
import pathlib
import copy 
from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools


class ParallelConnexionWithLogManagement():
    def __init__(self,log_filepath,input_data,overwrite_log = False,input_root_folder = ""):
        """
        :param log_filepath: The path of the log file used to store and manage the downloaded, undownloaded, not found etc 
        :param input_data: A dictionnary where the keys are the file path and the value the content of the file
        :param overwrite_log: If true, the existing log file is overwriten. If not, the older log file is read and the updates are made from it 
        :param input_root_folder: The folder from which all the json files are searched from to be used as input files 
        """
        self.log_filepath = log_filepath
        self.input_root_folder = input_root_folder
        self.overwrite_log = overwrite_log
        
        
        self.log_data_initialisation_made = False
        
        self.element_dict = {}

        if not input_root_folder:
            raise ValueError("The value of variable input_root_folder must be given")



        self.meta_informations = {}
        
        # The information of the json input files 
        self.meta_informations["input_files_information"] = {}

        self.meta_informations["input_files_information"]["input_files"] = list(input_data.keys())


        # Add download log the element each element 
        for file_path in input_data:
            
            file_path_from_root_folder = _my_tools.get_uncommon_part_of_two_path(
                                                    self.input_root_folder,file_path)[1]
            
            file_path_from_root_folder = pathlib.Path(file_path_from_root_folder).parent
            
            # The subfolder from the root folder where the scraped data must be stored
            #  (the information of the author, topic, scripture, etc)
            intermediate_folders = list(file_path_from_root_folder.parts[1:])

            file_content  =  input_data[file_path]

            #print(self.meta_informations)

            self.prepare_input_data(file_content = file_content,
                                    intermediate_folders = intermediate_folders,
                                    file_path = file_path)
            


        self.log_file_content = {}
        #self.init_log_data()

                        
                
    async def init_log_data(self):
        """
        Open the log file and update to download and downloaded informations 
        """
        if self.overwrite_log:
            self.log_file_content = self.create_default_log_file_content()
            await _my_tools.async_write_json(self.log_filepath,self.log_file_content)
        else:
            # Create the log file if it does not exists 
            if not os.path.exists(self.log_filepath):
                self.log_file_content = self.create_default_log_file_content()
                await _my_tools.async_write_json(self.log_filepath,self.log_file_content)
            else:
                # Read the log dict 
                file_content = await _my_tools.async_read_file(self.log_filepath)
                
                if file_content:
                    file_content = json.loads(file_content)
                    if file_content.keys():
                        self.log_file_content = file_content
                        # Update it in with based on things downloaded or not 
                        await self.update_to_download_list()   
                    else:
                        self.log_file_content = self.create_default_log_file_content()
                        await _my_tools.async_write_json(self.log_filepath,self.log_file_content)
                else:
                    self.log_file_content = self.create_default_log_file_content()
                    await _my_tools.async_write_json(self.log_filepath,self.log_file_content)
                    
                    
    
        self.log_data_initialisation_made = True
        
        
    async def update_log_data(self):
        """
        Open the log file and update to download and downloaded informations 
        """
        await self.update_downloaded_and_to_download_from_drive(add_not_found_404_elements=False)
        
        await _my_tools.async_write_json(self.log_filepath,self.log_file_content)
        
                
        
    async def update_to_download_list(self):
        """
        This function take the element in the self.element_dict and take care that if there 
        is an element in the self.element_dict that is not downloaded and is not in the yet in 
        the to_download list. That happen if after the last scraping, new elements have been scrapped 
        and not yet downloaded
        """
        
        # A list of the url of of the link object which have been already downloaded 
        downloaded_list = [i for i in self.log_file_content.get("downloaded")] if self.log_file_content.get("downloaded") else []
        to_downlaod_list = [i for i in self.log_file_content.get("to_download")] if self.log_file_content.get("to_download") else []

        
        # We take "element_list" variable because it contains the link of the author, scripture or topic
        for element_name in self.element_dict:
            #print(element_name,self.element_dict[element_name],"Elvis","\n\n\n")
            if element_name not in downloaded_list: # If it is not already downloaded 
                if element_name not in to_downlaod_list: # It is not in the link prepared to for download. 
                    #print("\n\n\n\n\n",self.log_file_content["to_download"].keys(),"\n\n\n",self.element_dict.keys(),"\n\n\n\n",url,element_name)
                    #print(element_name)
                    self.log_file_content["to_download"][element_name] = self.element_dict[element_name]
                else: # If the element is already in the "to_download" list, there is no need to add it 
                    pass 
            else: # If the link is already downlaed. There is no need of modification of anything 
                pass


    async def update_downloaded_and_to_download_from_drive(self,add_not_found_404_elements):
        """
        This function verify if the data of the links in "downloaded" list are truly downloaded. 
        If not this link is put back in the "to_download" list. 
        If a link data is downloaded but is in to_download list, it is put in the downloaded list
        
        :param add_not_found_404_elements: If true, the elements in the not_found_404 list are
        added to the download list so that a new download attempt can be made for each one of them. 
        """

        # Remove from link_list the link whoes data are already downloaded 
        downloaded = {}
        to_download = {}
        
        if not self.log_data_initialisation_made:
            await self.init_log_data()
        
        #print(self.log_file_content)
        
        if add_not_found_404_elements:
            element_dict = {**copy.deepcopy(self.log_file_content["to_download"]),
                        ** copy.deepcopy(self.log_file_content["downloaded"]),
                        ** copy.deepcopy(self.log_file_content["not_found_404"])}
        else:
            element_dict = {**copy.deepcopy(self.log_file_content["to_download"]),
                        **copy.deepcopy(self.log_file_content["downloaded"])}
            

        for key in element_dict:
            #print(element_dict.keys())
                
            #print(key,element_dict[key],"\n",self.element_dict[key],"\n\n\n")
            is_downloaded = await self.is_element_data_downloaded(element_dict[key])
            
            
            if is_downloaded:
                #print(key,True)
                downloaded[key] = element_dict[key]
            else:
                
                #print(key,False)
                to_download[key] = element_dict[key]
        
        self.log_file_content["to_download"] = to_download
        self.log_file_content["downloaded"] = downloaded
        
        #print(len(self.log_file_content["to_download"].keys()))
        #print(len(self.log_file_content["downloaded"].keys()))
    
    
    async def update_downloaded_and_to_download_from_download_result(self,download_result_list):
        """
        This method take the result of downloads and update the downloaded and to download 
        dict of the log file content 
        """

     
        for download_result in download_result_list:
            #print(download_result,"--------- download result --------------")
            if download_result.get("success"):
                # Add the downloaded element to the downloaded list
                self.log_file_content["downloaded"][download_result.get("element").get("name")] = download_result.get("element")
                
                if download_result.get("element").get("name") in self.log_file_content["to_download"].keys():
                    # Delete it from the to_download list 
                    del self.log_file_content["to_download"][download_result.get("element").get("name")]
                    
    
    

    def create_default_log_file_content(self):

        return {
                "meta_info":self.meta_informations,
                "to_download":self.element_dict,
                "downloaded":{},
                "not_found_404":{}
                }

    async def download_element_data(self,element):
        """This element take an element ( for example the information of an author or topic) 
        and download the data that must be downloaded from it """


    async def download(self,download_batch_size,download_total_number = 0):
        """
        Download the content of the input files concurrently 
        by a batch of size :data:`download_batch` 
        """
        result = []

        # Init the log informations 
        await self.init_log_data() 
        
        #print(self.log_file_content.keys())
        
        # Update before the begining of downloads
        await self.update_downloaded_and_to_download_from_drive(add_not_found_404_elements = True) 
        
        
        
        element_to_download = list(self.log_file_content["to_download"].values())

        #print(self.log_file_content["to_download"].keys(),self.log_file_content["to_download"])
        
        if download_total_number:
            # Take only the number have to be downloaded and set in the download_total_number variable
            element_to_download = element_to_download[:min(download_total_number,len(element_to_download))]
       
       
        # Split it by size download_batch_size to download
        #  them in parralel 
        element_to_download_splitted = _my_tools.sample_list(element_to_download,
                                                      download_batch_size)

        
        # This is used to show a progress bar 
        for download_batch in element_to_download_splitted:
            
            await self.print_download_informations(check_from_file=False)
            
            tasks = [self.download_element_data(element) for element in download_batch]
            result = await asyncio.gather(*tasks)
           
            await self.update_downloaded_and_to_download_from_download_result(result)
           
        
            await _my_tools.async_write_json(self.log_filepath,self.log_file_content)
            
    
    
    async def download_from_element_list(self,element_list,download_batch_size):
        """
        Download the content of the input files concurrently 
        by a batch of size :data:`download_batch` 
        """
        result = []

        # Init the log informations 
        await self.init_log_data() 
        
        
        # Update before the begining of downloads
        await self.update_downloaded_and_to_download_from_drive(add_not_found_404_elements = False) 
               
        # Split it by size download_batch_size to download
        #  them in parralel 
        element_to_download_splitted = _my_tools.sample_list(element_list,
                                                      download_batch_size)

        
        # This is used to show a progress bar 
        for download_batch in element_to_download_splitted:
            #print([type(element) for element in download_batch_size])
            tasks = [self.download_element_data(element) for element in download_batch]
            result = await asyncio.gather(*tasks)
            #print(result)
            await self.update_downloaded_and_to_download_from_download_result(result)
            
            
            #break 
            await self.print_download_informations(check_from_file=False)
        
            await _my_tools.async_write_json(self.log_filepath,self.log_file_content)
           
           
           
    async def is_key_in_logfile_keys(self,key:str) -> bool:
        """

        Args:
            key (str): The key to check if it is in the log file to_download dict or downloaded dict. 

        Returns:
            bool: 
        """

        

        # Init the log informations 
        await self.init_log_data() 
        
        
        # Update before the begining of downloads
        await self.update_downloaded_and_to_download_from_drive(add_not_found_404_elements = True) 
        
        return (key in self.log_file_content["to_download"] or key in self.log_file_content["downloaded"])
    
    async def download_from_element_key_list(self,key_list,download_batch_size):
        """
        Download the content of the input files concurrently 
        by a batch of size :data:`download_batch` 
        """
        result = []

        # Init the log informations 
        await self.init_log_data() 
        
        
        # Update before the begining of downloads
        await self.update_downloaded_and_to_download_from_drive(add_not_found_404_elements = True) 
        
        element_to_download = []
        
        
        #print(self.log_file_content["to_download"].keys())
        #print(self.log_file_content["downloaded"].keys())
        #print(self.element_dict.keys())
        #print(self.input_root_folder)
        
        
        
        for key in key_list:
            if key in self.log_file_content["to_download"]:
                element_to_download.append(self.log_file_content["to_download"][key])
            elif key in self.log_file_content["downloaded"]:
                element_to_download.append(self.log_file_content["downloaded"][key])
            else:
                raise ValueError(f'The element "{key}" is not available')
                
       
        # Split it by size download_batch_size to download
        #  them in parralel 
        element_to_download_splitted = _my_tools.sample_list(element_to_download,
                                                      download_batch_size)

        
        # This is used to show a progress bar 
        for download_batch in element_to_download_splitted:
            tasks = [self.download_element_data(element) for element in download_batch]
            result = await asyncio.gather(*tasks)
           
            await self.update_downloaded_and_to_download_from_download_result(result)
           
            await self.print_download_informations(check_from_file=False)
        
            await _my_tools.async_write_json(self.log_filepath,self.log_file_content)
 
               
  
    
    def prepare_input_data(self,**kwargs):
        """
        This method take a json file content and create input data for download 
        that are put int dict self.element_dict

        """

    def write_log_file(self):
        return _my_tools.write_json(self.log_filepath,self.log_file_content)
        
    def is_element_data_downloaded(self,element):
        """
        Check if the element data was downloaded 
        """
        
    def prepare_log_metadata_input_files_path(self,root_folder):
        """
        Return the log, metatdata and input files path in a dict
        """
        
                
    async def print_download_informations(self,check_from_file = False):
        """
        This method show the number of the already downloaded and the number 
        of the to downloaded and the number of not found 404 
        :param check_from_file: If true, the class variable log_file_content is updated 
        by runing and checking in the hard drive which is time consuming. If not, the display
        is made from the current state the variable log_file_content. 
        """
        if check_from_file:
            await self.init_log_data()
            await self.update_downloaded_and_to_download_from_drive(add_not_found_404_elements=False)
        
        
        #print(self.log_file_content)
              
        len_downloaded =  len(self.log_file_content['downloaded'])
        len_to_download = len(self.log_file_content["to_download"])
        len_not_found_404 = len(self.log_file_content["not_found_404"])
        
        print(f"downloaded = {len_downloaded} to_download = {len_to_download} not_found_404 = {len_not_found_404}")