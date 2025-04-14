from Instrumentum_sanae_doctrinae.my_tools import general_tools as _my_tools 
import sys 
import os 

root_folder ='/home/elvis/Documents/ForGod/outside_test_folder' 

print(_my_tools.process_path_according_to_cwd(root_folder))

print(_my_tools.get_uncommon_part_of_two_path(os.getcwd(),root_folder))