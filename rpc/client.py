import json
import traceback
import time
import rpc_requests as rreq
import cache_rpc
from constants import operations_code as opc,cache_const as cac, const_rpc as crpc
from typing import List
import connections as cnn
import random
class Client:
    def __init__(self,ip,port) -> None:
        self.ip = ip
        self.port = port
        self.name_server_socket = cnn.make_client_connection(ip,port,False)
        self.time_out_name_server_count = 0
        self.conection = None
        self.cache = cache_rpc.get_cache()
        cache_rpc.create_time_key_cache(self.cache)
        self.time = 0
    
    def intercept(func):
        def wrapper(*args, **kwargs):
            self_instance = args[0]
            caller_name = func.__name__

            if self_instance.get_connection_server(caller_name) == True:
                response = func(*args,**kwargs)
                self_instance.disconnect_server()
            else:
                response = 'Nao foi possivel conectar ao servidor'
            return response
        return wrapper

    def get_connection_server(self,function_name):
        LIMIT_ATTEMPS = 10
        attemps = 0
        while True:

            hosts = self.get_hosts_list(function_name)
            attemps+=1
            if hosts == None and attemps > LIMIT_ATTEMPS:
                return None
            if(len(hosts) == 0):
                print('Nenhum servidor realiza essa operação')
                return None
            return self.connect_to_server(hosts)
            
        pass

    def get_hosts_list(self,function_name):
        self.name_server_socket.settimeout(1.0)
        self.name_server_socket.sendto(function_name.encode(),(self.ip,self.port))

        try:
            data = self.name_server_socket.recv(crpc.BUFFER_SIZE)
            data_json = json.loads(data.decode())['response']
            self.time_out_name_server_count = 0
            return data_json
        except:
            return None

    def connect_to_server(self,hosts):
        print(hosts)
        server = random.choice(hosts)
        server_ip = server[0]
        server_port = server[1]
        try:
            self.conection = cnn.make_client_connection(server_ip,server_port)
            return True
        except Exception:
            return False
        
    def disconnect_server(self):
        self.conection.send(json.dumps(rreq.prepare_request(opc.END,())).encode())
    
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
                print('veio do cache')
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
            return None
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
            cache_rpc.write_cache(self.cache)

    @intercept
    def sum(self,numbers:tuple) -> float:
        req = rreq.prepare_request(opc.SUM,numbers)
        return self.process_request(req)

    @intercept
    def subtract(self,numbers:tuple) -> float:
        req = rreq.prepare_request(opc.SUB,numbers)
        return self.process_request(req)
    
    @intercept
    def divide(self,numbers:tuple) -> float:
        req = rreq.prepare_request(opc.DIV,numbers)
        return self.process_request(req)
    
    @intercept
    def multiply(self,numbers:tuple) -> float:
        req = rreq.prepare_request(opc.MUL,numbers)
        return self.process_request(req)

    @intercept
    def is_prime(self,start:int,end:int,step:int) -> List[int]:
        numbers = (start,end,step)
        req = rreq.prepare_request(opc.IS_PRIME,numbers)
        return self.process_request(req)

    @intercept
    def last_news_ifbarbacena(self,quantity_news:int) -> List:
        req = rreq.prepare_request(opc.LAST_NEWS,quantity_news)
        return self.process_request(req)

    @intercept
    def validate_cpf(self,cpf:str) -> bool:
        req = rreq.prepare_request(opc.VALIDATE_CPF,cpf)
        return self.process_request(req)


    def get_response(self):
        response_data = rreq.receive_complete_message(self.conection)
        return json.loads(response_data.decode(crpc.ENCODE))

    def __del__(self) -> str:
        cache_rpc.write_cache(self.cache)
        return 