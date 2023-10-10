import PyPDF2
from docx import Document
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
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

    # Sort sentences by their scores
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    # Select the top 'num_sentences' sentences as the summary
    summary = sorted_sentences[:num_sentences]

    return " ".join(summary)

# Read the contents of the file (DOCX or PDF)
def read_file(file_path):
    if file_path.endswith('.docx'):
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    elif file_path.endswith('.pdf'):
        with open(file_path, 'rb') as pdf_input:
            pdf_reader = PyPDF2.PdfFileReader(pdf_input)
            text = ""
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
    else:
        raise ValueError("Unsupported file format")

    return text

# Replace 'your_input_file.docx' or 'your_input_file.pdf' with your file path
input_file = 'Ethics Situation Analysis.docx'  # Change to your input file
output_summary_file = 'summary.txt'

# Read the contents of the file
file_contents = read_file(input_file)

# Generate a summary
summary = generate_summary(file_contents)

# Write the summary to an output file
with open(output_summary_file, 'w', encoding='utf-8') as summary_output:
    summary_output.write(summary)

# Print the summary to the console
print(summary)
