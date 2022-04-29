FROM openjdk:11
FROM mozilla/sbt:8u292_1.5.7 AS build

ENV SCALA_VERSION 2.13.8
ENV SBT_VERSION 1.5.7

RUN curl -L -o sbt-$SBT_VERSION.zip https://github.com/sbt/sbt/releases/download/v$SBT_VERSION/sbt-$SBT_VERSION.zip
RUN unzip sbt-$SBT_VERSION.zip -d ops

WORKDIR /archive_service
ADD . /archive_service
CMD /ops/sbt/bin/sbt run