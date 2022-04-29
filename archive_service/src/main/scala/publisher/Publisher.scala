package publisher

import com.rabbitmq.client._
import utils.Utils

class Publisher(connectionFactory: ConnectionFactory) {
  def publish(message : String) {
    val connection = connectionFactory.newConnection()
    val channel = connection.createChannel()
    channel.basicPublish(Utils.PUBLISHER_EXCHANGE_NAME, Utils.PUBLISHER_ROUTING_KEY, null, message.getBytes("UTF-8"))
    Utils.logger.info("PUBLISHED MESSAGE: " + message + "'")
    channel.close()
    connection.close()
  }
}
