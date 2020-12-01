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
from sdk.moduels.contractFactory import ContractFactory
import pickle
import numpy as np
class EventCallbackImpl01(EventCallbackHandler):
    """sample event push handler for application level,
    user can make a class base on "ChannelPushHandler" ,implement the on_push interface
    handle the message from nodes,message in ChannelPack type #see client/channelpack.py
    EVENT_LOG_PUSH type is 0x1002
    message in pack.data decode by utf-8
    EVENT_LOG  format see https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/docs/sdk/java_sdk.html#id19
    """
    abiparser: DatatypeParser = None

    def __init__(self,model,Update,Gmodel,round):
        self.model = model
        self.Update = Update
        self.Gmodel = Gmodel
        self.round = round

    def on_event(self, eventdata):
        loglist = self.abiparser.parse_event_logs(eventdata["logs"])
        print("- FilterID >>> ", eventdata["filterID"])
        print(
            "--------------------EventCallbackImpl01--------------------\n",
            json.dumps(loglist, indent=4))

        # 获取weights
        #xxxx
        print('client is getting weights')
        weights = pickle.loads(loglist[0]['eventdata'][1])
       
        self.model.set_weights(weights)

        print("client starts training")
        self.model.start()
        
        #获取 Update and Update sum 
        
        print("client updates weights")

        update = np.array(self.model.weights)

        update_sum = self.Update.get()[1][0]
        update_sum = pickle.loads(update_sum)
        update_sum = np.array(update_sum)

        update_sum =  update + update_sum

        update = update.tolist()
        update_sum = update_sum.tolist()

        self.Update.set(update,update_sum)
        cur_round = self.Update.get_round()[1][0]
        
        # 获取Update.set () 返回值 round 
        if self.round != cur_round:
            print("Gmodel is updating")
            update_sum = self.Update.get()[1][0]
            update_sum = pickle.loads(update_sum)
            update_sum = np.array(update_sum)

            #进行weights平均计算
            print("averaging update_sum")
            weights = update_sum /5
            weights = weights.tolist()
            weights = pickle.dumps(weights)
            
            #update_sum 清零
            print("init update_sum")
            update_sum = update_sum-update_sum
            update_sum = update_sum.tolist()
            update_sum = pickle.dumps(update_sum)
            self.Update.clean(update_sum)

            #更新全局模型
            self.Gmodel.set(weights)
            print("Gmodel has updated ")
        
