import connections as cnn
from constants import const_rpc as crpc,operations_code as opc
from typing import Dict
import json
from threading import Thread

OPERATION_ARG = 0
ADDR_ARG = 1
class NameServer:
    
    def __init__(self, server_ip,server_port) -> None:
        self.socket =  cnn.make_server_connection(server_ip,server_port,False)
        self.ip = server_ip
        self.port = server_port
        self.operations_hosts = self.__get_operation_dict()

    def __get_operation_dict(self) -> Dict:
        return {
            'sum' : [('127.0.0.1',8000),('127.0.0.1',8000)],
            'subtract' : [('127.0.0.1',8000)],
            'multiply' : [('127.0.0.1',8000)],
            'divide' : [('127.0.0.1',8000)],
            'is_prime' : [('127.0.0.1',8000)],
            'last_news_ifbarbacena' : [('127.0.0.1',8000)],
            'validate_cpf':[('127.0.0.1',8000)]
        }
    
    def start(self):
        print(f'ouvindo na porta {self.port}')
        while True:
            operation,addr = self.socket.recvfrom(crpc.BUFFER_SIZE)
            data = (
                operation.decode(),
                addr
            )

            client_thread = Thread(target=self.handle_client,args=(data,))
            client_thread.start()
        pass

    def handle_client(self,data):
        response = self.get_host_list_from_operation(data[OPERATION_ARG])
        self.socket.sendto(json.dumps({'response' : response}).encode(),data[ADDR_ARG])
        pass

    def get_host_list_from_operation(self,operation):
        return self.operations_hosts[operation] if operation in self.operations_hosts else []
        pass