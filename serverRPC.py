from rpc import server

rpc_server = server.Server('127.0.0.1',8000)
rpc_server.start()