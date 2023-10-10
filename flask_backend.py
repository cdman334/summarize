from flask import Flask, request, jsonify
import PyPDF2
from docx import Document
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.cluster.util import cosine_distance

# Download NLTK resources
nltk.download("punkt")
nltk.download("stopwords")

# Define a function to preprocess the text
def preprocess_text(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalnum()]
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    return sentences, words

# Calculate the sentence similarity based on cosine similarity
def sentence_similarity(sent1, sent2, words):
    vector1 = [1 if word in sent1 else 0 for word in words]
    vector2 = [1 if word in sent2 else 0 for word in words]
    return 1 - cosine_distance(vector1, vector2)

# Generate a summary of the text
def generate_summary(text, num_sentences=3):
    sentences, words = preprocess_text(text)
    sentence_scores = {}

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j:
                continue
            score = sentence_similarity(sentences[i], sentences[j], words)
            if sentences[i] not in sentence_scores:
                sentence_scores[sentences[i]] = score
            else:
                sentence_scores[sentences[i]] += score

    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary = sorted_sentences[:num_sentences]
    return " ".join(summary)


app = Flask(__name__, static_folder="static", template_folder="static")

@app.route('/')
def main_page():
    return app.send_static_file('index.html')


@app.route('/')
def main_page():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify(error="No selected file"), 400

    file_content = uploaded_file.read().decode('utf-8')
    try:
        summary = generate_summary(file_content)
    except Exception as e:
        return jsonify(error=str(e)), 500

    return jsonify(summary=summary)

if __name__ == "__main__":
    app.run(port=5000)
