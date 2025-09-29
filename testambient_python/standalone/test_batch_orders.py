#!/usr/bin/env python3
"""
Test Ambient Finance Batch Order Operations:
1. Place multiple limit orders using batchOrder
2. Cancel all orders using cancel with multiple order IDs
3. Test cancelByCloid with multiple CLOIDs
"""

import json
import time
import subprocess
import tempfile
import os
import requests
from datetime import datetime
from typing import List, Dict, Any

# API Configuration
AMBIENT_URL = "https://embindexer.net/ember/api/dev/v1"
SDK_PATH = "../ambient-ember-sdk"
DEVKEY_PATH = "../devkey.json"

class AmbientBatchTester:
    """Test batch operations on Ambient Finance"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.operations_log = []
        
    def _sign_payload_with_sdk(self, payload: Dict[str, Any]) -> Dict[str, Any]:
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

    def _make_signed_request(self, payload: Dict[str, Any], operation_name: str) -> Dict[str, Any]:
        """Sign and send request, logging for documentation"""
        print(f"\n🔄 {operation_name}")
        print("=" * 70)
        
        # Sign payload
        signed_payload = self._sign_payload_with_sdk(payload)
        print(f"📝 Request Payload:")
        print(json.dumps(payload, indent=2))
        print(f"\n📝 Signed Payload:")
        print(json.dumps(signed_payload, indent=2))
        
        # Send request
        try:
            response = self.session.post(f"{AMBIENT_URL}/exchange", json=signed_payload)
            response_data = response.json()
            
            print(f"\n📡 Response ({response.status_code}):")
            print(json.dumps(response_data, indent=2))
            
            # Log the operation
            log_entry = {
                "operation": operation_name,
                "timestamp": datetime.now().isoformat(),
                "request_payload": payload,
                "signed_payload": signed_payload,
                "response_status": response.status_code,
                "response_data": response_data
            }
            self.operations_log.append(log_entry)
            
            return response_data
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Request failed: {error_msg}")
            log_entry = {
                "operation": operation_name,
                "timestamp": datetime.now().isoformat(),
                "request_payload": payload,
                "signed_payload": signed_payload,
                "error": error_msg
            }
            self.operations_log.append(log_entry)
            raise

    def test_batch_operations(self):
        """Test all batch order operations"""
        
        print("🧪 AMBIENT FINANCE BATCH ORDER OPERATIONS TEST")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Test User: 5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK")
        
        placed_order_ids = []
        placed_cloids = []
        
        # Test 1: Place Multiple Orders with batchOrder
        try:
            base_cloid = int(time.time())
            cloid1 = str(base_cloid + 1)
            cloid2 = str(base_cloid + 2) 
            cloid3 = str(base_cloid + 3)
            
            placed_cloids = [cloid1, cloid2, cloid3]
            
            batch_order_payload = {
                "action": {
                    "type": "batchOrder",
                    "orders": [
                        {
                            "a": 0,  # BTC asset index
                            "b": True,  # Buy
                            "p": "109000.0",  # Price
                            "s": "0.00005000",  # Size  
                            "r": False,  # Not reduce only
                            "t": {
                                "limit": {
                                    "tif": "Gtc"
                                }
                            },
                            "c": cloid1  # Custom client order ID
                        },
                        {
                            "a": 0,
                            "b": True, 
                            "p": "108500.0",
                            "s": "0.00006000",
                            "r": False,
                            "t": {
                                "limit": {
                                    "tif": "Gtc" 
                                }
                            },
                            "c": cloid2
                        },
                        {
                            "a": 0,
                            "b": False,  # Sell
                            "p": "116000.0", 
                            "s": "0.00004000",
                            "r": False,
                            "t": {
                                "limit": {
                                    "tif": "Gtc"
                                }
                            },
                            "c": cloid3
                        }
                    ]
                }
            }
            
            batch_response = self._make_signed_request(batch_order_payload, "Batch Order - Place 3 Orders")
            
            # Extract order IDs if successful
            if batch_response.get("status") == "ok" and "response" in batch_response:
                if "data" in batch_response["response"]:
                    data = batch_response["response"]["data"]
                    # Handle different response formats
                    if isinstance(data, list):
                        for item in data:
                            if "oid" in item:
                                placed_order_ids.append(item["oid"])
                    elif "oid" in data:
                        placed_order_ids.append(data["oid"])
                        
                print(f"✅ Batch order placed. Order IDs: {placed_order_ids}")
                
        except Exception as e:
            print(f"❌ Batch order placement failed: {e}")
            
        # Wait for orders to be indexed
        if placed_order_ids or placed_cloids:
            print(f"\n⏱️ Waiting 3 seconds for orders to be indexed...")
            time.sleep(3)
        
        # Test 2: Cancel Multiple Orders by Order ID
        if placed_order_ids:
            try:
                cancel_payload = {
                    "action": {
                        "type": "cancel",
                        "cancels": [
                            {
                                "a": 0,  # Asset index
                                "o": order_id  # Order ID
                            } for order_id in placed_order_ids
                        ]
                    }
                }
                
                self._make_signed_request(cancel_payload, f"Cancel Multiple Orders by ID ({len(placed_order_ids)} orders)")
                
            except Exception as e:
                print(f"❌ Cancel by order IDs failed: {e}")
        
        # Test 3: Place orders and cancel by CLOID
        try:
            # Place new orders with predictable CLOIDs
            base_cloid = int(time.time()) + 100
            new_cloid1 = str(base_cloid + 1)
            new_cloid2 = str(base_cloid + 2)
            
            cloid_batch_payload = {
                "action": {
                    "type": "batchOrder", 
                    "orders": [
                        {
                            "a": 0,
                            "b": True,
                            "p": "107000.0",
                            "s": "0.00003000",
                            "r": False,
                            "t": {
                                "limit": {
                                    "tif": "Gtc"
                                }
                            },
                            "c": new_cloid1
                        },
                        {
                            "a": 0,
                            "b": False,
                            "p": "118000.0", 
                            "s": "0.00003000",
                            "r": False,
                            "t": {
                                "limit": {
                                    "tif": "Gtc"
                                }
                            },
                            "c": new_cloid2
                        }
                    ]
                }
            }
            
            self._make_signed_request(cloid_batch_payload, "Batch Order for CLOID Cancel Test")
            
            # Wait and then cancel by CLOID
            time.sleep(2)
            
            cancel_cloid_payload = {
                "action": {
                    "type": "cancelByCloid",
                    "cancels": [
                        {
                            "asset": 0,
                            "cloid": new_cloid1
                        },
                        {
                            "asset": 0,
                            "cloid": new_cloid2
                        }
                    ]
                }
            }
            
            self._make_signed_request(cancel_cloid_payload, "Cancel Multiple Orders by CLOID")
            
        except Exception as e:
            print(f"❌ CLOID batch operations failed: {e}")
        
        print(f"\n🎉 Batch operations test completed!")
        print(f"📊 Total operations logged: {len(self.operations_log)}")
        
        return self.operations_log

def generate_batch_documentation(operations_log):
    """Generate markdown documentation for batch operations"""
    
    doc = f"""# Ambient Finance Batch Order Operations - Response Documentation

This document contains actual API responses from Ambient Finance batch order operations.

**Base URL:** `https://embindexer.net/ember/api/dev/v1/exchange`  
**Method:** POST  
**Content-Type:** application/json

**Test User Address:** `5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK`  
**Test Asset:** BTC (Universe Index: 0)

---

"""
    
    for i, operation in enumerate(operations_log, 1):
        doc += f"## {i}. {operation['operation']}\n\n"
        doc += f"**Timestamp:** {operation['timestamp']}\n\n"
        
        if 'error' in operation:
            doc += f"**Status:** Failed with error: {operation['error']}\n\n"
            doc += f"**Request Payload:**\n```json\n{json.dumps(operation['request_payload'], indent=2)}\n```\n\n"
        else:
            doc += f"**HTTP Status:** {operation['response_status']}\n\n"
            doc += f"**Request Payload:**\n```json\n{json.dumps(operation['request_payload'], indent=2)}\n```\n\n"
            
            doc += f"**Signed Payload:**\n```json\n{json.dumps(operation['signed_payload'], indent=2)}\n```\n\n"
            
            doc += f"**Response:**\n```json\n{json.dumps(operation['response_data'], indent=2)}\n```\n\n"
        
        doc += "---\n\n"
    
    doc += f"""
## Batch Operations Summary

### Supported Batch Actions

1. **`batchOrder`** - Place multiple limit orders in single transaction
2. **`cancel`** - Cancel multiple orders by Order ID  
3. **`cancelByCloid`** - Cancel multiple orders by Client Order ID

### Request Schema

#### Batch Order Placement
```json
{{
  "action": {{
    "type": "batchOrder",
    "orders": [
      {{
        "a": 0,
        "b": true,
        "p": "109000.0", 
        "s": "0.00005000",
        "r": false,
        "t": {{"limit": {{"tif": "Gtc"}}}},
        "c": "optional_cloid"
      }}
    ]
  }}
}}
```

#### Multiple Cancel by Order ID
```json
{{
  "action": {{
    "type": "cancel",
    "cancels": [
      {{"a": 0, "o": order_id_1}},
      {{"a": 0, "o": order_id_2}}
    ]
  }}
}}
```

#### Multiple Cancel by Client Order ID  
```json
{{
  "action": {{
    "type": "cancelByCloid",
    "cancels": [
      {{"asset": 0, "cloid": "client_id_1"}},
      {{"asset": 0, "cloid": "client_id_2"}}
    ]
  }}
}}
```

---

**Generated on:** {datetime.now().isoformat()}  
**Total Operations:** {len(operations_log)}
"""
    
    return doc

if __name__ == "__main__":
    # Run comprehensive batch test
    tester = AmbientBatchTester()
    operations_log = tester.test_batch_operations()
    
    # Generate documentation
    print("\n📝 Generating batch operations documentation...")
    documentation = generate_batch_documentation(operations_log)
    
    # Save to file
    filename = "../docs/AMBIENT_BATCH_ORDERS_RESPONSES.md"
    with open(filename, "w") as f:
        f.write(documentation)
    
    print(f"✅ Documentation saved to: {filename}")
    print(f"📄 File size: {len(documentation)} characters")