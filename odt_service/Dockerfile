FROM maven:3.8.4-openjdk-17 AS build

COPY src /home/odt_service/src
COPY pom.xml /home/odt_service
RUN mvn -f /home/odt_service/pom.xml dependency:resolve
RUN mvn -f /home/odt_service/pom.xml clean package

FROM openjdk:17-oracle

COPY --from=build /home/odt_service/target/odt_service*.jar /usr/local/lib/odt_service.jar

ENTRYPOINT ["java", "-jar", "/usr/local/lib/odt_service.jar"]