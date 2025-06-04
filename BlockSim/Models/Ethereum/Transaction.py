from BlockSim.Models.Ethereum.Distribution.DistFit import DistFit
import random
from BlockSim.InputsConfig import InputsConfig as p
import numpy as np
from BlockSim.Models.Network import Network
import operator
from BlockSim.Models.Ethereum.Distribution.DistFit import DistFit

class Transaction(object):

    """ Defines the Ethereum Block model.

    :param int id: the uinque id or the hash of the transaction
    :param int timestamp: the time when the transaction is created. In case of Full technique, this will be array of two value (transaction creation time and receiving time)
    :param int sender: the id of the node that created and sent the transaction
    :param int to: the id of the recipint node
    :param int value: the amount of cryptocurrencies to be sent to the recipint node
    :param int size: the transaction size in MB
    :param int gasLimit: the maximum amount of gas units the transaction can use. It is specified by the submitter of the transaction
    :param int usedGas: the amount of gas used by the transaction after its execution on the EVM
    :param int gasPrice: the amount of cryptocurrencies (in Gwei) the submitter of the transaction is willing to pay per gas unit
    :param float fee: the fee of the transaction (usedGas * gasPrice)
    """

    def __init__(self,
	 id=0,
	 timestamp=0 or [],
	 sender=0,
         to=0,
         value=0,
	 size=0.000546,
         gasLimit= 8000000,
         usedGas=0,
         gasPrice=0,
         fee=0,
         creation_time = 0.0,
         verification_time = 0.0):

        self.id = id
        self.timestamp = timestamp
        self.sender = sender
        self.to= to
        self.value=value
        self.size = size
        self.gasLimit=gasLimit
        self.usedGas = usedGas
        self.gasPrice=gasPrice
        self.fee= usedGas * gasPrice
        # Creation time in the transaction based on benchmarks
        self.creation_time = creation_time
        self.verification_time = verification_time



class LightTransaction():

    pool=[] # shared pool of pending transactions
    #x=0 # counter to only fit distributions once during the simulation

    def create_transactions():

        LightTransaction.pool=[]
        Psize= int(p.Tn * p.Binterval)

        #if LightTransaction.x<1:
        DistFit.fit() # fit distributions
        gasLimit,usedGas,gasPrice,_ = DistFit.sample_transactions(Psize) # sampling gas based attributes for transactions from specific distribution

        for i in range(Psize):
            # assign values for transactions' attributes. You can ignore some attributes if not of an interest, and the default values will then be used
            tx= Transaction()

            tx.id= random.randrange(100000000000)
            tx.sender = random.choice (p.NODES).id
            tx.to= random.choice (p.NODES).id
            tx.gasLimit=gasLimit[i]
            tx.usedGas=usedGas[i]
            tx.gasPrice=gasPrice[i]/1000000000
            tx.fee= tx.usedGas * tx.gasPrice
            tx.creation_time = calculate_creation_time()
            tx.verification_time = calculate_verification_time()

            LightTransaction.pool += [tx]


        random.shuffle(LightTransaction.pool)


    ##### Select and execute a number of transactions to be added in the next block #####
    def execute_transactions():
        transactions= [] # prepare a list of transactions to be included in the block
        limit = 0 # calculate the total block gaslimit
        count=0
        blocklimit = p.Blimit

        pool = sorted(LightTransaction.pool, key=lambda x: x.gasPrice, reverse=True) # sort pending transactions in the pool based on the gasPrice value

        while count < len(pool):
                if  (blocklimit >= pool[count].gasLimit):
                    blocklimit -= pool[count].usedGas
                    transactions += [pool[count]]
                    limit += pool[count].usedGas
                count+=1

        return transactions, limit

class FullTransaction():
    x=0 # counter to only fit distributions once during the simulation

    def create_transactions():
        Psize= int(p.Tn * p.Binterval)

        if FullTransaction.x<1:
            DistFit.fit() # fit distributions
        gasLimit,usedGas,gasPrice,_ = DistFit.sample_transactions(Psize) # sampling gas based attributes for transactions from specific distribution

        for i in range(Psize):
            # assign values for transactions' attributes. You can ignore some attributes if not of an interest, and the default values will then be used
            tx= Transaction()

            tx.id= random.randrange(100000000000)
            creation_time= random.randint(0,p.simTime-1)
            receive_time= creation_time
            tx.timestamp= [creation_time,receive_time]
            sender= random.choice (p.NODES)
            tx.sender = sender.id
            tx.to= random.choice (p.NODES).id
            tx.gasLimit=gasLimit[i]
            tx.usedGas=usedGas[i]
            tx.gasPrice=gasPrice[i]/1000000000
            tx.fee= tx.usedGas * tx.gasPrice
            tx.creation_time = calculate_creation_time()
            tx.verification_time = calculate_verification_time()

            sender.transactionsPool.append(tx)
            FullTransaction.transaction_prop(tx)

    # Transaction propogation & preparing pending lists for miners
    def transaction_prop(tx):
        # Fill each pending list. This is for transaction propogation
        for i in p.NODES:
            if tx.sender != i.id:
                t= tx
                t.timestamp[1] = t.timestamp[1] + Network.tx_prop_delay() # transaction propogation delay in seconds
                i.transactionsPool.append(t)



    def execute_transactions(miner,currentTime):
        transactions= [] # prepare a list of transactions to be included in the block
        limit = 0 # calculate the total block gaslimit
        count=0
        blocklimit = p.Blimit
        miner.transactionsPool.sort(key=operator.attrgetter('gasPrice'), reverse=True)
        pool= miner.transactionsPool

        while count < len(pool):
                if  (blocklimit >= pool[count].gasLimit and pool[count].timestamp[1] <= currentTime):
                    blocklimit -= pool[count].usedGas
                    transactions += [pool[count]]
                    limit += pool[count].usedGas
                count+=1

        return transactions, limit

# TODO use the more acurate values
def calculate_creation_time():
    mean = 113086.11
    standard_deviation = 52726.01806856582
    return random.gauss(mu=mean,sigma=standard_deviation)

# TODO use the more acurate values
def calculate_verification_time():
    # language_algorithm = (p.means_from_language, p.Signing_Algorithm)

    # match language_algorithm:
    #     case ("Java", "ECDSA384"):
    #         mean = 0.18335970950
    #         standard_deviation = 0.01330874960
    #     case ("Java", "Dillithium3"):
    #         mean = 0.49128941910
    #         standard_deviation = 0.30889319890 
    #     case ("Java", "Sphincs+192f"):
    #         mean = 56.09813371590
    #         standard_deviation = 0.38878176013

    #     case ("Python", "ECDSA384"):
    #         mean = 0.36977098660
    #         standard_deviation = 0.00168400000
    #     case ("Python", "Dillithium3"):
    #         mean = 0.03722764010
    #         standard_deviation = 0.00059083910
    #     case ("Python", "Sphincs+192f"):
    #         mean = 0.63858025320
    #         standard_deviation = 0.00761349060

    #     case ("C-C++", "ECDSA384"):
    #         mean = 1.02015166
    #         standard_deviation = 0.005019122382
    #     case ("C-C++", "Dillithium3"):
    #         mean = 0.1111510
    #         standard_deviation = 0.06584563651

    return random.gauss(mu=p.mean_verify,sigma=p.std_verify)