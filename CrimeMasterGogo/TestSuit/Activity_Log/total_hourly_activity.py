import os
import unittest
from src.testResults import testResults

os.environ['PYTHONPATH'] = os.curdir
from src.configs import parser
from src import gogo


class TestLoginToUI_1(unittest.TestCase):
    def test_testLogin(self):
        testResults.summary("Testing Activity : Total Hourly Activity")
        driver = gogo.appUI.init()
        gogo.appUI.login()
        gogo.appUI.goToInsight('total_hourly_activity')
        gogo.appUI.selectDate()
        gogo.appUI.waitTillLoading()
        print "Checking if URL is correct"
        expected_url = '%s/insights?insight=activityByHour&entity=activity&date=1438560000000,1441584000000' % parser.URL
        gogo.appUI.URLValidator(driver.current_url, expected_url)
        testResults.passed()