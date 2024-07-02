import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re


url = 'https://www.jumia.co.ke'
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    
    print(soup.prettify())

  
    deals_section = soup.find('section', {'class': 'item'})
    if deals_section is None:
        print("Deals section not found. Please check the class name and structure of the page.")
    else:
        products = deals_section.find_all('article', {'class': 'prdx'})

        product_data = []
        for product in products:
            product_name = product.find('h3', {'class': 'name'}).text.strip()
            brand_name = product.find('a', {'class': 'link'}).text.strip()
            price = product.find('div', {'class': 'prc'}).text.strip()
            discount = product.find('div', {'class': 'tag _dsct'}).text.strip() if product.find('div', {'class': 'tag _dsct'}) else '0%'
            reviews = product.find('div', {'class': 'rev'}).text.strip() if product.find('div', {'class': 'rev'}) else '0'
            rating = product.find('div', {'class': 'stars _s'}).text.strip() if product.find('div', {'class': 'stars _s'}) else '0'

            product_data.append([product_name, brand_name, price, discount, reviews, rating])

    
        with open('jumia_deals.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Product Name', 'Brand Name', 'Price (Ksh)', 'Discount (%)', 'Total Number of Reviews', 'Product Rating (out of 5)'])
            writer.writerows(product_data)
        
   
        df = pd.DataFrame(product_data, columns=['Product Name', 'Brand Name', 'Price (Ksh)', 'Discount (%)', 'Total Number of Reviews', 'Product Rating (out of 5)'])
        df.to_csv('jumia_deals_pandas.csv', index=False)
else:
    print('Failed to retrieve the website. Status code:', response.status_code)
