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

# Read data from updateuserdata.json file
with open('testdata/updateuserdata.json', 'r') as file:
    updateuserdata = json.load(file)
# Extract update_data 
update_data = updateuserdata.get('update_data')

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

