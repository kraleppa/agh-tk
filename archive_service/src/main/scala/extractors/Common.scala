package extractors

import org.apache.commons.compress.archivers.{ArchiveEntry, ArchiveInputStream}
import org.apache.commons.compress.utils.IOUtils
import java.io.{File, IOException, OutputStream}
import java.nio.file.Files
import org.json.JSONObject
import publisher.Publisher
import utils.Utils

object Common {

  def handleExtraction(inputStream: ArchiveInputStream, inputArchivePath: String, outputDirectoryPathRoot: String, message: JSONObject): Unit = {
    val outputDirectory: File = createOutputDirectory(outputDirectoryPathRoot)
    try {
      var entry: ArchiveEntry = null
      while ( {
        entry = inputStream.getNextEntry
        entry != null
      }) {
        if (outputDirectory != null) {
          extractFiles(inputStream, outputDirectory, entry)
          val archive: JSONObject = new JSONObject()
          archive.put("filePathInVolume", joinPaths(outputDirectory.getPath, entry.getName))
          archive.put("filePathInArchive", joinPaths(inputArchivePath, entry.getName))
          message.put("archive", archive)
          Publisher.publish(message.toString)
        }
      }
    } catch {
      case e: IOException =>
        e.printStackTrace()
    } finally if (inputStream != null) inputStream.close()
  }

  private[this] def createOutputDirectory(outputDirectoryPathRoot: String) : File = {
    val outputDirectoryPath: String = joinPaths(outputDirectoryPathRoot, getUniqueDirectoryPath())
    val outputDirectory: File = new File(outputDirectoryPath)
    try {
      if (!outputDirectory.mkdirs()) {
        throw new IOException("Failed to create directory " + outputDirectory);
      }
    } catch {
      case e: IOException =>
        e.printStackTrace()
    }
    outputDirectory
  }

  private[this] def extractFiles(inputStream: ArchiveInputStream, outputDirectory: File, archiveEntry: ArchiveEntry) : Unit = {
    val extractedFilePath: String = joinPaths(outputDirectory.getPath, archiveEntry.getName)
    val extractedFile: File = new File(extractedFilePath)
    if (archiveEntry.isDirectory) {
      if (!extractedFile.isDirectory && !extractedFile.mkdirs()) {
        throw new IOException("Failed to create directory " + extractedFile);
      }
    } else {
      val parent: File = extractedFile.getParentFile
      if (!parent.isDirectory && !parent.mkdirs()) {
        throw new IOException("Failed to create directory " + parent);
      }
      val outputStream: OutputStream = Files.newOutputStream(extractedFile.toPath)
      IOUtils.copy(inputStream, outputStream)
      Utils.logger.info("Extracted file: " + archiveEntry.getName + " to " + extractedFilePath)
    }
  }

  private[this] def getUniqueDirectoryPath(): String = {
    "archive-" + System.currentTimeMillis()
  }

  private[this] def joinPaths(directoryPath: String, filePath: String): String = {
    directoryPath + "/" + filePath
  }
}
