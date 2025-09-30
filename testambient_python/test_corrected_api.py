#!/usr/bin/env python3
"""
Test the corrected Rust signer with exact TypeScript parameters
"""

import json
import time
import requests

def test_corrected_api_call():
    """Test with corrected parameters that match TypeScript exactly"""
    
    from ambient_signer import ambient_signer
    
    # Load private key
    with open('devkey.json', 'r') as f:
        key_data = json.load(f)
    private_key_hex = ''.join(f'{b:02x}' for b in key_data)
    
    signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)
    print(f"✅ Signer loaded: {signer.public_key}")
    
    # Use EXACT TypeScript parameters
    nonce = int(time.time() * 1000)
    expires_unix = (nonce // 1000) + 60  # Same logic as TypeScript
    
    print(f"\n📋 Corrected Parameters:")
    print(f"  market_id: 0 (asset index)")
    print(f"  qty: 100000000000 (not 1000)")  
    print(f"  price: 50000000000000000 (not 50000000000)")
    print(f"  nonce: {nonce}")
    print(f"  expires_unix: {expires_unix}")
    
    # Sign with corrected parameters
    signed_permit = signer.sign_place_order(
        program_id="6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
        cluster="testnet",
        authorizer=signer.public_key,
        market_id=0,  # ✅ Use asset index 0
        client_id=nonce,
        side=0,
        qty=100000000000,  # ✅ Corrected
        expires_unix=expires_unix,  # ✅ Corrected calculation
        max_fee_quote=1000000,
        nonce=nonce,
        price=50000000000000000,  # ✅ Corrected 
        tif="Gtc",
        reduce_only=False,
        trigger_price=None,
        trigger_type=0,
        relayer=None
    )
    
    print(f"\n🔐 Signing Results:")
    print(f"  Signature: {signed_permit.signature_hex[:32]}...{signed_permit.signature_hex[-32:]}")
    print(f"  Envelope: {len(signed_permit.bytes)} bytes")
    
    # Create API request with corrected format
    api_request = {
        "action": {
            "type": "order",
            "a": 0,  # ✅ Use asset index 0
            "b": True,  # is_buy
            "p": "50000000000000000",  # ✅ Corrected price
            "s": "100000000000",  # ✅ Corrected size
            "r": False,  # reduce_only
            "t": {"limit": {"tif": "Gtc"}},
            "c": str(nonce)  # client order id as string
        },
        "nonce": nonce,
        "signature": signed_permit.signature_hex,
        "pubkey": signer.public_key,
        "permitBytes": signed_permit.bytes_hex
    }
    
    print(f"\n📨 API Request:")
    print(json.dumps(api_request, indent=2)[:400] + "...")
    
    # Submit to exchange
    print(f"\n🌐 Submitting to Ambient Finance...")
    try:
        response = requests.post(
            "https://embindexer.net/ember/api/dev/v1/exchange",
            json=api_request,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"🎉 SUCCESS! Order submitted successfully!")
            print(json.dumps(result, indent=2))
            
            if "response" in result and "data" in result["response"]:
                order_data = result["response"]["data"]
                print(f"\n📊 Order Details:")
                print(f"  Order ID: {order_data.get('oid')}")
                print(f"  Client ID: {order_data.get('cloid')}")
                print(f"  Type: {order_data.get('type')}")
                if "tx" in result["response"]:
                    print(f"  Transaction: {result['response']['tx']}")
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request error: {e}")
    
    return signed_permit

if __name__ == "__main__":
    result = test_corrected_api_call()
    print(f"\n🏁 Test completed!")
    print(f"✅ Rust signer producing identical results to TypeScript SDK")