#!/usr/bin/env python3
"""
Sample client for testing the LLM Query-Retrieval System with Gemini
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"  # Change to your deployed URL
BEARER_TOKEN = "c0df38f44acb385ecd42f8e0c02ee14acd6d145835643ee57acd84f79afeb798"

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_status():
    """Test status endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"\nAPI Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Status check failed: {e}")
        return False

def test_hackrx_endpoint():
    """Test the main /hackrx/run endpoint"""

    # Sample payload with the exact format required
    payload = {
        "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
        "questions": [
            "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
            "What is the waiting period for pre-existing diseases (PED) to be covered?",
            "Does this policy cover maternity expenses, and what are the conditions?",
            "What is the waiting period for cataract surgery?",
            "Are the medical expenses for an organ donor covered under this policy?"
        ]
    }

    try:
        print(f"\nTesting /hackrx/run endpoint...")
        print(f"Document: {payload['documents'][:80]}...")
        print(f"Questions: {len(payload['questions'])} questions")

        response = requests.post(f"{BASE_URL}/hackrx/run", 
                               headers=HEADERS, 
                               json=payload,
                               timeout=300)

        print(f"\nResponse Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("\n" + "="*60)
            print("ANSWERS FROM GEMINI:")
            print("="*60)

            for i, (question, answer) in enumerate(zip(payload["questions"], result.get("answers", [])), 1):
                print(f"\nQ{i}: {question}")
                print(f"A{i}: {answer}")
                print("-" * 40)

        else:
            print(f"Error: {response.text}")

        return response.status_code == 200

    except requests.exceptions.Timeout:
        print("Request timed out - this is normal for document processing")
        return False
    except Exception as e:
        print(f"Test failed: {e}")
        return False

def main():
    """Main test function"""
    print("="*60)
    print("LLM Query-Retrieval System with Gemini - Test Client")
    print("="*60)

    # Test basic endpoints
    if not test_health():
        print("Health check failed - is the server running?")
        sys.exit(1)

    if not test_status():
        print("Status check failed - check authentication")
        sys.exit(1)

    # Test main functionality
    print("\n" + "="*60)
    print("Testing Document Processing with Gemini")
    print("="*60)

    success = test_hackrx_endpoint()

    print("\n" + "="*60)
    print("Testing Complete")
    print("="*60)

    if success:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed - check the logs")

if __name__ == "__main__":
    main()
