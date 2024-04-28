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
   