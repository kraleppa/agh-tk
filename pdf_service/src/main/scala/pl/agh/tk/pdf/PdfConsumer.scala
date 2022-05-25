package pl.agh.tk.pdf

import com.rabbitmq.client.{AMQP, Channel, DefaultConsumer, Envelope}
import org.json.JSONObject
import org.slf4j.{Logger, LoggerFactory}
import pl.agh.tk.PdfParser

import java.nio.charset.StandardCharsets

class PdfConsumer(channelIn: Channel, channelOut: Channel) extends DefaultConsumer(channelIn) {

  val logger : Logger = LoggerFactory.getLogger(getClass)

  override def handleDelivery(consumerTag: String, envelope: Envelope, properties: AMQP.BasicProperties, body: Array[Byte]): Unit = {
    if(body != null){
      val json = new JSONObject(new String(body, StandardCharsets.UTF_8))
      val extractedText = PdfParser.getTextFrom(json.getString("file"))
      setState(json, extractedText)

      channelOut.basicPublish("text", "text", new AMQP.BasicProperties, json.toString.getBytes(StandardCharsets.UTF_8))

      logger.info("sent response with {}", json)
    }
  }

  private def setState(json: JSONObject, extractedText: String): Unit = {
    val fileState = getJsonObject(json)
    if (extractedText != null) {
      json.put("text", extractedText)
      fileState.put("fileProcessed", true)
    }
    else {
      json.put("text", "")
      fileState.put("fileProcessingError", true)
    }
    json.put("fileState", fileState)
  }

  private def getJsonObject(json: JSONObject) = if (json.has("fileState")) json.get("fileState").asInstanceOf[JSONObject]
  else new JSONObject

}
