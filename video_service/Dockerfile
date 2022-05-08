
FROM rust:1.57.0-bullseye as init

ARG OPENCV_VERSION=4.5.1
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install -y python3-opencv
RUN apt install -y clang libclang-dev
RUN apt -y install "libopencv-dev=${OPENCV_VERSION}*"

FROM init as build

COPY ./ /src

WORKDIR /src

#RUN cargo test
RUN cargo build

FROM init as final

RUN mkdir /app
RUN mkdir /data
RUN mkdir /data/input
RUN mkdir /data/output

COPY --from=build /src/target/debug/video_service /app/

WORKDIR /app

ENV RABBIT_CONNECTION_STRING=amqp://admin:admin@rabbitmq:5672
ENV INPUT_DIR=/data/input/
ENV OUTPUT_DIR=/extracted/output/

VOLUME /data/input/
VOLUME /extracted/output/

ENTRYPOINT ./video_service
