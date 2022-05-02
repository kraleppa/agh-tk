package extractors

import java.nio.file.Paths
import org.json.JSONObject
import utils.Utils

class ExtractorService {
  val extractorZip : ExtractorZip = new ExtractorZip()

  def extractFiles(jsonMessage : JSONObject) : Unit = {
    if(jsonMessage.has("file")) {
      val filePath : String = jsonMessage.get("file").toString()
      Utils.logger.debug("RECEIVED FILE WITH FILE PATH: " + filePath)
      val fileExtension = Paths.get(filePath).getFileName.toString.split("\\.").last
      Utils.logger.debug("RECEIVED FILE WITH FILE EXTENSION: " + fileExtension)

      Utils.logger.info("Extracting archive: " + filePath)
      fileExtension match {
        case "zip" => extractorZip.extractFiles(filePath)
        case _ => Utils.logger.error("Received message with incorrect file extension: " + filePath)
      }
    }
  }
}
