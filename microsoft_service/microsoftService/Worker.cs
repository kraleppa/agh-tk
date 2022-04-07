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
        private MicrosoftExtractor MicrosoftExtractor = new MicrosoftExtractor();
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
                        _logger.LogInformation(" jsonOBJ: {0}", jsonObj);
                        _logger.LogInformation(" routing key: {0}", routingKey);


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
            var receivedMessage = jsonObj.ToObject<JsonToAnalyze>();

            var extension = routingKey.Split(".");
            _logger.LogInformation(" extension: {0}", extension[extension.Length - 1]);


            string text = extension[^1] switch
            {
                "xlsx" => MicrosoftExtractor.ReadMessageFromExcel(receivedMessage.path),
                "pptx" => MicrosoftExtractor.ReadMessageFromPowerPoint(receivedMessage.path),
                "docx" => MicrosoftExtractor.ReadMessageFromWord(receivedMessage.path),
                _ => ThorwAndLog()
            };


            ForwardResult(factory, jsonObj, text);

            string ThorwAndLog()
            {
                _logger.LogWarning("This extension is not correct. {0}", extension[extension.Length - 1]);
                throw new ArgumentException();
            }
        }

    }
}