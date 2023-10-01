import json
from constants import const_rpc as crpc,operations_code as opc
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
        opc.OPERATION_KEY: operation_code,
        opc.ARGS_KEY: args
    }

def extract_operations_and_arguments(req:str):
        request_data = json.loads(req)
        return get_operation_code(request_data),get_arguments(request_data)



def get_operation_code(request_data:dict) -> str:
    try:
        return request_data[opc.OPERATION_KEY]
    except Exception:
        return None

def get_arguments(request_data: dict) -> tuple:
    try:
       return request_data[opc.ARGS_KEY]
    except Exception:
        return None