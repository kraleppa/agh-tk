using System.Text;
using Microsoft.Extensions.Options;
using Newtonsoft.Json.Linq;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;

namespace TextAnalyzer.Worker
{
    public class Worker : BackgroundService
    {
        public const string targetExchange = "result";
        const string queueName = "text";
        const string exchangeName = "text";

        private readonly IOptions<WorkerOptions> _options;
        private readonly ILogger<Worker> _logger;

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

                channel.QueueBind(queue: queueName, exchange: exchangeName, routingKey: queueName);

                var consumer = new EventingBasicConsumer(channel);
                consumer.Received += (model, ea) =>
                {
                    try
                    {
                        var rawMsg = Encoding.UTF8.GetString(ea.Body.ToArray());
                        var jsonObj = JObject.Parse(rawMsg);

                        var receivedMessage = jsonObj.ToObject<MessageToAnalyze>();
                        var contains = CheckIfTextContainWord(receivedMessage);
                        _logger.LogInformation($" {rawMsg} | {receivedMessage?.text} | {contains}");

                        ForwardResult(factory, jsonObj, contains);
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

        private void ForwardResult(ConnectionFactory factory, JObject receivedMessage, bool contains)
        {
            using var connection = factory.CreateConnection();
            using var channel = connection.CreateModel();

            receivedMessage["contains_word"] = contains;

            var jsonText = receivedMessage.ToString();
            var messageBuffer = Encoding.Default.GetBytes(jsonText);
            channel.BasicPublish(exchange: targetExchange, routingKey: targetExchange, basicProperties: null, messageBuffer);
            _logger.LogInformation(" [x] Sent {0}", jsonText);
        }

        public static bool CheckIfTextContainWord(MessageToAnalyze analyze) => analyze.words.Any(word => analyze.text.Contains(word));
    }
}