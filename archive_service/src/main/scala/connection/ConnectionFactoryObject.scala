package connection

import com.rabbitmq.client.{Connection, ConnectionFactory}
import utils.Utils

object ConnectionFactoryObject {
  val connectionFactory = new ConnectionFactory()
  connectionFactory.setHost(Utils.HOST)

  def connection (): Connection = {
    connectionFactory.newConnection()
  }
}
