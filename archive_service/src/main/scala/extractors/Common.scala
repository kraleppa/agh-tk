package extractors

import org.apache.commons.compress.archivers.{ArchiveEntry, ArchiveInputStream}
import org.apache.commons.compress.utils.IOUtils
import utils.Utils

import java.io.{File, IOException, OutputStream}
import java.nio.file.Files

object Common {
  def createOutputDirectory(outputFolderRootPath : String) : File = {
    val outputFolderPath = outputFolderRootPath + "/" + uniqueFolderPath()
    val outputFolder = new File(outputFolderPath)
    try {
      if (!outputFolder.mkdirs()) {
        throw new IOException("Failed to create directory " + outputFolder);
      }
    } catch {
      case e: IOException =>
        e.printStackTrace()
    }
    outputFolder
  }

  def copyFiles(archiveInputStream : ArchiveInputStream, outputFolder : File, entry : ArchiveEntry) : Unit = {
    val filename: String = outputFolder + "/" + entry.getName()
    val file: File = new File(filename)
    Utils.logger.info("Extracting file: " + entry.getName() + " to " + filename)
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

  def uniqueFolderPath() : String = {
    "archive-" + System.currentTimeMillis()
  }
}
