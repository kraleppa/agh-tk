FROM maven:3.6.0-jdk-11-slim AS build
COPY src /home/state_service/src
COPY pom.xml /home/state_service
RUN mvn -f /home/state_service/pom.xml dependency:resolve
RUN mvn -f /home/state_service/pom.xml clean package

#
# Package stage
#
FROM openjdk:11-jre-slim

COPY --from=build /home/state_service/target/state_service-1.0-SNAPSHOT-jar-with-dependencies.jar /usr/local/lib/state_service.jar
ENTRYPOINT ["java","-jar","/usr/local/lib/state_service.jar"]