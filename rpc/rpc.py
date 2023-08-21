import socket
import threading
from functools import reduce
from typing import Callable,Dict

SUM = '__SUM__'
SUB = '__SUB__'
MUL = '__MUL__'
DIV = '__DIV__'
END = '__END__'

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

    def __numbers_tuple_to_string(self,numbers: tuple[float]) -> str:
        numbers_str = ';'.join(map(str,numbers))
        return numbers_str
    
    def __prepare_request(self,operation_code:str,args:tuple) -> str:
       return f'{operation_code};{self.__numbers_tuple_to_string(args)}'

    def sum(self,numbers:tuple[float]) -> float:
        req = self.__prepare_request(SUM,numbers)
        self.conection.send(req.encode('UTF-8'))
        resp = self.conection.recv(1024).decode()
        return self.__get_float_resp(resp)

    def subtract(self,numbers:tuple[float]) -> float:
        req = self.__prepare_request(SUB,numbers)
        self.conection.send(req.encode('UTF-8'))
        resp = self.conection.recv(1024).decode()
        return self.__get_float_resp(resp)
    
    def divide(self,numbers:tuple[float]) -> float:
        req = self.__prepare_request(DIV,numbers)
        self.conection.send(req.encode('UTF-8'))
        resp = self.conection.recv(1024).decode()
        return self.__get_float_resp(resp)
    
    def multiply(self,numbers:tuple[float]) -> float:
        req = self.__prepare_request(MUL,numbers)
        self.conection.send(req.encode('UTF-8'))
        resp = self.conection.recv(1024).decode()
        return self.__get_float_resp(resp)

    def end(self) -> str:
        self.conection.send(END.encode())
        return self.conection.recv(1024).decode()
    
    
class Server: 

    __OPERATION_ARG = 0
    __FIRST_ARG = 1
    __SEPARATOR_CHAR = ';'

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


    def get_operation_code(self,req:str) -> str:
        reqArray = req.split(self.__SEPARATOR_CHAR)
        return reqArray[self.__OPERATION_ARG] if reqArray else None
    
    def get_argument_tuple(self,req:str) -> tuple:
        reqArray = req.split(self.__SEPARATOR_CHAR)
        if len(reqArray) <= self.__FIRST_ARG:
            return None
        return tuple(reqArray[self.__FIRST_ARG:])

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
       with conn:
            try:
                while True:
                    req = conn.recv(1024).decode()

                    operation_code = self.get_operation_code(req)
                    if operation_code == END:
                        conn.sendall('finalizado'.encode())
                        break
                    args = self.get_argument_tuple(req)
                    operation = self.__get_operation(operation_code)

                    if operation is None:
                        continue
                    result = operation(args)
                    str_result = str(result)

                    conn.send(str_result.encode())
            except Exception as e:
                print("Error:", e)

    def start(self) -> None:
        
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()
        print('aguardando conexões')

        while True:
            conn,addr = self.server_socket.accept()
            t1 = threading.Thread(target=self._handle_client,args=(addr,conn))
            t1.start()