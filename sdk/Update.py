from __init__ import ContractManager
import json
import traceback

path = './contracts/'

class Update(object):
    def __init__(self, contract_name = 'update', sol_file=path+'update.sol', abi_file=path+'update.abi', bin_file=path+'update.bin'):

        self.contractManager = ContractManager(sol_file, abi_file, bin_file, DEBUG=True)
        # checkContractExit这个函数出问题了
        result, self.contractAddress = self.contractManager.checkContractExit(contract_name)
        if result is False:
            self.contract_abi, self.contract_info = self.contractManager.deploy()
            self.contractAddress = self.contract_info["contractAddress"]
        else:
            self.contract_abi, self.contractAddress = self.contractManager.getContractInfo(self.contractAddress)

    # try, catch
    

    def set(self,weights,sum):
        args=[weights,sum]
        try:
            receipt = self.contractManager.transaction(self.contract_abi, self.contractAddress, 'set',args)
            return receipt
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
    
    def get_round(self):
        args = []
        try:
            response = self.contractManager.call(self.contractAddress, self.contract_abi, "get_round", args)
            return response
        except:
            traceback.print_exc()
            return None

    def clean(self,sum):
        args=[sum]
        try:
            receipt = self.contractManager.transaction(self.contract_abi, self.contractAddress,'clean', args)
            return receipt['transactionHash']
        except:
            traceback.print_exc()
            return None









