from transformers import pipeline

# Gunakan model summarization publik yang ringan
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text: str):
    """
    Fungsi untuk melakukan summarization teks.
    """
    result = summarizer(
        text,
        max_length=130,
        min_length=30,
        do_sample=False
    )
    return result[0]["summary_text"]
