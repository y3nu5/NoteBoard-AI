FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements dari subfolder Backend
COPY Backend/requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install PyTorch CPU
RUN pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download model saat build (opsional, bisa di-comment jika build terlalu lama)
# RUN python -c "from transformers import T5Tokenizer, T5ForConditionalGeneration; \
#     T5Tokenizer.from_pretrained('panggi/t5-base-indonesian-summarization-cased'); \
#     T5ForConditionalGeneration.from_pretrained('panggi/t5-base-indonesian-summarization-cased')"

# Copy semua file Backend ke /app
COPY Backend/ .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]