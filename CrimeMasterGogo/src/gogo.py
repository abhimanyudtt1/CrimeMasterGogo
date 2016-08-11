import selenium.webdriver.chrome.service as service
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
from selenium.common import exceptions
os.environ['PYTHONPATH'] = os.curdir
from src.configs import parser
from src import slice

class appUI(object):
    def __init__(self):
        self.URL = parser.URL

        self.server = parser.remote_location

    def getCurrentTestSuit(self):
        import inspect
        #print inspect.stack()
        x = inspect.stack()[2][1].split('/')[-2]
        return x

    def init(self):
        if slice.isSliceAvailable(self.getCurrentTestSuit()):
            return slice.getSlice(self.getCurrentTestSuit())
        else :
            serv = service.Service(parser.chromeDriver)
            serv.start()
            # time.sleep(5) # Let the user actually see something!
            self.driver = webdriver.Remote(
                command_executor='http://%s:4444/wd/hub' % self.server,
                desired_capabilities=DesiredCapabilities.CHROME)
            print 'Loading URL : %s' % parser.URL
            self.driver.get(parser.URL)
            print 'Loading complete'
            slice.setSlice(self.getCurrentTestSuit(),self.driver)
        return self.driver

    def getStartTime(self):
        return parser.startTime

    def getEndTime(self):
        return parser.endTime


    def waiter(self,tag):
        counter = 1
        lag = parser.timeWait
        while True:
            try :
                self.driver.find_element_by_css_selector(tag)
                break
            except exceptions.NoSuchElementException :
                time.sleep(1)
                counter += 1
                if counter > int(lag) :
                    print "CheckPoint"
                    raise exceptions.NoSuchElementException
                print "Searching for the element on the screen. Element : %s" % tag
        while True:
            element = self.driver.find_element_by_css_selector(tag)
            if element.is_displayed() and element.is_enabled():
                break
                #print element.is_displayed(), element.is_enabled()
        return self.driver.find_element_by_css_selector(tag)


    def clickElement(self,element):
        counter = 0
        lag = parser.timeWait
        while True :
            counter += 1
            try :
                element.click()
                break
            except exceptions.WebDriverException :
                print "Element not clickable, Waiting to click on element %s" % element
                time.sleep(1)
                if int(counter) > int(lag):
                    print "Timeout Error"
                    raise exceptions.WebDriverException

    def login(self):
        email = self.waiter(parser.email_tag)
        email.send_keys(parser.email)
        password = self.waiter(parser.password_tag)
        password.send_keys(parser.password)
        submit = self.waiter(parser.submit)
        self.clickElement(submit)
        self.waiter(parser.explore)

    def goToInsight(self,sight):
        try :
            tag = getattr(parser,sight)
        except AttributeError :
            print "No xpath or css selector present for %s " % sight
            exit(127)
        tag = self.waiter(tag)
        self.clickElement(tag)
        self.clearAllFilters(parser.clear_all_button)

    def clearAllFilters(self,tag):
        while True :
            elements = self.driver.find_elements_by_css_selector(tag)
            if len(elements) > 1 :
                break
        elements = filter(lambda x : x.is_displayed() and x.is_enabled(),elements)
        for element in elements :
            self.clickElement(element)






appUI = appUI()

