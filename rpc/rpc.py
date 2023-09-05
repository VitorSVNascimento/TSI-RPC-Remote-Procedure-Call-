import socket
import threading
import json
import multiprocessing as mp
import traceback
import time
import os
import pickle

from functools import reduce
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
CACHE_FILE = './cache/dict.cache'
REGISTER_NUMBERS = 20
TIME_LIMIT = 60


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
        self.insertion_order = []
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
        
        if req in self.cache:
            response = self.cache[req]
        self.conection.send(req.encode(crpc.ENCODE))
        self.cache[req] = response
        response = self.__get_response()

        self.check_time()

    def sync_dict():
        pass

    def check_time(self):
        if time.time() - self.time >= TIME_LIMIT:
            self.time = time.time()

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
        
    def get_cache(self,cache_str:str):
        return self.cache.get(cache_str)
        pass

    def add_cache(self):
        pass
    
    def read_cache(self):
        try:
            with open(CACHE_FILE,'rb') as file:
                cache = pickle.load(file)
                return cache
        except TypeError as e:
            print('O arquivo esta vazio')
            return {}

    def write_cache(self):
        with open(CACHE_FILE, 'wb') as file:
            pickle.dump(self.cache, file)

    def __get_response(self):
        response_data = receive_complete_message(self.conection)
        return json.loads(response_data.decode(crpc.ENCODE))

    def __del__(self) -> str:
        self.conection.send(self.__prepare_request(END,()).encode())
        write_cache()
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