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
            currentDirectory = AppDomain.CurrentDomain.BaseDirectory;
            switch (extension)
            {
                case "pptx":
                    file = System.IO.Path.Combine(currentDirectory, @".\TestData\TestPowerPoint.pptx");
                    Console.Write(file);
                    return Path.GetFullPath(file);
                case "xlsx":
                    file = System.IO.Path.Combine(currentDirectory, @".\TestData\TestExcel.xlsx");
                    return Path.GetFullPath(file);
                default:
                    file = System.IO.Path.Combine(currentDirectory, @".\TestData\TestWord.docx");
                    return Path.GetFullPath(file);
            }
        }


        [TestMethod]
        public void TestReadingMessageFromPowerPoint()
        {
            string text;
            string filePath = init("pptx");
            JsonToAnalyze analyze = new JsonToAnalyze();
            analyze.file = filePath;
            MicrosoftExtractor extractor = new MicrosoftExtractor();

            text = extractor.ReadMessageFromPowerPoint(analyze.file);

            Assert.IsNotNull(text);
            Assert.AreEqual(text, "Testowa wiadomo�� powerpoint");
        }

        [TestMethod]
        public void TestReadingMessageFromWord()
        {
            string text;
            string filePath = init("docx");
            JsonToAnalyze analyze = new JsonToAnalyze();
            analyze.file = filePath;
            MicrosoftExtractor extractor = new MicrosoftExtractor();

            text = extractor.ReadMessageFromWord(analyze.file);

            Assert.IsNotNull(text);
            Assert.AreEqual(text, "Testowa wiadomosc");
        }

        [TestMethod]
        public void TestReadingMessageFromExcel()
        {
            string text;
            string filePath = init("xlsx");
            JsonToAnalyze analyze = new JsonToAnalyze();
            analyze.file = filePath;
            MicrosoftExtractor extractor = new MicrosoftExtractor();

            text = extractor.ReadMessageFromExcel(analyze.file);

            Assert.IsNotNull(text);
            Assert.AreEqual(text, "Testowa wiadomosc excel\r\nTestowa wiadomosc excel\r\nTestowa wiadomosc excel\r\n");
        }
    }
}