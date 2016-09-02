import os
import unittest
from src.testResults import testResults

os.environ['PYTHONPATH'] = os.curdir
from src.configs import parser
from src import gogo


class TestLoginToUI_1(unittest.TestCase):
    def test_testLogin(self):
        testResults.summary("Testing Brand - Percentage Of Products Discounted")
        driver = gogo.appUI.init()
        gogo.appUI.login()
        gogo.appUI.goToInsight('brand_percentage_of_products_discounted')
        gogo.appUI.selectDate()
        gogo.appUI.selectFilter('category', 'coffee maker')
        gogo.appUI.selectFilter('brand', 'coffeemaker')
        #gogo.appUI.waitTillLoading()
        print "Checking if URL is correct"
        expected_url = '%s/insights?insight=productBICC_percentOnSale&entity=sku&date=1438560000000,1441584000000&category=1&brand=Coffeemaker&mode=sku' % parser.URL
        gogo.appUI.URLValidator(driver.current_url, expected_url)
        testResults.passed()