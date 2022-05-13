using System.Text;
using Microsoft.Extensions.Options;
using Newtonsoft.Json.Linq;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;


namespace microsoftService
{
    public class Worker : BackgroundService
    {
        private readonly IOptions<WorkerOptions> _options;
        private readonly ILogger<Worker> _logger;
        private MicrosoftExtractor MicrosoftExtractor = new MicrosoftExtractor();
        const string queueName = "format.microsoft";
        const string targetExchange = "text";
        const string resultExchange = "result";

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

        private void ExtractMessageFromMicrosoftDocument(ConnectionFactory factory, JObject jsonObj, string routingKey)
        {
            var receivedMessage = jsonObj.ToObject<JsonToAnalyze>();
            var extension = routingKey.Split(".");
            _logger.LogInformation(" extension: {0}", extension[extension.Length - 1]);

            using var fileStream = File.OpenRead(receivedMessage.file);
            string text = extension[^1] switch
            {
                "xlsx" => MicrosoftExtractor.ReadMessageFromExcel(fileStream),
                "pptx" => MicrosoftExtractor.ReadMessageFromPowerPoint(fileStream),
                "docx" => MicrosoftExtractor.ReadMessageFromWord(fileStream),
                _ => ThorwAndLog()
            };


            ForwardResult(factory, jsonObj, text);

            string ThorwAndLog()
            {
                _logger.LogWarning("This extension is not correct. {0}", extension[extension.Length - 1]);
                throw new ArgumentException();
            }
        }

        private void ForwardResult(ConnectionFactory factory, JObject jsonObj, string text)
        {
            using var connection = factory.CreateConnection();
            using var channel = connection.CreateModel();

            jsonObj["text"] = text;
            var fileStateJson = jsonObj["fileState"];
            if(fileStateJson != null
                && fileStateJson is JObject fileStateJsonObject)
                fileStateJsonObject["fileProcessed"] = true;

            var jsonText = jsonObj.ToString();
            var messageBuffer = Encoding.Default.GetBytes(jsonText);
            
            channel.BasicPublish(exchange: targetExchange, routingKey: targetExchange, basicProperties: null,
                messageBuffer);
            _logger.LogInformation(" [x] Sent message to text exchange: {0}", jsonText);
            channel.BasicPublish(exchange: resultExchange, routingKey: resultExchange, basicProperties: null,
                messageBuffer);
            _logger.LogInformation(" [x] Sent message to result exchange: {0}", jsonText);
        }
    }
}