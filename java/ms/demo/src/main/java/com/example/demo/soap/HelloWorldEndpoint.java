package com.example.demo.soap;

import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

@Endpoint
public class HelloWorldEndpoint {

    private static final String NAMESPACE_URI = "http://example.com/microservice/soap";

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "helloWorldRequest")
    @ResponsePayload
    public HelloWorldResponse sayHello(@RequestPayload HelloWorldRequest request) {
        HelloWorldResponse response = new HelloWorldResponse();
        response.setMessage("Hello, " + request.getName() + "!");
        return response;
    }
}
