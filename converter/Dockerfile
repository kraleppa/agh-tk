FROM python:3.10-slim-buster

RUN mkdir -p /wordsServices_textExtractor_config

COPY ./wordsServices_textExtractor_config ./wordsServices_textExtractor_config

RUN mkdir -p /converter

WORKDIR /converter

COPY ./converter/converter_callback.py ./audio_extractor_callback.py
COPY ./converter/aconverter_run.py ./audio_extractor_run.py

COPY ./converter/requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
RUN apt update && apt install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Samples
COPY ./converter/samples/eng.mp3 /home/converter/samples/
COPY ./converter/samples/pl.mp3 /home/converter/samples/

ENTRYPOINT ["python", "converter_run.py"]
