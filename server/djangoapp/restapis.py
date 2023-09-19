"""This is the restapis.py file for the djangoapp app"""
import json
import requests
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
import pdb


def get_request(url, api_key, **kwargs):
    """the get_request method"""
    print(kwargs)
    print(f"GET from {url} ")
    try:
        if api_key:
            # If an API key is provided, use basic authentication with the API key
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        else:
            # If no API key is provided, make a GET request without authentication
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, timeout=10)
        # If the response was successful, no Exception will be raised
    except requests.exceptions.RequestException as err:
        # If any error occurs
        print(f"Network exception occurred: {err}")

    status_code = response.status_code
    print(f"With status {status_code}")
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    """Send an HTTP POST request with JSON payload."""
    try:
        json_payload = json.loads(json_payload)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=json_payload, headers=headers, params=kwargs, timeout=10)
        if response.status_code == 201:
            # Successful response
            return response.json()
        else:
            # Handle errors or non-200 status codes here
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as err:
        # Handle network-related errors
        print(f"Network exception occurred: {err}")
        return None


def get_dealers_from_cf(url, api_key, **kwargs):
    """this gets dealers from a cloud function"""
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, api_key)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"],
                                   long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"], state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_by_id_from_cf(url, dealerId, api_key):
    """This gets dealers by id from a cloud function and assigns sentiment to reviews."""
    results = []

    # Call get_request with a URL parameter and dealerId
    json_result = get_request(url, dealerId=dealerId, api_key=api_key)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer

            # Create a DealerReview object with values in `doc` object
            dealer_obj = DealerReview(
                dealership=dealer_doc["dealership"],
                name=dealer_doc["name"],
                purchase=dealer_doc["purchase"],
                review=dealer_doc["review"],
                purchase_date=dealer_doc["purchase_date"],
                car_make=dealer_doc["car_make"],
                car_model=dealer_doc["car_model"],
                car_year=dealer_doc["car_year"],
                id=dealer_doc["id"]
            )
            # Analyze sentiment for the review and assign it to the sentiment attribute
            if api_key:
                sentiment_result = analyze_review_sentiments(dealer_obj.review, api_key=api_key)
                dealer_obj.sentiment = sentiment_result['keywords'][0]['sentiment']['label']
            results.append(dealer_obj)
    return results


def analyze_review_sentiments(dealerreview, api_key):
    """This analyzes review sentiments."""
    # Define your API key and endpoint URL
    api_key = "aa1cPksgn9BNNMDnmfXSNi3Zw1uVVGBW96LwiOhIhS9p"
    url = "https://api.jp-tok.natural-language-understanding.watson.cloud.ibm.com/instances/01f15925-3af7-4d7c-82f9-dc38d7559563/v1/analyze?version=2019-07-12"
    # Define the headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {api_key}",
    }
    # Define your custom text and parameters
    if len(dealerreview) <= 15:
        parameters = {
            "text": dealerreview,
            "features": {
                "keywords": {
                    "sentiment": True,
                    "limit": 1
                }
            },
            "language": "en"
        }
    elif len(dealerreview) > 15:
        parameters = {
            "text": dealerreview,
            "features": {
                "keywords": {
                    "sentiment": True,
                    "limit": 1
                }
            }
        }
    # Convert the parameters to JSON
    data = json.dumps(parameters)
    # Send the POST request
    response = requests.post(url, data=data, headers=headers, auth=('apikey', api_key))
    # Check if the request was successful
    if response.status_code == 200:
        analysis_result = response.json()
        return analysis_result
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
