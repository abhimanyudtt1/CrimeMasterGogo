import sys

class slice(object):
    def __init__(self):
        self.q = {}

    def isSliceAvailable(self,suite):
        try :
            self.q[suite]
        except KeyError:
            return False
        return True

    def getSlice(self,suite):
        try :
            return self.q[suite]
        except KeyError :
            return None


    def freeSlice(self,index):
        sys.argv[index] = 0
        self.q[index-1] = 0

    def setSlice(self,index,value):
        self.q[index] = value

slice = slice()