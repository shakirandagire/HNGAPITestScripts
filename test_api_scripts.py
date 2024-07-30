import pytest
import requests
BASE_URL = "https://deployment.api-csharp.boilerplate.hng.tech/api/v1"
# BASE_URL = "https://deployment.api-golang.boilerplate.hng.tech/api/v1"
# Test data
register_data = {
    "firstName": "John",
    "lastName": "Diana",
    "email": "john.doe@example.com",
    "password": "TestsecurePass123",
    "phoneNumber": "09011123345"
}
job_data = {
    "title": "Software Engineer",
    "description": "Develop and maintain software solutions.",
    "location": "Remote",
    "salary": 100000,
    "level": 2,
    "company": "Tech Corp PLC"
}
org_data = {
    "name": "HNG Tech PLC",
    "description": "A technology company.",
    "email": "hng-contact@techcorp.com",
    "industry": "Technology",
    "type": "Private",
    "country": "NG",
    "address": "1234 HNG Tech Street",
    "state": "LA"
}
@pytest.fixture
def auth_token():
    # Register user
    requests.post(f"{BASE_URL}/auth/register", json=register_data)
    # Login user
    login_data = {
        "email": register_data['email'],
        "password": register_data['password']
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    return data['data']['token']

@pytest.fixture
def job_id(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/jobs", json=job_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    return data['id']

@pytest.fixture
def org_id(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/organizations", json=org_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    return data['data']['id']

def test_get_jobs():
    response = requests.get(f"{BASE_URL}/jobs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
      # Assuming the response is a list of jobs
def test_get_job_by_id(job_id):
    response = requests.get(f"{BASE_URL}/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == job_id
    assert data['title'] == job_data['title']

def test_create_job(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/jobs", json=job_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == job_data['title']

def test_contact():
    contact_data = {
        "name": "John Diana",
        "email": "john.doe@example.com",
        "message": "Hello, I don't have python."
    }
    response = requests.post(f"{BASE_URL}/contact", json=contact_data)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "Message received"

def test_help_center_topics():
    response = requests.get(f"{BASE_URL}/help-center/topics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data['topics'], list)

def test_help_center_search():
    response = requests.get(f"{BASE_URL}/help-center/topics/search?title=Help")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data['topics'], list)

def test_faqs():
    response = requests.get(f"{BASE_URL}/faqs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_newsletter():
    newsletter_data = {
        "email": "john.doe@example.com"
    }
    response = requests.post(f"{BASE_URL}/pages/newsletter", json=newsletter_data)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "Subscribed"

def test_create_organization(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/organizations", json=org_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data['data']['name'] == org_data['name']

def test_update_organization(auth_token, org_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    update_data = {"name": "Updated Tech Corp"}
    response = requests.patch(f"{BASE_URL}/organizations/{org_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['org']['name'] == update_data['name']

def test_get_organization_users(auth_token, org_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/organizations/{org_id}/users", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data['users'], list)

def test_get_organization_by_id(auth_token, org_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/organizations/{org_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['data']['id'] == org_id

def test_delete_user_from_organization(auth_token, org_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    user_id = "some_user_id"  # Replace with actual user_id
    response = requests.delete(f"{BASE_URL}/organizations/{org_id}/users/{user_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data['message'] == "user deleted successfully"

def test_delete_organization(auth_token, org_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.delete(f"{BASE_URL}/organizations/{org_id}", headers=headers)
    assert response.status_code == 200

def test_initiate_product_transaction():
    transaction_data = {
        "email": "john.diana2@example.com",
        "amount": 100,
        "productId": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/transactions/initiate/product", headers=headers,
        json=transaction_data)
    assert response.status_code == 201
    data = response.json()
    for product in data:
        assert product["email"]
        assert product["amount"]
        assert product["productId"]

def test_initiate_subscription_transaction():
    transaction_data = {
        "email": "string",
        "amount": 0,
        "plan": "string",
        "frequency": "string"
        }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/transactions/initiate/subscription", headers=headers,
        json=transaction_data)
    assert response.status_code == 201
    data = response.json()
    for subscription in data:
        assert subscription["email"]
        assert subscription["amount"]
        assert subscription["plan"]
        assert subscription["frequency"]

def test_transaction_callback():
    transaction_data = {
        "string": "string",
        }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/transactions/callback", headers=headers,
        json=transaction_data)
    assert response.status_code == 201
    data = response.json()

def test_verify_transaction_reference():
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/transactions/verify/reference1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    for verify in data:
        assert verify["email"]
        assert verify["amount"]
        assert verify["plan"]
        assert verify["frequency"]

def test_get_users():
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    assert response.status_code == 200
    data = response.json()
    for user in data:
        assert user["name"]
        assert user["id"]
        assert user["email"]
        assert user["profile"]

def test_get_single_user():
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{BASE_URL}/users/b9747cdd-4da1-4eca-b289-91a6de53de42", headers=headers)
    assert response.status_code == 200
    data = response.json()
    for user in data:
        assert user["name"]
        assert user["id"]
        assert user["email"]
        assert user["profile"]

# Run tests
if __name__ == "__main__":
    pytest.main()