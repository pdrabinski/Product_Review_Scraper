from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from dateutil.parser import parse
import time


# url = 'https://www.backcountry.com/patagonia-fjord-flannel-shirt-long-sleeve-mens?ti=UDEzV2lkZ2V0OlAxM24gUHJvZHVjdHM6MToxOg=='

# url = 'https://www.backcountry.com/the-north-face-kilowatt-varsity-jacket-mens?skid=TNF032G-ASPGREGRE-S&ti=UExQIENhdDpNZW4ncyBDbGltYiBKYWNrZXRzOjg6MTE6YmMtbWVucy1jbGltYi1qYWNrZXRz'

url = 'https://www.backcountry.com/the-north-face-apex-bionic-jacket-mens?skid=TNF02HH-URBNAVNV-S&ti=UExQIENhdDpNZW4ncyBDbGltYiBKYWNrZXRzOjE6ODpiYy1tZW5zLWNsaW1iLWphY2tldHM='

def get_reviews(url, reviews_filename, products_filename):
    driver = webdriver.Firefox()
    driver.get(url)
    response = driver.page_source
    driver.quit()

    soup = BeautifulSoup(response, 'html.parser')

    product_name = soup.find('h1', attrs={'class': 'product-name'})
    product_name = product_name.text.strip()
    brand_name = product_name.split()[0]
    product_name = " ".join(product_name.split(" ")[1:])

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
    if total_ratings == 0:
        return
    avg_rating = float(five_rating * 5 + four_rating * 4 + three_rating * 3 + two_rating * 2 + one_rating * 1) / (five_rating + four_rating + three_rating + two_rating + one_rating)
    avg_rating = round(avg_rating,3)

    with open(products_filename,'a', newline='') as pf:
        writer = csv.writer(pf, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([brand_name,product_name,avg_rating, five_rating,four_rating,three_rating,two_rating,one_rating])

    reviews = soup.find_all('article', attrs={'class': 'js-pdp-wall-masonry-item'})
    with open(reviews_filename,'a', newline='') as f:
        writer = csv.writer(f, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

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
    print(total_time)
