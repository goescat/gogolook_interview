import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


def CheckElementExist(xpath: str, timeout: int = 15) -> None:
    WebDriverWait(browser, timeout, 0.5).until(EC.visibility_of_element_located((By.XPATH, xpath)),
                                               message="Element not exist.")


def GetAnElement(xpath, timeout: int = 15):
    elem = WebDriverWait(browser, timeout, 0.5).until(EC.presence_of_element_located((By.XPATH, xpath)),
                                                      message="Element not exist.")
    return elem


def GetElements(xpath, timeout: int = 15):
    elems = WebDriverWait(browser, timeout, 0.5).until(EC.presence_of_all_elements_located((By.XPATH, xpath)),
                                                       message="Element not exist.")
    return elems


def ClickElement(xpath: str, timeout: int = 15) -> None:
    elem = WebDriverWait(browser, timeout, 0.5).until(EC.presence_of_element_located((By.XPATH, xpath)),
                                                      message="Element not exist.")
    elem.click()


def InputElement(xpath: str, text: str) -> None:
    elem = WebDriverWait(browser, 15, 0.5).until(
        EC.presence_of_element_located((By.XPATH, xpath)), message="Element not exist.")
    elem.send_keys(text)


def MoveToElement(xpath):
    elem = WebDriverWait(browser, 15, 0.5).until(EC.presence_of_element_located((By.XPATH, xpath)),
                                                 message="Element not exist.")
    action = ActionChains(browser).move_to_element(elem)
    action.perform()


curr_path = os.path.dirname(__file__)
local_path = os.path.join(curr_path, "chromedriver")

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--window-size=1440x768")

browser = webdriver.Chrome(local_path, options=options)
browser.set_page_load_timeout(20)

url = "https://www.twse.com.tw/zh/index.html"
browser.get(url)

xpath = "(//li/a[text()='交易資訊'])[2]"
ClickElement(xpath)

xpath = "(//a[@href='/zh/trading/historical/stock-day-avg.html'])[2]"
ClickElement(xpath)

xpath = "//select[@name='yy']"
ClickElement(xpath)

xpath = "//option[@value='2023']"
ClickElement(xpath)

xpath = "//select[@name='mm']"
ClickElement(xpath)

xpath = "//option[@value='1']"
ClickElement(xpath)

xpath = "//input[@name='stockNo']"
InputElement(xpath, "2330")

xpath = "//button[@class='search']"
ClickElement(xpath)

date_list = []
price_list = []

# Print
xpath = "//tr/td[1]"
date = GetElements(xpath)
for _ in date:
    date_list.append(_.text)

xpath = "//tr/td[2]"
price = GetElements(xpath)
for _ in price:
    price_list.append(_.text)

for day in zip(date_list, price_list):
    print(f"日期：{day[0]} 收盤價：{day[1]}")

# Screenshot
cmd = f"window.scrollBy(0, 350)"
time.sleep(0.5)
browser.execute_script(cmd)

cmd = "document.getElementById('toast').removeAttribute('class')"
browser.execute_script(cmd)

xpath = "//div[@id='reports']"
elem = GetAnElement(xpath)

screenshot = elem.screenshot_as_png
with open('112_Jan_stock_info.png', 'wb') as f:
    f.write(screenshot)

browser.quit()
