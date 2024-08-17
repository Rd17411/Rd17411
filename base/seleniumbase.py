import logging
import os.path
import time
import traceback
from traceback import print_stack
import utilities.custom_logger as cl
from selenium.common import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class SeleniumDriver:
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):
        filename = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotDir = "../screenshot/"
        relativeFilename = screenshotDir + filename
        currentDir = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDir, relativeFilename)
        destinationDir = os.path.join(currentDir, screenshotDir)
        try:
            if not os.path.exists(destinationDir):
                os.makedirs(destinationDir)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot save to directory : " + destinationFile)
        except:
            self.log.error("exception occurred")
            print_stack()

    def getTitle(self):
        return self.driver.title

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "tag_name":
            return By.TAG_NAME
        elif locatorType == "link_text":
            return By.LINK_TEXT
        elif locatorType == "css_selector":
            return By.CSS_SELECTOR
        elif locatorType == "class_name":
            return By.CLASS_NAME
        else:
            self.log.error(" Locator type not supported " + locatorType)
        return locatorType

    def getElement(self, locator, locatorType):
        ele = None
        try:
            locatorType = locatorType.lower()
            ByType = self.getByType(locatorType)
            ele = self.driver.find_element(ByType, locator)

        except:
            self.log.error("element not found with locator " + locator + " and locator type " + locatorType)

        return ele

    def ElementClick(self, locator, locatorType="xpath"):
        try:
            element = self.getElement(locator, locatorType)
            element.click()

        except:
            self.log.error("cannot click on element with locator " + locator + " locator type " + locatorType)
            print_stack()
            # traceback.print_exc()

    def MoveandClick(self, locator, locatorType="xpath"):
        element = self.getElement(locator, locatorType)
        ActionChains(self.driver).move_to_element(element).click(element).perform()

        # element = self.driver.execute_script("return document.getElementByXpath('locatorType');")

    def Move(self, locator, locatorType="xpath"):
        element = self.getElement(locator, locatorType)
        ActionChains(self.driver).move_to_element(element).perform()

        # element = self.driver.execute_script("return document.getElementByXpath('locatorType');")

    def Doubleclick(self, locator, locatorType="xpath"):
        element = self.getElement(locator, locatorType)
        ActionChains(self.driver).double_click(element).perform()

    def ElementClickJS(self, locator, locatorType="xpath"):
        element = self.getElement(locator, locatorType)
        self.driver.execute_script("arguments[0].click();", element)

    def alertChk(self):
        alerts = self.driver.switch_to.alert
        alerts.dismiss()

    def sendKeys(self, data, locator, locatorType="xpath"):
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(Keys.CONTROL + "a")
            element.send_keys(Keys.DELETE)
            element.send_keys(data)

        except:
            self.log.error("cannot send data on element with locator " + locator + " and locator type " + locatorType)
            print_stack()
            # traceback.print_exc()

    def isElementPresent(self, locator, locatorType="xpath"):
        try:
            ele = self.getElement(locator, locatorType)
            if ele is not None:
                element = ele
            else:
                element = False
        except:
            self.log.error("element not present with locator " + " and locator type " + locatorType)
            element = False
        return element

    def isElementTextPresent(self, locator, locatorType):
        try:
            # element = self.isElementPresent(locator, locatorType)
            # element = self.waitForElement(locator, locatorType)
            element = self.wait_for_located_element(locator, locatorType)
            if element is not None:
                element = element.text
            else:
                element = False
            return element
        except:
            self.log.error("element not present with locator " + " and locator type " + locatorType)
            return False

    def isElementVisible(self, locator, locatorType="xpath"):
        try:
            ele = self.getElement(locator, locatorType)
            if ele.is_displayed():
                return True
            else:
                return False
        except:
            self.log.error("element not present with locator " + " and locator type " + locatorType)
            return False

    def elementPresenceCheck(self, ByType, locator):
        ele_list = []
        try:
            ele_list = self.driver.find_elements(ByType, locator)
            if len(ele_list) > 0:
                return ele_list
            else:
                print("Element list is empty")
                return ele_list

        except:
            self.log.error("element not found with locator " + locator)
            return ele_list

    def waitForElement(self, locator, locatorType="xpath", timeout=80):
        element = None
        try:
            self.driver.implicitly_wait(0)
            byType = self.getByType(locatorType)
            wait = WebDriverWait(self.driver, timeout, poll_frequency=1, ignored_exceptions=[NoSuchElementException,
                                                                                             ElementNotVisibleException,
                                                                                             ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
        except:


            # print_stack()
            traceback.print_exc()


            print_stack()
            # traceback.print_exc()

        self.driver.implicitly_wait(2)
        return element

    def waitForElementPresent(self, locator, locatorType="xpath", timeout=80):
        element = None
        try:
            self.driver.implicitly_wait(0)
            byType = self.getByType(locatorType)
            wait = WebDriverWait(self.driver, timeout, poll_frequency=1, ignored_exceptions=[NoSuchElementException,
                                                                                             ElementNotVisibleException,
                                                                                             ElementNotSelectableException])
            element = wait.until(EC.invisibility_of_element((byType, locator)))
        except:

            print_stack()
            # traceback.print_exc()
        self.driver.implicitly_wait(2)
        return element

    def scroll_Down(self):
        # self.waitForElement(locator="body", locatorType="tag_name")
        time.sleep(2)
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)

    def scroll_view_element(self, locator, locatorType="xpath"):
        get_element = self.getElement(locator, locatorType)
        # get_element.send_keys(Keys.HOME)
        return get_element

    def webScroll(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(2)

    def scroll_up(self):
        time.sleep(2)
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)
        time.sleep(2)

    def press_enter(self, locator, locatorType):
        element = self.getElement(locator, locatorType)
        element.send_keys(Keys.RETURN)

    def sendKeysForFileUpload(self, data, locator, locatorType="xpath"):
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(data)

        except:
            self.log.error("cannot send data on element with locator " + locator + " and locator type " + locatorType)
            print_stack()
            # traceback.print_exc()

    def waitForElements(self, locator, locatorType="xpath", timeout=80):
        elements = None
        try:
            self.driver.implicitly_wait(0)
            byType = self.getByType(locatorType)
            wait = WebDriverWait(self.driver, timeout, poll_frequency=1, ignored_exceptions=[NoSuchElementException,
                                                                                             ElementNotVisibleException,
                                                                                             ElementNotSelectableException])
            elements = wait.until(EC.presence_of_all_elements_located((byType, locator)))
        except:

            print_stack()
            # traceback.print_exc()

        self.driver.implicitly_wait(2)
        return elements

    def waitForvisibilityOfElement(self, locator, locatorType="xpath", timeout=80):
        element = None
        try:
            self.driver.implicitly_wait(0)
            byType = self.getByType(locatorType)
            wait = WebDriverWait(self.driver, timeout, poll_frequency=1, ignored_exceptions=[NoSuchElementException,
                                                                                             ElementNotVisibleException,
                                                                                             ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((byType, locator)))
        except:

            print_stack()
            # traceback.print_exc()
        self.driver.implicitly_wait(2)
        return element

    def click_the_element(self, element):
        try:

            element.click()

        except:
            self.log.error("cannot click on element " + str(element))
            print_stack()

    def wait_for_located_element(self, locator, locatorType="xpath", timeout=80):
        element = None
        try:
            self.driver.implicitly_wait(0)
            byType = self.getByType(locatorType)
            wait = WebDriverWait(self.driver, timeout, poll_frequency=1, ignored_exceptions=[NoSuchElementException,
                                                                                             ElementNotVisibleException,
                                                                                             ElementNotSelectableException])
            element = wait.until(EC.presence_of_element_located((byType, locator)))
        except:
            print_stack()
            # traceback.print_exc()
        self.driver.implicitly_wait(2)
        return element