package pl.agh.tk

import org.apache.pdfbox.pdmodel.PDDocument
import org.apache.pdfbox.text.PDFTextStripper

import java.io.File

object PdfParser {

  val stripper = new PDFTextStripper

  def getTextFrom(path: String): String = {
    val pdf = PDDocument.load(new File(path))
    stripper.getText(pdf).toLowerCase
  }

}
