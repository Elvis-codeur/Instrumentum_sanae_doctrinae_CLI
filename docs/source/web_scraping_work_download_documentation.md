

# The data structure for the download work 

For monergism as sermonindex, the code is this one 

- The code of sermonindex 
```python
def prepare_input_data(self,**kwargs):
        """
        This method take a json file content and create input data for download 
        that are put int dict self.element_dict

        :param file_content: the content of a json file where input data will be taken 
        :param intermediate_folders: The intermediate folders from the root folder to 
        the json file 
        :param file_path: The path of the json file 
        """

        element = kwargs.get("file_content").get("data")
        
        name  = pathlib.Path(kwargs.get("file_path")).parent.parent.as_posix()
        
        name = name.split("/")[-1]
        
        self.element_dict[name] = {
            **{"pages":element.get("pages"),"name":name},
            
             **{
                "meta_data": {
                    "input_file_index":self.meta_informations["input_files_information"]\
                                                        ["input_files"].index(kwargs.get("file_path")),                
                }
             }
                        
            **{"download_log":{
                "intermediate_folders":kwargs.get("intermediate_folders")}
                }
            
                }
``` 

- The code of monergism 

```python

      
        if not name in self.element_dict.keys():
            self.element_dict[name]  = {
                "name":name,
                "data":{"url_list":[]}
            }

                
        self.element_dict[name]["data"]["url_list"].append({
                    "name":name,
                    "pages":element.get("pages"),
                
                     **{
                        "meta_data": {
                            "input_file_index":self.meta_informations["input_files_information"]\
                                                                ["input_files"].index(kwargs.get("file_path")),                
                        },
                        **{"download_log":{
                            "intermediate_folders":kwargs.get("intermediate_folders")[2:]}
                            }
                    },
                     
                })
```
