using System.Text;
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Presentation;
using DocumentFormat.OpenXml.Spreadsheet;
using DocumentFormat.OpenXml.Wordprocessing;
using Microsoft.Extensions.Options;
using Newtonsoft.Json.Linq;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using A = DocumentFormat.OpenXml.Drawing;

namespace microsoftService
{
    public class Worker : BackgroundService
    {
        private readonly IOptions<WorkerOptions> _options;
        private readonly ILogger<Worker> _logger;
        const string queueName = "format.microsoft";
        const string targetExchange = "text";

        public Worker(IOptions<WorkerOptions> options,
            ILogger<Worker> logger)
        {
            _options = options;
            _logger = logger;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            var options = _options.Value;
            var factory = new ConnectionFactory()
            {
                HostName = options.Hostname,
                Port = options.Port
            };

            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    using var con = factory.CreateConnection();
                    break;
                }
                catch
                {
                    _logger.LogInformation("Waiting for queue to be reachable");
                    await Task.Delay(1_000);
                }
            }

            while (!stoppingToken.IsCancellationRequested)
            {
                using var connection = factory.CreateConnection();
                using var channel = connection.CreateModel();

                channel.QueueDeclarePassive(queue: queueName);

                var consumer = new EventingBasicConsumer(channel);
                consumer.Received += (model, ea) =>
                {
                    try
                    {
                        var rawMsg = Encoding.UTF8.GetString(ea.Body.ToArray());
                        var jsonObj = JObject.Parse(rawMsg);
                        var routingKey = ea.RoutingKey;
                        _logger.LogInformation(" rawMSG {0}", rawMsg);
                        _logger.LogInformation(" jsonOBJ {0}", jsonObj);
                        _logger.LogInformation(" routing key {0}", routingKey);


                        ExtractMessageFromMicrosoftDocument(factory, jsonObj, routingKey);
                    }
                    catch (Exception ex)
                    {
                        _logger.LogWarning(ex, $"Something went wrong.");
                        Task.Delay(1_000, stoppingToken).GetAwaiter().GetResult();
                    }
                };
                channel.BasicConsume(queue: queueName, autoAck: true, consumer: consumer);

                await Task.Delay(Timeout.Infinite, stoppingToken);
            }
        }

        private void ForwardResult(ConnectionFactory factory, JObject jsonObj, string text)
        {
            using var connection = factory.CreateConnection();
            using var channel = connection.CreateModel();

            jsonObj["text"] = text;

            var jsonText = jsonObj.ToString();
            var messageBuffer = Encoding.Default.GetBytes(jsonText);
            channel.BasicPublish(exchange: targetExchange, routingKey: targetExchange, basicProperties: null,
                messageBuffer);
            _logger.LogInformation(" [x] Sent {0}", jsonText);
        }

        private void ExtractMessageFromMicrosoftDocument(ConnectionFactory factory, JObject jsonObj, string routingKey)
        {
            _logger.LogInformation(" ENTERED ExtractMessageFromMicrosoftDocument");
            var receivedMessage = jsonObj.ToObject<JsonToAnalyze>();

            _logger.LogInformation(" ");

            var extension = routingKey.Split(".");
            _logger.LogInformation(" extension {0}", extension[extension.Length - 1]);


            string text = extension[^1] switch
            {
                "xlsx" => ReadMessageFromExcel(receivedMessage.path),
                "pptx" => ReadMessageFromPowerPoint(receivedMessage.path),
                "docx" => ReadMessageFromWord(receivedMessage.path),
                _ => ThorwAndLog()
            };


            ForwardResult(factory, jsonObj, text);

            string ThorwAndLog()
            {
                _logger.LogWarning("This extension is not correct. {0}", extension[extension.Length - 1]);
                throw new ArgumentException();
            }
        }


        private string ReadMessageFromExcel(string filePath)
        {
            using (SpreadsheetDocument spreadsheetDocument = SpreadsheetDocument.Open(filePath, false))
            {
                StringBuilder text = new StringBuilder();

                WorkbookPart workbookPart = spreadsheetDocument.WorkbookPart;
                SharedStringTablePart sstpart = workbookPart.GetPartsOfType<SharedStringTablePart>().First();
                SharedStringTable sst = sstpart.SharedStringTable;

                WorksheetPart worksheetPart = workbookPart.WorksheetParts.First();
                Worksheet sheet = worksheetPart.Worksheet;

                var rows = sheet.Descendants<Row>();

                foreach (Row row in rows)
                {
                    foreach (Cell c in row.Elements<Cell>())
                    {
                        if ((c.DataType != null) && (c.DataType == CellValues.SharedString))
                        {
                            int ssid = int.Parse(c.CellValue.Text);
                            string str = sst.ChildElements[ssid].InnerText;
                            text.Append(str);
                            text.Append(Environment.NewLine);
                        }
                        
                    }
                }
                return text.ToString();
            }
        }

        private string ReadMessageFromWord(string filePath)
        {
            string text;

            using (WordprocessingDocument wordDoc = WordprocessingDocument.Open(filePath, false))
            {
                Body body = wordDoc.MainDocumentPart.Document.Body;
                text = body.InnerText;
                return text;

            }
        }

        private string ReadMessageFromPowerPoint(string filePath)
        {
            string text = null;

            int numberOfSlides = CountSlides(filePath);
            for (int i = 0; i < numberOfSlides; i++)
            {
                string newText = GetSlideIdAndText(filePath, i);
                text += newText;
            }

            return text;
        }


        public static int CountSlides(string filePath)
        {
            using (PresentationDocument presentationDocument = PresentationDocument.Open(filePath, false))
            {
                if (presentationDocument == null)
                {
                    throw new ArgumentNullException("presentationDocument");
                }

                int slidesCount = 0;

                PresentationPart presentationPart = presentationDocument.PresentationPart;
                if (presentationPart != null)
                {
                    slidesCount = presentationPart.SlideParts.Count();
                }

                return slidesCount;
            }
        }

        public static string GetSlideIdAndText( string filePath, int index)
        {
            using (PresentationDocument ppt = PresentationDocument.Open(filePath, false))
            {
                PresentationPart part = ppt.PresentationPart;
                OpenXmlElementList slideIds = part.Presentation.SlideIdList.ChildElements;

                string relId = (slideIds[index] as SlideId).RelationshipId;

                SlidePart slide = (SlidePart) part.GetPartById(relId);

                StringBuilder paragraphText = new StringBuilder();

                IEnumerable<A.Text> texts = slide.Slide.Descendants<A.Text>();
                foreach (A.Text text in texts)
                {
                    paragraphText.Append(text.Text);
                }

                return paragraphText.ToString();
            }
        }
    }
}