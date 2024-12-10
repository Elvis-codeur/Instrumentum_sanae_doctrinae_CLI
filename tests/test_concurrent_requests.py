import sys
import time 
import requests
import aiohttp 
import asyncio
import aiodns 


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


url_list = [
    "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=1",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=2",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=3",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=4",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=5",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=6",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=7",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=8",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=9",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=10",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=11",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=12",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=13",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=14",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=15",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=16",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=17",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=18",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=19",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=20",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=21",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=22",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=23",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=24",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=25",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=26",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=27",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=28",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=29",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=30",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=31",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=32",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=33",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=34",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=35",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=36",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=37",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=38",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=39",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=40",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=41",
            "https://www.monergism.com/search?f%5B0%5D=author%3A34468&page=42"
]



class Connect():
    def __init__(self,url_list):
        self.url_list = url_list
        
        
    def get_sychronously(self):
        with requests.session() as session:
            for url in self.url_list:
                response = session.get(url)
            
    async def get_asynchronously(self):
        async with aiohttp.ClientSession() as session:
            for url in self.url_list:
                async with session.get(url) as response:
                    html = await response.text()
    
    
    
    def run_sync(self,print_time_used = False):
        t1 = time.time()
        self.get_sychronously()
        t2 = time.time()
        if print_time_used:
            print("sync run time = ",t2 - t1)
        
        
        
    def run_async(self,print_time_used = False):
        t1 = time.time()
        asyncio.run(self.get_asynchronously())
        t2 = time.time()
        if print_time_used:
            print("sync run time = ",t2 - t1)
        


def measure_runtime(function_to_run,**kwargs):
    t1 = time.time()
    function_to_run(**kwargs)
    t2 = time.time()
    print("run time = ",t2 - t1)
    
    
def sequential_connection():
    with requests.session() as session:
        for url in url_list:
            session.get(url)
            

async def asynchronous_connection():
    async with aiohttp.ClientSession() as session:
        for url in url_list:
            async with session.get(url) as response:
                html = await response.text()
                
    
    
def run_the_asynchronous_connection():
    asyncio.run(asynchronous_connection())
                
            
            
            

if __name__ == "__main__":
    if sys.platform == 'win32':
	    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
 
    ob = Connect(url_list)

    ob.run_sync()
    ob.run_async()
    