import time
import fitz  # PyMuPDF
import nltk
import matplotlib.pyplot as plt
from langchain.text_splitter import RecursiveCharacterTextSplitter
from nltk.tokenize import sent_tokenize

class RecursiveCharacterTextSplitterWithSplitMethod(RecursiveCharacterTextSplitter):
    def split_text(self, text, chunk_size=512):  # Increased chunk size for more processing time
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i+chunk_size]
            chunks.append(chunk)
        return chunks

def reference_splitter(text):
    return sent_tokenize(text)

def evaluate_performance(test_documents, num_runs=5):
    recursive_splitter = RecursiveCharacterTextSplitterWithSplitMethod()

    metrics = {
        "time_taken_recursive": [],
        "time_taken_reference": []
    }

    for document in test_documents:
        recursive_times = []
        reference_times = []

        for _ in range(num_runs):
            # Measure performance for RecursiveCharacterTextSplitter
            start_time = time.perf_counter_ns()
            recursive_chunks = recursive_splitter.split_text(document)
            end_time = time.perf_counter_ns()
            recursive_times.append(end_time - start_time)

            # Debugging: Print number of chunks produced by RecursiveCharacterTextSplitter
            print(f"RecursiveCharacterTextSplitter produced {len(recursive_chunks)} chunks")

            # Measure performance for reference sentence splitter
            start_time = time.perf_counter_ns()
            reference_chunks = reference_splitter(document)
            end_time = time.perf_counter_ns()
            reference_times.append(end_time - start_time)

            # Debugging: Print number of sentences produced by Reference Splitter
            print(f"Reference Splitter produced {len(reference_chunks)} sentences")

        metrics["time_taken_recursive"].append(sum(recursive_times) / num_runs / 1_000_000)  # Convert to milliseconds
        metrics["time_taken_reference"].append(sum(reference_times) / num_runs / 1_000_000)  # Convert to milliseconds

    # Debugging: Print metrics collected
    print("Metrics collected:", metrics)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(metrics["time_taken_recursive"], label="RecursiveCharacterTextSplitter")
    plt.plot(metrics["time_taken_reference"], label="Reference Splitter")
    plt.xlabel("Document Index")
    plt.ylabel("Average Time Taken (milliseconds)")
    plt.title("Average Time Taken for Text Splitting (over multiple runs)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Ensure nltk punkt tokenizer is downloaded
nltk.download('punkt')

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""

# Path to the local PDF documents
pdf_paths = [
    r"C:\Users\sande\Desktop\SA_Bot\SA_Bot\Test\Fellowship of the ring.pdf",
    r"C:\Users\sande\Desktop\SA_Bot\SA_Bot\Test\stephen_hawking_a_brief_history_of_time.pdf"
]

# Extract text from the PDF documents
test_documents = [extract_text_from_pdf(pdf_path) for pdf_path in pdf_paths]

# Verify the extracted text
for i, extracted_text in enumerate(test_documents):
    if extracted_text:
        print(f"Extracted text from document {i}:")
        print(extracted_text[:2000])  # Print the first 2000 characters for verification
    else:
        print(f"No text extracted from document {i}.")

# Evaluate performance of the text splitters if text extraction was successful
if all(test_documents):
    evaluate_performance(test_documents, num_runs=5)
else:
    print("Text extraction failed for one or more documents.")
