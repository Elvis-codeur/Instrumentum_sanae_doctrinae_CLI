import asyncio
import os
import sys 


from Instrumentum_sanae_doctrinae.web_scraping.monergism import mn_manage_downlaod


root_folder = os.path.join(os.getcwd(),'test_folder')


def test_manage_download():
    browse_by_type = "scripture"
    ob = mn_manage_downlaod.ManageDownload(root_folder,browse_by_type)
    ob.load_input_file_content()
    ob.download()
    
    
if __name__ == "__main__":
    test_manage_download()
    
    
