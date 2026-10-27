using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System.Text;
using System.Text.Json;

namespace NotifierService
{
    public class RabbitMqConsumer : BackgroundService
    {
        private readonly ILogger<RabbitMqConsumer> _logger;
        private IConnection? _connection;
        private IModel? _channel;

        public RabbitMqConsumer(ILogger<RabbitMqConsumer> logger)
        {
            _logger = logger;
        }

        protected override Task ExecuteAsync(CancellationToken stoppingToken)
        {
            var factory = new ConnectionFactory() { HostName = "localhost", Port = 5672, UserName = "guest", Password = "guest" };
            
            _connection = factory.CreateConnection();
            _channel = _connection.CreateModel();

            // Объявляем очередь (на случай, если Java-сервис еще не успел это сделать)
            _channel.QueueDeclare(queue: "feedback.notify", durable: false, exclusive: false, autoDelete: false, arguments: null);

            var consumer = new EventingBasicConsumer(_channel);
            consumer.Received += (model, ea) =>
            {
                var body = ea.Body.ToArray();
                var json = Encoding.UTF8.GetString(body);
               _logger.LogInformation("RAW JSON: " + json); // Выведем сырой текст в консоль для проверки
var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
var feedback = JsonSerializer.Deserialize<FeedbackMessage>(json, options);

                if (feedback != null)
                {
                    _logger.LogInformation("=== ПОЛУЧЕНО ИЗ RABBITMQ ===");
                    _logger.LogInformation("Кому: {Name} <{Email}>", feedback.Name, feedback.Email);
                    _logger.LogInformation("Текст: {Message}", feedback.Message);
                    _logger.LogInformation("===========================");
                    
                    // Подтверждаем обработку (Требование на 4 балла)
                    _channel.BasicAck(deliveryTag: ea.DeliveryTag, multiple: false);
                }
            };

            _channel.BasicConsume(queue: "feedback.notify", autoAck: false, consumer: consumer);

            return Task.CompletedTask;
        }

        public override void Dispose()
        {
            _channel?.Close();
            _connection?.Close();
            base.Dispose();
        }
    }
}