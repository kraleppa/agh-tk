package consumer

import com.rabbitmq.client._
import extractors.ExtractorService
import org.json.JSONObject
import utils.Utils

class Consumer(connectionFactory : ConnectionFactory) {
  val extractorService : ExtractorService = new ExtractorService()

  def run() = {
    connectionFactory.setHost(Utils.HOST)
    val connection = connectionFactory.newConnection()
    val channel = connection.createChannel()
    Utils.logger.info("WAITING FOR MESSAGES")

    val deliverCallback: DeliverCallback = (_, delivery) => {
      val message = new String(delivery.getBody, "UTF-8")
      Utils.logger.info("RECEIVED MESSAGE: " + message + "'")
      val messageJson : JSONObject = new JSONObject(new String(message))
      Utils.logger.info("RECEIVED MESSAGE JSON: " + messageJson + "'")
      extractorService.extractFiles(messageJson)
    }

    channel.basicConsume(Utils.CONSUMER_QUEUE_NAME, true, deliverCallback, _ => {})
  }
}
