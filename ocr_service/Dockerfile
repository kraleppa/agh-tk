FROM maven:3.6.0-jdk-8-slim AS build
COPY src /home/ocr_service/src
COPY pom.xml /home/ocr_service
RUN mvn -f /home/ocr_service/pom.xml dependency:resolve
RUN mvn -f /home/ocr_service/pom.xml clean package

#
# Package stage
#
FROM openjdk:8-jre-alpine

RUN apk update
RUN apk add --no-cache tesseract-ocr
ENV LC_ALL C
COPY tessdata /home/ocr_service/tessdata

COPY --from=build /home/ocr_service/target/ocr_service-1.0-SNAPSHOT-jar-with-dependencies.jar /usr/local/lib/ocr_service.jar
COPY test_images/test1.png /home/ocr_service/test_images/
COPY test_images/test2.png /home/ocr_service/test_images/
ENTRYPOINT ["java","-jar","/usr/local/lib/ocr_service.jar"]