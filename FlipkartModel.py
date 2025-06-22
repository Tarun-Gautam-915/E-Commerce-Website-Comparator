from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager



def extract_data_from_divs(divs_list):
    result = []

    for div_content in divs_list:
        soup = BeautifulSoup(str(div_content), 'html.parser')
        div_4rR01T = soup.find('div', class_='_4rR01T')
        div_30jeq3 = soup.find('div', class_='_30jeq3 _1_WHN1')
        div_3LWZlK = soup.find('div', class_='_3LWZlK')

        result.append([
            div_4rR01T.text.strip() if div_4rR01T else "Name not available",
            div_30jeq3.text.strip() if div_30jeq3 else "Price not available",
            div_3LWZlK.text.strip()+"/5" if div_3LWZlK else "NA"
        ])

    return result



def htmlFetch(item):
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    if(len(item.split())!=1):
        item = "+".join(item.split())

    url="https://www.flipkart.com/search?q="+item
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    get_url = driver.current_url
    wait.until(EC.url_to_be(url))
    if get_url == url:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        divs_step1 = soup.find_all('div', class_='_1AtVbE col-12-12')
        divs_step2 = []
        for div in divs_step1:
            elem = div.find('div', class_='_13oc-S')
            if elem:
                divs_step2.append(elem)
                
        return divs_step2
    
def main(item):
    # item = input("Enter the item: ")
    html_content = htmlFetch(item)
    res = extract_data_from_divs(html_content)
    fData = ""
    for r in res:
        fData += "Name : " + r[0] + "\nPrice : " + r[1] + "\nRating : " + r[2]+"<hr>\n"

    return fData
