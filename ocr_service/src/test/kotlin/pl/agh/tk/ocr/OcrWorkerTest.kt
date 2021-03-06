package pl.agh.tk.ocr

import org.junit.jupiter.api.Test
import kotlin.io.path.Path
import kotlin.io.path.absolutePathString
import kotlin.test.assertContains
import kotlin.test.assertNotNull

internal class OcrWorkerTest {

    private val ocrWorker = OcrWorker(Path("./tessdata").absolutePathString())

    @Test
    fun extractTextFromFile1Test() {
        val extractedText = ocrWorker.extractText(Path("./test_images/test1231.png").absolutePathString())
        assertNotNull(extractedText)
        assertContains(extractedText, "some test text")
        assertContains(extractedText, "more text")
    }

    @Test
    fun extractTextFromFile2Test() {
        val extractedText = ocrWorker.extractText(Path("./test_images/test2.png").absolutePathString())
        assertNotNull(extractedText)
        assertContains(extractedText, "bLuUeee")
        assertContains(extractedText, "ReD TEXXt")
        assertContains(extractedText, "YellowT ext")
    }
}