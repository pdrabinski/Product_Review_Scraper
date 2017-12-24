from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
import random
import time
from scraper import get_reviews


def get_product_links(base_url, url_suffix,n_pages, reviews_filename, products_filename):

    """Parse through product gallery pages and get links for products. Parser only parse a tags. Might be able to remove product link list."""

    only_a_tags = SoupStrainer('a')

    j = 0 #track number of product links scraped

    for i in range(n_pages):
        url_page = base_url + str(int(i)) + url_suffix
        driver = webdriver.Firefox()
        driver.get(url_page)
        response = driver.page_source
        driver.quit()
        soup = BeautifulSoup(response, 'html.parser', parse_only=only_a_tags)
        product_links = soup.find_all('a', attrs={'class': 'ui-pl-link'})
        for a in product_links:
            time.sleep(random.randint(1,2))
            product_url = 'https://www.backcountry.com' + a.get('href')
            get_reviews(product_url, reviews_filename, products_filename)
            print(j, "Products")
            j += 1
        print("Page {} done, {} links".format(i+1, j))
    print(j, "Product Links")

if __name__ == '__main__':
    url = 'https://www.backcountry.com/arcteryx?show=all&p=reviewAverage%3A%5B1+TO+*%5D&page='

    add_on = '&nf=1'
    n_pages = 9
    products_filename = '../data/products/arcteryx_products.csv'
    reviews_filename = '../data/reviews/arcteryx_reviews.csv'
    get_product_links(url, add_on, n_pages, reviews_filename, products_filename)
