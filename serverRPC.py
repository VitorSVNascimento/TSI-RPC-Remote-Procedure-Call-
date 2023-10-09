from rpc import server

rpc_server = server.Server('',8000)
rpc_server.start()