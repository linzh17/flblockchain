
import sys
from client.bcosclient import BcosClient
from client.datatype_parser import DatatypeParser
from client.contractnote import ContractNote
import json
import time
from client.channel_push_dispatcher import ChannelPushHandler
from client.event_callback import BcosEventCallback
from client.event_callback import EventCallbackHandler
from client_config import client_config
from event import EventCallbackImpl01
class Client():
    def __init__(self,id,model,contract_factory,fdfs):
        self.id = id 
        self.model = model
        self.Gmodel = contract_factory.getGmodel()
        self.Update = contract_factory.getUpdate()
        self.cur_round = 1
        self.fdfs = fdfs
    
    def start(self):
        print('client '+str(self.id)+" start")

        bcos_event = BcosEventCallback()
        bcos_event.setclient(BcosClient())

        cn = ContractNote()
        address = cn.get_last('gmodel')

        abifile = "contracts/gmodel.abi"
        abiparser = DatatypeParser(abifile)

        eventcallback01 = EventCallbackImpl01(self.model,self.Update,self.Gmodel,self.cur_round,self.fdfs)

        eventcallback01.abiparser = abiparser

        print("register events")

        result = bcos_event.register_eventlog_filter(
            eventcallback01, abiparser, [address], 'modelupdate', None)

        print(
            "after register ,event_name:{},result:{},all:{}".format(
                'modelupdate',
                result['result'], result))

        #获取全局模型轮次
        cur_round = self.Gmodel.get_round()[1][0]

        while(cur_round<5):
            print("the "+str(cur_round)+" th round")
            print("client "+str(self.id)+" waiting gmodel_update...")
            cur_round = self.Gmodel.get_round()[1][0]
            time.sleep(10)


