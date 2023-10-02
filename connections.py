import multiprocessing as mp
from typing import Callable
import socket
DEFAULT_PORT = 8888
LOCAL_HOST = '127.0.0.1'

def crate_socket(is_tcp:bool = True):
    return socket.socket(socket.AF_INET,socket.SOCK_STREAM if is_tcp else socket.SOCK_DGRAM)

def make_server_connection(server_ip:str=LOCAL_HOST,server_port:int=DEFAULT_PORT,is_tcp:bool = True):
    server_socket = crate_socket(is_tcp)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((server_ip, server_port))
    if is_tcp:
        listen_connection(server_socket)
    return server_socket


def listen_connection(server_socket):
    server_socket.listen(0)

def accept_conection(rpc_server):
    return rpc_server.server_socket.accept()

def make_client_thread_in_server(server_rpc,thread_function,addr,conn):
    cliente = mp.Process(target=thread_function,args=(addr,conn))
    cliente.start()


def make_client_connection(server_ip:str=LOCAL_HOST,server_port:int=DEFAULT_PORT,is_tcp:bool = True) -> socket.socket:
    client_conection = crate_socket(is_tcp)
    if is_tcp:
        client_conection.connect((server_ip,server_port))
    pass

