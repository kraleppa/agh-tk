import org.json.JSONObject
import java.io.File
import scala.reflect.io.Directory
import extractors.{ExtractorTar, ExtractorTarGz, ExtractorZip}

class MySuite extends munit.FunSuite {

  test(".zip archive extraction test") {
    //create new result directory
    val resultDirectory = new File("src/test/output/zip")
    resultDirectory.mkdir()

    //extract files
    val archivePath = getClass.getResource("/test.zip").getPath
    val resultPath: String = "src/test/output/zip"
    val message: JSONObject = new JSONObject("{'file': '../inputs/test.zip'}")
    val extractorZip: ExtractorZip = new ExtractorZip()
    extractorZip.extractFiles(archivePath, message, resultPath)

    //check if file exists in the extracted directory
    assert(resultDirectory.listFiles(_.isDirectory).toList.nonEmpty)
    assert(resultDirectory.listFiles(_.isDirectory).toList.head.listFiles(_.isFile).toList.nonEmpty)
    assert(resultDirectory.listFiles(_.isDirectory).toList.head.listFiles(_.isFile).toList.head.getName == "zipfile1.txt")

    //cleanup
    val prevResultDirectory = new Directory(new File("src/test/output/zip"))
    prevResultDirectory.deleteRecursively()
  }

  test(".tar archive extraction test") {
    //create new result directory
    val resultDirectory = new File("src/test/output/tar")
    resultDirectory.mkdir()

    //extract files
    val archivePath = getClass.getResource("/test.tar").getPath
    val resultPath: String = "src/test/output/tar"
    val message: JSONObject = new JSONObject("{'file': '../inputs/test.tar'}")
    val extractorTar: ExtractorTar = new ExtractorTar()
    extractorTar.extractFiles(archivePath, message, resultPath)

    //check if file exists in the extracted directory
    assert(resultDirectory.listFiles(_.isDirectory).toList.nonEmpty)
    assert(resultDirectory.listFiles(_.isDirectory).toList.head.listFiles(_.isFile).toList.nonEmpty)
    assert(resultDirectory.listFiles(_.isDirectory).toList.head.listFiles(_.isFile).toList.head.getName == "tarfile1.txt")

    //cleanup
    val prevResultDirectory = new Directory(new File("src/test/output/tar"))
    prevResultDirectory.deleteRecursively()
  }

  test(".tar.gz archive extraction test") {
    //create new result directory
    val resultDirectory = new File("src/test/output/targz")
    resultDirectory.mkdir()

    //extract files
    val archivePath = getClass.getResource("/test.tar.gz").getPath
    val resultPath: String = "src/test/output/targz"
    val message: JSONObject = new JSONObject("{'file': '../inputs/test.tar.gz'}")
    val extractorTarGz: ExtractorTarGz = new ExtractorTarGz()
    extractorTarGz.extractFiles(archivePath, message, resultPath)

    //check if file exists in the extracted directory
    assert(resultDirectory.listFiles(_.isDirectory).toList.nonEmpty)
    assert(resultDirectory.listFiles(_.isDirectory).toList.head.listFiles(_.isFile).toList.nonEmpty)
    assert(resultDirectory.listFiles(_.isDirectory).toList.head.listFiles(_.isFile).toList.head.getName == "targzfile1.txt")

    //cleanup
    val prevResultDirectory = new Directory(new File("src/test/output/targz"))
    prevResultDirectory.deleteRecursively()
  }
}
