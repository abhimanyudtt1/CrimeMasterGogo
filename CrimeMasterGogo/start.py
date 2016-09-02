import optparse
import os
import sys
import src.configs
import unittest
import threading
from src import slice
#import xmlrunner
#import src.HTMLTestRunner as HTML
from src.testResults import *
import time


# add here some import paths
os.environ['PYTHONPATH'] = './trial'   # Not required now, still a relic


# globals are here

def cleanDir(dir):
    for m in ['init','pyc']:
        dir = [x for x in dir if m not in x]
    return dir

def createTestDesign(path,root={}):
    dir = os.listdir(path)
    dir = cleanDir(dir)
    for file in dir:
        filepath = os.path.join(path,file)
        if os.path.isfile(filepath):
            if 'py' in file:
                try :
                    root[path.split('/')[-1]].append(file)
                except KeyError :
                    root[path.split('/')[-1]] = [file]
        else :
            try:
                root[path.split('/')[-1]].append(createTestDesign(filepath,{}))
            except KeyError :
                root[path.split('/')[-1]] = [createTestDesign(filepath,{})]
    return root


#global testSuite
testSuite = {}

def createTestSuitFromTdd(tdd,root = ''):
    for suiteName in tdd.keys():  # could also be os.walk
        for sub in tdd[suiteName]:
            if isinstance(sub,dict):
                if root == '':
                    createTestSuitFromTdd(sub,root = suiteName+'.'+sub.keys()[0])
                else :
                    createTestSuitFromTdd(sub, root = root+'.'+sub.keys()[0])
            else :
                if root == '':
                    root = suiteName
                if '.py' in sub.lower():
                    try :
                        testSuite[root].append(unittest.defaultTestLoader.loadTestsFromName(root+'.'+sub.split('.')[0]))
                    except KeyError :
                        __import__(root+'.'+sub.split('.')[0])
                        testSuite[root] = [unittest.defaultTestLoader.loadTestsFromName(root+'.'+sub.split('.')[0])]

def checkOperatingSystem(configFile):
    # To check the operating system and to determine which chrome driver is to be used accordingly
    import platform

    if 'darwin' in platform.version().lower():
        FH = open(configFile,'r')
        li = []
        for line in FH :
            if 'chromeDriver' in line :
                li.append('chromeDriver = ./extensions/mac/chromedriver\n')
                os = 'mac'
            else :
                li.append(line)
        FI = open(configFile,'w')
        for line in li :
            FI.write(line)

    elif 'ubuntu' in platform.version().lower() :
        FH = open(configFile, 'r')
        li = []
        for line in FH:
            if 'chromeDriver' in line:
                li.append('chromeDriver = ./extensions/ubuntu/chromedriver\n')
                os = 'ubuntu'
            else:
                li.append(line)
        FI = open(configFile, 'w')
        for line in li:
            FI.write(line)

    return os
def StartSeleniumServer(os):

    if os == 'mac':
        cmd = 'java -Dwebdriver.chrome.driver=./extensions/mac/chromedriver -jar ./extensions/jars/selenium-server-standalone-3.0.0-beta1.jar 1>./selenium_logs 2>./selenium_logs &'
    elif os == 'ubuntu' :
        cmd = 'java -Dwebdriver.chrome.driver=./extensions/ubuntu/chromedriver -jar ./extensions/jars/selenium-server-standalone-3.0.0-beta1.jar 1>./selenium_logs 2>./selenium_logs &'

    import subprocess
    subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)


def StopSeleniumServer():
    cmd = 'ps -ef | grep selenium | grep -v grep | awk \'{print $2}\' | xargs kill -9'
    import subprocess
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()



def main():  # The stating function

    parse = optparse.OptionParser()
    parse.add_option("-t", "--testSuit", dest="suit",
                  help="Give path of the test Suit folder here. Each folder in itself will be treated as a sub testSuit.Each py file will be taken up as testcase which may or may not have smaller specs in it")

    parse.add_option("-c",'--config',dest='config',
                  help='To provide config files')
    parse.add_option('-v','--variable-list',dest='variable',
                  help='To define a file that will give a list of variables that may or maynot be used in the check pointing scripts')
    parse.add_option("-s",'--singleTest',dest='test',
                     help='To give a Single Test case to run')
    parse.add_option('-r','--report',dest='report',
                     help='Directory in which reports need to be generated')

    
    (options,args) = parse.parse_args()

    if not (options.suit or options.config or options.variable) or not(options.test or options.config or options.variable ):
        print "Invalid syntax."
        parse.print_help()
        sys.exit(1)
    import os
    if options.report :
        if not os.path.exists(options.report):
            os.mkdir(options.report)
    os = checkOperatingSystem(options.config)
    src.configs.parser.config(options.config)
    src.configs.parser.parseVariable(options.variable)

    return (options.suit,options.test,options.report)

def reportFileCreate(i,report):
    import re
    if not isinstance(i,str):
        i = str(i)
    li = i.split(' ')
    index = len(li)
    while True :
        index -= 1
        if 'testMethod' in li[index] :
            break
    fileName = re.search('tests=\[\<([A-Za-z_\-\.1-9]+)', li[index-1]).group(1)
    return '/'.join([report,fileName])

# MAIN STARTS HERE #####################

(path,singleTest,report) = main()

# Now checking if test suit path exits in config or in cmd argument
# More priority given to command line argument
# In case single test is present then no path is taken even from the config file

if singleTest and path:
    print "Both single test and test suit cannot be run. Please give one option only. Exiting.. "
    sys.exit(127)
elif singleTest and not path :
    path = singleTest
elif not (singleTest or path) and src.configs.parser.path :
    path = src.configs.parser.path
elif path and not singleTest :
    pass
else :
    print "No test subject given to run. Exiting.."
    sys.exit(127)

try :
    l = os.listdir(path)
except OSError as e :
    if e.args[1] == 'Not a directory' :
        l = ['%s' % path.split('/')[-1]]
    elif e.args[1] == 'No such file or directory':
        if singleTest :
            print "In valid Test Case file provided"
            exit(127)
        else :
            print "Invalid Test Suit provided"
            exit(128)



tdd = createTestDesign(path)
createTestSuitFromTdd(tdd)


threads = []
for i in testSuite.values():
    if report == None :
        report = sys.stderr
    reportFile = reportFileCreate(i,report)
    i = unittest.TestSuite(i)
    t = threading.Thread(target=unittest.TextTestRunner(stream=sys.stderr).run,args=(i,))
    threads.append(t)
    t.start()

while not threading.active_count() == 1:
    time.sleep(1)


outfile = open('./report','w')

outfile.write('%s' % testResults.getFullReport())
outfile.close()

slice.freeSliceAll()

