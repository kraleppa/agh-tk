import com.rabbitmq.client.ConnectionFactory
import scala.language.postfixOps
import utils.Utils
import consumer.Consumer

object Main {
  def main(args: Array[String]): Unit = {
    val connectionFactory = new ConnectionFactory()
    connectionFactory.setHost(Utils.HOST)
    new Consumer(connectionFactory).run()
  }
}
