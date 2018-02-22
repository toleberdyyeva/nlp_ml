#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 05:49:20 2017

@author: d1vin3
"""

import pickle, os
import pandas as pd
import numpy as np
import sqlite3
import re
from collections import OrderedDict


# Create sqlite3 file and table
def create_db():
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE review
                 (review text, predicted real)''')
    conn.commit()
    conn.close()
    

# Insert values into Review table
def insert_db(review, predicted):
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute('''INSERT INTO review (review, predicted) 
                VALUES (?,?)''', (review, predicted))
    conn.commit()
    conn.close()
    
    
# Select statements from Review table
def read_db():
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    # for row in c.execute('''SELECT * FROM review '''):
    #     print(row)
    conn.commit()
    conn.close()
    
    
def drop_db():
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute('''Drop table review ''')
    conn.commit()
    conn.close()


# Split arrays into review and returns pandas.DataFrame
def get_reviews_from_array(reviews):
    dic = {'Review': []}
    for r in reviews:
        dic['Review'].append(r)
        #review = re.split(',|\n|\.', r)
        #for r in review:
        #    dic['Phrase'].append(r)
    
    # print(dic)
    df = pd.DataFrame.from_dict(dic)
    # print(df)
    return df


# Main predict function    
def predict(reviews):
    # Load model
    clf = pickle.load(open(os.path.join('','classifier.pkl'), 'rb'))
    count_vector = pickle.load(open(os.path.join('', 'vectorizer.pkl'), 'rb'))
    tfidf_transformer = pickle.load(open(os.path.join('', 'transformer.pkl'), 'rb'))
    
    # Get DataFrame from array of reviews
    df = get_reviews_from_array(reviews)
    
    # Apply CountVectorizer and Tfidf Transformer, then predict
    x_test_counts = count_vector.transform(df['Review'])
    x_test_tfidf = tfidf_transformer.transform(x_test_counts)
    predicted = clf.predict(x_test_tfidf)
    # print(predicted)
    result = []
    # Insert reviews and their prediction into db
    for r in range(len(reviews)):
        result.append([reviews[r],int(predicted[r])])
        insert_db(reviews[r], int(predicted[r]))
    read_db()
    return  predicted


reviews = ['Decent film, im excited', 'Extremely bad, worse']
# Executed only once
# create_db()
# predict(reviews)

