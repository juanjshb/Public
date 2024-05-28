package com.example.clm;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;

import com.example.clm.services.CLMService;

@SpringBootApplication
public class ClmApplication {

	public static void main(String[] args) {
		SpringApplication.run(ClmApplication.class, args);
	}

	@Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
	
	@Bean
    public CLMService clmService() {
        return new CLMService();
    }
}

