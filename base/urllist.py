from selenium.webdriver.chrome import webdriver

class UrlLists:

    def __init__(self, browser):
        self.browser = browser

    def getUrl(self, url):
        self.browser.get(url)
        self.browser.implicitly_wait(2)
        self.browser.maximize_window()
        self.browser.set_window_size(1920, 1080)
