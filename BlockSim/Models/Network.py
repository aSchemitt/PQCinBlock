import random

class Network:
    
    # Delay for propagating blocks in the network
    def block_prop_delay():
        from BlockSim.InputsConfig import InputsConfig as p
        return random.expovariate(1/p.Bdelay)

    # Delay for propagating transactions in the network
    def tx_prop_delay():
        from BlockSim.InputsConfig import InputsConfig as p
        return random.expovariate(1/p.Tdelay)
