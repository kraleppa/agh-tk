package publisher

import com.rabbitmq.client._
import utils.Utils
import connection.ConnectionFactoryObject

object Publisher {
  def publish(message: String): Unit = {
    val connection: Connection = ConnectionFactoryObject.connection()
    val channel: Channel = connection.createChannel()
    Utils.logger.info("Sent message to scraper: " + message + "'")
    channel.basicPublish(Utils.PUBLISHER_EXCHANGE_NAME, Utils.PUBLISHER_ROUTING_KEY, null, message.getBytes("UTF-8"))
    channel.close()
    connection.close()
  }

  def publishToResult(message: String): Unit = {
    val connection: Connection = ConnectionFactoryObject.connection()
    val channel: Channel = connection.createChannel()
    Utils.logger.info("Sent message to result: " + message + "'")
    channel.basicPublish(Utils.RESULT_EXCHANGE_NAME, Utils.RESULT_ROUTING_KEY, null, message.getBytes("UTF-8"))
    channel.close()
    connection.close()
  }
}
