import multiprocessing as mp
def make_listen(rpc_server):
    rpc_server.server_socket.bind((rpc_server.ip, rpc_server.port))
    rpc_server.server_socket.listen()

def listen_connection(rpc_server):
    conn,addr = rpc_server.server_socket.accept()
    cliente = mp.Process(target=rpc_server.client_loop,args=(addr,conn))
    cliente.start()

