from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time

def get_url(zipcode):
    template = 'https://www.zillow.com/homes/{}_rb/'
    return template.format(zipcode)

def extract_data(item):  

    atag = item.div.a
    atag = 'https://zillow.com' + atag.get('href')
    
        
    try:
        price = item.find('div',{'class':'list-card-price'}).text
    except AttributeError:
        return
     
    try:
        address = item.find('address',{'class':'list-card-addr'}).text
    except:
        address = ''
    
    details = item.find_all('li',{'class':''})
    
    chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    try:
        bedrooms = details[0].text
        for i in chars:
            bedrooms = bedrooms.replace(i, '')
    except:
        bedrooms = ''
    
    try:    
        bathrooms = details[1].text
        for i in chars:
            bathrooms = bathrooms.replace(i, '')
    except:
        bathrooms = ''
    
    try:
        size = details[2].text
        for i in chars:
            size = size.replace(i, '')
            size = size.replace(' ','')
    except:
        size = ''
    
    try:
        sale_type = item.find('div',{'class':'list-card-type'}).text
    except:
        sale_type = ''
    
    data = (address, price, bedrooms, bathrooms, size, sale_type, atag)
    
    return data
    
def main(zipcode, total_pages):
    driver = webdriver.Chrome(executable_path ="/Applications/chromedriver87")
    url = 'https://www.zillow.com'
    driver.get(url)
    
    records = []
    url = get_url(zipcode)
    
    for page in range(1, total_pages+1):
        time.sleep(3)
        driver.get('https://www.zillow.com/homes/' + str(zipcode) + '_rb/' + str(page) + '_p/')
        driver.maximize_window()
        driver.get(driver.current_url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(3)
        results = soup.find_all('article',{'class':'list-card list-card_not-saved'})
        time.sleep(3)
        
        for item in results:
            record = extract_data(item)
            if record:
                records.append(record)
        time.sleep(3)
                
    driver.close()
    
    with open('/Users/noahhallberg/Desktop/WebScraping/zillow_house.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Address', 'Price', 'Bedrooms', 'Bathrooms', 'Size', 'Sale Type','URL'])
        writer.writerows(records)
