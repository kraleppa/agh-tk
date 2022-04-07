package pl.agh.tk.ocr

import com.rabbitmq.client.AMQP
import com.rabbitmq.client.Channel
import com.rabbitmq.client.DefaultConsumer
import com.rabbitmq.client.Envelope
import org.json.JSONObject
import org.slf4j.Logger
import org.slf4j.LoggerFactory

class OcrConsumer(channelIn: Channel, private val channelOut: Channel) : DefaultConsumer(channelIn) {

    private val ocrWorker: OcrWorker = OcrWorker()

    private val logger: Logger = LoggerFactory.getLogger(javaClass)

    override fun handleDelivery(
        consumerTag: String?,
        envelope: Envelope?,
        properties: AMQP.BasicProperties?,
        body: ByteArray?
    ) {
        if (body != null) {
            val json = JSONObject(String(body))
            val extractedText: String = ocrWorker.extractText(json.getString("path"))
            json.put("text", extractedText)

            channelOut.basicPublish(
                Utils.EXCHANGE_NAME,
                Utils.ROUTING_KEY,
                AMQP.BasicProperties(),
                json.toString().toByteArray()
            )
            logger.info("sent response with: $json")
        }
    }
}