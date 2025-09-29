#!/usr/bin/env python3
"""
Test modifyBatch (correct action type) operation
"""

import json
import time
import subprocess
import tempfile
import os
import requests

# API Configuration
AMBIENT_URL = "https://embindexer.net/ember/api/dev/v1"
SDK_PATH = "../ambient-ember-sdk"
DEVKEY_PATH = "../devkey.json"

def sign_payload_with_sdk(payload):
    """Sign a payload using the SDK"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_path = f.name

    try:
        result = subprocess.run([
            'node',
            f'{SDK_PATH}/scripts/signPayload.mjs',
            DEVKEY_PATH,
            temp_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"SDK signing failed: {result.stderr}")

        return json.loads(result.stdout)
    finally:
        os.unlink(temp_path)

def make_signed_request(payload, operation_name):
    """Sign and send request"""
    print(f"\n🔄 {operation_name}")
    print("=" * 60)
    
    # Sign payload
    signed_payload = sign_payload_with_sdk(payload)
    print(f"📝 Request Payload:")
    print(json.dumps(payload, indent=2))
    print(f"\n📝 Signed Payload:")
    print(json.dumps(signed_payload, indent=2))
    
    # Send request
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    
    response = session.post(f"{AMBIENT_URL}/exchange", json=signed_payload)
    
    print(f"\n📡 Response ({response.status_code}):")
    print(f"Raw response: {response.text}")
    
    try:
        response_data = response.json()
        print(f"Parsed response:")
        print(json.dumps(response_data, indent=2))
        return response_data
    except:
        print("Failed to parse JSON response")
        return {"error": "JSON parse failed", "raw": response.text}

def test_modify_batch_correct():
    """Test modifyBatch with correct action type"""
    
    print("🔧 TESTING CORRECT MODIFY BATCH ACTION TYPE")
    print("=" * 60)
    
    # Step 1: Place 2 orders
    base_time = int(time.time())
    cloid1 = str(base_time + 1)
    cloid2 = str(base_time + 2)
    
    place_payload = {
        "action": {
            "type": "batchOrder",
            "orders": [
                {
                    "a": 0,
                    "b": True,
                    "p": "105000.0",
                    "s": "0.00004000",
                    "r": False,
                    "t": {"limit": {"tif": "Gtc"}},
                    "c": cloid1
                },
                {
                    "a": 0,
                    "b": True,
                    "p": "104500.0",
                    "s": "0.00005000",
                    "r": False,
                    "t": {"limit": {"tif": "Gtc"}},
                    "c": cloid2
                }
            ]
        }
    }
    
    place_response = make_signed_request(place_payload, "Place Orders for modifyBatch Test")
    
    # Extract order IDs
    order_ids = []
    if place_response.get("status") == "ok" and "response" in place_response:
        response_data = place_response["response"]
        if isinstance(response_data, list):
            for item in response_data:
                if item.get("status") == "ok" and "data" in item:
                    order_ids.append(item["data"]["oid"])
    
    print(f"✅ Placed orders: {order_ids}")
    
    if len(order_ids) < 2:
        print("❌ Need at least 2 orders for modifyBatch test")
        return
    
    time.sleep(4)  # Wait for indexing
    
    # Step 2: Test modifyBatch (correct action type)
    modify_base = int(time.time()) + 400
    new_cloid1 = str(modify_base + 1)
    new_cloid2 = str(modify_base + 2)
    
    modify_batch_payload = {
        "action": {
            "type": "modifyBatch",  # ← Correct action type
            "modifies": [
                {
                    "oid": order_ids[0],
                    "order": {
                        "a": 0,
                        "b": True,
                        "p": "104000.0",
                        "s": "0.00007000",
                        "r": False,
                        "t": {"limit": {"tif": "Gtc"}},
                        "c": new_cloid1
                    }
                },
                {
                    "oid": order_ids[1],
                    "order": {
                        "a": 0,
                        "b": True,
                        "p": "103500.0",
                        "s": "0.00008000",
                        "r": False,
                        "t": {"limit": {"tif": "Gtc"}},
                        "c": new_cloid2
                    }
                }
            ]
        }
    }
    
    modify_response = make_signed_request(modify_batch_payload, "modifyBatch Test (Correct Action Type)")
    
    # Step 3: Cleanup
    print(f"\n🧹 Cleanup")
    try:
        cleanup_payload = {
            "action": {
                "type": "cancel",
                "cancels": [{"a": 0, "o": oid} for oid in order_ids]
            }
        }
        make_signed_request(cleanup_payload, "Cleanup Orders")
    except Exception as e:
        print(f"⚠️ Cleanup failed: {e}")

if __name__ == "__main__":
    test_modify_batch_correct()