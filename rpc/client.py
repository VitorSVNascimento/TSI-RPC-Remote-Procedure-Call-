import socket
import threading
import json
import multiprocessing as mp
import traceback
import time
import os
import pickle
import bs4
import requests
import concurrent.futures as cf

import rpc_requests as rreq
import mathOperations
from constants import operations_code as opc,cache_const as cac, files_and_urls as fiu, const_rpc as crpc

from functools import reduce
from typing import Callable,Dict,List


class Client:
    def __init__(self,ip,port) -> None:
        self.ip = ip
        self.port = port
        self.conection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conection.connect((self.ip,self.port))
        self.cache = self.read_cache()
        if cac.TIME_KEY not in self.cache:
            self.cache[cac.TIME_KEY] = 0
        self.time = 0
    
    def process_request(self,req):
        req_str = json.dumps(req)

        if req[opc.OPERATION_KEY] == opc.LAST_NEWS:
            cache_news = self.get_last_news_cache(req[opc.ARGS_KEY])
            if cache_news != None: 
                print('veio do cache')
                return cache_news
        else:
            if req_str in self.cache:
                response = self.cache[req_str]

                return response

        self.conection.send(req_str.encode(crpc.ENCODE))
        response = self.get_response()
        
        if req[opc.OPERATION_KEY] == opc.LAST_NEWS:
            self.add_cache_register(req[opc.OPERATION_KEY],response)
        else:    
            self.add_cache_register(req_str,response)
        self.check_time()
        print('nao veio do cache')
        return response

    def get_last_news_cache(self,news_quantity):
        try:
            if opc.LAST_NEWS in self.cache:
                if (time.time() - self.cache[cac.TIME_KEY]) >= (5 * 60):
                        del self.cache[opc.LAST_NEWS]
                self.cache[cac.TIME_KEY] = time.time()
                    
                return None
                
                if len(self.cache[opc.LAST_NEWS]) < news_quantity:
                    del self.cache[opc.LAST_NEWS]
                    return None
                return self.cache[opc.LAST_NEWS][:news_quantity]
        except:
            traceback.print_exc()
            return None
        pass


    def add_cache_register(self,req,response):
        if len(self.cache) == cac.MAX_REGISTER_IN_CACHE:
            self.remove_oldest_register()
        self.cache[req] = response

    def remove_oldest_register(self):
        oldest_register = next(iter(self.cache))
        del self.cache[oldest_register]

    def check_time(self):
        if time.time() - self.time >= cac.TIME_LIMIT:
            self.time = time.time()
            self.write_cache()

    def sum(self,numbers:tuple) -> float:
        req = rreq.prepare_request(opc.SUM,numbers)
        return self.process_request(req)

    def subtract(self,numbers:tuple) -> float:
        req = rreq.prepare_request(opc.SUB,numbers)
        return self.process_request(req)
    
    def divide(self,numbers:tuple) -> float:
        req = rreq.prepare_request(opc.DIV,numbers)
        return self.process_request(req)
    
    def multiply(self,numbers:tuple) -> float:
        req = rreq.prepare_request(opc.MUL,numbers)
        return self.process_request(req)

    def is_prime(self,start:int,end:int,step:int) -> List[int]:
        numbers = (start,end,step)
        req = rreq.prepare_request(opc.IS_PRIME,numbers)
        return self.process_request(req)

    def last_news_ifbarbacena(self,quantity_news:int) -> List:
        req = rreq.prepare_request(opc.LAST_NEWS,quantity_news)
        return self.process_request(req)
        pass

    def read_cache(self):
        try:
            if not os.path.exists(fiu.CACHE_FILE):
                file = open(fiu.CACHE_FILE,crpc.WRITE_MODE)
                file.close()
                return {}
            with open(fiu.CACHE_FILE,crpc.BINARY_READ_MODE) as file:
                if os.path.getsize(fiu.CACHE_FILE) == 0:
                    return {}
                cache = pickle.load(file)
                return cache
        except TypeError as e:
            print('O arquivo esta vazio')
            traceback.print_exc()
            return {}


    def get_response(self):
        response_data = rreq.receive_complete_message(self.conection)
        return json.loads(response_data.decode(crpc.ENCODE))

    def write_cache(self):
        with open(fiu.CACHE_FILE, crpc.BINARY_WRITE_MODE) as file:
            pickle.dump(self.cache, file)

    def __del__(self) -> str:
        self.conection.send(json.dumps(rreq.prepare_request(opc.END,())).encode())
        self.write_cache()
        return 


    pass