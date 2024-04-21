import pytest
import requests
import json

# Read data from data.json file
with open('testdata/data.json', 'r') as file:
    data = json.load(file)

# Extract base URL, resource URL, and user_data
BASE_URL = data.get('base_url')
resource = data.get('resource')
user_data = data.get('user_data')
update_data = data.get('update_data')
userdata_id_46 = data.get("userdata_id_46")

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


# Test case for Create operation
## Create a new user with valid data
def test_create_post(setup_create_user):
    response, id = setup_create_user
    assert id is not None  # Check if the user has been created successfully
    # Verify that the response body contains the created user data 
    created_user = response.json()
    assert created_user["title"] == user_data["title"]
    assert created_user["body"] == user_data["body"]
    assert created_user["userId"] == user_data["userId"]
    #Verify newly created user in database with id
    response = requests.get(f"{BASE_URL}/{resource}{id}")
    assert response.status_code == 200 # test case will fail beacause newly created user is not updating in database 
    
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

# Test case for Update operation
## update an user details
def test_update_user(setup_create_user):
    response, id = setup_create_user
    #updated_response = requests.put(f"{BASE_URL}/{resource}/{id}", json=update_data)  # > newly created user was not updating in database hence trying to update existing user with id = 1
    updated_response = requests.put(f"{BASE_URL}/{resource}/1", json=update_data)  
    #Verify that the user has been updated succefully
    assert updated_response.status_code == 200
    #Verify the id in response body = 1
    assert updated_response.json()["id"] == 1

    #Verify the user has been updated in data base with id 1
    response = requests.get(f"{BASE_URL}/{resource}/1")
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]  # > test case will fail beacause user has not been upadted in database  

## update an non existing user details
def test_update_nonexisting_user():
    response = requests.get(f"{BASE_URL}/{resource}/1000") 
    assert response.status_code == 404 # to check, there is no user with id=1000
    updated_response = requests.put(f"{BASE_URL}/{resource}/1000", json=update_data)  #for id=1000 there will be no user
    assert response.status_code == 404 # check error code for no user found while trying to update user deatils

# Test case for Delete operation
## test delete existing user
def test_delete_user(setup_create_user):
    response, id = setup_create_user
    response = requests.delete(f"{BASE_URL}/{resource}/{id}")
    assert response.status_code == 200

## test delete non-existing user
def test_delete_nonexisting_user():
    response = requests.delete(f"{BASE_URL}/{resource}/1000") 
    assert response.status_code == 404 # The test case fails because it expects a response code of 404 since there is no user existing for the ID=1000. However, the actual response code received is 200.