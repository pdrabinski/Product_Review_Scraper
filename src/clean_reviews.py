import pandas as pd
import re
from glob import glob

def clean_reviews(reviews):
    """
    Input: numpy array of reviews
    Output: numpy array of cleaned reviews
    Purpose is to remove special characters and unreadable text.
    """
    strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
    for i,review in enumerate(reviews):
        review = review.lower().replace("<br />", " ").replace("\n", " ")
        review = re.sub(strip_special_chars, "", review)
        review = " ".join(review.split())
        reviews[i] = re.sub("pron","", review)
        if i % 100 == 0:
            print(i, "reviews done...")
    return reviews

def clean_file(d):
    file_paths = glob(d + "/*.csv")
    for doc in file_paths:
        df = pd.read_csv(doc, header=None, names=['Brand', 'Product', 'User_ID', 'Rating','Review', 'BC_emp?','Date', 'Familiarity', 'Gearhead?'])
        df['Review'] = clean_reviews(df['Review'].values)
        brand = df['Brand'].values[1]
        df.to_pickle(d + 'clean/' + brand + '_clean' + '.p')
    print(brand, 'done...')

if __name__ == '__main__':
    clean_file('../data/reviews/')
