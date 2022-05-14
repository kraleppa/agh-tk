package pl.agh.tk.ocr

object Utils {

    const val HOST = "rabbitmq"

    const val EXCHANGE_NAME = "text"

    const val ROUTING_KEY = "text"

    const val QUEUE_NAME = "format.image"

    const val TESS_DATA = "/home/ocr_service/tessdata"

    const val STATE_FIELD = "fileState"

    val LANGUAGES: List<String> = listOf("eng", "pol")
}