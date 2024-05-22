# Microservice Demo

This project is a basic microservice using Spring Boot, Spring Web, and Spring Web Services.

## Getting Started

These instructions will help you set up and run the microservice on your local machine.

### Prerequisites

- Java 17 or higher
- Maven 3.6.3 or higher

### Project Structure

src
├── main
│ ├── java
│ │ └── com
│ │ └── example
│ │ └── demo
│ │ ├── MicroserviceDemoApplication.java
│ │ ├── controller
│ │ │ └── HelloWorldController.java
│ │ ├── soap
│ │ │ ├── HelloWorldEndpoint.java
│ │ │ ├── HelloWorldRequest.java
│ │ │ └── HelloWorldResponse.java
│ │ └── config
│ │ └── WebServiceConfig.java
│ └── resources
│ └── helloworld.xsd
└── test
└── java

### Installing

1. Clone the repository:
    ```bash
    git clone https://github.com/juanjshb/Public/java/ms/demo.git
    cd demo
    ```

2. Build the project using Maven:
    ```bash
    mvn clean install
    ```

### Running the Application

Run the Spring Boot application by executing the `main` method in `MicroserviceDemoApplication.java` or using the following Maven command:

```bash
mvn spring-boot:run
