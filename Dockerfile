FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependency OS minimum (jangan kebanyakan biar image kecil)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements dulu (biar cache efektif)
COPY Backend/requirements.txt .

RUN pip install --upgrade pip

# 🔥 TORCH CPU (BENAR — TANPA +cpu, TANPA -f)
RUN pip install torch==2.9.1

# Install dependency lain
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code backend
COPY Backend/ .

# Jalankan FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
