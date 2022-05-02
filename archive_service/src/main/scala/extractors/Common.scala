package extractors

import org.apache.commons.compress.archivers.{ArchiveEntry, ArchiveInputStream}
import org.apache.commons.compress.utils.IOUtils
import java.io.{File, IOException, OutputStream}
import java.nio.file.Files
import org.json.JSONObject
import publisher.Publisher
import utils.Utils

object Common {

  def handleExtracting(inputStream : ArchiveInputStream, inputArchivePath : String, outputFolderRootPath: String, message : JSONObject): Unit = {
    val outputFolder = createOutputDirectory(outputFolderRootPath)
    try {
      var entry: ArchiveEntry = null
      while ( {
        entry = inputStream.getNextEntry
        entry != null
      }) {
        if (outputFolder != null) {
          copyFiles(inputStream, outputFolder, entry)
          val archive : JSONObject = new JSONObject()
          archive.put("filePathInVolume", createPath(outputFolder.getPath, entry.getName))
          archive.put("filePathInArchive", createPath(inputArchivePath, entry.getName))
          message.put("archive", archive)
          Publisher.publish(message.toString)
        }
      }
    } catch {
      case e: IOException =>
        e.printStackTrace()
    } finally if (inputStream != null) inputStream.close()
  }

  private[this] def createOutputDirectory(outputFolderRootPath : String) : File = {
    val outputFolderPath = createPath(outputFolderRootPath, getUniqueFolderPath())
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

  private[this] def copyFiles(inputStream : ArchiveInputStream, outputFolder : File, entry : ArchiveEntry) : Unit = {
    val filename: String = createPath(outputFolder.getPath, entry.getName)
    val file: File = new File(filename)
    if (entry.isDirectory) {
      if (!file.isDirectory && !file.mkdirs()) {
        throw new IOException("Failed to create directory " + file);
      }
    } else {
      val parent: File = file.getParentFile
      if (!parent.isDirectory && !parent.mkdirs()) {
        throw new IOException("Failed to create directory " + parent);
      }
      val outputStream: OutputStream = Files.newOutputStream(file.toPath)
      IOUtils.copy(inputStream, outputStream)
      Utils.logger.info("Extracted file: " + entry.getName + " to " + filename)
    }
  }

  private[this] def getUniqueFolderPath() : String = {
    "archive-" + System.currentTimeMillis()
  }

  private[this] def createPath(directoryPath : String, filePath : String) : String = {
    directoryPath + "/" + filePath
  }
}
