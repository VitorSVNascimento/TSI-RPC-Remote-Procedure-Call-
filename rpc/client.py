class Client:
    def __init__(self,ip,port) -> None:
        self.ip = ip
        self.port = port
        self.conection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conection.connect((self.ip,self.port))
        self.cache = self.read_cache()
        if 'time' not in self.cache:
            self.cache['time'] = 0
        self.time = 0
    


    def process_request(self,req):
        req_str = json.dumps(req)

        if req['operation'] == LAST_NEWS:
            cache_news = self.get_last_news_cache(req['args'])
            if cache_news != None: 
                print('veio do cache')
                return cache_news
        else:
            if req_str in self.cache:
                response = self.cache[req_str]

                return response

        self.conection.send(req_str.encode(crpc.ENCODE))
        response = self.__get_response()
        
        if req['operation'] == LAST_NEWS:
            self.add_cache_register(req['operation'],response)
        else:    
            self.add_cache_register(req_str,response)
        self.check_time()
        print('nao veio do cache')
        return response

    def get_last_news_cache(self,news_quantity):
        try:
            if (time.time() - self.cache['time']) >= (5 * 60):
                if LAST_NEWS in self.cache:
                    del self.cache[LAST_NEWS]
                self.cache['time'] = time.time()
                
                return None
            if len(self.cache[LAST_NEWS]) < news_quantity:
                del self.cache[LAST_NEWS]
                return None
            return self.cache[LAST_NEWS][:news_quantity]
        except:
            traceback.print_exc()
            return None
        pass


    def add_cache_register(self,req,response):
        if len(self.cache) == MAX_REGISTER_IN_CACHE:
            self.remove_oldest_register()
        self.cache[req] = response

    def remove_oldest_register(self):
        oldest_register = next(iter(self.cache))
        del self.cache[oldest_register]

    def check_time(self):
        if time.time() - self.time >= TIME_LIMIT:
            self.time = time.time()
            self.write_cache()

    def sum(self,numbers:tuple) -> float:
        req = self.__prepare_request(SUM,numbers)
        return self.process_request(req)

    def subtract(self,numbers:tuple) -> float:
        req = self.__prepare_request(SUB,numbers)
        return self.process_request(req)
    
    def divide(self,numbers:tuple) -> float:
        req = self.__prepare_request(DIV,numbers)
        return self.process_request(req)
    
    def multiply(self,numbers:tuple) -> float:
        req = self.__prepare_request(MUL,numbers)
        return self.process_request(req)

    def is_prime(self,start:int,end:int,step:int) -> List[int]:
        numbers = (start,end,step)
        req = self.__prepare_request(IS_PRIME,numbers)
        return self.process_request(req)

    def last_news_ifbarbacena(self,quantity_news:int) -> List:
        req = self.__prepare_request(LAST_NEWS,quantity_news)
        return self.process_request(req)
        pass

    def read_cache(self):
        try:
            if not os.path.exists(CACHE_FILE):
                file = open(CACHE_FILE,'w')
                file.close()
                return {}
            with open(CACHE_FILE,'rb') as file:
                if os.path.getsize(CACHE_FILE) == 0:
                    return {}
                cache = pickle.load(file)
                return cache
        except TypeError as e:
            print('O arquivo esta vazio')
            traceback.print_exc()
            return {}


    def __get_response(self):
        response_data = receive_complete_message(self.conection)
        return json.loads(response_data.decode(crpc.ENCODE))

    def write_cache(self):
        with open(CACHE_FILE, 'wb') as file:
            pickle.dump(self.cache, file)

    def __del__(self) -> str:
        self.conection.send(json.dumps(self.__prepare_request(END,())).encode())
        self.write_cache()
        return 


    pass