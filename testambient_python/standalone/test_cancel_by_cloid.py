#!/usr/bin/env python3
"""
Test cancel by client order ID operation
"""

import json
import time
import subprocess
import tempfile
import os
import requests
from datetime import datetime

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
    print(f"📝 Signed Payload:")
    print(json.dumps(signed_payload, indent=2))
    
    # Send request
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    
    response = session.post(f"{AMBIENT_URL}/exchange", json=signed_payload)
    response_data = response.json()
    
    print(f"\n📡 Response ({response.status_code}):")
    print(json.dumps(response_data, indent=2))
    
    return response_data

def test_cancel_by_cloid():
    """Test cancel by client order ID"""
    
    print("🧪 TESTING CANCEL BY CLIENT ORDER ID")
    print("=" * 60)
    
    # Use a simple numeric CLOID that won't overflow
    custom_cloid = str(int(time.time()))  # Simple timestamp
    print(f"Using CLOID: {custom_cloid}")
    
    # Test 1: Place order with numeric CLOID
    try:
        order_payload = {
            "action": {
                "type": "order",
                "a": 0,
                "b": False,  # Sell order
                "p": "115000.0",
                "s": "0.00005000",
                "r": False,
                "t": {
                    "limit": {
                        "tif": "Gtc"
                    }
                },
                "c": custom_cloid
            }
        }
        order_response = make_signed_request(order_payload, "Place Order with Numeric CLOID")
        
        if order_response.get("status") == "ok":
            print(f"✅ Order placed successfully with CLOID: {custom_cloid}")
            
            # Test 2: Cancel by Client Order ID
            time.sleep(2)
            try:
                cancel_cloid_payload = {
                    "action": {
                        "type": "cancelByCloid",
                        "cancels": [
                            {
                                "asset": 0,
                                "cloid": custom_cloid
                            }
                        ]
                    }
                }
                cancel_response = make_signed_request(cancel_cloid_payload, "Cancel Order by Client Order ID")
                
                if cancel_response.get("status") == "ok":
                    print("✅ Cancel by CLOID successful!")
                else:
                    print("⚠️ Cancel by CLOID may have failed")
                    
            except Exception as e:
                print(f"❌ Cancel by CLOID failed: {e}")
        else:
            print("⚠️ Order placement failed")
            
    except Exception as e:
        print(f"❌ Order placement failed: {e}")

if __name__ == "__main__":
    test_cancel_by_cloid()