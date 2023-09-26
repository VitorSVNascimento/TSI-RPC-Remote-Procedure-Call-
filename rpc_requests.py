import constRPC as crpc
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

def prepare_request(operation_code:str,args:tuple) -> str:
    return {
        "operation": operation_code,
        "args": args
    }