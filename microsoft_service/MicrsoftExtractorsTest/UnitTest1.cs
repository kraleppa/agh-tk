using System;
using System.IO;
using System.Reflection;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace MicrosoftExtractorsTest
{
    [TestClass]
    public class UnitTest1
    {
        public Stream ReadResource(string name)
        {
            // Determine path
            var assembly = Assembly.GetExecutingAssembly();
            var resourceName = $"MicrosoftExtractorsTest.TestData.{name}";

            var stream = assembly.GetManifestResourceStream(resourceName);
            return stream;
        }


        [TestMethod]
        public void TestReadingMessageFromPowerPoint()
        {
            string text;
            using var file = ReadResource("TestPowerPoint.pptx");
            MicrosoftExtractor extractor = new MicrosoftExtractor();

            text = extractor.ReadMessageFromPowerPoint(file);

            Assert.IsNotNull(text);
            Assert.AreEqual(text, "Testowa wiadomosc powerpoint");
        }

        [TestMethod]
        public void TestReadingMessageFromWord()
        {
            string text;
            using var file = ReadResource("TestWord.docx");
            MicrosoftExtractor extractor = new MicrosoftExtractor();

            text = extractor.ReadMessageFromWord(file);

            Assert.IsNotNull(text);
            Assert.AreEqual(text, "Testowa wiadomosc");
        }

        [TestMethod]
        public void TestReadingMessageFromExcel()
        {
            string text;
            using var file = ReadResource("TestExcel.xlsx");
            MicrosoftExtractor extractor = new MicrosoftExtractor();

            text = extractor.ReadMessageFromExcel(file);

            Assert.IsNotNull(text);
            Assert.AreEqual(text, "Testowa wiadomosc excel");
        }
    }
}