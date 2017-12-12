from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from dateutil.parser import parse
import time


# url = 'https://www.backcountry.com/patagonia-fjord-flannel-shirt-long-sleeve-mens?ti=UDEzV2lkZ2V0OlAxM24gUHJvZHVjdHM6MToxOg=='

# url = 'https://www.backcountry.com/the-north-face-kilowatt-varsity-jacket-mens?skid=TNF032G-ASPGREGRE-S&ti=UExQIENhdDpNZW4ncyBDbGltYiBKYWNrZXRzOjg6MTE6YmMtbWVucy1jbGltYi1qYWNrZXRz'

url = 'https://www.backcountry.com/marmot-tullus-down-jacket-mens?skid=MAR00XO-STOCLO-S&ti=UExQIENhdDpNZW4ncyBDbGltYiBKYWNrZXRzOjE6OTpiYy1tZW5zLWNsaW1iLWphY2tldHM='

def get_reviews(url, reviews_filename, products_filename):
    """
    Gathers reviews and product info from url and writes the results to 2 csv's.
    """

    driver = webdriver.Firefox()
    driver.get(url)
    response = driver.page_source
    driver.quit()

    soup = BeautifulSoup(response, 'html.parser')

    """Get number of ratings and the average rating"""
    five_rating = soup.find('a', attrs={'class': 'js-five-star-rank'})
    if five_rating == None:
        return
    five_rating = int(five_rating.text.strip())
    four_rating = soup.find('a', attrs={'class': 'js-four-star-rank'})
    four_rating = int(four_rating.text.strip())
    three_rating = soup.find('a', attrs={'class': 'js-three-star-rank'})
    three_rating = int(three_rating.text.strip())
    two_rating = soup.find('a', attrs={'class': 'js-two-star-rank'})
    two_rating = int(two_rating.text.strip())
    one_rating = soup.find('a', attrs={'class': 'js-one-star-rank'})
    one_rating = int(one_rating.text.strip())
    total_ratings = five_rating + four_rating + three_rating + two_rating + one_rating
    if total_ratings < 5:
        return
    avg_rating = float(five_rating * 5 + four_rating * 4 + three_rating * 3 + two_rating * 2 + one_rating * 1) / (five_rating + four_rating + three_rating + two_rating + one_rating)
    avg_rating = round(avg_rating,3)

    """Get Brand name and Product name"""
    product = soup.find('h1', attrs={'class': 'product-name'})
    brand_name = product.find('span', attrs={'class':'qa-brand-name'})
    brand_name = brand_name.text.strip()
    product_name = product.text.strip()
    brand_name_n_words = len(brand_name.split())
    product_name = " ".join(product_name.split(" ")[brand_name_n_words:])

    """Get product price"""
    price = soup.find('span', attrs={'class': 'product-pricing__retail'})
    if price == None:
        price = soup.find('span', attrs={'class': 'product-pricing__inactive'})
    price = float(price.text.strip()[1:])
    print(price)

    """Add to product.csv"""
    with open(products_filename,'a', newline='') as pf:
        writer = csv.writer(pf, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([brand_name,product_name,price,avg_rating, five_rating,four_rating,three_rating,two_rating,one_rating])

    """Get all reviews for product"""
    reviews = soup.find_all('article', attrs={'class': 'js-pdp-wall-masonry-item'})
    with open(reviews_filename,'a', newline='') as f:
        writer = csv.writer(f, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

        """Get user review, associated info, and write to reviews.csv"""
        for review in reviews:
            user_review = review.get('data-description')
            if len(user_review) > 0:
                user_rating = review.get('data-rank')
                user_rating = int(user_rating) if len(user_rating) > 0 else ""
                user_emp_bool = review.get('data-user-employee')
                user_id = review.get('data-user-id')
                date = review.get('data-created')
                date = parse(date)
                familiarity = review.get('data-familiarity')
                gearhead = review.get('data-is_gearhead')
                writer.writerow([brand_name,product_name,user_id, user_rating, user_review, user_emp_bool, date, familiarity, gearhead])


if __name__ == '__main__':
    start = time.time()
    get_reviews(url, '../data/test_reviews.csv', '../data/test_products.csv')
    total_time = time.time() - start
    print(total_time, "sec")
