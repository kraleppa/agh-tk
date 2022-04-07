using System;
using System.IO;
using System.Reflection;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace MicrsoftExtractorsTest
{
    [TestClass]
    public class UnitTest1
    {

        public string init(string extension)
        {
            string currentDirectory, file;
            switch (extension)
            {
                case "pptx":
                    currentDirectory = AppDomain.CurrentDomain.BaseDirectory;
                    file = System.IO.Path.Combine(currentDirectory, @"..\..\..\TestData\TestPowerPoint.pptx");
                    return Path.GetFullPath(file);
                case "xlsx":
                    currentDirectory = AppDomain.CurrentDomain.BaseDirectory;
                    file = System.IO.Path.Combine(currentDirectory, @"..\..\..\TestData\TestExcel.xlsx");
                    return Path.GetFullPath(file);
                default:
                    currentDirectory = AppDomain.CurrentDomain.BaseDirectory;
                    file = System.IO.Path.Combine(currentDirectory, @"..\..\..\TestData\TestWord.docx");
                    return Path.GetFullPath(file);

            }
        }


        [TestMethod]
        public void TestReadingMessageFromPowerPoint()
        {
            string text;
            string filePath = init("pptx");
            JsonToAnalyze analyze = new JsonToAnalyze();
            analyze.path = filePath;
            MicrosoftExtractor extractor = new MicrosoftExtractor();

            text = extractor.ReadMessageFromPowerPoint(analyze.path);

            Assert.IsNotNull(text);
            Assert.AreEqual(text, "Testowa wiadomoœæ powerpoint");

        }

        [TestMethod]
        public void TestReadingMessageFromWord()
        {
            string text;
            string filePath = init("docx");
            JsonToAnalyze analyze = new JsonToAnalyze();
            analyze.path = filePath;
            MicrosoftExtractor extractor = new MicrosoftExtractor();

            text = extractor.ReadMessageFromWord(analyze.path);

            Assert.IsNotNull(text);
            Assert.AreEqual(text, "Testowa wiadomosc");

        }

        [TestMethod]
        public void TestReadingMessageFromExcel()
        {
            string text;
            string filePath = init("xlsx");
            JsonToAnalyze analyze = new JsonToAnalyze();
            analyze.path = filePath;
            MicrosoftExtractor extractor = new MicrosoftExtractor();

            text = extractor.ReadMessageFromExcel(analyze.path);

            Assert.IsNotNull(text);
            Assert.AreEqual(text, "Testowa wiadomosc excel\r\nTestowa wiadomosc excel\r\nTestowa wiadomosc excel\r\n");

        }

    }
}