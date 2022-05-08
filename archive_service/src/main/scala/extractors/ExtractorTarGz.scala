package extractors

import org.apache.commons.compress.archivers.ArchiveInputStream
import org.apache.commons.compress.archivers.tar.TarArchiveInputStream
import org.apache.commons.compress.compressors.gzip.GzipCompressorInputStream
import org.json.JSONObject

import java.io.{BufferedInputStream, FileInputStream, FileNotFoundException}
import utils.Utils

class ExtractorTarGz() {
  def extractFiles(inputArchivePath: String, message: JSONObject, outputDirectoryPathRoot: String = "/host/extracted"): Unit = {
    System.out.println(inputArchivePath)
    var archiveInputStream: ArchiveInputStream = null
    try {
      archiveInputStream = new TarArchiveInputStream(new GzipCompressorInputStream(new BufferedInputStream(new FileInputStream(inputArchivePath))))
    } catch {
      case e: FileNotFoundException =>
        Utils.logger.error("File provided in the message not found")
        return
    }
    Common.handleExtraction(archiveInputStream, inputArchivePath, outputDirectoryPathRoot, message)
  }
}
