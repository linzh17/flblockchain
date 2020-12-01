from Update import Update
from Gmodel import Gmodel

class ContractFactory(object):

    def __init__(self):
        self.update = Update()
        self.gmodel = Gmodel()

    def getUpdate(self):
        return self.update

    def getGmodel(self):
        return self.gmodel
