import requests
import json

BASE_URL = 'http://127.0.0.1:5000'


def test_login():
    print("\n=== Testing Login ===")
    
    # Login as admin
    response = requests.post(f"{BASE_URL}/api/login", json={
        "email": "admin@example.com",
        "password": "Admin123"
    })
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        token = response.json()['token']
        print(f"Token obtained: {token[:50]}...")
        return token
    
    return None


def test_protected_endpoint(token):
    """Test accessing protected endpoint"""
    print("\n=== Testing Protected Endpoint ===")
    
    # Try without token
    print("\n1. Without token (should fail):")
    response = requests.get(f"{BASE_URL}/api/customers")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Try with token
    print("\n2. With valid token (should succeed):")
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{BASE_URL}/api/customers", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Customers: {len(response.json()) if response.status_code == 200 else 0}")

def main():
    # Step 1: Login
    token = test_login()
    
    if token:
        # Step 2: Test protected endpoint
        test_protected_endpoint(token)


if __name__ == "__main__":
    main()