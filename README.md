# Chatbot Concierge #

CS-GY 9923 FALL 2024 I <br />
Anitej Srivastava - as19440 

# Chatbot Concierge

![AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-Serverless-orange?style=for-the-badge&logo=awslambda)
![Amazon Lex](https://img.shields.io/badge/Amazon%20Lex-Chatbot-blue?style=for-the-badge&logo=amazonaws)
![API Gateway](https://img.shields.io/badge/API%20Gateway-API%20Management-yellow?style=for-the-badge&logo=amazonaws)
![OpenSearch](https://img.shields.io/badge/OpenSearch-Search-green?style=for-the-badge&logo=opensearch)
![DynamoDB](https://img.shields.io/badge/DynamoDB-NoSQL-blue?style=for-the-badge&logo=amazondynamodb)
![S3](https://img.shields.io/badge/S3-Storage-red?style=for-the-badge&logo=amazons3)
![Swagger](https://img.shields.io/badge/Swagger-API%20Documentation-brightgreen?style=for-the-badge&logo=swagger)

## Overview

**Chatbot Concierge** is a serverless, event-driven application designed to provide restaurant recommendations in Manhattan based on user dining preferences. Leveraging various AWS services, the chatbot interacts with users, processes their inputs, and delivers tailored suggestions.

## Key Features

- **Natural Language Processing**: Utilizes **Amazon Lex** to understand and process user inputs.
- **Serverless Architecture**: Employs **AWS Lambda** for backend processing, ensuring scalability and cost-effectiveness.
- **API Management**: **Amazon API Gateway** facilitates secure and efficient API interactions.
- **Data Storage and Retrieval**:
  - **Amazon S3**: Stores scraped Yelp data and other assets.
  - **Amazon DynamoDB**: Serves as a NoSQL database for quick data access.
  - **Amazon OpenSearch**: Provides advanced search capabilities for restaurant data.
- **API Documentation**: **Swagger** is used for comprehensive API documentation, ensuring clarity and ease of use.

## Architecture Diagram

```plaintext
User
  |
  v
Amazon Lex Chatbot
  |
  v
API Gateway
  |
  v
AWS Lambda Functions
  |
  v
+---------------------------+
|        Data Layer         |
|---------------------------|
| DynamoDB | OpenSearch | S3|
+---------------------------+
```


## Usage ##

1. Clone the repository.
2. Replace `/assets/js/sdk/apigClient.js` with your own SDK file from API
   Gateway.
3. Open `chat.html` in any browser.
4. Start sending messages to test the chatbot interaction.


