from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager



def checkTitle(div_content):
    soup = BeautifulSoup(div_content, 'html.parser')
    return div_content

def retrieveTitle(div_content):
    soup = BeautifulSoup(div_content, 'html.parser')
    h2_tags = soup.find_all('h2')

    for h2_tag in h2_tags:
        anchor_tag = h2_tag.find('a')
        if anchor_tag:
            span_tag = anchor_tag.find('span')
            if span_tag:
                return span_tag.text.strip()

    return ""

def retrievePrice(div_content):
    soup = BeautifulSoup(div_content, 'html.parser')
    price_span = soup.find('span', class_='a-price')
    if price_span:
        price_whole_span = price_span.find('span', class_='a-price-whole')

        if price_whole_span:
            return price_whole_span.text.strip()
    return ""

def retrieveReview(div_content):
    soup = BeautifulSoup(div_content, 'html.parser')
    reviewText = soup.find('span', class_='a-icon-alt')
    if reviewText:
        return reviewText.text.strip().split()[0]

    return "No review yet"


def htmlFetch(item):
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    if(len(item.split())!=1):
        item = "+".join(item.split())
    wait = WebDriverWait(driver, 10)
    url="https://www.amazon.in/s?k="+item+"&ref=nb_sb_noss_2"
    driver.get(url)
    get_url = driver.current_url
    wait.until(EC.url_to_be(url))
    if get_url == url:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        divs = soup.find_all('div', {'data-index': lambda x: x and int(x) > 3 and int(x) < 32})
        div_contents = [str(div) for div in divs]
        return div_contents


def main(item):
    # item = input("Enter the item: ")
    html_content = htmlFetch(item)
    data = []
    fData = ""
    if html_content:
        for div_content in enumerate(html_content, start=1):
            div_content = div_content[1]
            title = retrieveTitle(div_content)
            if title != "":
                price = retrievePrice(div_content)
                review = retrieveReview(div_content)
                fData += "Title : " + title + "\n"
                fData += "Price : " + price + "\n"
                fData += "Review : " + review + "/5" + "\n<hr>"
                data.append([title, price, review])
                fData += "\n "

    return fData
