package com.example.feedbackapiv2;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.web.bind.annotation.*;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api/feedback")
public class FeedbackController {

    private final RabbitTemplate rabbitTemplate;
    
    // Храним заявки в памяти (как требует задание на 3 балла)
    private final List<FeedbackRequest> feedbackList = new ArrayList<>();

    public FeedbackController(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    @PostMapping
    public FeedbackRequest createFeedback(@RequestBody FeedbackRequest request) {
        // 1. Сохраняем в память
        feedbackList.add(request);

        // 2. Отправляем в очередь RabbitMQ с именем "feedback.notify"
        rabbitTemplate.convertAndSend("feedback.notify", request);
        
        System.out.println("=== ОТПРАВЛЕНО В RABBITMQ ===");
        System.out.println("Имя: " + request.name);
        System.out.println("Email: " + request.email);
        System.out.println("Сообщение: " + request.message);

        return request;
    }

    // Простой метод, чтобы проверить, что заявки сохраняются в памяти
    @GetMapping
    public List<FeedbackRequest> getAllFeedback() {
        return feedbackList;
    }
}