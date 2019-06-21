from threading import Thread
import random
import time
import datetime

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

count = Counter()

count2 = Counter()

crypto_wallet = []

def go():
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
			print(token)

def seqScan():
	CHARS = "0123456789abcdefghijklmnopqrstuvwxyz"
	COIN_LEN = 6

	token = ""

	notFound = True
	
	while notFound == True:
	
		for _ in range(0, COIN_LEN):
			token += random.choice(CHARS)
			
		if (tokens[count2.value] == token):
			count.increment()
			crypto_wallet.append(token)
			notFound = False
			count2.increment()
			print(token)
			
		end = time.time()	
			
		if (end - start) > 30:
			break;
			
print("Commencing the mining program!")
wolf = False
start = time.time()

while wolf == False:
	end = time.time()

	
	t1 = Thread(target=go)
	t1.start()

	t2 = Thread(target=go)
	t2.start()
	
	t3 = Thread(target=seqScan)
	t3.start()
	t4 = Thread(target=seqScan)
	t4.start()
	
	print("Now starting Randomly Generated Hash Scan")
	
	t1.join()
	t2.join()
	
	print("Now starting sequential scan")
	
	t3.join()
	t4.join()
		
	if (end - start) > 30:
		wolf = True
		
print(count.value, " BIT's mined")


