import os
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import PyPDF2

def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text()
    return text

def preprocess(text):
    stop_words = set(stopwords.words('english'))
    words = re.findall(r'\b\w+\b', text.lower())
    filtered = [word for word in words if word not in stop_words]
    return " ".join(filtered)

def calculate_similarity(input_text, reference_texts):
    texts = [input_text] + reference_texts
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    cosine_sim = (tfidf_matrix * tfidf_matrix.T).toarray()
    return cosine_sim[0][1:]
