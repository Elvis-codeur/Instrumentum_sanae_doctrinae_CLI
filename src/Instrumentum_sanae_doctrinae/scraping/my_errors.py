
class HTTP404Error(Exception):
    def __init__(self,url, *args):
        super().__init__(f"Not found {url}")