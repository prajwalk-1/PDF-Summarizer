import nltk
import gradio as gr
import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

nltk.download('punkt')

def summarize_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    if not text.strip():
        return "Could not extract text from the PDF. Please try another file."

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()

    summary = summarizer(parser.document, sentences_count=5)

    summary_text = "\n".join(str(sentence) for sentence in summary)
    
    return summary_text

# Gradio Interface
def pdf_summary_interface(pdf_file):
    return summarize_pdf(pdf_file)

# Create the Gradio UI for uploading a PDF file
interface = gr.Interface(
    fn=pdf_summary_interface,
    inputs=gr.File(file_types=['.pdf']),
    outputs="text",
    title="PDF Summarizer",
    description="Upload a PDF file to get a summarized version of the content."
)

interface.launch()
