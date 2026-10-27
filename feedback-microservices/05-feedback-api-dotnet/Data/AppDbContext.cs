using Microsoft.EntityFrameworkCore;
using FeedbackApi.Models;

namespace FeedbackApi.Data
{
    public class AppDbContext : DbContext
    {
        // Конструктор, который передает настройки подключения
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }

        // Таблица с нашими заявками
        public DbSet<FeedbackRecord> Feedback { get; set; }
    }
}