package consumer

import com.rabbitmq.client._
import org.json.JSONObject
import java.io.IOException
import java.util.concurrent.TimeoutException
import connection.ConnectionFactoryObject
import extractors.ExtractorService
import utils.Utils

class Consumer() {
  val extractorService: ExtractorService = new ExtractorService()

  def run(): Unit = {
    var connection: Connection = null
    while(connection == null) {
      try {
        connection = ConnectionFactoryObject.connection()
      } catch {
        case e @ (_ : IOException | _ : TimeoutException) =>
          Utils.logger.info("Waiting for connection...")
          Thread.sleep(10000)
      }
    }
    val channel = connection.createChannel()
    Utils.logger.info("Connected - waiting for messages")
    channel.basicConsume(Utils.CONSUMER_QUEUE_NAME, true, deliverCallback, _ => {})
  }

  val deliverCallback: DeliverCallback = (_, delivery) => {
    val message: String = new String(delivery.getBody, "UTF-8")
    val messageJson: JSONObject = new JSONObject(new String(message))
    Utils.logger.info("Received message: " + messageJson + "'")
    extractorService.extractFiles(messageJson)
  }
}
