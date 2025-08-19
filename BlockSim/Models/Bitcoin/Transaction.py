import random
import copy
import operator
from BlockSim.Models.Network import Network

class Transaction(object):
    def __init__(self,
                 id=0,
                 timestamp=0 or [],
                 sender=0,
                 to=0,
                 value=0,
                 size=0.000546,
                 fee=0,
                 creation_time = 0.0,
                 verification_time = 0.0):

        self.id = id
        self.timestamp = timestamp
        self.sender = sender
        self.to = to
        self.value = value
        self.size = size
        self.fee = fee
        self.creation_time = creation_time
        self.verification_time = verification_time

class LightTransaction():
    pool = []

    def create_transactions():
        from BlockSim.InputsConfig import InputsConfig as p
        LightTransaction.pool = []
        Psize = int(p.Tn * p.Binterval)

        for i in range(Psize):
            tx = Transaction()
            tx.id = random.randrange(100000000000)
            tx.sender = random.choice(p.NODES).id
            tx.to = random.choice(p.NODES).id
            tx.creation_time = calculate_creation_time()
            tx.verification_time = calculate_verification_time()
            LightTransaction.pool += [tx]

        random.shuffle(LightTransaction.pool)

    def execute_transactions():
        size = 0
        for tx in LightTransaction.pool:
            size += tx.size
        return LightTransaction.pool, size

class FullTransaction():

    def create_transactions():
        from BlockSim.InputsConfig import InputsConfig as p
        Psize= int(p.Tn * p.simTime)

        for i in range(Psize):
            tx= Transaction()

            tx.id= random.randrange(100000000000)
            creation_time= random.randint(0,p.simTime-1)
            receive_time= creation_time
            tx.timestamp= [creation_time,receive_time]
            sender= random.choice (p.NODES)
            tx.sender = sender.id
            tx.to= random.choice (p.NODES).id
            tx.size= random.expovariate(1/p.Tsize)
            tx.fee= random.expovariate(1/p.Tfee)
            tx.creation_time = calculate_creation_time()
            tx.verification_time = calculate_verification_time()

            sender.transactionsPool.append(tx)
            FullTransaction.transaction_prop(tx)

    def transaction_prop(tx):
        from BlockSim.InputsConfig import InputsConfig as p
        from BlockSim.Models.Network import Network
        for i in p.NODES:
            if tx.sender != i.id:
                t= copy.deepcopy(tx)
                t.timestamp[1] = t.timestamp[1] + Network.tx_prop_delay()
                i.transactionsPool.append(t)

    def execute_transactions(miner,currentTime):
        from BlockSim.InputsConfig import InputsConfig as p
        transactions= []
        size = 0
        count=0
        blocksize = p.Bsize
        miner.transactionsPool.sort(key=operator.attrgetter('fee'), reverse=True)
        pool= miner.transactionsPool

        while count < len(pool):
                if  (blocksize >= pool[count].size and pool[count].timestamp[1] <= currentTime):
                    blocksize -= pool[count].size
                    transactions += [pool[count]]
                    size += pool[count].size
                count+=1

        return transactions, size

def calculate_creation_time():
    mean = 113086.11
    standard_deviation = 52726.01806856582
    return random.gauss(mu=mean, sigma=standard_deviation)

def calculate_verification_time():
    from BlockSim.InputsConfig import InputsConfig as p
    return random.gauss(mu=p.mean_verify, sigma=p.std_verify)
