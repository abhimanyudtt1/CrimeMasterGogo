class reports(object):
    def __init__(self):
        self._pas = 0
        self._fail = 0
        self._total = 0
        self._report = {}
    def passed(self,msg):
        self._pas += 1
        self._total += 1
        self._report[msg] = 1
    def failed(self,msg):
        self._fail += 1
        self._total += 1
        self._report[msg] = 0

    def getReport(self):
        return (self.pas,self.fail,self.total)
    def getFullReport(self):
        return self._report

testResults = reports()

