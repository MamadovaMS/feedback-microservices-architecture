using Microsoft.AspNetCore.Mvc;
using FeedbackApi.Models;
using FeedbackApi.Data;
using NotifierService; // Пространство имен из proto-файла

namespace FeedbackApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class FeedbackController : ControllerBase
    {
        private readonly AppDbContext _context;
        private readonly Notifier.NotifierClient _notifierClient; // Наш gRPC клиент

        public FeedbackController(AppDbContext context, Notifier.NotifierClient notifierClient)
        {
            _context = context;
            _notifierClient = notifierClient;
        }

        /// <summary>
        /// Создает новую заявку обратной связи.
        /// </summary>
        [HttpPost]
        public async Task<IActionResult> PostFeedback([FromBody] FeedbackRequest request)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var record = new FeedbackRecord
            {
                Id = Guid.NewGuid().ToString(),
                Name = request.Name,
                Email = request.Email,
                Phone = request.Phone,
                Topic = request.Topic,
                Message = request.Message
            };

            // Сохраняем в базу данных
            _context.Feedback.Add(record);
            await _context.SaveChangesAsync();

            // ВЫЗОВ gRPC СЕРВИСА (отправляем уведомление)
            try
            {
                var grpcRequest = new EmailRequest
                {
                    Email = record.Email,
                    Name = record.Name,
                    Message = record.Message
                };
                // Асинхронно вызываем метод SendEmail
                await _notifierClient.SendEmailAsync(grpcRequest);
            }
            catch (Exception ex)
            {
                // Если gRPC упал, мы не должны ломать сохранение заявки
                Console.WriteLine($"Ошибка при отправке gRPC уведомления: {ex.Message}");
            }

            return Created($"/api/feedback/{record.Id}", record);
        }

        /// <summary>
        /// Получает одну заявку по её уникальному идентификатору.
        /// </summary>
        [HttpGet("{id}")]
        public async Task<IActionResult> GetFeedback(string id)
        {
            var record = await _context.Feedback.FindAsync(id);
            if (record == null) return NotFound();
            return Ok(record);
        }
    }
}