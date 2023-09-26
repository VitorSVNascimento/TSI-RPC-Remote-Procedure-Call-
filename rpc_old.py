import socket
import threading
import json
import multiprocessing as mp
import traceback
import time
import os
import pickle
import bs4
import requests

from functools import reduce
import concurrent.futures as cf
from typing import Callable,Dict,List

import mathOperations
import constRPC as crpc

SUM = '__SUM__'
SUB = '__SUB__'
MUL = '__MUL__'
DIV = '__DIV__'
END = '__END__'
IS_PRIME = '__IS_PRIME__'
MP_IS_PRIME = '__MP_IS_PRIME'
LAST_NEWS = '__LAST_NEWS__'
CACHE_FILE = './cache/dict.cache'
URL_NEWS_IF_BQ = 'https://www.ifsudestemg.edu.br/noticias/barbacena/?b_start:int='
MAX_REGISTER_IN_CACHE = 5
TIME_LIMIT = 1





class Client:
   pass
    
