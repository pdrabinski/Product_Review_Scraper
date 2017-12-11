from bs4 import BeautifulSoup
# from scraper import AppURLopener
from selenium import webdriver
import random
import time
from scraper import get_reviews


url = 'https://www.backcountry.com/mens-climb-jackets?p=brand%3AArc%27teryx%7Cbrand%3AMarmot%7Cbrand%3APatagonia%7Cbrand%3AOutdoor%5C+Research%7Cbrand%3AThe%5C+North%5C+Face&page='

add_on = '&nf=1'

product_link_list = []

for i in range(5):
    url_page = url + str(int(i)) + add_on
    driver = webdriver.Firefox()
    driver.get(url_page)
    response = driver.page_source
    driver.quit()
    soup = BeautifulSoup(response, 'html.parser')
    product_links = soup.find_all('a', attrs={'class': 'ui-pl-link'})
    j = 0
    for a in product_links:
        time.sleep(random.randint(1,2))
        product_url = 'https://www.backcountry.com' + a.get('href')
        product_link_list.append(product_url)
        get_reviews(product_url, '../data/reviews.csv', '../data/products.csv')
        print(j, "Products")
        j += 1
    print("Page {} done, {} links".format(i, len(product_link_list)))

print(product_link_list)
print(len(product_link_list), "Product Links")
