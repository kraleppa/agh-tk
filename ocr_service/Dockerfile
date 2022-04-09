FROM maven:3.6.0-jdk-11-slim AS build
COPY src /home/ocr_service/src
COPY pom.xml /home/ocr_service
COPY test_images /home/ocr_service
RUN mvn -f /home/ocr_service/pom.xml clean package

#
# Package stage
#
FROM openjdk:11-jre-slim
COPY --from=build /home/ocr_service/target/ocr_service-1.0-SNAPSHOT-jar-with-dependencies.jar /usr/local/lib/ocr_service.jar
ENTRYPOINT ["java","-jar","/usr/local/lib/ocr_service.jar"]