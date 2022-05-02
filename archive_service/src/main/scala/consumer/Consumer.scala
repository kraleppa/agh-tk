package consumer

import com.rabbitmq.client._
import org.json.JSONObject
import connection.ConnectionFactoryObject
import extractors.ExtractorService
import utils.Utils

class Consumer() {
  val extractorService : ExtractorService = new ExtractorService()

  def run(): Unit = {
    val connection : Connection = ConnectionFactoryObject.connection()
    val channel = connection.createChannel()
    Utils.logger.info("APPLICATION IS RUNNING - WAITING FOR MESSAGES")
    channel.basicConsume(Utils.CONSUMER_QUEUE_NAME, true, deliverCallback, _ => {})
  }

  val deliverCallback: DeliverCallback = (_, delivery) => {
    val message = new String(delivery.getBody, "UTF-8")
    val messageJson : JSONObject = new JSONObject(new String(message))
    Utils.logger.info("Received message: " + messageJson + "'")
    extractorService.extractFiles(messageJson)
  }
}
