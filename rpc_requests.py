def prepare_request(operation_code:str,args:tuple) -> str:
    return {
        "operation": operation_code,
        "args": args
    }