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

from functools import reduce
import concurrent.futures as cf
from typing import Callable,Dict,List

import mathOperations
import constRPC as crpc

SUM = '__SUM__'
SUB = '__SUB__'
MUL = '__MUL__'
DIV = '__DIV__'
END = '__END__'
IS_PRIME = '__IS_PRIME__'
MP_IS_PRIME = '__MP_IS_PRIME'
LAST_NEWS = '__LAST_NEWS__'
CACHE_FILE = './cache/dict.cache'
URL_NEWS_IF_BQ = 'https://www.ifsudestemg.edu.br/noticias/barbacena/?b_start:int='
MAX_REGISTER_IN_CACHE = 5
TIME_LIMIT = 1


def receive_complete_message(connection):
    
    complete_message = b""

    while True:
        data = connection.recv(crpc.BUFFER_SIZE)
        if not data:
            break
        complete_message += data

        if len(data) < crpc.BUFFER_SIZE:
            break
    return complete_message


class Client:
    def __init__(self,ip,port) -> None:
        self.ip = ip
        self.port = port
        self.conection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conection.connect((self.ip,self.port))
        self.cache = self.read_cache()
        self.time = 0

    def __get_float_resp(self,resp:str) -> float:
        try:
            resp_float = float(resp)
            return resp_float
        except:
            return None 

    def __numbers_tuple_to_string(self,numbers: tuple) -> str:
        numbers_str = crpc.SEPARATOR_CHAR.join(map(str,numbers))
        return numbers_str
    
    def __prepare_request(self,operation_code:str,args:tuple) -> str:
       return json.dumps({
        "operation": operation_code,
        "args": args
       })

    def process_request(self,req):
        req_str = json.dumps(req)

        if req in self.cache:
            print('resposta do cache')
            response = self.cache[req]
            return response

        self.conection.send(req.encode(crpc.ENCODE))
        response = self.__get_response()
        
        self.add_cache_register(req,response)
        self.check_time()
        print('resposta sem cache')
        return response

    def add_cache_register(self,req,response):
        if len(self.cache) == MAX_REGISTER_IN_CACHE:
            self.remove_oldest_register()
        self.cache[req] = response

    def remove_oldest_register(self):
        oldest_register = next(iter(self.cache))
        del self.cache[oldest_register]

    def check_time(self):
        if time.time() - self.time >= TIME_LIMIT:
            self.time = time.time()
            self.write_cache()

    def sum(self,numbers:tuple) -> float:
        req = self.__prepare_request(SUM,numbers)
        return self.process_request(req)

    def subtract(self,numbers:tuple) -> float:
        req = self.__prepare_request(SUB,numbers)
        return self.process_request(req)
    
    def divide(self,numbers:tuple) -> float:
        req = self.__prepare_request(DIV,numbers)
        return self.process_request(req)
    
    def multiply(self,numbers:tuple) -> float:
        req = self.__prepare_request(MUL,numbers)
        return self.process_request(req)

    def is_prime(self,start:int,end:int,step:int) -> List[int]:
        numbers = (start,end,step)
        req = self.__prepare_request(IS_PRIME,numbers)
        return self.process_request(req)

    def last_news_ifbarbacena(self,quantity_news:int) -> List:
        req = self.__prepare_request(LAST_NEWS,quantity_news)
        return self.process_request(req)
        pass

    def read_cache(self):
        try:
            if not os.path.exists(CACHE_FILE):
                file = open(CACHE_FILE,'w')
                file.close()
                return {}
            with open(CACHE_FILE,'rb') as file:
                if os.path.getsize(CACHE_FILE) == 0:
                    return {}
                cache = pickle.load(file)
                return cache
        except TypeError as e:
            print('O arquivo esta vazio')
            traceback.print_exc()
            return {}


    def __get_response(self):
        response_data = receive_complete_message(self.conection)
        return json.loads(response_data.decode(crpc.ENCODE))

    def write_cache(self):
        with open(CACHE_FILE, 'wb') as file:
            pickle.dump(self.cache, file)

    def __del__(self) -> str:
        self.conection.send(self.__prepare_request(END,()).encode())
        self.write_cache()
        return 
    
class Server: 

    __OPERATION_ARG = 0
    __FIRST_ARG = 1

    def __init__(self,ip,port) -> None:
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.operations = self.__get_operations_dict()

    def __get_operations_dict(self) -> Dict[str, Callable]:
        return {
            SUM:self.__sum_function,
            SUB:self.__sub_function,
            MUL:self.__mul_function,
            DIV:self.__div_function,
            IS_PRIME:self.is_prime_function,
            LAST_NEWS:self.last_news_ifbarbacena,
        }


    def get_operation_code(self, req: str) -> str:
        try:
            request_data = json.loads(req)
            return request_data.get("operation")
        except json.JSONDecodeError:
            return None
    
    def get_argument_tuple(self, req: str) -> tuple:
        try:
            request_data = json.loads(req)
            args = request_data.get("args")
            return tuple(args) if args else None
        except json.JSONDecodeError:
            return None
        except TypeError as type:
            return int(args)
        except ValueError as vl:
            return None

    def __get_operation(self,operation_code:str) -> Callable:
        return self.operations.get(operation_code,lambda *args:None)



    def __sum_function(self,numbers:tuple) -> float:
        try:
            return sum(tuple(map(float,numbers)))
        except:
            return None
    
    def __sub_function(self,numbers:tuple) -> float:
        try:
            if len(numbers) == 1:
                return numbers[0]
            
            result = float(numbers[0]) -sum(map(float,numbers[1:]))
            return result
        except:
            return None
    
    def __mul_function(self,numbers:tuple) -> float:
        try:
            return reduce(lambda x, y: x * y, map(float,numbers))
        except:
            return None
    
    
    def __div_function(self,numbers:tuple) -> float:
        try:
            return reduce(lambda x, y: x / y, map(float,numbers))
        except:
            return None

    def is_prime_function(self,args:tuple) -> List[int]:
        START_POSITION = 0
        END_POSITION = 1
        STEP_POSITION = 2
        try:
            number_list = self.make_number_list(args[START_POSITION],args[END_POSITION],args[STEP_POSITION])
            numbers_tuple = tuple(map(int,number_list))

            if mathOperations.is_multiprocessing_better(len(numbers_tuple)):
                return self.multiprocessing_is_prime_function(numbers_tuple)
            return self.single_processing_is_prime_function(numbers_tuple)
        except:
          traceback.print_exc()

    def single_processing_is_prime_function(self,numbers:tuple) -> List[bool]:
        try: 
            list_numbers = list(map(int,numbers))
            start_time = time.time()

            is_prime_list = list(map(mathOperations.numbrer_is_prime,list_numbers))
            prime_numbers = [number for number, is_prime in zip(list_numbers, is_prime_list) if is_prime]

            end_time = time.time()  # Marca o tempo de término da operação
            elapsed_time = end_time - start_time  # Calcula o tempo decorrido

            print(f"Tempo gasto: {elapsed_time:.4f} segundos")
            return prime_numbers
        except:
            traceback.print_exc()
            return None
        pass

    def multiprocessing_is_prime_function(self, numbers:tuple) -> List[int]:
        try:
            list_numbers = list(map(int, numbers))
            with mp.Pool(processes=os.cpu_count()) as pool:
                start_time = time.time()  # Marca o tempo de início da operação

                results = pool.map(mathOperations.numbrer_is_prime, list_numbers)
                prime_numbers = [number for number, is_prime in zip(list_numbers, results) if is_prime]

                end_time = time.time()  # Marca o tempo de término da operação
                elapsed_time = end_time - start_time  # Calcula o tempo decorrido


                print(f"Tempo gasto MP: {elapsed_time:.4f} segundos")
                return prime_numbers

        except:
            traceback.print_exc()
            return None

    def last_news_ifbarbacena(self, news_quantity):
        urls = self.make_url_list(news_quantity)
        
        htmls = self.multithread_get_html_text(urls)
        headlines = []
        
        for html_text in htmls:
            
            soup = bs4.BeautifulSoup(html_text,'html.parser')
            news = soup.find_all('a',{'class':'summary url'})
            for article in news:
                headlines.append(article.text)
                news_quantity-=1
                if news_quantity == 0:
                    break
        return headlines


    def make_url_list(self,news_quantity):
        url_list = []
        for number in range(news_quantity // 20 + 1):
            url_list.append(f'{URL_NEWS_IF_BQ}{number * 20}')
        return url_list

    def get_html_text(self, url):
        try:
            return requests.get(url).text
        except:
            return None

    def multithread_get_html_text(self,url_list):
        MAX_THREADS = os.cpu_count()
        with cf.ThreadPoolExecutor(MAX_THREADS) as executor:
            htmls = executor.map(self.get_html_text,url_list)
        
        return list(htmls)
    
    def make_number_list(self,start: int, end: int, step: int = 1) -> List[int]:
        if step == 0:
            raise ValueError("O passo não pode ser zero.")
        
        if step > 0:
            return [i for i in range(start, end + 1, step)]
        else:
            return [i for i in range(start, end - 1, step)]

    
    def _handle_client(self,addr,conn):
       print(f'Conexão estabelecida com {addr}')
       with conn:
            try:
                while True:
                    req = receive_complete_message(conn).decode(crpc.ENCODE)

                    operation_code = self.get_operation_code(req)
                    if operation_code == END:
                        conn.close()
                        break
                    args = self.get_argument_tuple(req)
                    operation = self.__get_operation(operation_code)

                    if operation is None:
                        continue
                    result = operation(args)
                    result_str = json.dumps(result)

                    conn.send(result_str.encode())
            except Exception as e:
                traceback.print_exc()
                print("Error:", e)
            print(f'Conexão finalizada com {addr}')

    def start(self) -> None:
        
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()
        print('aguardando conexões')

        while True:
            conn,addr = self.server_socket.accept()
            cliente = mp.Process(target=self._handle_client,args=(addr,conn))
            cliente.start()