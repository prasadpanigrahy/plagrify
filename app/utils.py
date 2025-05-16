from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        text = ""
    return text

def calculate_similarity(text1, text2):
    try:
        vectorizer = TfidfVectorizer().fit_transform([text1, text2])
        similarity_matrix = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
        return similarity_matrix[0][0] * 100
    except:
        return 0.0
