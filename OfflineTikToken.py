import os  
import tiktoken  
import tiktoken_ext.openai_public  
import inspect  
import re  
import urllib.request  
import hashlib  
  
class OfflineTikToken:  
    def __init__(self, debug=False):  
        self.debug = debug  
        self.current_dir = os.getcwd()  
        self.make_cache(self.current_dir)  
        os.environ["TIKTOKEN_CACHE_DIR"] = self.current_dir  
        self.encoding = tiktoken.get_encoding("cl100k_base")  
  
    def make_cache(self, dir):  
        fun_text = inspect.getsource(tiktoken_ext.openai_public.cl100k_base)  
        if self.debug:  
            print(fun_text)  
  
        url_pattern = r'https?://[^\s"]+'  
        matches = re.findall(url_pattern, fun_text)  
        url = matches[0]  
        if self.debug:  
            print(url)  
  
        cache_key = hashlib.sha1(url.encode()).hexdigest()  
        if self.debug:  
            print(cache_key)  
  
        target_path = os.path.join(dir, cache_key)  
  
        if not os.path.exists(target_path):  
            urllib.request.urlretrieve(url, target_path)  
        else:  
            if self.debug:  
                print(f"file {cache_key} has already existed.")  
  
    def encode(self, text):  
        return self.encoding.encode(text)  
  
# usage 
if __name__ == "__main__":  
    ott = OfflineTikToken(debug=True)  
    encoded_text = ott.encode("Hello, world")  
    print(encoded_text)
