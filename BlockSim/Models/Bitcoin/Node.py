from BlockSim.Models.Block import Block
from BlockSim.Models.Node import Node as BaseNode
from BlockSim.Models.Bitcoin.Transaction import LightTransaction

class Node(BaseNode):
    def __init__(self,id,hashPower):
        '''Initialize a new miner named name with hashrate measured in hashes per second.'''
        super().__init__(id)
        self.hashPower = hashPower
        self.blockchain= []
        self.transactionsPool= []
        self.blocks= 0
        self.balance= 0

    def build_block(self):
        LightTransaction.create_transactions()
        transactions = LightTransaction.execute_transactions()
        new_block = Block(transactions=transactions)
        return new_block
        
