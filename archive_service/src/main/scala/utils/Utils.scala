package utils

import com.typesafe.scalalogging.Logger

object Utils {
  val CONSUMER_QUEUE_NAME: String = "format.archive"
  val PUBLISHER_EXCHANGE_NAME: String = "words"
  val PUBLISHER_ROUTING_KEY: String = "words.scraper"
  val HOST: String = "rabbitmq"

  val logger = Logger("app")

  def uniqueFolderPath() : String = {
    "archive-" + System.currentTimeMillis()
  }
}