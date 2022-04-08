FROM openjdk:8-jre-alpine

RUN apk update

RUN apk add --no-cache tesseract-ocr

RUN tesseract --list-langs
RUN tesseract -v

ENV LC_ALL C

COPY target/ocr_service-1.0-SNAPSHOT-jar-with-dependencies.jar /home/app.jar
COPY tessdata /home/tessdata
COPY test1.png /home/test1.png
CMD ["java","-jar","/home/app.jar"]