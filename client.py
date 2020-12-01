import sys
from sdk.client.bcosclient import BcosClient
from sdk.client.datatype_parser import DatatypeParser
from sdk.client.contractnote import ContractNote
import json
import time
from sdk.client.channel_push_dispatcher import ChannelPushHandler
from sdk.client.event_callback import BcosEventCallback
from sdk.client.event_callback import EventCallbackHandler
from sdk.client_config import client_config
from sdk  import ContractFactory
from event import EventCallbackImpl01

class Client():
    def __init__(self,id,model,contract_factory):
        self.id = id 
        self.model = model
        self.Gmodel = contract_factory.getGmodel()
        self.Update = contract_factory.getUpdate()
        self.cur_round = 1
    
    def start(self):
        print('client'+self.i+"start")

        bcos_event = BcosEventCallback()
        bcos_event.setclient(BcosClient())

        cn = ContractNote()
        address = cn.get_last(contractname)

        abifile = "python-sdk/contracts/gmodel.abi"
        abiparser = DatatypeParser(abifile)

        eventcallback01 = EventCallbackImpl01(self.model,self.Update,self.Gmodel,self.cur_round)

        eventcallback01.abiparser = abiparser

        print("register events")

        result = bcos_event.register_eventlog_filter(
            eventcallback01, abiparser, [address], modelUpdate, indexed_value)

        print(
            "after register ,event_name:{},result:{},all:{}".format(
                event_name,
                result['result'], result))

        #获取全局模型轮次
        cur_round = self.Gmodel.get()[1][0]

        while(cur_round<5):
            print("client "+self.i+"waiting gmodel_update...")
            time.sleep(10)
