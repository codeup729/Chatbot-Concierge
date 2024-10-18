import boto3
import requests
import json
import os
from requests_aws4auth import AWS4Auth

access_key = 'AKIAQZFG5JYFOWX7IPWN'
secret_key = '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'
region = 'us-east-1'  

awsauth = AWS4Auth(access_key, secret_key, region, 'es')

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='AKIAQZFG5JYFOWX7IPWN',
    aws_secret_access_key='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',
    region_name='us-east-1'  
)
table = dynamodb.Table('yelp-restaurants')

opensearch_host = 'https://search-restaurants-oomvx7sjeke3puuq6o2lpqprsu.aos.us-east-1.on.aws'  # Replace with your OpenSearch endpoint
index_name = 'restaurants'
doc_type = '_doc'

mapping = {
  "mappings": {
    "properties": {
      "BusinessID": { "type": "keyword" },
      "Cuisine": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      }
    }
  }
}

# response = requests.put(f"{opensearch_host}/{index_name}",
#                         auth=awsauth,
#                         headers={"Content-Type": "application/json"},
#                         data=json.dumps(mapping))

# if response.status_code not in [200, 201]:
#     print(f"Failed to create index: {response.text}")
# else:
#     print("Index created successfully.")

def fetch_dynamodb_items():
    response = table.scan(
        ProjectionExpression='BusinessID, Cuisine'
    )
    data = response['Items']

    # Handle pagination
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression='BusinessID, Cuisine',
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        data.extend(response['Items'])
    return data

def prepare_opensearch_data(items):
    opensearch_data = []
    for item in items:
        
        document = {
            'BusinessID': item.get('BusinessID'),
            'Cuisine': item.get('Cuisine')
        }
        opensearch_data.append(document)
    return opensearch_data

def index_data_to_opensearch(documents):
    headers = {"Content-Type": "application/json"}

    for doc in documents:
        
        url = f"{opensearch_host}/{index_name}/{doc_type}/"

        # Post the document to OpenSearch
        response = requests.post(url,
                                 auth=awsauth,
                                 headers=headers,
                                 data=json.dumps(doc))
        if response.status_code not in [200, 201]:
            print(f"Failed to index document: {response.text}")
        else:
            print(f"Successfully indexed document: {doc['BusinessID']}")


def delete_all_documents(index_name):
    url = f"{opensearch_host}/{index_name}/_delete_by_query"
    query = {
        "query": {
            "match_all": {}
        }
    }
    response = requests.post(url, auth=awsauth, json=query)
    
    if response.status_code == 200:
        print(f"All documents in index {index_name} deleted successfully.")
    else:
        print(f"Error deleting documents from index {index_name}: {response.text}")
   
items = fetch_dynamodb_items()
print(f"Fetched {len(items)} items from DynamoDB.")

documents = prepare_opensearch_data(items)

index_data_to_opensearch(documents)
print("Data transfer complete.")

# delete_all_documents('restaurants')