package extractors

import org.apache.commons.compress.archivers.zip.ZipArchiveInputStream
import org.apache.commons.compress.archivers.ArchiveEntry
import java.io.{BufferedInputStream, FileInputStream, FileNotFoundException, IOException}
import utils.Utils

class ExtractorZip {
  def extractFiles(inputArchivePath: String, outputFolderRootPath: String = "/host/extracted", isTopLevel : Boolean = true): Unit = {

    var archiveInputStream : ZipArchiveInputStream = null
    try {
      archiveInputStream = new ZipArchiveInputStream(new BufferedInputStream(new FileInputStream(inputArchivePath)))
    } catch {
      case e: FileNotFoundException =>
        Utils.logger.error("File provided in the message not found")
        return
    }

    val outputFolder = Common.createOutputDirectory(outputFolderRootPath)

    try {
      var entry: ArchiveEntry = null
      while ( {
        entry = archiveInputStream.getNextEntry
        entry != null
      }) {
        if (outputFolder != null) {
          Common.copyFiles(archiveInputStream, outputFolder, entry)
        }
      }
    } catch {
      case e: IOException =>
        e.printStackTrace()
    } finally if (archiveInputStream != null) archiveInputStream.close()
  }
}
