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
![AWS SQS](https://img.shields.io/badge/AWS%20SQS-Queue%20Processing-blueviolet?style=for-the-badge&logo=amazonaws)
![Swagger](https://img.shields.io/badge/Swagger-API%20Documentation-brightgreen?style=for-the-badge&logo=swagger)

## Overview

**Chatbot Concierge** is a serverless, event-driven application designed to provide **restaurant recommendations in Manhattan** based on user dining preferences. The chatbot interacts with users, processes their inputs, and delivers tailored suggestions. 

- **Amazon Lex** is used to **map user intents**, understand queries, and trigger appropriate responses.
- **A separate AWS Lambda function** is invoked to process the **recognized intents** and retrieve relevant restaurant recommendations.
- **AWS SQS** is used to store **scraped Yelp restaurant data** (location, cuisine), which then triggers another **Lambda function** to **vectorize and index the data in OpenSearch**.

## Key Features

- **Intent Mapping with Amazon Lex**:  
  - Lex classifies **user intents** (e.g., "Find a restaurant near me", "Show Italian restaurants").
  - Once an intent is identified, Lex triggers a **Lambda function** for fulfillment.
  
- **Intent Processing with AWS Lambda**:  
  - A dedicated **Lambda function processes user requests**, queries OpenSearch, and retrieves the best restaurant recommendations.

- **Data Pipeline & Processing**:
  - **AWS SQS**: Stores all Yelp restaurant data (location, cuisine) and triggers a **Lambda function**.
  - **Lambda + boto3 SDK**: Processes messages from SQS, vectorizes restaurant data, and indexes it in **OpenSearch**.
  - **Amazon OpenSearch**: Enables **fast and efficient** search for restaurant recommendations.

- **Data Storage**:
  - **Amazon S3**: Stores scraped Yelp data and assets.
  - **Amazon DynamoDB**: Serves as a NoSQL database for quick data retrieval.

- **API Management & Documentation**:
  - **Amazon API Gateway**: Facilitates secure and efficient API interactions.
  - **Swagger**: Provides clear and structured API documentation.

## Architecture Diagram

```plaintext
User
  |
  v
Amazon Lex (Intent Mapping)
  |
  v
AWS Lambda (Intent Processing)
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
  |
  v
AWS SQS (Yelp Data Queue)
  |
  v
Lambda (Vectorizes & Indexes Data in OpenSearch)
```


## Usage ##

1. Clone the repository.
2. Replace `/assets/js/sdk/apigClient.js` with your own SDK file from API
   Gateway.
3. Open `chat.html` in any browser.
4. Start sending messages to test the chatbot interaction.


