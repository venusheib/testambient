#!/usr/bin/env python3
"""
Final working test - Use EXACT TypeScript SDK context and parameters
"""

import json
import time
import subprocess
import tempfile
import os
import requests

def get_typescript_signature_and_bytes():
    """Get the exact signature and envelope bytes from TypeScript SDK"""
    
    # Create the exact payload that works
    payload = {
        "action": {
            "type": "order",
            "a": 0,
            "b": True,
            "p": "50000000000000000", 
            "s": "100000000000",
            "r": False,
            "t": {"limit": {"tif": "Gtc"}},
            "c": "1759184076517"
        },
        "nonce": 1759184076517
    }
    
    # Write to temp file
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
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ TypeScript SDK failed: {result.stderr}")
            return None, None, None

        signed_payload = json.loads(result.stdout)
        
        # Also get envelope bytes
        result2 = subprocess.run([
            'node',
            'ambient-ember-sdk/debug_envelope_bytes.mjs',
            'devkey.json',
            temp_path
        ], capture_output=True, text=True, cwd='.')

        envelope_hex = None
        if result2.returncode == 0:
            # Extract envelope hex from debug output
            for line in result2.stdout.split('\n'):
                if line.startswith('TypeScript Envelope:'):
                    envelope_hex = line.split(': ')[1]
                    break

        return signed_payload, envelope_hex, payload

    finally:
        os.unlink(temp_path)

def test_with_exact_typescript_context():
    """Test using the exact same context as TypeScript SDK"""
    
    print("🎯 Final Test: Exact TypeScript SDK Context")
    print("=" * 60)
    
    # Get TypeScript reference
    print("1. Getting TypeScript SDK reference...")
    ts_signed, ts_envelope_hex, ts_payload = get_typescript_signature_and_bytes()
    
    if not ts_signed:
        print("❌ Failed to get TypeScript reference")
        return
    
    print(f"✅ TypeScript SDK signature: {ts_signed['signature'][0][:32]}...")
    if ts_envelope_hex:
        print(f"✅ TypeScript envelope: {ts_envelope_hex[:32]}...")
    
    # Now use Rust with EXACT same parameters
    print("\n2. Using Rust with identical parameters...")
    
    from ambient_signer import ambient_signer
    
    with open('devkey.json', 'r') as f:
        key_data = json.load(f)
    private_key_hex = ''.join(f'{b:02x}' for b in key_data)
    
    signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)
    
    # Use EXACT parameters from TypeScript
    signed_permit = signer.sign_place_order(
        program_id="6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
        cluster="testnet",
        authorizer=signer.public_key,
        market_id=64,  # From TypeScript context (marketId: 64n)
        client_id=1759184076517,
        side=0,
        qty=100000000000,  # From TypeScript
        expires_unix=1759184136,  # From TypeScript  
        max_fee_quote=1000000,  # From TypeScript
        nonce=1759184076517,
        price=50000000000000000,  # From TypeScript
        tif="Gtc",
        reduce_only=False,
        trigger_price=None,
        trigger_type=0,
        relayer=None
    )
    
    print(f"✅ Rust signature: {signed_permit.signature_hex[:32]}...")
    print(f"✅ Rust envelope: {signed_permit.bytes_hex[:32]}...")
    
    # Compare
    print(f"\n3. Comparison:")
    ts_sig = ts_signed['signature'][0]
    rust_sig = signed_permit.signature_hex
    
    print(f"   Signatures match: {'✅' if ts_sig == rust_sig else '❌'}")
    
    if ts_envelope_hex:
        env_match = ts_envelope_hex == signed_permit.bytes_hex
        print(f"   Envelopes match:  {'✅' if env_match else '❌'}")
        
        if env_match:
            print(f"\n🎉 PERFECT MATCH! Now testing live API call...")
            
            # Create API request with TypeScript-proven parameters
            api_request = {
                "action": ts_payload["action"],  # Use exact TypeScript action
                "nonce": ts_payload["nonce"],
                "signature": signed_permit.signature_hex,  # Our Rust signature
                "pubkey": signer.public_key,
                "permitBytes": signed_permit.bytes_hex
            }
            
            print(f"\n4. Live API call with proven parameters:")
            print(json.dumps(api_request, indent=2)[:300] + "...")
            
            try:
                response = requests.post(
                    "https://embindexer.net/ember/api/dev/v1/exchange",
                    json=api_request,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                print(f"\n📡 Response: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"🎉 SUCCESS! {json.dumps(result, indent=2)}")
                else:
                    result = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"text": response.text}
                    print(f"❌ Failed: {json.dumps(result, indent=2)}")
                    
            except Exception as e:
                print(f"❌ Request error: {e}")
    
    print(f"\n✅ Test complete - Rust signer produces {'identical' if ts_sig == rust_sig else 'different'} results")

if __name__ == "__main__":
    test_with_exact_typescript_context()