package com.example.clm.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import com.example.clm.models.TokenModel;
import com.example.clm.services.CLMService;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

@RestController
@RequestMapping("/token")
public class TokenController {

  @Autowired
  private RestTemplate restTemplate;

  @PostMapping
  public ResponseEntity<String> getToken() {

    CLMService appConfig =  new CLMService();
    String url = appConfig.baseURL + "login";
    // Replace with actual values (avoid hardcoding sensitive data)

    // Build the request body with x-www-form-urlencoded format
    MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
    body.add("client_id", appConfig.apiKey);
    body.add("client_secret", appConfig.apiSecret);

    // Set headers with Content-Type application/x-www-form-urlencoded
    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

    HttpEntity<MultiValueMap<String, String>> requestEntity = new HttpEntity<>(body, headers);

    ResponseEntity<String> response = restTemplate.postForEntity(url, requestEntity, String.class);
    return response;
  }

  public TokenModel parseToken(ResponseEntity<String> responseEntity) {
    TokenModel token = null;
    try {
        // Check if the response is successful before parsing
        if (responseEntity != null && responseEntity.getStatusCode().is2xxSuccessful()) {
            // Read JSON from the response body
            String responseBody = responseEntity.getBody();
            if (responseBody != null) {
                // Parse JSON
                ObjectMapper objectMapper = new ObjectMapper();
                JsonNode jsonNode = objectMapper.readTree(responseBody);

                // Extract token fields
                String accessToken = jsonNode.get("access_token").asText();
                String tokenType = jsonNode.get("token_type").asText();
                int expiresIn = jsonNode.get("expires_in").asInt();
                String scope = jsonNode.get("scope").asText();
                String jti = jsonNode.get("jti").asText();

                // Create TokenModel object
                token = new TokenModel(accessToken, tokenType, expiresIn, scope, jti);
            }
        } else {
            // Handle non-successful response
            System.out.println("Error: Non-successful response");
        }
    } catch (Exception e) {
        // Handle parsing or other exceptions
        System.out.println("Error parsing token: " + e.getMessage());
    }
    return token;
}
}