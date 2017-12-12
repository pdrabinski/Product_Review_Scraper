from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from selenium import webdriver
import random
import time
from scraper import get_reviews


def get_product_links(base_url, url_suffix,n_pages, reviews_filename, products_filename):

    """Crawl through product gallery pages and get links for products. Parser only parse a tags. Might be able to remove product link list."""

    product_link_list = []
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
            product_link_list.append(product_url)
            get_reviews(product_url, reviews_filename, products_filename)
            print(j, "Products")
            j += 1
        print("Page {} done, {} links".format(i+1, len(product_link_list)))

    print(product_link_list)
    print(len(product_link_list), "Product Links")

if __name__ == '__main__':
    #url = 'https://www.backcountry.com/mens-climb-jackets?p=brand%3AArc%27teryx%7Cbrand%3AMarmot%7Cbrand%3APatagonia%7Cbrand%3AOutdoor%5C+Research%7Cbrand%3AThe%5C+North%5C+Face&page='

    url = 'https://www.backcountry.com/womens-climb-jackets?p=brand%3AMarmot%7Cbrand%3APatagonia%7Cbrand%3AArc%27teryx%7Cbrand%3AThe%5C+North%5C+Face%7Cbrand%3AOutdoor%5C+Research&page='

    add_on = '&nf=1'
    n_pages = 3
    products_filename = '../data/products.csv'
    reviews_filename = '../data/reviews.csv'
    get_product_links(url, add_on, n_pages, reviews_filename, products_filename)
