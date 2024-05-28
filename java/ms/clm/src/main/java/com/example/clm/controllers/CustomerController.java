package com.example.clm.controllers;

import org.apache.commons.logging.Log;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import com.example.clm.models.TokenModel;
import com.example.clm.services.CLMService;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

@RestController
@RequestMapping("/customer")
public class CustomerController {

     @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private CLMService clmService; // Assuming CLMService is a Spring-managed component
    
    @Autowired
    private TokenController tokenController; // Assuming CLMService is a Spring-managed component

    @GetMapping
    public ResponseEntity<String> getCustomer() {
        try {
            // Get access token
            var at =  tokenController.parseToken(tokenController.getToken());

            // Construct URL for customer data
            String url = clmService.baseURL + "/profile/customers/51";

            // Set up headers with access token
            HttpHeaders headers = new HttpHeaders();
            headers.setBearerAuth(at.accessToken);
            HttpEntity<String> entity = new HttpEntity<>(headers);

            // Make request to fetch customer data
            ResponseEntity<String> responseEntity = restTemplate.exchange(url, HttpMethod.GET, entity, String.class);
            return responseEntity; // Return the response from the other service
        } catch (Exception e) {
            // Handle exceptions gracefully
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Failed to fetch customer data");
        }
    }
    
    
}
