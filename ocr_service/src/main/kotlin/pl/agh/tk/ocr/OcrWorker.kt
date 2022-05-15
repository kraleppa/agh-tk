package pl.agh.tk.ocr

import net.sourceforge.tess4j.Tesseract
import net.sourceforge.tess4j.TesseractException
import org.slf4j.LoggerFactory
import pl.agh.tk.ocr.Utils.LANGUAGES
import pl.agh.tk.ocr.Utils.TESS_DATA
import java.io.File
import java.io.FileNotFoundException

class OcrWorker(tessData: String = TESS_DATA) {

    private val tesseract = Tesseract()

    private val logger = LoggerFactory.getLogger(javaClass)

    init {
        tesseract.setDatapath(tessData)
    }

    fun extractText(filePath: String): String? {
        logger.info("starting extracting text")
        var result = ""
        val file = File(filePath)
        try {
            if (!file.exists()) {
                throw FileNotFoundException("file $filePath does not exist")
            }
            for (lang in LANGUAGES) {
                result = extractText(lang, result, file)
            }
        } catch (e: Exception) {
            logger.error(e.stackTraceToString())
            return null
        }
        logger.info("filePath: $filePath, extracted text: $result")
        return result
    }

    private fun extractText(lang: String, result: String, file: File): String {
        tesseract.setLanguage(lang)
        var extractedText: String? = null
        try {
            extractedText = tesseract.doOCR(file)
        } catch (e: TesseractException) {
            logger.error(e.stackTraceToString())
        }
        return if (extractedText != null) {
            logger.info("lang: $lang, extracted text: $extractedText")
            result.plus(" \n ").plus(extractedText)
        } else {
            logger.error("cannot extract text for lang: $lang")
            result
        }
    }
}