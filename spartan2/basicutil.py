import numpy as np
import spartan2.ioutil as ioutil

class IAT:
    aggiat = {}  # key:user; value:iat list
    iatpaircount = {}  # key:(iat1, iat2); value:count
    iatcount = {}  # key:iat; value:count

    def __init__(self, aggiat={}, iatcount={}):
        self.aggiat = aggiat
        self.iatcount = iatcount

    def calaggiat(self, aggts):
        'aggts: key->user; value->timestamp list'
        for k, lst in aggts.items():
            if len(lst)<2:
                continue
            lst.sort()
            iat = np.diff(lst)
            self.aggiat[k]= iat

    def save_aggiat(self, outfile):
        ioutil.saveDictListData(self.aggiat, outfile)

    def load_aggiat(self, infile):
        self.aggiat = ioutil.loadDictListData(infile, ktype=str, vtype=int)

    def getiatpairs(self):
        xs, ys = [], []
        for k, lst in self.aggiat.items():
            for i in range(len(lst)-1):
                xs.append(lst[i])
                ys.append(lst[i+1])
        return xs, ys

    def caliatcount(self):
        for k, lst in self.aggiat.items():
            for iat in lst:
                if iat not in self.iatcount:
                    self.iatcount[iat] = 0
                self.iatcount[iat] += 1

    def caliatpaircount(self):
        for k, lst in self.aggiat.items():
            if len(lst) >= 2:
                iat1 = lst[0]
                for iat2 in lst[1:]:
                    iatpair = (iat1, iat2)
                    iat1 = iat2
                    if iatpair not in self.iatcount:
                        self.iatpaircount[iatpair] = 0
                    self.iatpaircount[iatpair] += 1
            else:
                continue

    def findUsers(self, iats):
        usrlist = []
        for k, lst in self.aggiat.items():
            for iat in lst:
                if iat in iats:
                    usrlist.append(k)
        return usrlist

