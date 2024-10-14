import requests
import boto3
from datetime import datetime
import time
from decimal import Decimal

# Set up Yelp API key and endpoint
YELP_API_KEY = 'Ktf5TEcZteShnVVd4BxD1jdg8WMo2mj3bKT8ehVNVPaDsyI3w0stl35bz-FV5c7v3Ju4izdL_bzmaE8Au8sUwHG8pnl0frN_drp7c37moIedRl0uma7-fJ-lqUsNZ3Yx'
headers = {'Authorization': f'Bearer {YELP_API_KEY}'}
base_url = 'https://api.yelp.com/v3/businesses/search'

# Set up AWS DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='AKIAQZFG5JYFOWX7IPWN',
    aws_secret_access_key='cUYO45lmYXiV9CznJiVLvM5HvJaVv165xYs2Q5kq',
    region_name='us-east-1'  
)
table = dynamodb.Table('yelp-restaurants')

# Define your cuisine types and Manhattan search parameters
cuisine_types = ['Chinese', 'Italian', 'Indian', 'Mexican', 'Japanese', 'American', 'Thai', 'Mediterranean']
params = {
    'location': 'Manhattan, NY',
    'limit': 50,
    'offset': 0,
    'categories': ''
}

# Function to fetch data from Yelp API
def fetch_restaurants(cuisine):
    restaurants = []
    params['categories'] = cuisine
    params['offset'] = 0
    while len(restaurants) < 1000:  # Targeting 1000 restaurants per cuisine
        response = requests.get(base_url, headers=headers, params=params)
        data = response.json()
        if 'businesses' not in data:
            break
        restaurants.extend(data['businesses'])
        params['offset'] += 50
        time.sleep(1)  # Avoid hitting rate limits
    return restaurants

# Function to store restaurant data in DynamoDB
def store_in_dynamodb(restaurants, cuisine):
    for restaurant in restaurants:
        try:
            item = {
                'BusinessID': restaurant['id'],
                'Name': restaurant['name'],
                'Address': ', '.join(restaurant['location']['display_address']),
                'Coordinates': {
            'latitude': Decimal(str(restaurant['coordinates']['latitude'])),
            'longitude': Decimal(str(restaurant['coordinates']['longitude']))
        },
                'Cuisine': cuisine,
                'NumberOfReviews': restaurant['review_count'],
                'Rating': str(restaurant['rating']),
                'ZipCode': restaurant['location']['zip_code'],
                'insertedAtTimestamp': datetime.utcnow().isoformat()
            }
            table.put_item(Item=item)
        except Exception as e:
            print(f"Error storing item: {e}")

# Main loop to fetch and store restaurants by cuisine
for cuisine in cuisine_types:
    restaurants = fetch_restaurants(cuisine)
    store_in_dynamodb(restaurants, cuisine)
    print(f"Stored {len(restaurants)} {cuisine} restaurants in DynamoDB.")
