from rpc import client
import time

client_rpc = client.Client('127.0.0.1',8000)

# list_numbers = [x for x in range(10,1000000)]

# print(client.sum((70,20)))
# print(client.sum((30,20)))
# print(client.sum((40,20)))
# print(client.sum((60,20)))
headlines = client_rpc.sum((10,20))



# prime_numbers = [number for number, is_prime in zip(list_numbers, is_prime_list) if is_prime]
#print(f'Numeros primos {is_prime_list} total = {len(is_prime_list)}')


 

# prime_numbers = [number for number, is_prime in zip(list_numbers, is_prime_list) if is_prime]
#print(f'Numeros primos cache{is_prime_list} total = {len(is_prime_list)}')

# is_prime_list_mp = client.mp_is_prime(list_numbers)
# prime_numbers_mp = list(filter(lambda x: x[1], zip(list_numbers, is_prime_list_mp)))
# print(f'Numeros primos MP{[number for number,_ in prime_numbers_mp]} total = {len(prime_numbers_mp)}')

# print(client.subtract((10,5,2)))
# print(client.sum((10,20,10)))
# print(client.divide((10,2,2)))
# print(client.multiply((10,2,2)))
# print('chegou')
