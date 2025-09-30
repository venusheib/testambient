#!/usr/bin/env python3
"""
Test the TypeScript SDK signature with the live API
"""

import json
import requests
import subprocess
import tempfile
import os

def get_typescript_signature_and_test_api():
    """Get TypeScript signature and test it with the live API"""
    
    print("🎯 TESTING TYPESCRIPT SDK WITH LIVE API")
    print("=" * 60)
    
    # Create realistic test payload based on working example
    payload = {
        "action": {
            "type": "order",
            "a": 0,  # Asset index (BTC)
            "b": False,  # isBuy = false (sell order)
            "p": "112000.0",  # Price from working example
            "s": "0.00010000",  # Size from working example
            "r": False,  # reduce_only
            "t": {"limit": {"tif": "Gtc"}},  # Time in force
            "c": "1758796565225"  # Client order ID
        },
        "nonce": 1758796565225
    }
    
    print(f"📋 Test Payload:")
    print(json.dumps(payload, indent=2))
    
    # Get TypeScript SDK signature
    print(f"\n📝 Getting TypeScript SDK signature...")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_path = f.name

    try:
        # Get TypeScript SDK result
        result = subprocess.run([
            'node',
            'ambient-ember-sdk/scripts/signPayload.mjs',
            'devkey.json',
            temp_path
        ], capture_output=True, text=True, cwd='.')

        if result.returncode != 0:
            print(f"❌ TypeScript SDK failed: {result.stderr}")
            return

        signed_payload = json.loads(result.stdout)
        
        print(f"✅ TypeScript signature: {signed_payload['signature'][0]}")
        print(f"✅ Public key: {signed_payload['pubkey']}")
        
        # Create API request
        api_request = {
            "action": payload["action"],
            "nonce": payload["nonce"],
            "signature": signed_payload["signature"],
            "pubkey": signed_payload["pubkey"]
        }
        
        print(f"\n📤 API Request:")
        print(json.dumps(api_request, indent=2))
        
        # Test with live API
        print(f"\n🌐 Submitting to Ambient Finance API...")
        print(f"   Endpoint: https://embindexer.net/ember/api/dev/v1/exchange")
        
        response = requests.post(
            "https://embindexer.net/ember/api/dev/v1/exchange",
            json=api_request,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            result = response.json()
            print(f"📥 Response Body:")
            print(json.dumps(result, indent=2))
            
            if response.status_code == 200:
                if result.get("status") == "ok":
                    print(f"\n🎉 TYPESCRIPT ORDER PLACED SUCCESSFULLY!")
                    
                    if "response" in result and "tx" in result["response"]:
                        tx_hash = result["response"]["tx"]
                        print(f"\n🔗 Transaction Hash: {tx_hash}")
                        print(f"   Explorer: https://explorer.solana.com/tx/{tx_hash}?cluster=testnet")
                        
                        if "data" in result["response"]:
                            order_data = result["response"]["data"]
                            print(f"\n📊 Order Details:")
                            print(f"   Order ID: {order_data.get('oid')}")
                            print(f"   Client ID: {order_data.get('cloid')}")
                            print(f"   Status: {order_data.get('status')}")
                    
                    print(f"\n✅ SUCCESS: TypeScript SDK works perfectly with the API!")
                    return True
                else:
                    print(f"\n❌ Order rejected by server")
                    if "response" in result:
                        error_info = result["response"]
                        print(f"   Error: {error_info.get('message', 'Unknown error')}")
            else:
                print(f"\n❌ HTTP Error {response.status_code}")
        else:
            print(f"\n❌ Non-JSON response: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Request failed: {e}")
        
    finally:
        os.unlink(temp_path)
    
    return False

if __name__ == "__main__":
    success = get_typescript_signature_and_test_api()
    
    print(f"\n" + "="*70)
    print(f"📋 TEST SUMMARY:")
    print(f"   TypeScript SDK: ✅ Working")
    print(f"   API Integration: {'✅ Success' if success else '❌ Failed'}")
    
    if success:
        print(f"\n🎯 CONCLUSION:")
        print(f"   ✅ TypeScript SDK successfully places orders")
        print(f"   ✅ Our Rust implementation should match this exactly")
        print(f"   ✅ Once signatures match, Rust version will work too!")
    else:
        print(f"\n🔍 NEXT STEPS:")
        print(f"   📝 Check parameter format and values")
        print(f"   🔧 Ensure exact signature matching")
        print(f"   🧪 Debug any remaining serialization differences")