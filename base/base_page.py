from selenium.webdriver.common.by import By

from base.seleniumbase import SeleniumDriver

from utilities.common_function import CommonUtil

import logging
import utilities.custom_logger as cl


class BasePage(SeleniumDriver):
    log = cl.customLogger(logging.DEBUG)
    utiles = CommonUtil()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    montAndYear = "//button[@aria-label='Choose month and year']"
    previous = "//button[@aria-label='Previous 24 years']"
    next = "//button[@aria-label='Next 24 years']"
    range = "//*[@class='mat-calendar-controls']/button[1]//span[2]"
    yearList = "//*[@class='mat-calendar-body']/tr/td"

    def click_calender(self, locator, locatorType):
        self.waitForElement(locator, locatorType)
        self.ElementClick(locator, locatorType)

    def click_month_year(self, locatorType="xpath"):
        self.waitForElement(self.montAndYear, locatorType)
        self.ElementClick(self.montAndYear, locatorType)

    def click_previous_button(self, locatorType="xpath"):
        self.waitForElement(self.previous, locatorType)
        self.ElementClick(self.previous, locatorType)

    def click_next_button(self, locatorType="xpath"):
        self.waitForElement(self.next, locatorType)
        self.ElementClick(self.next, locatorType)

    def year_range(self, locatorType="xpath"):
        self.waitForElement(self.range, locatorType)
        return self.getElement(self.range, locatorType).text

    def find_year(self, lower, higher, years_list, input_year):

        if lower <= input_year <= higher:
            year_sel = self.utiles.find_year_to_select(years_list, input_year)
            year_sel.click()

        elif lower > input_year:
            print("previous")
            self.click_previous_button()
            self.year_selection(input_year)

        elif higher < input_year:
            print("Next")
            self.click_next_button()
            self.year_selection(input_year)

    def year_selection(self, input_year):
        year_range = self.year_range()
        years_list = self.elementPresenceCheck(By.XPATH, self.yearList)
        lowest_year, highest_year = self.utiles.split_string(year_range)
        self.find_year(lowest_year, highest_year, years_list, input_year)

    def month_selection(self, input_month):
        month_list = self.elementPresenceCheck(By.XPATH, self.yearList)
        month_sel = self.utiles.find_month_to_select(input_month, month_list)
        month_sel.click()

    def date_selection(self, input_date):
        date_list = self.elementPresenceCheck(By.XPATH, self.yearList)
        day_sel = self.utiles.find_date_to_select(input_date, date_list)
        day_sel.click()

    def select_date_from_calender(self, input_date, locator, locatorType="xpath"):
        if input_date is not None:
            isValidDate = self.utiles.dateValidation(input_date)
            if isValidDate:
                self.click_calender(locator, locatorType)
                self.click_month_year()
                input_day, input_month, input_year = self.utiles.split_date_fun(input_date)
                self.year_selection(str(input_year))
                self.month_selection(str(input_month))
                self.date_selection(str(input_day))
            else:
                self.log("Input date " + input_date + " is an invalid date ")
        else:
            self.log.error("Input is none")
