import os
import unittest
import sys
os.environ['PYTHONPATH'] = os.curdir
from src.configs import parser
import src.gogo


class TestLoginToUI_2(unittest.TestCase):

    def test_testLogin(self):
        print "test_2"
        #driver = src.gogo.appUI.init()
        #driver.get('http://www.facebook.com')
        #sys.argv[1] = driver
        #driver.quit()
        


