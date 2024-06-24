# -*- coding: utf-8 -*-
"""Questão 2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15ID8kxZjBIbA3Gh3KzzJDfZsauE_0nb5
"""

import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

nltk.download('punkt')
nltk.download('stopwords')


def preprocess(text):
    # Remove special characters, numbers, punctuation
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\d+', '', text)

    # Tokenization
    tokens = word_tokenize(text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Remove numbers

    # Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]

    # Reconstruct the processed text
    processed_text = ' '.join(tokens)

    return processed_text

# Load CSV
train_dataset = pd.read_csv(r'/content/sample_data/ReutersGrain-test.csv', delimiter=';', encoding='utf-8')
test_dataset = pd.read_csv(r'/content/sample_data/ReutersGrain-test.csv', delimiter=';', encoding='utf-8')

# Apply preprocessing to train and test datasets
train_dataset['ProcessedText'] = train_dataset['Text'].apply(preprocess)
test_dataset['ProcessedText'] = test_dataset['Text'].apply(preprocess)

vectorizer = TfidfVectorizer(max_features=1000)  # Example with max 1000 features

# Fit and transform on train set
X_train = vectorizer.fit_transform(train_dataset['ProcessedText']).toarray()
y_train = train_dataset['class-att']

# Transform test set (only transform using fitted vectorizer)
X_test = vectorizer.transform(test_dataset['ProcessedText']).toarray()
y_test = test_dataset['class-att']

# Initialize models
gnb = GaussianNB()
rf = RandomForestClassifier()

# Train models
gnb.fit(X_train, y_train)
rf.fit(X_train, y_train)

# Predictions
naive_preds = gnb.predict(X_test)
rf_preds = rf.predict(X_test)

# Evaluate accuracy
naive_accuracy = accuracy_score(y_test, naive_preds)
rf_accuracy = accuracy_score(y_test, rf_preds)

print(f'\nRandom Forest Acc: {rf_accuracy}')
print(f'\nNaive Bayes Acc: {naive_accuracy}')