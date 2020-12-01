from fdfs_client.client import *

client_conf = get_tracker_conf(r'/root/flblockchain/client.conf')

class Fdfs(object):
    def __init__(self):
        self.client  = Fdfs_client(client_conf)

    def get(self,file_id):
        buffer = self.client.download_to_buffer(file_id)
        #return weights (bytes)
        return buffer['Content']

    def up(self,weights):
        ret = self.client.upload_by_buffer(weights)
        #return file id
        return ret['Remote file_id']
