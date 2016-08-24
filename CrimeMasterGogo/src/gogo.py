import selenium.webdriver.chrome.service as service
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
import os
import time
from selenium.common import exceptions
os.environ['PYTHONPATH'] = os.curdir
from src.configs import parser
from src import slice
from testResults import testResults

class appUI(object):
    def __init__(self):
        self.URL = parser.URL
        self.driver = {}

        self.server = parser.remote_location

    def getCurrentTestCase(self):
        import inspect
        x = inspect.stack()[2][1]
        return x

    def getCurrentTestSuit(self):
        import inspect
        #print inspect.stack()
        x = inspect.stack()[2][1].split('/')[-2]
        return x

    def init(self):

        if slice.isSliceAvailable(self.getCurrentTestSuit()):
            self.driver[self.getCurrentTestSuit()] = slice.getSlice(self.getCurrentTestSuit())
            #self.driver.get(parser.URL+'/explore')
            x = self.getCurrentTestSuit()
            return self.driver[self.getCurrentTestSuit()]
        else :
            serv = service.Service(parser.chromeDriver)
            serv.start()
            # time.sleep(5) # Let the user actually see something!
            self.driver[self.getCurrentTestSuit()] = webdriver.Remote(
                command_executor='http://%s:4444/wd/hub' % self.server,
                desired_capabilities=DesiredCapabilities.CHROME)
            print 'Loading URL : %s' % parser.URL
            self.driver[self.getCurrentTestSuit()].get(parser.URL)
            print 'Loading complete'
            slice.setSlice(self.getCurrentTestSuit(),self.driver[self.getCurrentTestSuit()])
        return self.driver[self.getCurrentTestSuit()]

    def getStartTime(self):
        return parser.startTime

    def getEndTime(self):
        return parser.endTime


    def waiter(self,tag,multiple = False,driver = None):
        counter = 1
        if driver == None :
            driver = self.driver[self.getCurrentTestSuit()]
        else :
            if isinstance(driver, str):
                driver = self.driver[driver]
            else:
                pass
        lag = parser.timeWait
        if not multiple:
            while True:
                try :
                    driver.find_element_by_css_selector(tag)
                    break
                except exceptions.NoSuchElementException :
                    time.sleep(1)
                    counter += 1
                    if counter > int(lag) :
                        raise exceptions.NoSuchElementException
                    print "Searching for the element on the screen. Element : %s" % tag
            while True:
                element = driver.find_element_by_css_selector(tag)
                try :
                    if element.is_displayed() and element.is_enabled():
                        break
                except exceptions.StaleElementReferenceException :
                    continue
            return driver.find_element_by_css_selector(tag)
        else :
            while True :
                FLAG = 0
                self.waiter(tag,driver=driver)
                elements = driver.find_elements_by_css_selector(tag)
                for element in elements :
                    if not (element.is_displayed() and element.is_enabled()):
                        FLAG = 1
                if not FLAG:
                    break
            return elements

    def clickElement(self,element,driver = None):
        counter = 0
        if driver == None :
            driver = self.driver[self.getCurrentTestSuit()]
        else:
            if isinstance(driver, str):
                driver = self.driver[driver]
            else:
                pass
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
        try :
            counter = 0
            suite = self.getCurrentTestSuit()
            while True :
                counter += 1
                try :
                    element = self.driver[suite].find_element_by_css_selector(parser.explore)
                    element.click()
                    break
                except exceptions.NoSuchElementException:
                    if counter > 5 :
                        raise exceptions.NoSuchElementException
                time.sleep(1)
            time.sleep(2)
            counter = 0
            while True :
                counter += 1
                try:
                    element = self.driver[suite].find_element_by_css_selector(parser.warning_message)
                    element.click()
                    break
                except exceptions.NoSuchElementException :
                    if counter > 5:
                        raise exceptions.NoSuchElementException
                time.sleep(1)
        except exceptions.NoSuchElementException:
            email = self.waiter(parser.email_tag,driver=suite)
            email.send_keys(parser.email)
            password = self.waiter(parser.password_tag,driver=suite)
            password.send_keys(parser.password)
            submit = self.waiter(parser.submit,driver= suite)
            self.clickElement(submit,driver= suite)
            self.waiter(parser.explore,driver= suite)

    def goToInsight(self,sight):
        try :
            tag = getattr(parser,sight)
        except AttributeError :
            print "No xpath or css selector present for %s " % sight
            exit(127)
        tag = self.waiter(tag,driver=self.getCurrentTestSuit())
        self.clickElement(tag,driver=self.getCurrentTestSuit())
        self.clearAllFilters(parser.clear_all_button,driver=self.getCurrentTestSuit())

    def selectDate(self,single = False):
        # To set the date on any insight page
        driver = self.getCurrentTestSuit()
        pattern = '%d-%m-%Y %H:%M:%S'
        zone = time.strftime("%z", time.gmtime())
        if zone == '+0530':
            startTime = parser.startTime + ' 5:30:00'
            endTime = parser.endTime + ' 5:30:00'
        elif zone == '+0000':
            startTime = parser.startTime + ' 0:00:00'
            endTime = parser.endTime + ' 0:00:00'

        startTime = str(int(time.mktime(time.strptime(startTime, pattern))))
        endTime = str(int(time.mktime(time.strptime(endTime, pattern))))
        elements = self.waiter(parser.date_tag,multiple=True,driver=self.getCurrentTestSuit())
        fromEle = elements[0]
        self.clickElement(fromEle,driver=driver)
        while True:
            try :
                element = self.driver[driver].find_element_by_css_selector('[from-date="%s000"]'% startTime)
                element.click()
                break
            except exceptions.NoSuchElementException :
                self.driver[driver].find_element_by_css_selector(parser.calander_left).click()
        time.sleep(2)
        self.waitTillLoading(driver=driver)
        if not single:
            while True :
                try:
                    x = str(int(endTime)- 6*86400)
                    element = self.driver[driver].find_element_by_css_selector('[from-date="%s000"]' % x )
                    element.click()
                    break
                except exceptions.NoSuchElementException:
                    self.driver[driver].find_element_by_css_selector(parser.calander_right).click()
            time.sleep(1)
        print "date selected : %s to %s " % ( parser.startTime,parser.endTime)

    def selectFilter(self,fil,text):
        self.waitTillLoading(driver=self.getCurrentTestSuit())
        repos = {'category': '#categoryFilter ',
                 'brand': '#brandFilter ',
                 'merchant': '#merchantFilter ',
                }
        try :
            tag = repos[fil]
        except KeyError :
            print "Invalid key used in selectFilter"
            exit(127)

        element = self.waiter(tag+ parser.filter_title,driver=self.getCurrentTestSuit())
        action_chains = ActionChains(self.driver[self.getCurrentTestSuit()]).move_to_element(element).perform()
        elements = self.driver[self.getCurrentTestSuit()].find_elements_by_css_selector(tag+parser.filter_clear_button)
        for element in elements:
            if element.is_displayed():
                element.click()
        if isinstance(text,str):
            self.sendKeys(tag+parser.filter_input_field,text,driver=self.getCurrentTestSuit())
            time.sleep(1)
            element = self.waiter(tag + parser.filter_select_all,driver=self.getCurrentTestSuit())
            self.clickElement(element,driver=self.getCurrentTestSuit())
            self.waitTillLoading(driver=self.getCurrentTestSuit())
        else :
            for tx in text :
                self.sendKeys(tag + parser.filter_input_field, tx,driver=self.getCurrentTestSuit())
                time.sleep(1)
                element = self.waiter(tag + parser.filter_select_all,driver=self.getCurrentTestSuit())
                self.clickElement(element,driver=self.getCurrentTestSuit())
                element = self.waiter(tag + parser.filter_input_clear_button,driver=self.getCurrentTestSuit())
                self.clickElement(element,driver=self.getCurrentTestSuit())


    def sendKeys(self,tag,text,driver = None):
        if driver == None :
            driver = self.driver[self.getCurrentTestSuit()]
        else:
            if isinstance(driver, str):
                driver = self.driver[driver]
            else:
                pass
        lag = parser.timeWait
        counter = 0
        while True:
            counter += 1
            try :
                element = self.waiter(tag,driver=driver)
                element.send_keys(text)
                break
            except exceptions.WebDriverException :
                print "Cannot access element. Waiting.. "
                time.sleep(1)
            if int(lag) < counter:
                print "Page loading timeout"
                raise exceptions.WebDriverException

    def waitTillLoading(self,driver = None):
        if driver == None:
            driver = self.driver[self.getCurrentTestSuit()]
        else:
            if isinstance(driver,str):
                driver = self.driver[driver]
            else :
                pass
        lag = parser.timeWait
        counter = 0
        while True :
            counter += 1
            try :
                driver.find_element_by_css_selector('[loading="true"]')
                print "Waiting for page to load"
                time.sleep(1)
            except exceptions.NoSuchElementException :
                if counter == 1 :
                    time.sleep(1)
                    continue
                print "Page loading complete"
                break
            if int(lag) < counter :
                print "Page loading timeout"
                raise exceptions.WebDriverException

    def clearAllFilters(self,tag,driver = None):
        if driver == None:
            driver = self.driver[self.getCurrentTestSuit()]
        else:
            if isinstance(driver, str):
                driver = self.driver[driver]
            else:
                pass
        self.waitTillLoading(driver=driver)
        while True :
            elements = driver.find_elements_by_css_selector(tag)
            if len(elements) == 0 :
                break
            elements = filter(lambda x : x.is_displayed() and x.is_enabled(),elements)
            for element in elements :
                self.clickElement(element,driver=driver)
            if len(elements) == 0:
                break

    def breakURL(self,URL):
        aAPI = URL.split('?')[1]
        filters = aAPI.split('&')
        filterAPI = {}
        for i in filters:
            filterAPI[i.split('=')[0]] = i.split('=')[1]
        return (URL.split('?')[0],filterAPI)

    def URLValidator(self,URL,sampleURL):
        # Break the URL into sub parts and verify if the URL is correct
        (aURL,afilters) = self.breakURL(URL)
        (eURL,efilters) = self.breakURL(sampleURL)
        if aURL != eURL :
            raise ValueError('Expected and actual URL in correct.\nExpected: %s \nActual: %s' % (eURL,aURL))
        for filterElement in afilters :
            try :
                efilters[filterElement]
            except KeyError :
                raise ValueError(
                    'Extra Filter found in Actual URL than the expected URL. Filter :%s \nExpected: %s \nActual: %s' % (
                        filterElement,URL,sampleURL))
        for filterElement in afilters :
            if not afilters[filterElement] in sampleURL :
                if str(filterElement).lower() == 'date':
                    if ',' in afilters[filterElement] :
                        dates = str(afilters[filterElement]).split(',')
                        if not efilters[filterElement] in dates :
                            raise ValueError(
                                'Filter value not found in Actual URL. Filter :%s \nActual: %s\nURL :%s \nActual: %s' % (
                                    filterElement, afilters[filterElement], URL, sampleURL))
                    else :
                        raise ValueError(
                            'Filter value not found in Actual URL. Filter :%s \nActual: %s\nURL :%s \nActual: %s' % (
                                filterElement, afilters[filterElement], URL, sampleURL))
                else :
                    raise ValueError(
                        'Filter value not found in Actual URL. Filter :%s \nActual: %s\nURL :%s \nActual: %s' % (
                        filterElement,afilters[filterElement],URL,sampleURL))






appUI = appUI()

