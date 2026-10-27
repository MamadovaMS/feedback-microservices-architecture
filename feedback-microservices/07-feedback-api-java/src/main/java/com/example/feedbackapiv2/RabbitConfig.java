package com.example.feedbackapiv2;

import org.springframework.amqp.core.Queue;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitConfig {

    // 1. Создаем очередь с именем "feedback.notify"
    @Bean
    public Queue feedbackQueue() {
        return new Queue("feedback.notify", false);
    }

    // 2. Учим Java превращать объекты в JSON для RabbitMQ
    @Bean
    public Jackson2JsonMessageConverter jsonMessageConverter() {
        return new Jackson2JsonMessageConverter();
    }
}