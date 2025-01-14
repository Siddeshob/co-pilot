from transformers import pipeline

def generate_summary(text):
    """Generate summary using transformers"""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=130, min_length=30)
    return summary[0]['summary_text']