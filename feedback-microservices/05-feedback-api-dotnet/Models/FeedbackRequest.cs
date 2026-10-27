using System.ComponentModel.DataAnnotations;

namespace FeedbackApi.Models
{
    public class FeedbackRequest
    {
        // Атрибут [Required] означает, что поле обязательно для заполнения (Требование Л5)
        [Required(ErrorMessage = "Имя обязательно")]
        public string Name { get; set; } = string.Empty;

        [Required(ErrorMessage = "Email обязателен")]
        [EmailAddress(ErrorMessage = "Некорректный формат Email")]
        public string Email { get; set; } = string.Empty;

        public string? Phone { get; set; } // Знак вопроса означает, что поле необязательное

        public string? Topic { get; set; }

        [Required(ErrorMessage = "Сообщение обязательно")]
        public string Message { get; set; } = string.Empty;
    }
}