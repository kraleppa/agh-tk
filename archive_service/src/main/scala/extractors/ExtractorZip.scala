package extractors

import org.apache.commons.compress.archivers.zip.ZipArchiveInputStream
import org.json.JSONObject
import java.io.{BufferedInputStream, FileInputStream, FileNotFoundException}
import utils.Utils

class ExtractorZip () {
  def extractFiles(inputArchivePath: String, message : JSONObject, outputFolderRootPath: String = "/host/extracted"): Unit = {

    var archiveInputStream : ZipArchiveInputStream = null
    try {
      archiveInputStream = new ZipArchiveInputStream(new BufferedInputStream(new FileInputStream(inputArchivePath)))
    } catch {
      case e: FileNotFoundException =>
        Utils.logger.error("File provided in the message not found")
        return
    }

    Common.handleExtracting(archiveInputStream, inputArchivePath, outputFolderRootPath, message)
  }
}
