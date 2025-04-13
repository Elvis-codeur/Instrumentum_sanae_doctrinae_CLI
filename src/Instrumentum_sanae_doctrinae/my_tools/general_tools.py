import datetime
import os 
import random
import shutil
import string
import json 
import aiofiles
import re
import urllib.parse

url_pattern = re.compile(
    r'https?://(?:www\.)?[-\w@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-\w()@:%_\+.~#?&//=]*)'
)

hashtag_pattern = re.compile(r'#\w+')

def datetimeToGoogleFormat(date:datetime.datetime):
    """
    Return A datetime in the google format(the format is like this "%Y-%m-%dT%H:%M:%S.%fZ")
    """
    return date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def datetimeToSrtFormat(date:datetime.datetime):
    """
    Format a date as an string using with the format "%H:%M:%S,%f"
    """
    return date.strftime("%H:%M:%S,%f")

def datetimeFromGoogleFormat(text):
    """
    Return a datetime from a text formated in the google format 
    """
    try:
        return datetime.datetime.strptime(text,"%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        try:
            return datetime.datetime.strptime(text,"%Y-%m-%dT%H:%M:%SZ")
        except:
            try:
                return datetime.datetime.strptime(text,"%Y-%m-%dT%H-%M-%S.%fZ")
            except:
                try:
                    return datetime.datetime.strptime(text,"%Y-%m-%dT%H-%M-%SZ")
                except:
                    raise ValueError("Date format {} doesn't match with (%Y-%m-%dT%H:%M:%S.%fZ), (%Y-%m-%dT%H:%M:%SZ), (%Y-%m-%dT%H-%M-%S.%fZ) nor (%Y-%m-%dT%H-%M-%SZ)".format(text))


def remove_forbiden_char_in_filepath(filepath:str):
    """
    Remove the chars (<>:"|?*) from the filepath. It does not remove / and \ because we except a
      filepath as input and not a text  
    """
    invalid = '<>:"|?*'
    for char in invalid:
        filepath = filepath.replace(char, '')
    return filepath


def remove_forbiden_char_in_text(text): 
    """
        Remove the chars (<>:"|?*\/) from the text
    """
    invalid = '<>:"|?*/\\'
    for char in invalid:
        text = text.replace(char, '')
    return text


def replace_forbiden_char_in_text(text):
    """
    This functin replace :

    < by _a_
    > by _b_
    : by _c_
    " by _d_
    | by _e_
    ? by _f_
    * by _g_
    / by _h_
    \\ by _i_
    ... by _k_
    """
    #invalid = '<>:"|?*/\\'
    if not text:
        return ""
    
    return text.replace("<","_a_").replace(">","_b_").replace(":","_c_")\
                .replace('"',"_d_").replace("|","_e_").replace("?","_f_")\
                .replace("*","_g_").replace("/","_h_").replace("\\","_i_").replace("...","_k_")


def remove_consecutive_spaces(text):
    name = list(text)
    for indice in  range(len(name)-1):
        if  name[indice] == " " and name[indice+1] == " ":
            name[indice] = ""
            
    return "".join(name).strip()
    



def generateID(prefix = "",suffix = "",length = 20):
    """
    Generate a string of random character with the given prefix and suffix and of
      the lenght asked 
    """ 
    assert (len(prefix) + len(suffix)) < length

    letters = string.ascii_letters + string.digits + string.punctuation
    return prefix +\
        "".join([random.choice(letters) for i in range(length - len(prefix) - len(suffix))]) \
              + suffix



def sample_list(l,sample_size:int):
    """
    Sample a list of in a smaller list of size of sample_size. 

    For example sample_list([1,'a','b','c'],2) = [[1,'a'],['b','c']]
    """
    s = len(l)
    #print(s)
    if s % sample_size:
        n = s //sample_size + 1
    else:
        n = s // sample_size
    return [l[i:i+sample_size] for i in range(0,s,sample_size)]


def get_disk_free_space_mb(disk_path,MEGABYTE_SIZE = 2**20):
    disk_usage = shutil.disk_usage(disk_path)
    free_space_mb = disk_usage.free // MEGABYTE_SIZE
    return free_space_mb


def get_folder_files(folder):
    result = []
    for folder,subfolders,filenames in os.walk(folder):
        result = filenames

    result = [os.path.join(folder,i) for i in result]
    return result



def read_json(filename,encoding = "utf-8",mode = "r"):
    
    f = open(filename,encoding=encoding,mode=mode)
    result = f.read()
    f.close()
    return json.loads(result)
    

def write_json(filename,data,encoding = "utf-8",mode = "w",create_path= True,correct_file_path = True):
    if correct_file_path:
        filename = remove_forbiden_char_in_filepath(filename)
        
    if create_path == False:
        assert os.path.exists(os.path.dirname(filename))
        
   
    # Write the dirname if necessary
    dirname = os.path.dirname(filename)
    if str(dirname) != "":
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    #print(filename,"-Elvis-")

    f = open(filename,encoding=encoding,mode=mode)
    f.write(json.dumps(data))
    f.close()
    return 1
    

def read_file(filename,mode = "r",encoding = "utf-8"):
    f = open(filename,mode = mode,encoding = encoding)
    result = f.read()
    f.close()
    return result 

def write_file(filename,content,mode = "w",encoding="utf-8",create_path= True,correct_file_path = True):
    if correct_file_path:
        filename = remove_forbiden_char_in_filepath(filename)


    if create_path == False and os.path.dirname(filename) != "":
        assert os.path.exists(os.path.dirname(filename))
    
    # Write the dirname if necessary
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname) and dirname != "":
        os.makedirs(dirname)

    with open(filename,encoding=encoding if not mode=="wb" else None,
                mode=mode) as f:
        f.write(content)
        f.close()
        
    return 1
    

async def async_read_file(filename,mode = "r",encoding = "utf-8"):
    async with aiofiles.open(filename,mode = mode,encoding = encoding) as f:
        result = await f.read()
        return result 
    
async def async_write_file(filename,content,mode = "w",encoding="utf-8",create_path= True,correct_file_path = True):
    if correct_file_path:
        filename = remove_forbiden_char_in_filepath(filename)

    if create_path == False and os.path.dirname(filename) != "":
        assert os.path.exists(os.path.dirname(filename))
    
    # Write the dirname if necessary
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname) and dirname != "":
        os.makedirs(dirname)

    async with aiofiles.open(filename,encoding=encoding if not mode=="wb" else None,
                mode=mode) as f:
        await f.write(content)
    
        
    return 1

async def async_read_json(filename,encoding = "utf-8",mode = "r"):
    
    async with aiofiles.open(filename,encoding=encoding,mode=mode) as f:    
        result = await f.read()
        return json.loads(result)

async def async_write_json(filename,data,encoding = "utf-8",mode = "w",create_path= True,correct_file_path = True):
    if correct_file_path:
        filename = remove_forbiden_char_in_filepath(filename)
        
    if create_path == False:
        assert os.path.exists(os.path.dirname(filename))
        
   
    # Write the dirname if necessary
    dirname = os.path.dirname(filename)
    if str(dirname) != "":
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    #print(filename,"-Elvis-")

    async with aiofiles.open(filename,encoding=encoding,mode=mode) as f:
        await f.write(json.dumps(data))
        return 1
    


def get_important_information_from_request_response(request_response):
    request_history = [
                            {
                                'status_code': r.status,
                                'url': str(r.url),
                                'headers': dict(r.headers),
                            } for r in request_response.history
                        ]
        

    cookies = []
    for key, morsel in request_response.cookies.items():
        cookie = {
            "name": key,
            "value": morsel.value,
            "domain": morsel["domain"],
            "path": morsel["path"],
            "expires": morsel["expires"]
        }
    

    result = {
        "request_header":dict(request_response.headers),
            "request_status_code": request_response.status,
            "request_cookies":cookies,
            "request_history":request_history,
    }
    return result


def get_uncommon_part_of_two_path(path1,path2):
    """
    Return the uncommon path of path1 and path2 in that order 
    """
    common_prefix = os.path.commonprefix([os.path.normpath(path1),os.path.normpath(path2)])
    return os.path.relpath(path1,common_prefix),os.path.relpath(path2,common_prefix)


def process_path_according_to_cwd(folder_path):
    """
    This method verify if the output folder is child of the current working directory and folder path accordingly
    """
    #result,_ = get_uncommon_part_of_two_path(folder_path,os.getcwd())

    return folder_path


def get_url_list_in_text(text):
    return url_pattern.findall(text)

def get_hashtag_list_in_text(text):
    return hashtag_pattern.findall(text)



class YouTubeURL:
    def __init__(self, url):
        self.url = url
        self.parsed = urllib.parse.urlparse(url)
        self.query = urllib.parse.parse_qs(self.parsed.query)

    def get_video_id(self):
        """Returns the video ID if present"""
        return self.query.get('v', [None])[0]

    def get_playlist_id(self):
        """Returns the playlist ID if present"""
        return self.query.get('list', [None])[0]

    def get_channel_id(self):
        """Returns the channel or user from the path if present"""
        parts = self.parsed.path.strip('/').split('/')
        if parts and parts[0] in ('channel', 'user', 'c'):
            return parts[1] if len(parts) > 1 else None
        return None

    def get_full_info(self):
        return {
            'video_id': self.get_video_id(),
            'playlist_id': self.get_playlist_id(),
            'channel': self.get_channel_id(),
            'hostname': self.parsed.hostname,
            'path': self.parsed.path,
            'query': self.query
        }
