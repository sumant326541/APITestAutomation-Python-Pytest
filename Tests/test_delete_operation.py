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