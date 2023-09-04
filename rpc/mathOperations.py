import constRPC as crpc

def numbrer_is_prime(number:int) -> bool:
    try:
        if number <= 1:
            return False
        
        if number <= crpc.SMALLEST_PRIME:
            return True
        
        if number % crpc.LOWEST_PRIME == 0 or number % crpc.SMALLEST_PRIME == 0:
            return False
        
        i = crpc.FIRST_PRIME_FACTOR
        while i * i <= number:
            if number % i == 0 or number % (i + 2) == 0:
                return False
            i += crpc.PRIME_STEP
        
        return True 
    except:
        return False

def is_multiprocessing_better(list_size:int):
    IS_BETTER = 10000
    return list_size >= IS_BETTER