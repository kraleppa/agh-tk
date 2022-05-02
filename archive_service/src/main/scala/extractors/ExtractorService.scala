package extractors

import java.nio.file.Paths
import org.json.JSONObject
import utils.Utils

class ExtractorService {
  val extractorZip: ExtractorZip = new ExtractorZip()

  def extractFiles(jsonMessage: JSONObject): Unit = {
    if(jsonMessage.has("file")) {
      val inputArchivePath: String = jsonMessage.get("file").toString
      Utils.logger.info("Received message with archive: " + inputArchivePath)
      val inputArchiveExtension: String = Paths.get(inputArchivePath).getFileName.toString.split("\\.").last
      Utils.logger.info("Extracting archive: " + inputArchivePath)

      inputArchiveExtension match {
        case "zip" => extractorZip.extractFiles(inputArchivePath, jsonMessage)
        case _ => Utils.logger.error("Received message with incorrect file extension: " + inputArchivePath)
      }
    } else {
      Utils.logger.error("Received message without a file path")
    }
  }
}
