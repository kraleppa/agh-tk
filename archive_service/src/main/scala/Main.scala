import com.rabbitmq.client.ConnectionFactory
import scala.language.postfixOps
import utils.Utils
import consumer.Consumer
import publisher.Publisher

object Main {
  def main(args: Array[String]): Unit = {
    val connectionFactory = new ConnectionFactory()
    connectionFactory.setHost(Utils.HOST)

    new Consumer(connectionFactory).run()
    val publisher : Publisher = new Publisher(connectionFactory)

    //publisher test
    publisher.publish("Test message 1")
    publisher.publish("Test message 2")
    publisher.publish("Test message 3")
  }
}
