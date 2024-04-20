import pytest
import requests
import json

# Read data from data.json file
with open('data.json', 'r') as file:
    data = json.load(file)

# Extract base URL, resource URL, and post data
BASE_URL = data.get('base_url')
resource_url = data.get('resource')
post_data = data.get('post_data')
update_data = data.get('update_data')

# Fixture for setup actions (creating a test post)
@pytest.fixture
def setup_create_post(): 
    response = requests.post(f"{BASE_URL}/posts", json=post_data)
    assert response.status_code == 201
    post_id = response.json()["id"]

    yield [response, post_id]  # Provide the response, post_id, post_data to the test function

    # Teardown: Delete the created post after the test completes
    requests.delete(f"{BASE_URL}/posts/{post_id}")


# Test case for Create operation
def test_create_post(setup_create_post):
    response, post_id = setup_create_post
    assert post_id is not None  # Check if the post was created successfully
    # Verify that the response body contains the created user data 
    created_user = response.json()
    assert created_user["title"] == post_data["title"]
    assert created_user["body"] == post_data["body"]
    assert created_user["userId"] == post_data["userId"]
    #Verify newly created user in database with post_id
    response = requests.get(f"{BASE_URL}/posts{post_id}")
    assert response.status_code == 200 # test case will fail beacause newly created post is not updating in database 
    
# Test case for Read operation
def test_read_post():
    response = requests.get(f"{BASE_URL}/posts/100")
    assert response.status_code == 200
    
# Test case for Update operation
def test_update_post(setup_create_post):
    response, post_id = setup_create_post
    #updated_response = requests.put(f"{BASE_URL}/posts/{post_id}", json=update_data)  # > newly created post is not updating in database hence trying to update existing post with id = 1
    updated_response = requests.put(f"{BASE_URL}/posts/1", json=update_data)  
    #Verify that the post was updated succefully
    assert updated_response.status_code == 200
    #Verify that the id in response body = 1
    assert updated_response.json()["id"] == 1

    #Verify that post is updated in data base with id 1
    response = requests.get(f"{BASE_URL}/posts/1")
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"] # # test case will fail beacause post is not updating in database  

# Test case for Delete operation
def test_delete_post(setup_create_post):
    response, post_id = setup_create_post
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200

