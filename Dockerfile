FROM python:3.11-slim

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    ca-certificates \
    bash \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app/pipeline
COPY . /app/pipeline

RUN pip install --no-cache-dir \
    pandas \
    numpy \
    matplotlib \
    scikit-learn \
    scipy \
    requests

RUN mkdir -p /app/pipeline/results
CMD ["bash"]

