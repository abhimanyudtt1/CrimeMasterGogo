import os
import unittest
from src.testResults import testResults

os.environ['PYTHONPATH'] = os.curdir
from src.configs import parser
from src import gogo


class TestLoginToUI_1(unittest.TestCase):
    def test_testLogin(self):
        testResults.summary("Testing Product assortment - Pie Chart")
        driver = gogo.appUI.init()
        gogo.appUI.login()
        gogo.appUI.goToInsight('product_assortment_pie_chart')
        gogo.appUI.selectDate(single=True)
        gogo.appUI.selectFilter('category', 'coffee maker')
        gogo.appUI.waitTillLoading()
        print "Checking if URL is correct"
        expected_url = '%s/insights?insight=productPie&entity=sku&date=1438560000000&category=1&mode=sku' % parser.URL
        gogo.appUI.URLValidator(driver.current_url, expected_url)
        testResults.passed()