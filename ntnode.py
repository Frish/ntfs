#encoding: utf-8

class NTNode(dict):
    def __getitem__(self,k):
        return self.setdefault(k,NTNode())


