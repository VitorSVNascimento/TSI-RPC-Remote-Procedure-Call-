import socket
import threading
import json
import multiprocessing as mp
import traceback

import constRPC as crpc
from functools import reduce
from typing import Callable,Dict

SUM = '__SUM__'
SUB = '__SUB__'
MUL = '__MUL__'
DIV = '__DIV__'
END = '__END__'

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

    def sum(self,numbers:tuple) -> float:
        req = self.__prepare_request(SUM,numbers)
        self.conection.send(req.encode(crpc.ENCODE))
        return self.__get_response()

    def subtract(self,numbers:tuple) -> float:
        req = self.__prepare_request(SUB,numbers)
        self.conection.send(req.encode(crpc.ENCODE))
        return self.__get_response()
    
    def divide(self,numbers:tuple) -> float:
        req = self.__prepare_request(DIV,numbers)
        self.conection.send(req.encode(crpc.ENCODE))
        return self.__get_response()
    
    def multiply(self,numbers:tuple) -> float:
        req = self.__prepare_request(MUL,numbers)
        self.conection.send(req.encode(crpc.ENCODE))
        return self.__get_response()

    def __get_response(self):
        response_data = receive_complete_message(self.conection)
        return json.loads(response_data.decode(crpc.ENCODE))

    def __del__(self) -> str:
        self.conection.send(self.__prepare_request(END,()).encode())
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
            DIV:self.__div_function
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
    
    def _handle_client(self,addr,conn):
       print(f'Conexão estabelecida com {addr}')
       with conn:
            try:
                while True:
                    req = receive_complete_message(conn).decode(crpc.ENCODE)

                    operation_code = self.get_operation_code(req)
                    print(operation_code)
                    if operation_code == END:
                        print('entrou')
                        conn.close()
                        break
                    args = self.get_argument_tuple(req)
                    operation = self.__get_operation(operation_code)

                    if operation is None:
                        continue
                    result = operation(args)
                    str_result = str(result)

                    conn.send(str_result.encode())
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
            p1 = mp.Process(target=self._handle_client,args=(addr,conn))
            p1.start()
            p1.join()