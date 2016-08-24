import os
import unittest
from src.testResults import testResults

os.environ['PYTHONPATH'] = os.curdir
from src.configs import parser
from src import gogo


class TestLoginToUI_1(unittest.TestCase):
    # self.old_driver = sys.argv[1]
    def test_testLogin(self):
        print "Testing Product assortment - Bar Chart"
        testResults.summary("Testing Product assortment - Bar Chart")
        print testResults.getFullReport()
        exit(0)
        driver = gogo.appUI.init()
        gogo.appUI.login()
        gogo.appUI.goToInsight('product_assortment_bar_chart')
        gogo.appUI.selectDate(single=True)
        gogo.appUI.selectFilter('category', 'coffee maker')
        print "Checking if URL is correct"
        expected_url = '%s/insights?insight=productBar&entity=sku&date=1438560000000&category=1&mode=sku' % parser.URL
        gogo.appUI.URLValidator(driver.current_url,expected_url)
        testResults.passed()
