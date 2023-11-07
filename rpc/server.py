import rpc_requests as rreq
import json
import multiprocessing as mp
import traceback
import time
import os
import bs4
import requests

from functools import reduce
import concurrent.futures as cf
from typing import Callable,Dict,List

from constants import operations_code as opc,cache_const as cac, files_and_urls as fiu, const_rpc as crpc
import connections as cnn
import mathOperations

import re

class Server: 

    def __init__(self,ip,port) -> None:
        self.ip = ip
        self.port = port
        self.server_socket = cnn.make_server_connection(self.ip,self.port,True)
        self.operations = self.get_operations_dict()

    def start(self) -> None:
        
        print('aguardando conexões')
        while True:
            conn,addr = cnn.accept_conection(self)
            cnn.make_client_thread_in_server(self,self.client_loop,addr,conn)
    

    def client_loop(self,addr,conn):
       print(f'Conexão estabelecida com {addr}')
       with conn:
            try:
                while self.handle_client(addr,conn):
                    pass
            except Exception as e:
                traceback.print_exc()
                print("Error:", e)
            print(f'Conexão finalizada com {addr}')

    def handle_client(self,addr,conn):
        start_time = time.time()
        req = rreq.receive_complete_message(conn).decode(crpc.ENCODE)

        operation_code,args = rreq.extract_operations_and_arguments(req)
        
        if operation_code == opc.END:
            conn.close()
            return False
        operation = self.get_operation(operation_code)

        if operation is None:
            print('operação inxestente')

        result_str = self.get_result_of_operation(operation,args)
        conn.send(result_str.encode())
        end_time = time.time()
        self.write_log(addr,time.time(),operation,end_time-start_time)
        return True

    def get_result_of_operation(self,operation:Callable,args)->str:
        try:
            result = operation(args)
            return json.dumps(operation(args))
        except Exception:
            traceback.print_exc()
            return None

    def get_operations_dict(self) -> Dict[str, Callable]:
        return {
            opc.SUM:self.sum_function,
            opc.SUB:self.sub_function,
            opc.MUL:self.mul_function,
            opc.DIV:self.div_function,
            opc.IS_PRIME:self.is_prime_function,
            opc.LAST_NEWS:self.last_news_ifbarbacena,
            opc.VALIDATE_CPF:self.validate_cpf
        }
    
    def get_operation(self,operation_code:str) -> Callable:
        return self.operations.get(operation_code,lambda *args:None)

    def sum_function(self,numbers:tuple) -> float:
        try:
            return sum(tuple(map(float,numbers)))
        except:
            return None
    
    def sub_function(self,numbers:tuple) -> float:
        try:
            if len(numbers) == 1:
                return numbers[0]
            
            result = float(numbers[0]) -sum(map(float,numbers[1:]))
            return result
        except:
            return None            
    def mul_function(self,numbers:tuple) -> float:
        try:
            return reduce(lambda x, y: x * y, map(float,numbers))
        except:
            return None
    
    
    def div_function(self,numbers:tuple) -> float:
        try:
            return reduce(lambda x, y: x / y, map(float,numbers))
        except:
            return None

    def is_prime_function(self,args:tuple) -> List[int]:
        START_POSITION = 0
        END_POSITION = 1
        STEP_POSITION = 2
        try:
            number_list = self.make_number_list(args[START_POSITION],args[END_POSITION],args[STEP_POSITION])
            numbers_tuple = tuple(map(int,number_list))

            if mathOperations.is_multiprocessing_better(len(numbers_tuple)):
                return self.multiprocessing_is_prime_function(numbers_tuple)
            return self.single_processing_is_prime_function(numbers_tuple)
        except:
          traceback.print_exc()

    def single_processing_is_prime_function(self,numbers:tuple) -> List[bool]:
        try: 
            list_numbers = list(map(int,numbers))
            start_time = time.time()

            is_prime_list = list(map(mathOperations.numbrer_is_prime,list_numbers))
            prime_numbers = [number for number, is_prime in zip(list_numbers, is_prime_list) if is_prime]

            end_time = time.time()  # Marca o tempo de término da operação
            elapsed_time = end_time - start_time  # Calcula o tempo decorrido

            print(f"Tempo gasto: {elapsed_time:.4f} segundos")
            return prime_numbers
        except:
            traceback.print_exc()
            return None

    def multiprocessing_is_prime_function(self, numbers:tuple) -> List[int]:
        try:
            list_numbers = list(map(int, numbers))
            with mp.Pool(processes=os.cpu_count()) as pool:
                start_time = time.time()  # Marca o tempo de início da operação

                results = pool.map(mathOperations.numbrer_is_prime, list_numbers)
                prime_numbers = [number for number, is_prime in zip(list_numbers, results) if is_prime]

                end_time = time.time()  # Marca o tempo de término da operação
                elapsed_time = end_time - start_time  # Calcula o tempo decorrido


                print(f"Tempo gasto MP: {elapsed_time:.4f} segundos")
                return prime_numbers

        except:
            traceback.print_exc()
            return None

    def last_news_ifbarbacena(self, news_quantity):
        urls = self.make_url_list(news_quantity)
        
        htmls = self.multithread_get_html_text(urls)
        headlines = []
        
        for html_text in htmls:
            
            soup = bs4.BeautifulSoup(html_text,'html.parser')
            news = soup.find_all('a',{'class':'summary url'})
            for article in news:
                headlines.append(article.text)
                news_quantity-=1
                if news_quantity == 0:
                    break
        return headlines


    def make_url_list(self,news_quantity):
        url_list = []
        for number in range(news_quantity // 20 + 1):
            url_list.append(f'{fiu.URL_NEWS_IF_BQ}{number * 20}')
        return url_list

    def get_html_text(self, url):
        try:
            return requests.get(url).text
        except:
            return None

    def multithread_get_html_text(self,url_list):
        MAX_THREADS = os.cpu_count()
        with cf.ThreadPoolExecutor(MAX_THREADS) as executor:
            htmls = executor.map(self.get_html_text,url_list)
        
        return list(htmls)
    
    def make_number_list(self,start: int, end: int, step: int = 1) -> List[int]:
        if step == 0:
            raise ValueError("O passo não pode ser zero.")
        
        if step > 0:
            return [i for i in range(start, end + 1, step)]
        else:
            return [i for i in range(start, end - 1, step)]
        
    def validate_cpf(self,cpf: str) -> bool:

        """ Efetua a validação do CPF, tanto formatação quando dígito verificadores.

        Parâmetros:
            cpf (str): CPF a ser validado

        Retorno:
            bool:
                - Falso, quando o CPF não possuir o formato 999.999.999-99;
                - Falso, quando o CPF não possuir 11 caracteres numéricos;
                - Falso, quando os dígitos verificadores forem inválidos;
                - Verdadeiro, caso contrário.

        Exemplos:

        >>> validate('529.982.247-25')
        True
        >>> validate('52998224725')
        True
        >>> validate('111.111.111-11')
        False
        """

        # Verifica a formatação do CPF
        if not re.match(r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}', cpf):
            return False

        # Obtém apenas os números do CPF, ignorando pontuações
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Verifica se o CPF possui 11 números ou se todos são iguais:
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validação do primeiro dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validação do segundo dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True
    
    def write_log(self,cliente_addr,timestamp,operation,response_time):
        print('chegou')
        with open('server.log','w') as file_log:
            file_log.write(f'{cliente_addr}| {timestamp} | {operation} | {response_time}')