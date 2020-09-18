from selenium import webdriver
import requests
import os

baseUrl = 'https://updates.jenkins.io/download/plugins/'

def find_page_items(driver, link):
    plugIns = []
    driver.get(link)
    lists = driver.find_elements_by_css_selector('tr a')
    for a in lists:
        url = a.get_attribute('href')
        plugIns.append(url)
    return plugIns
        
if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.binary_location = "chrome.exe"
    options.add_argument("--headless")
    chrome_driver_binary = "./chrome_driver/chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

    try:
        plugIns = find_page_items(driver, baseUrl)
        print(len(plugIns))
        for plugin in plugIns:
            vers = find_page_items(driver, plugin)
            for ver in vers:
                if '/latest/' in ver:
                    print(ver)
                    index = ver.rfind('/') + 1
                    fileName = os.path.join('./plugins/',ver[index:])
                    r = requests.get(ver, allow_redirects=True)
                    open(fileName, 'wb').write(r.content)
    finally:
        driver.quit()
