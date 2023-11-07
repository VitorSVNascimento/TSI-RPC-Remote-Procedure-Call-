from rpc import name_server

IP = '127.0.0.1'
PORT = 8888

server_name = name_server.NameServer('',PORT)

if __name__ == '__main__':
    server_name.start()