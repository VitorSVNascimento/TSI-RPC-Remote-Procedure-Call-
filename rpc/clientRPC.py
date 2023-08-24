from rpc import Client

client = Client('127.0.0.1',8000)
print(client.subtract((10,5,2)))
print(client.sum((10,20,10)))
print(client.divide((10,2,2)))
print(client.multiply((10,2,2)))
# print('chegou')
