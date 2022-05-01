package extractors

import org.apache.commons.compress.archivers.zip.{ZipArchiveEntry, ZipArchiveInputStream}
import org.apache.commons.compress.utils.IOUtils
import utils.Utils

import java.io.{BufferedInputStream, File, FileInputStream, FileNotFoundException, IOException, OutputStream}
import java.nio.file.Files

class ExtractorZip {
  def extractFiles(inputArchivePath: String, outputFolderRootPath: String = "/host/extracted"): Unit = {

    Utils.logger.info("Extracting archive: " + inputArchivePath)
    var archiveInputStream : ZipArchiveInputStream = null

    try {
      archiveInputStream = new ZipArchiveInputStream(new BufferedInputStream(new FileInputStream(inputArchivePath)))
    } catch {
      case e: FileNotFoundException =>
        Utils.logger.error("File provided in the message not found")
        return
    }

    //Create output directory with unique name
    val outputFolderPath = outputFolderRootPath + "/" + Utils.uniqueFolderPath()
    val outputFolder = new File(outputFolderPath)
    try {
      if (!outputFolder.mkdirs()) {
        throw new IOException("Failed to create directory " + outputFolder);
      }
    } catch {
      case e: IOException =>
        e.printStackTrace()
    }

    try {
      var entry: ZipArchiveEntry = null
      while ( {
        entry = archiveInputStream.getNextZipEntry();
        entry != null
      }) {
        if (outputFolder != null) {
          val filename: String = outputFolder + "/" + entry.getName()
          val file: File = new File(filename)
          Utils.logger.info("Extracting file from archive: " + inputArchivePath + "/" + entry.getName() + " to " + filename)
          if (entry.isDirectory()) {
            if (!file.isDirectory() && !file.mkdirs()) {
              throw new IOException("Failed to create directory " + file);
            }
          } else {
            val parent: File = file.getParentFile();
            if (!parent.isDirectory() && !parent.mkdirs()) {
              throw new IOException("Failed to create directory " + parent);
            }
            try {
              val outputStream: OutputStream = Files.newOutputStream(file.toPath())
              IOUtils.copy(archiveInputStream, outputStream)
            }
          }
        }
      }
    } catch {
      case e: IOException =>
        e.printStackTrace()
    } finally if (archiveInputStream != null) archiveInputStream.close()
  }
}
