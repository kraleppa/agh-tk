package pl.agh.tk.pdf
import org.scalatest.flatspec.AnyFlatSpec
import pl.agh.tk.PdfParser

class PdfParserSpec extends AnyFlatSpec {

  "Text from extracted file" should "contain given elements" in {
    val extractedTest = PdfParser.getTextFrom(getClass.getResource("ktane-manual.pdf").toString)
    val keywords = List("jedno", "rozbrajanie bomb", "licznik")
    assert(keywords.forall(word => extractedTest.contains(word)))
  }

}
