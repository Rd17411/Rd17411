from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service


class WebDriverFactory:
    def __init__(self, browser):
        self.browser = browser

    def getWebDriverInstance(self, baseurl):
        # baseurl = "https://devgovtportal.feathersoft.local/login"
        # baseurl = ReadConfig.getApplicationUrl()
        if self.browser == 'chrome':
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        elif self.browser == 'firefox':
            # driver = webdriver.Firefox(
            #     executable_path="C:\\Users\\saranya.tv\\Downloads\\geckodriver-v0.31.0-win64\\geckodriver.exe")
            driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
            driver = webdriver.Firefox(
                executable_path="C:\\Users\\saranya.tv\\Downloads\\geckodriver-v0.31.0-win64\\geckodriver.exe")
        elif self.browser == 'edge':
            driver = webdriver.Ie()
        else:
            driver = webdriver.Firefox()

        options = webdriver.ChromeOptions()
        p = {"download.default_directory": r"C:\Users\praveen.sebastian\Downloads",
             "download.prompt_for_download": False,
             "download.directory_upgrade": True, "plugins.always_open_pdf_externally": True}
        options.add_experimental_option("prefs", p)
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver.implicitly_wait(3)
        driver.maximize_window()
        driver.get(baseurl)
        return driver
