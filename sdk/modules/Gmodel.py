import sys
import ContractManager
import json
import traceback

path = '../contracts/'

class Gmodel(object):
    def __init__(self, contract_name = 'gmodel', sol_file=path+'gmodel.sol', abi_file=path+'gmodel.abi', bin_file=path+'gmodel.bin'):

        self.contractManager = ContractManager(sol_file, abi_file, bin_file, DEBUG=True)
        # checkContractExit这个函数出问题了
        result, self.contractAddress = self.contractManager.checkContractExit(contract_name)
        if result is False:
            self.contract_abi, self.contract_info = self.contractManager.deploy()
            self.contractAddress = self.contract_info["contractAddress"]
        else:
            self.contract_abi, self.contractAddress = self.contractManager.getContractInfo(self.contractAddress)

    def set(self,weights):
        args=[weights]
        try:
            txhash = self.contractManager.transaction(self.contract_abi, self.contractAddress, 'set',args)
            return txhash
        except:
            traceback.print_exc()
            return None
        
    def get(self):
        args = []
        try:
            response = self.contractManager.call(self.contractAddress, self.contract_abi, "get", args)
            return response
        except:
            traceback.print_exc()
            return None






