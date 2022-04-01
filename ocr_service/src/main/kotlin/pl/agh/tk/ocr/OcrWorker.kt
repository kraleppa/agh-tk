package pl.agh.tk.ocr

import net.sourceforge.tess4j.Tesseract
import org.slf4j.LoggerFactory
import pl.agh.tk.ocr.Utils.Lang
import pl.agh.tk.ocr.Utils.TESS_DATA
import java.io.File
import java.io.FileNotFoundException

class OcrWorker {

    private val tesseract = Tesseract()

    private val logger = LoggerFactory.getLogger(javaClass)

    init {
        tesseract.setDatapath(TESS_DATA)
        tesseract.setLanguage(Lang.ENG.value)
    }

    fun extractText(filePath: String): String? {
        logger.info("starting extracting text")
        var result: String?
        try {
            val file = File(filePath)
            if (!file.exists()) {
                throw FileNotFoundException("file $filePath does not exist")
            }
            result = tesseract.doOCR(file)
            logger.info("text extracted successfully: $result")
        } catch (e: Exception) {
            logger.error("file $filePath might not exist")
            logger.error(e.stackTraceToString())
            result = null
        }
        return result
    }
}