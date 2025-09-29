#!/usr/bin/env python3
"""
Comprehensive test of all Ambient Finance exchange operations
for documentation purposes.
"""

import json
import time
import subprocess
import tempfile
import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime

# API Configuration
AMBIENT_URL = "https://embindexer.net/ember/api/dev/v1"
SDK_PATH = "../ambient-ember-sdk"
DEVKEY_PATH = "../devkey.json"

class AmbientExchangeTester:
    """Test all exchange operations and document responses"""
    
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
        print("=" * 60)
        
        # Sign payload
        signed_payload = self._sign_payload_with_sdk(payload)
        print(f"📝 Signed Payload:")
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

    def _query_order_status(self, oid, operation_name: str) -> Dict[str, Any]:
        """Query order status via info endpoint"""
        print(f"\n🔍 {operation_name}")
        print("=" * 60)
        
        payload = {
            "type": "orderStatus",
            "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
            "orderId": oid
        }
        
        print(f"📝 Request Payload:")
        print(json.dumps(payload, indent=2))
        
        try:
            response = self.session.post(f"{AMBIENT_URL}/info", json=payload)
            response_data = response.json()
            
            print(f"\n📡 Response ({response.status_code}):")
            print(json.dumps(response_data, indent=2))
            
            # Log the operation
            log_entry = {
                "operation": operation_name,
                "timestamp": datetime.now().isoformat(),
                "request_payload": payload,
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
                "error": error_msg
            }
            self.operations_log.append(log_entry)
            raise

    def test_all_operations(self):
        """Run comprehensive test of all exchange operations"""
        
        print("🧪 AMBIENT EXCHANGE OPERATIONS TEST SUITE")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"Test User: 5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK")
        print()
        
        # Test 1: Update Leverage
        try:
            leverage_payload = {
                "action": {
                    "type": "updateLeverage",
                    "asset": 0,
                    "leverage": 20,
                    "isCross": True
                }
            }
            leverage_response = self._make_signed_request(leverage_payload, "Update Leverage (20x)")
            
        except Exception as e:
            print(f"⚠️ Update leverage failed: {e}")
        
        # Test 2: Place Order
        try:
            order_payload = {
                "action": {
                    "type": "order",
                    "a": 0,
                    "b": True,
                    "p": "110000.0",
                    "s": "0.00008000",
                    "r": False,
                    "t": {
                        "limit": {
                            "tif": "Gtc"
                        }
                    }
                }
            }
            order_response = self._make_signed_request(order_payload, "Place Limit Order")
            
            # Extract order details if successful
            order_id = None
            client_order_id = None
            if order_response.get("status") == "ok" and "response" in order_response:
                if "data" in order_response["response"]:
                    order_id = order_response["response"]["data"].get("oid")
                    client_order_id = order_response["response"]["data"].get("cloid")
                    print(f"✅ Order placed: OID={order_id}, CLOID={client_order_id}")
            
            # Test 3: Check Order Status
            if order_id:
                time.sleep(2)  # Wait for order to be indexed
                try:
                    self._query_order_status(order_id, "Check Order Status")
                except Exception as e:
                    print(f"⚠️ Order status check failed: {e}")
                
                # Test 4: Modify Order
                try:
                    modify_payload = {
                        "action": {
                            "type": "modify",
                            "oid": order_id,
                            "order": {
                                "a": 0,
                                "b": True,
                                "p": "109500.0",
                                "s": "0.00010000",
                                "r": False,
                                "t": {
                                    "limit": {
                                        "tif": "Gtc"
                                    }
                                }
                            }
                        }
                    }
                    modify_response = self._make_signed_request(modify_payload, "Modify Order")
                    
                    # Get new order ID after modification
                    new_order_id = order_id
                    if modify_response.get("status") == "ok" and "response" in modify_response:
                        if "data" in modify_response["response"]:
                            new_order_id = modify_response["response"]["data"].get("oid", order_id)
                    
                    # Test 5: Cancel Order by ID
                    time.sleep(2)
                    try:
                        cancel_payload = {
                            "action": {
                                "type": "cancel",
                                "cancels": [
                                    {
                                        "a": 0,
                                        "o": new_order_id
                                    }
                                ]
                            }
                        }
                        self._make_signed_request(cancel_payload, "Cancel Order by ID")
                        
                    except Exception as e:
                        print(f"⚠️ Cancel order failed: {e}")
                        
                except Exception as e:
                    print(f"⚠️ Modify order failed: {e}")
                    
                    # If modify failed, still try to cancel original order
                    time.sleep(1)
                    try:
                        cancel_payload = {
                            "action": {
                                "type": "cancel",
                                "cancels": [
                                    {
                                        "a": 0,
                                        "o": order_id
                                    }
                                ]
                            }
                        }
                        self._make_signed_request(cancel_payload, "Cancel Original Order")
                    except Exception as cancel_error:
                        print(f"⚠️ Cancel original order failed: {cancel_error}")
                        
        except Exception as e:
            print(f"⚠️ Place order failed: {e}")
        
        # Test 6: Place order with custom client ID for cancelByCloid test
        try:
            custom_cloid = f"test_cloid_{int(time.time() * 1000)}"
            cloid_order_payload = {
                "action": {
                    "type": "order",
                    "a": 0,
                    "b": False,
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
            cloid_response = self._make_signed_request(cloid_order_payload, "Place Order with Custom CLOID")
            
            # Test 7: Cancel by Client Order ID
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
                self._make_signed_request(cancel_cloid_payload, "Cancel Order by Client Order ID")
                
            except Exception as e:
                print(f"⚠️ Cancel by CLOID failed: {e}")
                
        except Exception as e:
            print(f"⚠️ Place order with CLOID failed: {e}")
        
        print("\n🎉 Test suite completed!")
        print(f"📊 Total operations logged: {len(self.operations_log)}")
        
        return self.operations_log

def generate_documentation(operations_log):
    """Generate markdown documentation from test results"""
    
    doc = """# Ambient Finance Exchange Operations - Complete Response Documentation

This document contains actual API responses from all Ambient Finance exchange operations for testing and integration purposes.

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
            if 'signed_payload' in operation:
                doc += f"**Signed Payload:**\n```json\n{json.dumps(operation['signed_payload'], indent=2)}\n```\n\n"
        else:
            doc += f"**HTTP Status:** {operation['response_status']}\n\n"
            doc += f"**Request Payload:**\n```json\n{json.dumps(operation['request_payload'], indent=2)}\n```\n\n"
            
            if 'signed_payload' in operation:
                doc += f"**Signed Payload:**\n```json\n{json.dumps(operation['signed_payload'], indent=2)}\n```\n\n"
            
            doc += f"**Response:**\n```json\n{json.dumps(operation['response_data'], indent=2)}\n```\n\n"
        
        doc += "---\n\n"
    
    doc += """
## Response Schema Summary

### Successful Exchange Response
```json
{
  "status": "ok",
  "response": {
    "status": "ok",
    "data": {
      "type": "limit",
      "oid": 1234567890,
      "cloid": "custom_client_id",
      "filled": {
        "totalSz": "0",
        "avgPx": "0"
      }
    },
    "tx": "solana_transaction_hash"
  }
}
```

### Order Status Response
```json
{
  "status": "open",
  "order": {
    "asset": 0,
    "side": "B",
    "limitPx": "110000.0",
    "sz": "0.00008000",
    "filledSz": "0",
    "cloid": "1234567890",
    "oid": 1234567890,
    "timestamp": 1234567890
  }
}
```

## Usage Examples

### Python with SDK Signing
```python
import subprocess
import json
import tempfile
import os

def sign_and_send_order(action):
    # Sign with SDK
    payload = {"action": action}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_path = f.name
    
    try:
        result = subprocess.run([
            'node', 'ambient-ember-sdk/scripts/signPayload.mjs',
            'devkey.json', temp_path
        ], capture_output=True, text=True)
        
        signed_payload = json.loads(result.stdout)
    finally:
        os.unlink(temp_path)
    
    # Send to exchange
    response = requests.post(
        'https://embindexer.net/ember/api/dev/v1/exchange',
        json=signed_payload,
        headers={'Content-Type': 'application/json'}
    )
    return response.json()

# Place order
order_action = {
    "type": "order",
    "a": 0,
    "b": True,
    "p": "110000.0",
    "s": "0.00008000",
    "r": False,
    "t": {"limit": {"tif": "Gtc"}}
}
result = sign_and_send_order(order_action)
```

---

**Generated on:** """ + datetime.now().isoformat() + """
**Total Operations Tested:** """ + str(len(operations_log)) + """
"""
    
    return doc

if __name__ == "__main__":
    # Run comprehensive test
    tester = AmbientExchangeTester()
    operations_log = tester.test_all_operations()
    
    # Generate documentation
    print("\n📝 Generating documentation...")
    documentation = generate_documentation(operations_log)
    
    # Save to file
    filename = "../docs/AMBIENT_EXCHANGE_OPERATIONS_RESPONSES.md"
    with open(filename, "w") as f:
        f.write(documentation)
    
    print(f"✅ Documentation saved to: {filename}")
    print(f"📄 File size: {len(documentation)} characters")