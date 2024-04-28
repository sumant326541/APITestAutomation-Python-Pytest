import pytest
import requests
import json

# Read data from apidata.json file
with open('testdata/apidata.json', 'r') as file:
    apidata = json.load(file)

# Extract base URL, resource URL
BASE_URL = apidata.get('base_url')
resource = apidata.get('resource')

# Read data from createuserdata.json file
with open('testdata/createuserdata.json', 'r') as file:
    createuserdata = json.load(file)
# Extract base URL, resource URL, and user_data
user_data = createuserdata.get('user_data')

# Read data from apidata.json file
with open('testdata/readdata.json', 'r') as file:
    readdata = json.load(file)
# Extract user_data with id 46
userdata_id_46 = readdata.get("userdata_id_46")

# Fixture for setup actions (creating a new user)
@pytest.fixture
def setup_create_user(): 
    response = requests.post(f"{BASE_URL}/{resource}", json=user_data)
    assert response.status_code == 201
    id = response.json()["id"]
    
    #we can also consider below point in SetUP
    #If authentication or authorization mechanisms are in place, ensure that test users are authenticated and authorized to perform CRUD operations.
    #Obtain necessary access tokens or credentials to authenticate test requests.

    yield [response, id]  # Provide the response, id to the test function

    # Teardown: Delete the created user after the test completes
    requests.delete(f"{BASE_URL}/{resource}/{id}")
    
# Test case for Read operation
## retrieve user data with id 46
def test_get_user_with_id():
    response = requests.get(f"{BASE_URL}/{resource}/46")
    assert response.status_code == 200
    # Verify the user data response for id 46
    response_user_id46 = response.json()
    assert response_user_id46["title"] == userdata_id_46["title"]
    assert response_user_id46["body"] == userdata_id_46["body"]
    assert response_user_id46["userId"] == userdata_id_46["userId"]

## retrieve all user data
def test_get_all_user():
    response = requests.get(f"{BASE_URL}/{resource}")
    assert response.status_code == 200

## retrieve user data with invalid id
def test_get_user_with_invalid_id():
    response = requests.get(f"{BASE_URL}/{resource}/1000")
    assert response.status_code == 404

## retrieve user data with limit user per page
def test_get_user_with_limit_user_per_page():
    page_number = 2
    limit_per_page = 10

    users = get_paginated_users(page_number, limit_per_page)
    if users:
        unique_user_count = count_unique_users(users)
        assert unique_user_count == limit_per_page
    else:
        print("Failed to fetch users.")

def get_paginated_users(page=1, limit=10):
    response = requests.get(f"{BASE_URL}/{resource}?_page={page}&_limit={limit}")
    assert response.status_code == 200
    return response.json()

def count_unique_users(users):
    ids = set()
    for user in users:
        ids.add(user['id'])
    return len(ids)

## retrieve user data with filter parameter
def test_get_user_with_filter():
    # Filtering parameters 
    filters = {
                "userId": 2  # Filter users by userId 2
              }
    
    response = requests.get(f"{BASE_URL}{resource}", params=filters)

    if response.status_code == 200:
        for user in response.json():
            assert user['userId'] == 2

## retrive newly created user 
def test_verify_newly_created_user(setup_create_user):
    response, id = setup_create_user
    assert id is not None  # Check if the user has been created successfully
    #Verify newly created user in database with id
    response = requests.get(f"{BASE_URL}/{resource}{id}")
    assert response.status_code == 200 # test case will fail beacause newly created user is not updating in database 
               

