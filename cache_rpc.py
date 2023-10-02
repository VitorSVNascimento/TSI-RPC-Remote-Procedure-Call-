import pickle
import os
import traceback

from typing import Dict

from constants import files_and_urls as fiu,const_rpc as crpc,cache_const as cac
def get_cache():
    try:
        if not os.path.exists(fiu.CACHE_FILE):
            return create_cache_file()
        with open(fiu.CACHE_FILE,crpc.BINARY_READ_MODE) as file:
            return read_cache(file)
    except TypeError as e:
        print('O arquivo esta vazio')
        traceback.print_exc()
        return {}

def create_cache_file(cache_file:str = fiu.CACHE_FILE):
    file = open(cache_file,crpc.WRITE_MODE)
    file.close()
    return {}

def read_cache(cache_file,cache_url:str = fiu.CACHE_FILE):
    if os.path.getsize(cache_url) == 0:
        return {}
    cache = pickle.load(cache_file)
    return cache

def create_time_key_cache(cache:Dict):
    print(cache)
    if cac.TIME_KEY not in cache:
        cache[cac.TIME_KEY] = 0

def write_cache(cache:Dict,cache_file:str = fiu.CACHE_FILE):
    with open(cache_file, crpc.BINARY_WRITE_MODE) as file:
        pickle.dump(cache, file)

def get_last_news_cache():
    pass