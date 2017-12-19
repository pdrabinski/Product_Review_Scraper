import spacy
import pandas as pd
from string import punctuation, printable
import pickle
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

def clean_review(reviews):
    i = 0
    for review in reviews:
        #stoplist words and punctuation to remove"
        stoplist = set(list(ENGLISH_STOP_WORDS) + ["n't", "'s", "'m", "ca", "'", "'re"])
        punct_dict = {ord(punc): None for punc in punctuation if punc not in ['_', '*']}

        #remove punctuation from string
        review = review.translate(punct_dict)
        #remove unicode
        cln_review = ''.join([char for char in review if char in printable])
        #run the review through SpaCy
        nlp = spacy.load('en')
        review = nlp(cln_review)
        tokens = [token.lemma_.lower().replace(' ', '_') for token in review]
        tokens = [token for token in tokens if token not in stoplist]
        review = ' '.join(w for w in tokens)
        i += 1
        if i % 100 == 0:
            print(i, "reviews done...")
    return reviews

def clean_file(file):
    with open(file) as f:
        df = pd.read_csv(f, header=None, names=['Brand', 'Product', 'User_ID', 'Rating','Review', 'BC_emp?','Date', 'Familiarity', 'Gearhead?' ])
        df['Review'] = clean_review(df['Review'].values)
    df.to_pickle('pickle_test.p')

if __name__ == '__main__':
    clean_file('../data/marmot_reviews.csv')
