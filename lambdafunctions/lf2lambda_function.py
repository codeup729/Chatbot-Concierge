import json
import boto3
import random
from decimal import Decimal
from requests_aws4auth import AWS4Auth
import requests
from botocore.exceptions import ClientError

# Get AWS credentials
access_key = 'AKIAQZFG5JYFOWX7IPWN'
secret_key = 'cUYO45lmYXiV9CznJiVLvM5HvJaVv165xYs2Q5kq'
region = 'us-east-1'  # e.g., 'us-east-1'

# Set up AWS authentication for OpenSearch
awsauth = AWS4Auth(access_key, secret_key, region, 'es')

# Set up OpenSearch endpoint (replace with your OpenSearch domain endpoint)
opensearch_endpoint = 'https://search-restaurants-oomvx7sjeke3puuq6o2lpqprsu.aos.us-east-1.on.aws'

# Set up DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('yelp-restaurants')  # Name of your DynamoDB table

# Set up SES client
ses = boto3.client('ses', region_name='us-east-1')  # Replace with your SES region

# Function to pull a message from SQS
def pull_sqs_message(event):
    print(event)
    # Extract the message body from the SQS event
    for record in event['Records']:
        print(f"Current Record: {record}")
        message_body = json.loads(record['body'])
        cuisine = message_body['Cuisine']
        email = message_body['Email']
        return cuisine, email

# Function to get a random restaurant from OpenSearch using Boto3
def get_random_restaurant_es(cuisine):
    index_name = 'restaurants'
    
    # Query for restaurants matching the cuisine
    query = {
        "query": {
            "match": {
                "Cuisine": cuisine
            }
        }
    }

    try:
        # Make the request to OpenSearch using SigV4 signing
        url = f"{opensearch_endpoint}/{index_name}/_search"
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, auth=awsauth, headers=headers, json=query)
        response_data = response.json()
        
        # Check if hits are available
        hits = response_data['hits']['hits']
        
        if hits:
            random_hit = random.choice(hits)
            return random_hit['_source']['BusinessID']
        
    except Exception as e:
        print(f"Error querying OpenSearch: {e}")
    
    return None

# Function to get restaurant details from DynamoDB using BusinessID
def get_restaurant_from_dynamodb(business_id, cuisine):
    try:
        # Get the restaurant details from DynamoDB
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('BusinessID').eq(business_id),
            FilterExpression=boto3.dynamodb.conditions.Attr('Cuisine').eq(cuisine)
        )

# Check if any items are returned
        if 'Items' in response and len(response['Items']) > 0:
            # Select a random item from the returned items
            random_item = random.choice(response['Items'])
            # Print the randomly selected item
            return random_item
        else:
            print(f"No items found for BusinessID: {business_id}")
    
    except ClientError as e:
        print(f"Error fetching from DynamoDB: {e}")
    
    return None

# Function to send an email with SES
def send_email(email, restaurant_details):
    subject = f"Your {restaurant_details['Cuisine']} Restaurant Recommendation"
    body = (
        f"Here is a random {restaurant_details['Cuisine']} restaurant recommendation for you:\n\n"
        f"Name: {restaurant_details['Name']}\n"
        f"Address: {restaurant_details['Address']}\n"
        f"Rating: {restaurant_details['Rating']}\n"
        f"Number of Reviews: {restaurant_details['NumberOfReviews']}\n\n"
        f"Enjoy your meal!"
    )
    
    try:
        response = ses.send_email(
            Source='anitejsri22@gmail.com',  # Must be a verified email in SES
            Destination={
                'ToAddresses': [email],
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )
        print(f"Email sent to {email} with response: {response}")
    except ClientError as e:
        print(f"Error sending email: {e}")

# Main Lambda handler
def lambda_handler(event, context):
    # Step 1: Pull the message from the SQS queue
    cuisine, email = pull_sqs_message(event)
    
    # Step 2: Get a random restaurant from OpenSearch for the given cuisine
    business_id = get_random_restaurant_es(cuisine)
    
    if business_id:
        # Step 3: Get the restaurant details from DynamoDB
        restaurant_details = get_restaurant_from_dynamodb(business_id, cuisine)
        
        if restaurant_details:
            print(restaurant_details)
            # Step 4: Send the restaurant details via email using SES
            send_email(email, restaurant_details)
        else:
            print(f"No restaurant details found in DynamoDB for BusinessID {business_id}")
    else:
        print(f"No restaurants found in OpenSearch for cuisine {cuisine}")