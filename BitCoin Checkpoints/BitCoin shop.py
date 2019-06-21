#threads
from threading import Thread
import random
import time
import datetime
#queues
import requests
from re import compile, MULTILINE
from queue import Queue
from threading import Thread
import time
from simple_rest_client.api import API
import json

api = API(
	api_root_url='https://reqres.in/api/pay/',
	append_slash=True,
	json_encode_body=False,
)
api.add_resource(resource_name='pay')
task_queue = Queue()
tokens = []

class BITCoin():
    CHARS = "0123456789abcdefghijklmnopqrstuvwxyz"
    COIN_LEN = 6
	
    def __init__(self):
        for _ in range(0, 100000):
            token = ""
            for _ in range(0, self.COIN_LEN):
                token += random.choice(self.CHARS)
            tokens.append(token)
        self._tokens = set(tokens)

    _instance = None
    @staticmethod
    def getInstance():
        if not BITCoin._instance:
            BITCoin._instance = BITCoin()
        return BITCoin._instance

    def isCoin(self, token):
        return token in self._tokens

class Counter(object):
	def __init__(self):
		self.value = 0
	def increment(self):
		self.value += 1
	def decrement(self):
		self.value -= 1

count = Counter()
count2 = Counter()

crypto_wallet = []

def RandomlyGeneratedHashScan():
	CHARS = "0123456789abcdefghijklmnopqrstuvwxyz"
	COIN_LEN = 6
	
	for i in range(100000):
		# to check if value is a valid coin:
		token = ""
		
		for _ in range(0, COIN_LEN):
			token += random.choice(CHARS)
		
		if (BITCoin.getInstance().isCoin(token)):
			count.increment()
			crypto_wallet.append(token)
			task_queue.put(token)
			print(token)

def seqScan():
	CHARS = "0123456789abcdefghijklmnopqrstuvwxyz"
	COIN_LEN = 6

	token = ""

	notFound = True
	
	while (notFound == True):
	
		for _ in range(0, COIN_LEN):
			token += random.choice(CHARS)
			
		if (tokens[count2.value] == token):
			count.increment()
			crypto_wallet.append(token)
			notFound = False
			count2.increment()
			task_queue.put(token)
			print(token)
			
		end = time.time()	
			
		if (end - start) >= 5:
			break
			
print("Starting to mine BITCoin!")

wolf = False
start = time.time()

while (wolf == False):
	t1 = Thread(target=RandomlyGeneratedHashScan)
	t1.start()
	t2 = Thread(target=RandomlyGeneratedHashScan)
	t2.start()	
	t3 = Thread(target=seqScan)
	t3.start()
	t4 = Thread(target=seqScan)
	t4.start()
	
	print("Generating Hash Scan")
	
	t1.join()
	t2.join()
	
	print("Starting sequential scan")
	
	t3.join()
	t4.join()
	
	end = time.time()
	
	if (end - start) >= 5:
		break
		
print("Number of BITcoins mined", count.value)

class DownloadTask():
	def download(self):
		print(":D")

class PayDownloadTask(DownloadTask):
	def __init__(self, id):
		self.id = id
	
	def download(Self):
		item = api.pay.retrieve(self.id)
		print(item.body)

shop_list = ["Guitar", "Bass Guitar", "Piano", "Drum Kit", "Guitar Pedal", "Violin", "Flute", "Amp", "Mic"]

class WorkerThread(Thread):
	while True:
		bitCoin_hash = task_queue.get()		
		queueSize = task_queue.qsize()		
		randomItem = int(random.randint(0, len(shop_list)-1) )		
		product = shop_list[randomItem]
		payload = {"BITCoin":bitCoin_hash,"Product":product}
		r = requests.post("https://reqres.in/api/pay/", data=payload)		
		print(r.text)
		task_queue.task_done()
		
		if queueSize == 0:
			break
			
numberOfWorkerThreads = 4

for _ in range(numberOfWorkerThreads):
    t = WorkerThread()
    t.setDaemon(True)
    t.start()