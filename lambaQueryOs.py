"""
This lambda function
helps to query the open search endpoint using 
"""
#import require libraries
import re
import boto3
import json
import logging
import requests
from requests_aws4auth import AWS4Auth

#setting up configuration, ensuring the servicese are in the same region
region = 'us-west-1' # For example, us-east-1
service = 'es'
credentials = boto3.Session().get_credentials()


awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Below code will be used while sending a request  
# The OpenSearch domain endpoint with https://
host= opensearchUrl

#Specify path and remove unwanted keys from output for better performance
path = '_plugins/_sql?format=json&filter_path=-hits.hits._type,-hits.hits._index,-hits.hits._id,-hits.hits._score,-hits.total,-_shards'

url = host + '/' + path

# Elasticsearch 6.x requires an explicit Content-Type header
headers = { "Content-Type": "application/json" }

#Main Lambda execution function

def lambda_handler(event, context):
    response = get_all_record(event)
    return response


#Lambda function that performs action
def get_all_record(event):
    payload = {
        "query": event['queryStringParameters']['searchParam']
     }
    
    # Make the signed HTTP request
    results = requests.post(url, auth=awsauth, headers=headers, data=json.dumps(payload))
    
    #Create a python object from the result
    #Manipulate your result
    json_object=json.dumps(results.text).replace('hits','hitvalues')


    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }

    # Add the search results to the response in json format
    response['body'] = json.loads(json_object)
    return response
