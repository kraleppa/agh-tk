package extractors

import org.apache.commons.compress.archivers.tar.TarArchiveInputStream
import org.json.JSONObject
import java.io.{BufferedInputStream, FileInputStream, FileNotFoundException}
import utils.Utils

class ExtractorTar () {
  def extractFiles(inputArchivePath: String, message: JSONObject, outputDirectoryPathRoot: String = "/host/extracted"): Unit = {
    System.out.println(inputArchivePath)
    var archiveInputStream: TarArchiveInputStream = null
    try {
      archiveInputStream = new TarArchiveInputStream(new BufferedInputStream(new FileInputStream(inputArchivePath)))
    } catch {
      case e: FileNotFoundException =>
        Utils.logger.error("File provided in the message not found")
        return
    }
    Common.handleExtraction(archiveInputStream, inputArchivePath, outputDirectoryPathRoot, message)
  }
}
