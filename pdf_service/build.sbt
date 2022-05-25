name := "pdf_service"

version := "0.1"

Compile/mainClass := Some("pl.agh.tk.pdf.Main")

scalaVersion := "2.13.8"
val akkaVersion     = "2.6.16"
val akkaHttpVersion = "10.2.6"

libraryDependencies ++= Seq(
  "org.apache.commons" % "commons-lang3" % "3.12.0",
  "org.apache.pdfbox" % "pdfbox" % "2.0.26",
  "ch.qos.logback" % "logback-classic" % "1.2.11",
  "com.rabbitmq" % "amqp-client" % "5.14.2",
  "org.json" % "json" % "20220320",
  "org.scalatest" %% "scalatest" % "3.2.12" % Test
)
