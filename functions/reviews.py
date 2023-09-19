"""This is the reviews.py file for the functions app"""
from cloudant.client import Cloudant
from cloudant.query import Query
from flask import Flask, jsonify, request, abort
import atexit

#Add your Cloudant service credentials here
CLOUDANT_USERNAME = '4c8890c0-6c08-4b00-92d6-084ab189f7fb-bluemix'
CLOUDANT_API_KEY = 'T54spJsMa4TYj3uTPv6GeyurH7xI31i5iu8x4RL-l-ll'
CLOUDANT_URL = 'https://4c8890c0-6c08-4b00-92d6-084ab189f7fb-bluemix.cloudantnosqldb.appdomain.cloud'
client = Cloudant.iam(CLOUDANT_USERNAME, CLOUDANT_API_KEY, connect=True, url=CLOUDANT_URL)

session = client.session()
print('Databases:', client.all_dbs())

db = client['reviews']

app = Flask(__name__)

@app.route('/api/get_reviews', methods=['GET'])
def get_reviews():
    """get_reviews function"""
    dealership_id = request.args.get('id')

    # Check if "id" parameter is missing
    if dealership_id is None:
        return jsonify({"error": "Missing 'id' parameter in the URL"}), 400

    # Convert the "id" parameter to an integer (assuming "id" should be an integer)
    try:
        dealership_id = int(dealership_id)
    except ValueError:
        return jsonify({"error": "'id' parameter must be an integer"}), 400

    # Define the query based on the 'dealership' ID
    selector = {
        'dealership': dealership_id
    }

    # Execute the query using the query method
    result = db.get_query_result(selector)

    # Create a list to store the documents
    data_list = []

    # Iterate through the results and add documents to the list
    for doc in result:
        data_list.append(doc)

    # Return the data as JSON
    return jsonify(data_list)


@app.route('/api/post_review', methods=['POST'])
def post_review():
    """the post_review function"""
    if not request.json:
        abort(400, description='Invalid JSON data')

    # Extract review data from the request JSON
    review_data = request.json

    # Validate that the required fields are present in the review data
    required_fields = ['id', 'name', 'dealership', 'review', 'purchase',
                       'purchase_date', 'car_make', 'car_model', 'car_year']
    for field in required_fields:
        if field not in review_data:
            abort(400, description=f'Missing required field: {field}')

    # Save the review data as a new document in the Cloudant database
    db.create_document(review_data)

    return jsonify({"message": "Review posted successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
    