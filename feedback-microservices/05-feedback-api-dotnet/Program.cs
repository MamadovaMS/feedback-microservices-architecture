using NotifierService;
using Microsoft.EntityFrameworkCore;
using FeedbackApi.Data;

var builder = WebApplication.CreateBuilder(args);

// Добавляем сервисы контроллеров
builder.Services.AddControllers();

// 1. Подключаем SQLite (скобка закрывается сразу после UseSqlite)
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection") ?? "Data Source=feedback.db"));

// 2. Подключаем gRPC-клиент (отдельным блоком)
builder.Services.AddGrpcClient<Notifier.NotifierClient>(o =>
{
    o.Address = new Uri("http://notifier:8080");
});

// Добавляем Swagger и проверяем наличие XML-файла
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    var xmlFile = $"{System.Reflection.Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    
    // Вот наша защита от падения:
    if (System.IO.File.Exists(xmlPath))
    {
        options.IncludeXmlComments(xmlPath);
    }
});

// Настраиваем CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowReactApp",
        policy =>
        {
            policy.WithOrigins("http://localhost:5173")
                  .AllowAnyHeader()
                  .AllowAnyMethod();
        });
});

var app = builder.Build();
// Автоматически применяем миграции при запуске (создаем таблицы, если их нет)
using (var scope = app.Services.CreateScope())
{
    var dbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    dbContext.Database.Migrate();
}

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors("AllowReactApp");
app.UseAuthorization();
app.MapControllers();

app.Run();