import os
from client.bcosclient import BcosClient
from client.stattool import StatTool
from client.datatype_parser import DatatypeParser
from client.common.compiler import Compiler
from client_config import client_config
from client.bcoserror import BcosException, BcosError
from eth_utils import to_checksum_address
from client.contractnote import ContractNote
from client.common.transaction_common import TransactionCommon
from client.bcoserror import CompilerNotFound, CompileError


class ContractManager(object):

    def __init__(self, sol_file, abi_file, bin_file, DEBUG=True):
        # 实例化client
        self.client = BcosClient()
        self.sol_file = sol_file
        self.abi_file = abi_file
        self.bin_file = bin_file
        self.DEBUG = DEBUG

        self.data_parser = DatatypeParser()

        if not os.path.isfile(self.abi_file):
            self.compile()

        self.data_parser.load_abi_file(self.abi_file)


    def compile(self):
        if os.path.isfile(client_config.solc_path) or os.path.isfile(client_config.solcjs_path):
            try:
                Compiler.compile_file(self.sol_file, output_path="contracts/")
            except CompileError:
                print (CompileError)
        else:
            print (client_config.solc_path)
            print (client_config.solcjs_path)

    def checkContractExit(self, contract_name):
        #address = ContractNote.get_contract_addresses(contract_name)
        address = ContractNote.get_last(contract_name)
        if address is None:
            return False, None
        else:
            # 暂时返回低一个就可以了
            return True, address

    def getContractInfo(self, contractAddress):
        contract_abi = self.data_parser.contract_abi
        return contract_abi, contractAddress




    def deploy(self):
        contract_abi = self.data_parser.contract_abi

        # 部署合约
        if self.DEBUG:
            print("\n>>Deploy:---------------------------------------------------------------------")

        with open(self.bin_file, 'r') as load_f:
            contract_bin = load_f.read()
            load_f.close()

        contract_info = self.client.deploy(contract_bin)

        if self.DEBUG:
            print("deploy", contract_info)
            print("new address : ", contract_info["contractAddress"])

        contract_name = os.path.splitext(os.path.basename(self.abi_file))[0]
        memo = "tx:" + contract_info["transactionHash"]

        # 把部署结果存入文件备查
        ContractNote.save_address(contract_name, contract_info["contractAddress"], int(contract_info["blockNumber"], 16), memo)
        ContractNote.save_contract_address(contract_name, contract_info["contractAddress"])

        return contract_abi, contract_info

    # url = "http://47.113.185.200/group1/M00/00/00/rBjqU16nnLiASd4YAMVnXomRO6M785.mp4"
    # hashvalue = "c3c93aae6dbed266a0dc55a517960273bc0b79c5ca13afe9ca5ab2d3825540f4"
    # args = [url, hashvalue]

    def transaction(self, contract_abi, to_address, method,args):
        # 发送交易，调用一个改写数据的接口
        if self.DEBUG:
            print("\n>>sendRawTransaction:----------------------------------------------------------")
            print ("to_address", to_address)
            print ("contract_abi", contract_abi)

        receipt = self.client.sendRawTransactionGetReceipt(to_address, contract_abi, method, args)
        #receipt = self.client.sendRawTransaction(to_address, contract_abi, method, args)
        #print(receipt)
        txhash = receipt['transactionHash']

        #if self.DEBUG:
        # 解析receipt里的log
        #    print("\n>>parse receipt and transaction:----------------------------------------------------------")
        #    print("transaction hash: ", txhash)
            #logresult = self.data_parser.parse_event_logs(receipt["logs"])
            #i = 0
            #for log in logresult:
            #    if 'eventname' in log:
            #        i = i + 1
            #        print("{}): log name: {} , data: {}".format(i, log['eventname'], log['eventdata']))

        return receipt

    def call(self, contract_address, contract_abi, method, args=None):

        # 调用一下call，获取数据
        try:
            response = self.client.call(contract_address, contract_abi, method, args)
            return True, response
        except:
            import traceback
            traceback.print_exc()
            return False, "call contract error"









