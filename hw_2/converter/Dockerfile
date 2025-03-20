FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y \
    texlive \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-xetex \
    libx11-dev \
    libxslt-dev \
    ghostscript \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /converter

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY malone.png .
CMD ["python", "app.py"]
