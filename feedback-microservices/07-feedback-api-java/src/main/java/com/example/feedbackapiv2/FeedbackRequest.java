package com.example.feedbackapiv2;

public class FeedbackRequest {
    public String name;
    public String email;
    public String message;

    // Пустой конструктор нужен для Spring
    public FeedbackRequest() {}

    // Конструктор для удобства
    public FeedbackRequest(String name, String email, String message) {
        this.name = name;
        this.email = email;
        this.message = message;
    }
}