package pl.agh.tk.ocr

import com.rabbitmq.client.Channel
import com.rabbitmq.client.Connection
import com.rabbitmq.client.ConnectionFactory
import com.rabbitmq.client.Consumer
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import pl.agh.tk.ocr.Main.logger
import pl.agh.tk.ocr.Utils.HOST
import pl.agh.tk.ocr.Utils.QUEUE_NAME
import java.net.ConnectException


object Main {
    val logger: Logger = LoggerFactory.getLogger(javaClass)
}

@Suppress("UNUSED_PARAMETER")
fun main(args: Array<String>) {
    val connectionFactory = ConnectionFactory()
    connectionFactory.host = HOST
    var connection: Connection? = null
    while (connection == null) {
        try {
            connection = connectionFactory.newConnection()
        } catch (e: ConnectException) {
            logger.warn("waiting for connection")
            Thread.sleep(10_000)
        }
    }
    val channelIn: Channel = connection.createChannel()
    val channelOut: Channel = connection.createChannel()
    val consumer: Consumer = OcrConsumer(channelIn, channelOut)

    logger.info("Connection opened and consumer instantiated, listening for messages")

    channelIn.basicConsume(QUEUE_NAME, true, consumer)
}