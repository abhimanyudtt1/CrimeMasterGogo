from configs import parser


def getCurrentTestCase():
    import inspect
    x = inspect.stack()[2][1]
    return x

class reports(object):
    def __init__(self):
        self._total = 0
        self._report = {}
        self._lock = 0
    def passed(self):
        self._total += 1
        self._report[getCurrentTestCase()] = [self._report[getCurrentTestCase()][0],'Passed']

    def summary(self,test):
        self._total += 1
        self._report[getCurrentTestCase()] = [test,'Failed']

    def getReport(self):
        return (self.pas,self.fail,self.total)
    def getFullReport(self):
        return self._report




testResults = reports()

