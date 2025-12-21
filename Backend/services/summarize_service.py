from transformers import T5Tokenizer, T5ForConditionalGeneration

MODEL_ID = "panggi/t5-base-indonesian-summarization-cased"

tokenizer = None
model = None

def load_model():
    global tokenizer, model
    if tokenizer is None or model is None:
        tokenizer = T5Tokenizer.from_pretrained(MODEL_ID)
        model = T5ForConditionalGeneration.from_pretrained(MODEL_ID)



def _summarize_sync(text: str):
    load_model()

    # Encode dengan batas maksimum 512 token
    input_ids = tokenizer.encode(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    # Parameter diganti agar sama seperti kode yang menurutmu lebih bagus
    summary_ids = model.generate(
        input_ids,
        max_length=250,
        min_length=40,
        num_beams=2,
        repetition_penalty=2.5,
        length_penalty=1.0,
        early_stopping=True,
        no_repeat_ngram_size=2,
        use_cache=True
    )

    summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary_text


async def summarize_text(text: str):
    return await asyncio.to_thread(_summarize_sync, text)
