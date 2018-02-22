#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 04:33:18 2017

@author: d1vin3
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle, os

# Reading training and testing data
train = pd.read_csv('train.tsv', sep = '\t')
test = pd.read_csv('test.tsv', sep = '\t')

# Unique sentiment classes
train['Sentiment'].unique()
#train['Sentiment'].hist(color = 'blue', alpha = 0.5)

# Extracting features from the text. i.e. Convert text content into numerical feature vector
# Bag of words
# Tokenizing text with scikit-learn
from sklearn.feature_extraction.text import CountVectorizer
count_vector = CountVectorizer()

x_train_counts = count_vector.fit_transform(train['Phrase'])

# Get feature names
print(count_vector.get_feature_names()[:5])

## From occurrences to frequencies: Term Frequencies
# Term Frequency times Inverse Document Frequency(tf-idf)
from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer(use_idf = False).fit(x_train_counts)

# Transform count-matrix to tf representation
x_train_tf = tf_transformer.transform(x_train_counts)

## Term Frequency times Inverse Document Frequency (tf-idf)
tfidf_transformer = TfidfTransformer()
x_train_tfidf = tfidf_transformer.fit_transform(x_train_counts)

# Naive Bayes Classifier
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(x_train_tfidf, train['Sentiment'])

# Test prediction
x_test_counts = count_vector.transform(test['Phrase'])
x_test_tfidf = tfidf_transformer.transform(x_test_counts)
predicted = clf.predict(x_test_tfidf)

print(predicted[:5])

# Save pkls in current directory
dest = os.path.join('')
pickle.dump(clf,open(os.path.join(dest, 'classifier.pkl'), 'wb'),protocol=4)
pickle.dump(count_vector,open(os.path.join(dest, 'vectorizer.pkl'), 'wb'),protocol=4)
pickle.dump(tfidf_transformer,open(os.path.join(dest, 'transformer.pkl'), 'wb'),protocol=4)

# Write result in csv
import csv
with open('Rotten_Sentiment.csv', 'w') as csvfile:
    csvfile.write('PhraseId,Sentiment\n')
    for i, j in zip(test['PhraseId'], predicted):
        csvfile.write('{},{}\n'.format(i, j))







