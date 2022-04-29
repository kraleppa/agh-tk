package consumer

import com.rabbitmq.client._
import utils.Utils

class Consumer(connectionFactory : ConnectionFactory) {
  def run() = {
    connectionFactory.setHost(Utils.HOST)
    val connection = connectionFactory.newConnection()
    val channel = connection.createChannel()
    Utils.logger.info("WAITING FOR MESSAGES")
    val deliverCallback: DeliverCallback = (_, delivery) => {
      val message = new String(delivery.getBody, "UTF-8")
      Utils.logger.info("RECEIVED MESSAGE: " + message + "'")
    }
    channel.basicConsume(Utils.CONSUMER_QUEUE_NAME, true, deliverCallback, _ => {})
  }
}
