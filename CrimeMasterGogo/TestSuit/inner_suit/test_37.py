import os
import unittest

os.environ['PYTHONPATH'] = os.curdir
from src.configs import parser
from src import gogo


class TestLoginToUI_1(unittest.TestCase):
    #self.old_driver = sys.argv[1]
    def test_testLogin(self):
        print "test_37"
        driver = gogo.appUI.init()
        driver.get(parser.URL)