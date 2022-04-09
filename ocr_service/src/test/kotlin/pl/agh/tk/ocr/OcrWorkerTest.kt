package pl.agh.tk.ocr

import org.junit.jupiter.api.Test
import kotlin.io.path.Path
import kotlin.io.path.absolutePathString
import kotlin.test.assertContains

internal class OcrWorkerTest {

    private val ocrWorker = OcrWorker(Path("./tessdata").absolutePathString())

    @Test
    fun extractTextFromFile1Test() {
        val extractedText = ocrWorker.extractText(Path("./test1.png").absolutePathString())
        assertContains(extractedText, "some test text")
        assertContains(extractedText, "more text")
    }

    @Test
    fun extractTextFromFile2Test() {
        val extractedText = ocrWorker.extractText(Path("./test2.png").absolutePathString())
        assertContains(extractedText, "bLuUeee")
        assertContains(extractedText, "ReD TEXXt")
        assertContains(extractedText, "YellowT ext")
    }

    @Test
    fun extractTextFromFile3Test() {
        val extractedText = ocrWorker.extractText(Path("./test1.png").absolutePathString())
        assertContains(extractedText, "some test text")
        assertContains(extractedText, "ASDASDASDASDADASD")
    }
}