package pl.agh.tk.pdf

import com.rabbitmq.client.{Connection, ConnectionFactory}
import org.slf4j.{Logger, LoggerFactory}

import java.util.concurrent.TimeoutException

object Main {
  val logger: Logger = LoggerFactory.getLogger(getClass)


  def main(args: Array[String]): Unit = {
    val connectionFactory = new ConnectionFactory()
    connectionFactory.setHost("rabbitmq")

    var connection : Connection = null

    while(connection == null){
      try{
        connection = connectionFactory.newConnection()
      }
      catch{
        case _: TimeoutException =>
          logger.warn("waiting for connection")
          Thread.sleep(10_000)
      }
    }

    logger.info("connected")

    val channelIn = connection.createChannel()
    val channelOut = connection.createChannel()
    val consumer = new PdfConsumer(channelIn, channelOut)

    channelIn.basicConsume("format.pdf", true, consumer)
  }



}
