#!/usr/bin/env python3
"""
Live test: Sign and submit an actual order to Ambient Finance exchange
This demonstrates the complete workflow from signing to API submission
"""

import json
import time
import requests
from typing import Dict, Any

def read_devkey():
    """Read the private key from devkey.json"""
    with open('devkey.json', 'r') as f:
        key_data = json.load(f)
    return ''.join(f'{b:02x}' for b in key_data)

def create_order_request(signed_permit, signer_pubkey, request_nonce, order_params):
    """Create the API request payload according to Ambient Finance format from TypeScript example"""
    return {
        "action": {
            "type": "order",
            "a": order_params["market_id"],  # asset (market ID - universe index)
            "b": order_params["side"] == 0,  # isBuy (True for buy, False for sell)
            "p": str(order_params["price"]),  # price as string
            "s": str(order_params["qty"]),   # size as string
            "r": order_params.get("reduce_only", False),  # reduceOnly
            "t": {
                "limit": {
                    "tif": order_params.get("tif", "Gtc")  # time in force
                }
            },
            "c": str(order_params["client_id"])  # cloid (client order id) as string
        },
        "nonce": request_nonce,
        "signature": signed_permit.signature_hex,
        "pubkey": signer_pubkey,
        "permitBytes": signed_permit.bytes_hex
    }

def submit_to_exchange(request_data):
    """Submit the signed request to Ambient Finance exchange"""
    # Ambient Finance API endpoint (dev environment)
    url = "https://embindexer.net/ember/api/dev/v1/exchange"
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "python-rust-signer/1.0.0"
    }
    
    print(f"🌐 Submitting to: {url}")
    print(f"📝 Request payload size: {len(json.dumps(request_data))} bytes")
    
    try:
        response = requests.post(url, json=request_data, headers=headers, timeout=30)
        
        print(f"📡 Response Status: {response.status_code}")
        print(f"📡 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                return True, response_data
            except json.JSONDecodeError:
                return True, {"raw_response": response.text}
        else:
            return False, {
                "status_code": response.status_code,
                "response": response.text,
                "headers": dict(response.headers)
            }
            
    except requests.exceptions.RequestException as e:
        return False, {"error": str(e)}

def main():
    print("🚀 Live Order Placement Test")
    print("=" * 50)
    
    # Import the Rust signer
    from ambient_signer import ambient_signer
    
    # Load private key and create signer
    private_key_hex = read_devkey()
    signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)
    
    print(f"✅ Signer loaded")
    print(f"✅ Public key: {signer.public_key}")
    
    # Create order parameters
    current_time = int(time.time())
    nonce = int(time.time() * 1000)
    
    order_params = {
        "program_id": "6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
        "cluster": "testnet",
        "authorizer": signer.public_key,  # Use the signer's public key as authorizer
        "market_id": 0,  # Using 0 as universe index like TypeScript example
        "client_id": nonce,
        "side": 0,  # Buy
        "qty": 1000,  # Small quantity for testing
        "expires_unix": current_time + 3600,  # 1 hour expiry
        "max_fee_quote": 100000,  # Max fee in quote currency
        "nonce": nonce,
        "price": 50000000000,  # $50 price (in quote currency units)
        "tif": "Gtc",  # Fixed case sensitivity
        "reduce_only": False,
        "trigger_price": None,
        "trigger_type": 0,
        "relayer": None
    }
    
    print(f"\n📋 Order Parameters:")
    for key, value in order_params.items():
        print(f"  {key}: {value}")
    
    # Sign the order
    print(f"\n🔐 Signing order...")
    signed_permit = signer.sign_place_order(**order_params)
    
    print(f"✅ Order signed successfully!")
    print(f"✅ Signature: {signed_permit.signature_hex[:32]}...{signed_permit.signature_hex[-32:]}")
    print(f"✅ Envelope: {signed_permit.bytes_hex[:32]}...{signed_permit.bytes_hex[-32:]}")
    
    # Create API request using correct Ambient Finance format
    api_request = create_order_request(
        signed_permit,
        signer.public_key,  # signer pubkey
        nonce,  # nonce
        order_params  # all order parameters
    )
    
    print(f"\n📨 API Request Preview:")
    print(json.dumps(api_request, indent=2)[:500] + "...")
    
    # Submit to exchange
    print(f"\n🌐 Submitting to Ambient Finance exchange...")
    success, response = submit_to_exchange(api_request)
    
    print(f"\n📥 Exchange Response:")
    print("=" * 30)
    
    if success:
        print(f"✅ Request submitted successfully!")
        print(f"📝 Response: {json.dumps(response, indent=2)}")
        
        # Check if order was accepted
        if isinstance(response, dict):
            if "error" in response:
                print(f"⚠️  Order rejected: {response['error']}")
            elif "result" in response or "data" in response:
                print(f"🎉 Order potentially accepted!")
            else:
                print(f"ℹ️  Unexpected response format")
    else:
        print(f"❌ Request failed!")
        print(f"📝 Error details: {json.dumps(response, indent=2)}")
    
    print(f"\n📊 Test Summary:")
    print(f"  Signing: ✅ Success")
    print(f"  API Call: {'✅ Success' if success else '❌ Failed'}")
    print(f"  Signature Length: {len(signed_permit.signature)} bytes")
    print(f"  Envelope Length: {len(signed_permit.bytes)} bytes")
    
    return success, response, signed_permit

if __name__ == "__main__":
    try:
        success, response, signed_permit = main()
        print(f"\n🏁 Test completed - {'Success' if success else 'Failed'}")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()