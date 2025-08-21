
import os

class InputsConfig:

    """ Seclect the model to be simulated.
    0 : The base model
    1 : Bitcoin model
    2 : Ethereum model
    3 : AppendableBlock model
    """
    model = 2
    

def set_model(model):
    InputsConfig.model = model
    ''' Input configurations for the base model '''
    if model == 0:

        ''' Block Parameters '''
        InputsConfig.Binterval = 600  # Average time (in seconds)for creating a block in the blockchain
        InputsConfig.Bsize = 1.0  # The block size in MB
        InputsConfig.Bdelay = 0.42  # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        InputsConfig.Breward = 12.5  # Reward for mining a block

        ''' Transaction Parameters '''
        InputsConfig.hasTrans = True  # True/False to enable/disable transactions in the simulator
        InputsConfig.Ttechnique = "Light"  # Full/Light to specify the way of modelling transactions
        InputsConfig.Tn = 10  # The rate of the number of transactions to be created per second
        # The average transaction propagation delay in seconds (Only if Full technique is used)
        InputsConfig.Tdelay = 5.1
        InputsConfig.Tfee = 0.000062  # The average transaction fee
        InputsConfig.Tsize = 0.000546  # The average transaction size  in MB

        ''' Node Parameters '''
        InputsConfig.Nn = 3  # the total number of nodes in the network
        InputsConfig.NODES = []
        from BlockSim.Models.Node import Node
        # here as an example we define three nodes by assigning a unique id for each one
        InputsConfig.NODES = [Node(id=0), Node(id=1)]

        ''' Simulation Parameters '''
        InputsConfig.simTime = 1000  # the simulation length (in seconds)
        InputsConfig.Runs = 2  # Number of simulation runs

    ''' Input configurations for Bitcoin model '''
    if model == 1:
        ''' Block Parameters '''
        InputsConfig.Binterval = 600  # Average time (in seconds)for creating a block in the blockchain
        InputsConfig.Bsize = 1.0  # The block size in MB
        InputsConfig.Bdelay = 0.42  # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        InputsConfig.Breward = 12.5  # Reward for mining a block

        ''' Transaction Parameters '''
        InputsConfig.hasTrans = True  # True/False to enable/disable transactions in the simulator
        InputsConfig.Ttechnique = "Light"  # Full/Light to specify the way of modelling transactions
        InputsConfig.Tn = 10  # The rate of the number of transactions to be created per second
        # The average transaction propagation delay in seconds (Only if Full technique is used)
        InputsConfig.Tdelay = 5.1
        InputsConfig.Tfee = 0.000062  # The average transaction fee
        InputsConfig.Tsize = 0.000546  # The average transaction size  in MB

        ''' Node Parameters '''
        InputsConfig.Nn = 3  # the total number of nodes in the network
        InputsConfig.NODES = []
        from BlockSim.Models.Bitcoin.Node import Node
        # here as an example we define three nodes by assigning a unique id for each one + % of hash (computing) power
        InputsConfig.NODES = [Node(id=0, hashPower=50), Node(
            id=1, hashPower=20), Node(id=2, hashPower=30)]

        ''' Simulation Parameters '''
        InputsConfig.simTime = 10000  # the simulation length (in seconds)
        InputsConfig.Runs = 2  # Number of simulation runs

        """ Other Parameters """
        InputsConfig.variant = ""
        InputsConfig.mean_verify = 0.0
        InputsConfig.std_verify = 0.0

    ''' Input configurations for Ethereum model '''
    if model == 2:

        ''' Block Parameters '''
        InputsConfig.Binterval = 12.42  # Average time (in seconds)for creating a block in the blockchain
        InputsConfig.Bsize = 1.0  # The block size in MB
        InputsConfig.Blimit = 8000000  # The block gas limit
        InputsConfig.Bdelay = 6  # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        InputsConfig.Breward = 2  # Reward for mining a block

        ''' Transaction Parameters '''
        InputsConfig.hasTrans = True  # True/False to enable/disable transactions in the simulator
        InputsConfig.Ttechnique = "Light"  # Full/Light to specify the way of modelling transactions
        InputsConfig.Tn = 20  # The rate of the number of transactions to be created per second
        # The average transaction propagation delay in seconds (Only if Full technique is used)
        InputsConfig.Tdelay = 3
        # The transaction fee in Ethereum is calculated as: UsedGas X GasPrice
        InputsConfig.Tsize = 0.000546  # The average transaction size  in MB

        ''' Drawing the values for gas related attributes (UsedGas and GasPrice, CPUTime) from fitted distributions '''

        ''' Uncles Parameters '''
        InputsConfig.hasUncles = True  # boolean variable to indicate use of uncle mechansim or not
        InputsConfig.Buncles = 2  # maximum number of uncle blocks allowed per block
        InputsConfig.Ugenerations = 7  # the depth in which an uncle can be included in a block
        InputsConfig.Ureward = 0
        InputsConfig.UIreward = InputsConfig.Breward / 32  # Reward for including an uncle

        ''' Node Parameters '''
        InputsConfig.Nn = 3  # the total number of nodes in the network
        InputsConfig.NODES = []
        from BlockSim.Models.Ethereum.Node import Node
        # here as an example we define three nodes by assigning a unique id for each one + % of hash (computing) power
        InputsConfig.NODES = [Node(id=0, hashPower=50), Node(
            id=1, hashPower=20), Node(id=2, hashPower=30)]

        ''' Simulation Parameters '''
        InputsConfig.simTime = 500  # the simulation length (in seconds)
        InputsConfig.Runs = 1  # Number of simulation runs

        """ Other Parameters """
        # Signing_Algorithm = "ECDSA384"
        # Signing_Algorithm = "Dillithium3"
        # Signing_Algorithm = "Sphincs+192f"
        
        # means_from_language = "Java"
        # means_from_language = "Python"
        # means_from_language = "C-C++"
        InputsConfig.variant = ""
        InputsConfig.mean_verify = 0.0
        InputsConfig.std_verify = 0.0

    ''' Input configurations for AppendableBlock model '''
    if model == 3:
        ''' Transaction Parameters '''
        InputsConfig.hasTrans = True  # True/False to enable/disable transactions in the simulator

        InputsConfig.Ttechnique = "Full"

        # The rate of the number of transactions to be created per second
        InputsConfig.Tn = 10

        # The maximum number of transactions that can be added into a transaction list
        InputsConfig.txListSize = 100

        ''' Node Parameters '''
        # Number of device nodes per gateway in the network
        InputsConfig.Dn = 10
        # Number of gateway nodes in the network
        InputsConfig.Gn = 2
        # Total number of nodes in the network
        InputsConfig.Nn = InputsConfig.Gn + (InputsConfig.Gn*InputsConfig.Dn)
        # A list of all the nodes in the network
        InputsConfig.NODES = []
        # A list of all the gateway Ids
        InputsConfig.GATEWAYIDS = [chr(x+97) for x in range(InputsConfig.Gn)]
        from BlockSim.Models.AppendableBlock.Node import Node

        # Create all the gateways
        for i in InputsConfig.GATEWAYIDS:
            otherGatewayIds = InputsConfig.GATEWAYIDS.copy()
            otherGatewayIds.remove(i)
            # Create gateway node
            NODES.append(Node(i, "g", otherGatewayIds))

        # Create the device nodes for each gateway
        InputsConfig.deviceNodeId = 1
        for i in InputsConfig.GATEWAYIDS:
            for j in range(InputsConfig.Dn):
                InputsConfig.NODES.append(Node(InputsConfig.deviceNodeId, "d", i))
                InputsConfig.deviceNodeId += 1

        ''' Simulation Parameters '''
        # The average transaction propagation delay in seconds
        InputsConfig.propTxDelay = 0.000690847927

        # The average transaction list propagation delay in seconds
        InputsConfig.propTxListDelay = 0.00864894

        # The average transaction insertion delay in seconds
        InputsConfig.insertTxDelay = 0.000010367235

        # The simulation length (in seconds)
        InputsConfig.simTime = 500

        # Number of simulation runs
        InputsConfig.Runs = 5

        ''' Verification '''
        # Varify the model implementation at the end of first run
        InputsConfig.VerifyImplemetation = True

        InputsConfig.maxTxListSize = 0


set_model(InputsConfig.model)