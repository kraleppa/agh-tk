name := "archive_service"
version := "0.1.0"

Compile/mainClass := Some("Main")

scalaVersion := "2.13.8"

libraryDependencies ++= Seq(
  "org.scalameta" %% "munit" % "0.7.29" % Test,
  "com.rabbitmq" % "amqp-client" % "5.14.2",
  "ch.qos.logback" % "logback-classic" % "1.2.11",
  "com.typesafe.scala-logging" %% "scala-logging" % "3.9.4",
  "org.apache.commons" % "commons-compress" % "1.21",
  "org.json" % "json" % "20220320"
)
