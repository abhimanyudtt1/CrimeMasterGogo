import os
import unittest
from src.testResults import testResults

os.environ['PYTHONPATH'] = os.curdir
from src.configs import parser
from src import gogo


class TestLoginToUI_1(unittest.TestCase):
    def test_testLogin(self):
        testResults.summary("Testing Discount - Discounted Product Count")
        driver = gogo.appUI.init()
        gogo.appUI.login()
        gogo.appUI.goToInsight('discounted_product_count')
        gogo.appUI.selectDate(single=True)
        gogo.appUI.selectFilter('category', 'coffee maker')
        gogo.appUI.waitTillLoading()
        print "Checking if URL is correct"
        expected_url = '%s/insights?insight=productSaleNoSale&entity=sku&category=1&date=1438560000000,1441584000000&mode=sku' % parser.URL
        gogo.appUI.URLValidator(driver.current_url, expected_url)
        testResults.passed()