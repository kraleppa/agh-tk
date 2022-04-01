package pl.agh.tk.ocr

object Utils {

    const val HOST = "host.docker.internal"

    const val EXCHANGE_NAME = "text"

    const val ROUTING_KEY = "text"

    const val QUEUE_NAME = "format.image"

    const val TESS_DATA = "/home/tessdata"

    @Suppress("unused")
    enum class Lang(val value: String) {
        ENG("eng"),
        POL("pol")
    }
}