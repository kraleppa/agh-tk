using System;
using System.Text;
using RabbitMQ.Client;
using Newtonsoft.Json;

class SendTestMessage
{
    public static void Main(string[] args)
    {
        var factory = new ConnectionFactory() { HostName = "localhost", Port = 5672 };
        using (var connection = factory.CreateConnection())
        using (var channel = connection.CreateModel())
        {
            Console.WriteLine(" write exit to quit.");
            do
            {
                Console.WriteLine("Provde msg to send");
                var text = Console.ReadLine();
                if (text == "exit")
                    return;
                List<string> list = new List<string>();
                list.Add("test");
                list.Add("asd");
                var ovj = new MessageToAnalyze
                {
                    words = list,
                    text = text
                };
                byte[] messagebuffer = Encoding.Default.GetBytes(JsonConvert.SerializeObject(ovj));
                channel.BasicPublish(exchange: "text", routingKey: "", basicProperties: null, messagebuffer);
                Console.WriteLine(" [x] Sent {0}", messagebuffer);
            } while (true);
            
        }
    }
}