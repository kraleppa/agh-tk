FROM python:3.10-slim-buster

RUN mkdir -p /wordsServices_textExtractor_config

COPY ./wordsServices_textExtractor_config ./wordsServices_textExtractor_config

RUN mkdir -p /audio_service

WORKDIR /audio_service

COPY ./audio_service/audio_extractor_callback.py ./audio_extractor_callback.py
COPY ./audio_service/audio_extractor_run.py ./audio_extractor_run.py

COPY ./audio_service/requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

# Samples
COPY ./audio_service/audio_samples/sample_eng.wav /home/audio_service/audio_samples/
COPY ./audio_service/audio_samples/sample_pl.wav /home/audio_service/audio_samples/

ENTRYPOINT ["python", "audio_extractor_run.py"]
