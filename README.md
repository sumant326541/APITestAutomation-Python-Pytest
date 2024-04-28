# API Testing With Pytest

## Getting started

* To download and install `pytest`, run this command from the terminal : `pip install pytest`
* To download and install `requests`, run this command from the terminal : `pip install requests`

To ensure all dependencies are resolved in a CI environment, in one go, add them to a `requirements.txt` file.
* Then run the following command : `pip install -r requirements.txt`

By default pytest only identifies the file names starting with `test_` or ending with `_test` as the test files.

Pytest requires the test method names to start with `test`. All other method names will be ignored even if we explicitly ask to run those methods.

A sample test below :

```python
def test_get_all_user():
    response = requests.get(f"{BASE_URL}/{resource}")
    assert response.status_code == 200

```

### Test step functionality : 

* A detailed explanation of each step has been mentioned in test file.

## Running tests

### Run All test case

If your tests are contained inside a folder 'tests', then run the following command : `pytest tests` 

### Run specific testcase/suite

run the following command for read_operation tests : `pytest tests_read_operation.py` 

## Report

To generate html report, run the following command : `pytest tests --html=report.html -s`

## Findings and issues:

Below test case will fail due to testing api provided not allow to update or create user in database but it will work with actual API

* FAILED tests/test_delete_operation.py::test_delete_nonexisting_user - assert 200 == 404

* FAILED tests/test_read_operation.py::test_verify_newly_created_user - assert 404 == 200

* FAILED tests/test_update_operation.py::test_update_user - AssertionError: assert 'sunt aut fac...reprehenderit' == 'updated title'


