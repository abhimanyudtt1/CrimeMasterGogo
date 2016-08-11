import optparse
import os
import sys
import src.configs
import unittest
import threading



# add here some import paths
os.environ['PYTHONPATH'] = './TestSuit'   # Not required now, still a relic


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
                    print "Sub",sub
                    createTestSuitFromTdd(sub,root = suiteName+'.'+sub.keys()[0])
                else :
                    createTestSuitFromTdd(sub, root = root+'.'+suiteName+'.'+sub.keys()[0])
            else :
                if root == '':
                    root = suiteName
                if '.py' in sub.lower():
                    try :
                        testSuite[root].append(unittest.defaultTestLoader.loadTestsFromName(root+'.'+sub.split('.')[0]))
                    except KeyError :
                        testSuite[root] = [unittest.defaultTestLoader.loadTestsFromName(root+'.'+sub.split('.')[0])]




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

    
    (options,args) = parse.parse_args()

    if not (options.suit or options.config or options.variable) or not(options.test or options.config or options.variable ):
        print "Invalid syntax."
        parse.print_help()
        sys.exit(1)
    src.configs.parser.config(options.config)
    src.configs.parser.parseVariable(options.variable)

    return (options.suit,options.test,options.variable)


(path,singleTest,variable) = main()

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
    i = unittest.TestSuite(i)
    t = threading.Thread(target=unittest.TextTestRunner().run,args=(i,))
    threads.append(t)
    t.start()