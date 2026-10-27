using Grpc.Core;
using NotifierService;

namespace NotifierService.Services
{
    public class NotifierService : Notifier.NotifierBase
    {
        private readonly ILogger<NotifierService> _logger;

        public NotifierService(ILogger<NotifierService> logger)
        {
            _logger = logger;
        }

        // Реализация метода SendEmail
        public override Task<EmailResponse> SendEmail(EmailRequest request, ServerCallContext context)
        {
            // Пока просто выводим в консоль то, что к нам пришло (это 3 балла)
            _logger.LogInformation("=== НОВОЕ УВЕДОМЛЕНИЕ ===");
            _logger.LogInformation("Кому: {Name} <{Email}>", request.Name, request.Email);
            _logger.LogInformation("Текст: {Message}", request.Message);
            _logger.LogInformation("========================");

            // Возвращаем ответ клиенту
            return Task.FromResult(new EmailResponse
            {
                Success = true,
                StatusMessage = "Email успешно отправлен (имитация)"
            });
        }
    }
}