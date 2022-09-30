FROM python:3.10-bullseye

USER root
WORKDIR /app

ENV TZ=Asia/Tokyo
ENV TRANSFORMERS_OFFLINE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  ca-certificates \
  git \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY . ./

RUN pip install -r requirements.txt
RUN python download_model.py
