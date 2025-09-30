#!/usr/bin/env python3
"""
Exact payload comparison between TypeScript SDK and Rust implementation
"""

import json
import time
import subprocess
import tempfile
import os

def create_test_payload():
    """Create a standardized test payload for comparison"""
    
    # Use realistic values based on working example
    fixed_nonce = 1758796565225  # Working timestamp from example
    fixed_expires = 1758796625   # 60 seconds later
    
    payload = {
        "action": {
            "type": "order",
            "a": 0,  # Asset index (BTC)
            "b": False,  # isBuy = false (sell order)
            "p": "112000.0",  # Price from working example
            "s": "0.00010000",  # Size from working example
            "r": False,  # reduce_only
            "t": {"limit": {"tif": "Gtc"}},  # Time in force
            "c": str(fixed_nonce)  # Client order ID
        },
        "nonce": fixed_nonce
    }
    
    return payload, fixed_nonce, fixed_expires

def get_typescript_signature(payload):
    """Get signature from TypeScript SDK"""
    
    print("📝 Getting TypeScript SDK signature...")
    
    # Write payload to temp file
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
            return None

        signed_payload = json.loads(result.stdout)
        
        print(f"✅ TypeScript signature: {signed_payload['signature'][0]}")
        return signed_payload

    finally:
        os.unlink(temp_path)

def get_rust_signature(fixed_nonce, fixed_expires):
    """Get signature from Rust implementation"""
    
    print("🦀 Getting Rust implementation signature...")
    
    # Build the signer first
    build_result = subprocess.run([
        'maturin', 'develop'
    ], capture_output=True, text=True, cwd='ambient_signer')
    
    if build_result.returncode != 0:
        print(f"❌ Rust build failed: {build_result.stderr}")
        return None
    
    # Create a simple test script
    test_script = f'''
import json
from ambient_signer import ambient_signer

# Load private key
with open('devkey.json', 'r') as f:
    key_data = json.load(f)
private_key_hex = ''.join(f'{{b:02x}}' for b in key_data)

# Create signer
signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)

# Sign with exact same parameters as TypeScript payload
signed_permit = signer.sign_place_order(
    program_id="6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
    cluster="testnet",
    authorizer=signer.public_key,
    market_id=0,  # Asset index 0 (BTC)
    client_id={fixed_nonce},
    side=1,  # Sell (b=false means sell)
    qty=10000000,  # 0.0001 BTC in base units (0.00010000 * 10^8)
    expires_unix={fixed_expires},
    max_fee_quote=1000000,
    nonce={fixed_nonce},
    price=11200000000000,  # 112000.0 * 10^8 (price in base units)
    tif="Gtc",
    reduce_only=False,
    trigger_price=None,
    trigger_type=0,
    relayer=None
)

print(f"Rust signature: {{signed_permit.signature_hex}}")
print(f"Rust envelope: {{signed_permit.bytes_hex}}")
print(f"Public key: {{signer.public_key}}")
'''
    
    # Write and run the test script
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script)
        temp_script = f.name
    
    try:
        result = subprocess.run([
            'python', temp_script
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode != 0:
            print(f"❌ Rust test failed: {result.stderr}")
            return None
            
        lines = result.stdout.strip().split('\n')
        rust_signature = None
        rust_envelope = None
        public_key = None
        
        for line in lines:
            if line.startswith('Rust signature: '):
                rust_signature = line.split(': ')[1]
            elif line.startswith('Rust envelope: '):
                rust_envelope = line.split(': ')[1]
            elif line.startswith('Public key: '):
                public_key = line.split(': ')[1]
        
        print(f"✅ Rust signature: {rust_signature}")
        
        return {
            'signature': rust_signature,
            'envelope': rust_envelope,
            'public_key': public_key
        }
        
    finally:
        os.unlink(temp_script)

def test_typescript_api_call(ts_result, payload):
    """Test the TypeScript signed payload with the live API"""
    
    print("\n🌐 TESTING TYPESCRIPT PAYLOAD WITH LIVE API")
    print("-" * 50)
    
    # Create API request using TypeScript signature
    api_request = {
        "action": payload["action"],
        "nonce": payload["nonce"],
        "signature": ts_result["signature"],
        "pubkey": ts_result["pubkey"]
    }
    
    print(f"📤 API Request:")
    print(json.dumps(api_request, indent=2))
    
    try:
        import requests
        
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
            
            if response.status_code == 200 and result.get("status") == "ok":
                print(f"\n🎉 TYPESCRIPT ORDER PLACED SUCCESSFULLY!")
                
                if "response" in result and "tx" in result["response"]:
                    tx_hash = result["response"]["tx"]
                    print(f"🔗 Transaction Hash: {tx_hash}")
                    print(f"   Explorer: https://explorer.solana.com/tx/{tx_hash}?cluster=testnet")
                
                return True, result
            else:
                print(f"\n❌ TypeScript order failed!")
                return False, result
        else:
            print(f"\n❌ Non-JSON response: {response.text}")
            return False, {"error": "Non-JSON response"}
            
    except Exception as e:
        print(f"\n❌ API request failed: {e}")
        return False, {"error": str(e)}

def compare_signatures():
    """Compare signatures from both implementations"""
    
    print("🔍 EXACT PAYLOAD SIGNATURE COMPARISON")
    print("=" * 60)
    
    # Create identical payload
    payload, fixed_nonce, fixed_expires = create_test_payload()
    
    print(f"📋 Test Payload:")
    print(json.dumps(payload, indent=2))
    print(f"   Nonce: {fixed_nonce}")
    print(f"   Expires: {fixed_expires}")
    print()
    
    # Get TypeScript signature
    ts_result = get_typescript_signature(payload)
    if not ts_result:
        print("❌ Failed to get TypeScript signature")
        return
    
    print()
    
    # Get Rust signature
    rust_result = get_rust_signature(fixed_nonce, fixed_expires)
    if not rust_result:
        print("❌ Failed to get Rust signature")
        return
    
    print()
    print("🔬 COMPARISON RESULTS:")
    print("-" * 40)
    
    # Compare signatures
    ts_sig = ts_result['signature'][0]
    rust_sig = rust_result['signature']
    
    print(f"TypeScript: {ts_sig}")
    print(f"Rust:       {rust_sig}")
    print(f"Match:      {'✅ IDENTICAL' if ts_sig == rust_sig else '❌ DIFFERENT'}")
    
    if ts_sig != rust_sig:
        print(f"\n🔍 Difference Analysis:")
        for i, (a, b) in enumerate(zip(ts_sig, rust_sig)):
            if a != b:
                print(f"   First difference at position {i}: '{a}' vs '{b}'")
                break
    
    print(f"\n📊 Summary:")
    print(f"   TypeScript signature length: {len(ts_sig)}")
    print(f"   Rust signature length:       {len(rust_sig)}")
    print(f"   Signatures identical:        {'✅' if ts_sig == rust_sig else '❌'}")
    
    if ts_sig == rust_sig:
        print(f"\n🎉 SUCCESS! Both implementations produce identical signatures!")
        print(f"   The signing core is working perfectly!")
        
        # Test TypeScript API call
        test_typescript_api_call(ts_result, payload)
        
    else:
        print(f"\n⚠️  Signatures differ - need to investigate parameter serialization")
        
        # Still test TypeScript API call to see if it works
        print(f"\n🧪 Testing TypeScript API call anyway...")
        test_typescript_api_call(ts_result, payload)

if __name__ == "__main__":
    compare_signatures()