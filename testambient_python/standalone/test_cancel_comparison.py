#!/usr/bin/env python3
"""
Test comparison between single cancel vs batch cancel response schemas
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
    print(f"📝 Request Payload:")
    print(json.dumps(payload, indent=2))
    
    # Send request
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    
    response = session.post(f"{AMBIENT_URL}/exchange", json=signed_payload)
    response_data = response.json()
    
    print(f"\n📡 Response ({response.status_code}):")
    print(json.dumps(response_data, indent=2))
    
    return response_data

def test_cancel_comparison():
    """Compare single vs batch cancel response schemas"""
    
    print("🔍 TESTING SINGLE VS BATCH CANCEL RESPONSE SCHEMAS")
    print("=" * 70)
    
    # Step 1: Place orders for testing
    base_time = int(time.time())
    cloid1 = str(base_time + 1)
    cloid2 = str(base_time + 2)
    cloid3 = str(base_time + 3)
    
    print("📋 Step 1: Place 3 orders for cancel testing")
    batch_order_payload = {
        "action": {
            "type": "batchOrder",
            "orders": [
                {
                    "a": 0,
                    "b": True,
                    "p": "106000.0",
                    "s": "0.00004000",
                    "r": False,
                    "t": {"limit": {"tif": "Gtc"}},
                    "c": cloid1
                },
                {
                    "a": 0,
                    "b": True,
                    "p": "105500.0",
                    "s": "0.00005000",
                    "r": False,
                    "t": {"limit": {"tif": "Gtc"}},
                    "c": cloid2
                },
                {
                    "a": 0,
                    "b": False,
                    "p": "119000.0",
                    "s": "0.00003000",
                    "r": False,
                    "t": {"limit": {"tif": "Gtc"}},
                    "c": cloid3
                }
            ]
        }
    }
    
    batch_response = make_signed_request(batch_order_payload, "Place 3 Orders")
    
    # Extract order IDs
    order_ids = []
    if batch_response.get("status") == "ok" and "response" in batch_response:
        response_data = batch_response["response"]
        if isinstance(response_data, list):
            for item in response_data:
                if item.get("status") == "ok" and "data" in item:
                    order_ids.append(item["data"]["oid"])
    
    print(f"✅ Placed orders with IDs: {order_ids}")
    
    if len(order_ids) < 2:
        print("❌ Need at least 2 orders for comparison test")
        return
    
    time.sleep(3)  # Wait for orders to be indexed
    
    # Step 2: Test SINGLE cancel
    print(f"\n📋 Step 2: Single Cancel Test")
    single_cancel_payload = {
        "action": {
            "type": "cancel",
            "cancels": [
                {
                    "a": 0,
                    "o": order_ids[0]  # Cancel just ONE order
                }
            ]
        }
    }
    
    single_response = make_signed_request(single_cancel_payload, "SINGLE Cancel")
    
    time.sleep(2)
    
    # Step 3: Test BATCH cancel (multiple orders)
    print(f"\n📋 Step 3: Batch Cancel Test")
    if len(order_ids) >= 2:
        batch_cancel_payload = {
            "action": {
                "type": "cancel", 
                "cancels": [
                    {
                        "a": 0,
                        "o": order_ids[1]  # Cancel second order
                    },
                    {
                        "a": 0,
                        "o": order_ids[2] if len(order_ids) > 2 else order_ids[1]  # Cancel third order
                    }
                ]
            }
        }
        
        batch_response = make_signed_request(batch_cancel_payload, "BATCH Cancel (Multiple Orders)")
    
    # Step 4: Schema Comparison
    print(f"\n🔍 SCHEMA COMPARISON ANALYSIS")
    print("=" * 60)
    
    print("📊 SINGLE Cancel Response Structure:")
    if single_response.get("status") == "ok":
        single_data = single_response["response"]
        print(f"- Response type: {type(single_data)}")
        if isinstance(single_data, dict):
            print(f"- Has 'data' field: {'data' in single_data}")
            if 'data' in single_data:
                data_fields = list(single_data['data'].keys())
                print(f"- Data fields: {data_fields}")
        elif isinstance(single_data, list):
            print(f"- Array length: {len(single_data)}")
            if single_data:
                first_item_fields = list(single_data[0].keys()) if isinstance(single_data[0], dict) else []
                print(f"- First item fields: {first_item_fields}")
    
    print("\n📊 BATCH Cancel Response Structure:")
    if 'batch_response' in locals() and batch_response.get("status") == "ok":
        batch_data = batch_response["response"]
        print(f"- Response type: {type(batch_data)}")
        if isinstance(batch_data, dict):
            print(f"- Has 'data' field: {'data' in batch_data}")
            if 'data' in batch_data:
                data_fields = list(batch_data['data'].keys())
                print(f"- Data fields: {data_fields}")
        elif isinstance(batch_data, list):
            print(f"- Array length: {len(batch_data)}")
            if batch_data:
                first_item_fields = list(batch_data[0].keys()) if isinstance(batch_data[0], dict) else []
                print(f"- First item fields: {first_item_fields}")
    
    print(f"\n✅ Schema comparison completed!")
    
    return {
        "single_cancel": single_response,
        "batch_cancel": batch_response if 'batch_response' in locals() else None
    }

if __name__ == "__main__":
    results = test_cancel_comparison()
    
    # Save results for analysis
    with open("../test_json_payloads/cancel_comparison_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Results saved to: cancel_comparison_results.json")