import os
import uuid
from flask import Blueprint, render_template, request
import PyPDF2
from difflib import SequenceMatcher

routes = Blueprint('routes', __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def calculate_similarity(text1, text2):
    return round(SequenceMatcher(None, text1, text2).ratio() * 100, 2)

@routes.route('/', methods=['GET', 'POST'])
def index():
    similarity_score = None
    if request.method == 'POST':
        file1 = request.files.get('file1')
        file2 = request.files.get('file2')

        if file1 and file2:
            filename1 = str(uuid.uuid4()) + "_" + file1.filename
            filepath1 = os.path.join(UPLOAD_FOLDER, filename1)
            file1.save(filepath1)

            filename2 = str(uuid.uuid4()) + "_" + file2.filename
            filepath2 = os.path.join(UPLOAD_FOLDER, filename2)
            file2.save(filepath2)

            text1 = extract_text_from_pdf(filepath1)
            text2 = extract_text_from_pdf(filepath2)

            similarity_score = calculate_similarity(text1, text2)

    return render_template('index.html', similarity=similarity_score)
