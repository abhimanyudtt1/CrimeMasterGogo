import os
import unittest
from src.testResults import testResults

os.environ['PYTHONPATH'] = os.curdir
from src.configs import parser
from src import gogo


class TestLoginToUI_1(unittest.TestCase):
    def test_testLogin(self):
        testResults.summary("Testing Screenshots : Twitter")
        driver = gogo.appUI.init()
        gogo.appUI.login()
        gogo.appUI.goToInsight('screenshots_twitter')
        gogo.appUI.selectDate()
        gogo.appUI.selectFilter('merchant', 'amazon')
        #gogo.appUI.waitTillLoading()
        print "Checking if URL is correct"
        expected_url = '%s/insights?insight=screenshotsTwitter&entity=twitter&date=1438560000000,1441584000000&merchant=6,2147483647,2147483646,2147483644,2147483645' % parser.URL
        gogo.appUI.URLValidator(driver.current_url, expected_url)
        testResults.passed()