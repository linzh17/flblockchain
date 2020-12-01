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

    def __init__(self,model,Update,Gmodel,round,fdfs):
        self.model = model
        self.Update = Update
        self.Gmodel = Gmodel
        self.round = round
        self.fdfs = fdfs

    def on_event(self, eventdata):
        loglist = self.abiparser.parse_event_logs(eventdata["logs"])
        print("- FilterID >>> ", eventdata["filterID"])
        #print(
        #    "--------------------EventCallbackImpl01--------------------\n",
        #    json.dumps(loglist, indent=4))

        # 获取weights
        #xxxx
        print('client is getting weights')
        self.round = self.Gmodel.get_round()[1][0]
        w_id = pickle.loads(loglist[0]['eventdata'][1])
        print(w_id)
        weights = self.fdfs.get(w_id)
        weights = pickle.loads(weights)

        self.model.set_weights(weights)

        print("client starts training")
        self.model.start()
        
        #获取 Update and Update sum 
        
        print("client updates weights")

        update = np.array(self.model.weights)

        us_id = self.Update.get()[1][0]
        us_id = pickle.loads(us_id)

        update_sum = self.fdfs.get(us_id)
                

        update_sum = pickle.loads(update_sum)
        print(update_sum)
        update_sum = np.array(update_sum)

        update_sum =  update + update_sum

        update = update.tolist()
        update_sum = update_sum.tolist()

        u_id = self.fdfs.up(pickle.dumps(update))
        u_id = pickle.dumps(u_id)

        us_id = self.fdfs.up(pickle.dumps(update_sum))
        us_id = pickle.dumps(us_id)

        self.Update.set(u_id,us_id)
        cur_round = self.Update.get_round()[1][0]
        print(cur_round)        
        # 获取Update.set () 返回值 round 
        if self.round != cur_round:
            print("Gmodel is updating")
            us_id = self.Update.get()[1][0]
            us_id = pickle.loads(us_id)

            update_sum = self.fdfs.get(us_id)
            update_sum = pickle.loads(update_sum)
            update_sum = np.array(update_sum)

            #进行weights平均计算
            print("averaging update_sum")
            weights = update_sum /2
            weights = weights.tolist()
            weights = pickle.dumps(weights)

            w_id = self.fdfs.up(weights)
            w_id = pickle.dumps(w_id)
            
            #update_sum 清零
            print("init update_sum")
            update_sum = update_sum-update_sum
            update_sum = update_sum.tolist()
            update_sum = pickle.dumps(update_sum)

            us_id = self.fdfs.up(update_sum)
            us_id = pickle.dumps(us_id)
            self.Update.clean(us_id)

            #更新全局模型
            self.Gmodel.set(w_id)
            print("Gmodel has updated ")
        

