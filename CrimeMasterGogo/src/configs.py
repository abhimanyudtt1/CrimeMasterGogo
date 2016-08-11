import re
import sys
import xml.etree.ElementTree as ET
import ast


class parser(object):
    def __init__(self):
        pass

    def config(self, path):
        FH = open(path,'r')
        pathmap = {}
        for line in FH :
            if line.startswith('#') or line == '\n':
                pass
            else :
                #try :
                line = re.sub('\s+','',line)
                par = re.search('([\[\]A-Za-z_\-\.0-9]+)=([\[\]:/A-Za-z_\-\.@0-9]+)',line)
                (k,v) = (par.group(1),par.group(2))
                #except Exception :
                #    print "Error in parsing configuration file.please check line : %s" % line
                #    sys.exit(127)
                setattr(self,k,v)


    def parseVariable(self, path):
        FH = open(path, 'r')
        pathmap = {}
        for line in FH:
            if line.startswith('#'):
                    pass
            else:
                line = re.sub('\s+:\s+', ':', line)
                line = re.sub('\'','',line)
                par = re.search('([\[\]\"=A-Za-z_\-\.0-9]+):([\[\]=/\" A-Za-z_\-\.@0-9]+)', line)
                (k, v) = (par.group(1), par.group(2))
                # except Exception :
                #    print "Error in parsing configuration file.please check line : %s" % line
                #    sys.exit(127)
                setattr(self, k, v)


parser = parser()
