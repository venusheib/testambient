#!/usr/bin/env python3
"""
Compare TypeScript SDK vs Rust implementation signatures

Uses the working TypeScript flow from test_fresh_typescript_order.py and compares
with our Rust implementation to identify exactly where signatures differ.
"""

import json
import time
import requests
import subprocess
import tempfile
import os
from typing import Dict, Any, Tuple

def create_test_payload():
    """Create a test payload for signature comparison"""
    
    # Use fixed timestamp for exact comparison
    fixed_nonce = 1759220000000  # Fixed for reproducible results
    
    payload = {
        "action": {
            "type": "order",
            "a": 0,  # Asset index (BTC)
            "b": True,  # isBuy = true (buy order)
            "p": "105000.0",  # Price
            "s": "0.00005000",  # Size
            "r": False,  # reduce_only
            "t": {"limit": {"tif": "Gtc"}},  # Good till cancelled
            "c": str(fixed_nonce)  # Client order ID
        },
        "nonce": fixed_nonce
    }
    
    return payload, fixed_nonce

def get_typescript_signature(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Get signature using TypeScript SDK"""
    
    print("🔵 Getting TypeScript SDK signature...")
    
    # Write payload to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_path = f.name

    try:
        # Run TypeScript SDK signing
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
        print(f"✅ Public key: {signed_payload['pubkey']}")
        
        return signed_payload

    finally:
        os.unlink(temp_path)

def get_rust_signature(fixed_nonce: int) -> Dict[str, Any]:
    """Get signature using our Rust implementation"""
    
    print("🟠 Getting Rust implementation signature...")
    
    # First build the Rust module
    print("   Building Rust module...")
    build_result = subprocess.run([
        'maturin', 'build', '--release'
    ], capture_output=True, text=True, cwd='ambient_signer')
    
    if build_result.returncode != 0:
        print(f"❌ Rust build failed: {build_result.stderr}")
        return None
    
    # Install the wheel
    print("   Installing Rust module...")
    wheel_path = None
    target_dir = 'ambient_signer/target/wheels'
    if os.path.exists(target_dir):
        for file in os.listdir(target_dir):
            if file.endswith('.whl'):
                wheel_path = os.path.join(target_dir, file)
                break
    
    if wheel_path:
        install_result = subprocess.run([
            'pip', 'install', wheel_path, '--force-reinstall', '--no-deps'
        ], capture_output=True, text=True)
        
        if install_result.returncode != 0:
            print(f"❌ Wheel install failed: {install_result.stderr}")
            # Try alternative installation method
            print("   Trying alternative installation...")
            subprocess.run(['pip', 'uninstall', 'ambient_signer', '-y'], capture_output=True)
    
    # Create Python test script to get Rust signature
    expires_unix = fixed_nonce // 1000 + 60  # 60 seconds after nonce
    
    test_script = f'''
import sys
sys.path.append('ambient_signer/target/release')

try:
    from ambient_signer import ambient_signer
    import json
    
    # Load private key
    with open('devkey.json', 'r') as f:
        key_data = json.load(f)
    private_key_hex = ''.join(f'{{b:02x}}' for b in key_data)
    
    # Create signer
    signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)
    
    # Sign with exact same parameters as TypeScript
    signed_permit = signer.sign_place_order(
        program_id="6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
        cluster="testnet",
        authorizer=signer.public_key,
        market_id=0,  # Asset index 0 (BTC)
        client_id={fixed_nonce},
        side=0,  # Buy (b=true means buy, side=0)
        qty=5000000,  # 0.00005000 BTC in base units (0.00005000 * 10^8)
        expires_unix={expires_unix},
        max_fee_quote=1000000,
        nonce={fixed_nonce},
        price=10500000000000,  # 105000.0 * 10^8 (price in base units)
        tif="Gtc",
        reduce_only=False,
        trigger_price=None,
        trigger_type=0,
        relayer=None
    )
    
    print(f"RUST_SIGNATURE:{signed_permit.signature_hex}")
    print(f"RUST_ENVELOPE:{signed_permit.bytes_hex}")
    print(f"RUST_PUBKEY:{signer.public_key}")
    
except ImportError as e:
    print(f"IMPORT_ERROR:{e}")
except Exception as e:
    print(f"RUST_ERROR:{e}")
'''
    
    # Write and run the test script
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script)
        temp_script = f.name
    
    try:
        result = subprocess.run([
            'python', temp_script
        ], capture_output=True, text=True, cwd='.')
        
        print(f"   Rust output: {result.stdout}")
        if result.stderr:
            print(f"   Rust stderr: {result.stderr}")
        
        # Parse the output
        rust_signature = None
        rust_envelope = None
        rust_pubkey = None
        error = None
        
        for line in result.stdout.strip().split('\n'):
            if line.startswith('RUST_SIGNATURE:'):
                rust_signature = line.split(':', 1)[1]
            elif line.startswith('RUST_ENVELOPE:'):
                rust_envelope = line.split(':', 1)[1]
            elif line.startswith('RUST_PUBKEY:'):
                rust_pubkey = line.split(':', 1)[1]
            elif line.startswith('RUST_ERROR:') or line.startswith('IMPORT_ERROR:'):
                error = line.split(':', 1)[1]
        
        if error:
            print(f"❌ Rust error: {error}")
            return None
        
        if rust_signature:
            print(f"✅ Rust signature: {rust_signature}")
            print(f"✅ Rust envelope: {rust_envelope[:32]}...{rust_envelope[-32:]}")
            print(f"✅ Rust pubkey: {rust_pubkey}")
            
            return {
                'signature': rust_signature,
                'envelope': rust_envelope,
                'pubkey': rust_pubkey
            }
        else:
            print(f"❌ No Rust signature found in output")
            return None
        
    finally:
        os.unlink(temp_script)

def compare_signatures(ts_result: Dict[str, Any], rust_result: Dict[str, Any], payload: Dict[str, Any]):
    """Compare TypeScript and Rust signatures in detail"""
    
    print(f"\n🔍 DETAILED SIGNATURE COMPARISON")
    print(f"=" * 70)
    
    ts_sig = ts_result['signature'][0]
    rust_sig = rust_result['signature']
    
    print(f"📋 Input Payload:")
    print(json.dumps(payload, indent=2))
    
    print(f"\n🔵 TypeScript Results:")
    print(f"   Signature: {ts_sig}")
    print(f"   Pubkey:    {ts_result['pubkey']}")
    print(f"   Length:    {len(ts_sig)} chars ({len(ts_sig)//2} bytes)")
    
    print(f"\n🟠 Rust Results:")
    print(f"   Signature: {rust_sig}")
    print(f"   Pubkey:    {rust_result['pubkey']}")
    print(f"   Length:    {len(rust_sig)} chars ({len(rust_sig)//2} bytes)")
    
    # Compare signatures
    signatures_match = ts_sig == rust_sig
    pubkeys_match = ts_result['pubkey'] == rust_result['pubkey']
    
    print(f"\n🔬 Comparison Results:")
    print(f"   Signatures match: {'✅ YES' if signatures_match else '❌ NO'}")
    print(f"   Public keys match: {'✅ YES' if pubkeys_match else '❌ NO'}")
    
    if not signatures_match:
        print(f"\n🔍 Signature Difference Analysis:")
        
        # Find first difference
        min_len = min(len(ts_sig), len(rust_sig))
        first_diff = None
        for i in range(min_len):
            if ts_sig[i] != rust_sig[i]:
                first_diff = i
                break
        
        if first_diff is not None:
            print(f"   First difference at position {first_diff}")
            print(f"   TypeScript: ...{ts_sig[max(0, first_diff-8):first_diff+8]}...")
            print(f"   Rust:       ...{rust_sig[max(0, first_diff-8):first_diff+8]}...")
        
        # Show hex breakdown for first 32 chars
        print(f"\n   First 32 characters:")
        print(f"   TS:   {ts_sig[:32]}")
        print(f"   Rust: {rust_sig[:32]}")
        
        # Show last 32 characters
        print(f"\n   Last 32 characters:")
        print(f"   TS:   {ts_sig[-32:]}")
        print(f"   Rust: {rust_sig[-32:]}")
    
    if not pubkeys_match:
        print(f"\n🔍 Public Key Difference:")
        print(f"   TypeScript: {ts_result['pubkey']}")
        print(f"   Rust:       {rust_result['pubkey']}")
    
    return signatures_match, pubkeys_match

def test_api_with_both_signatures(ts_result: Dict[str, Any], rust_result: Dict[str, Any], payload: Dict[str, Any]):
    """Test both signatures with the live API to see which one works"""
    
    print(f"\n🌐 TESTING BOTH SIGNATURES WITH LIVE API")
    print(f"=" * 60)
    
    # Test TypeScript signature
    print(f"🔵 Testing TypeScript signature...")
    ts_api_request = {
        "action": payload["action"],
        "nonce": payload["nonce"],
        "signature": ts_result["signature"],
        "pubkey": ts_result["pubkey"]
    }
    
    try:
        ts_response = requests.post(
            "https://embindexer.net/ember/api/dev/v1/exchange",
            json=ts_api_request,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"   Status: {ts_response.status_code}")
        if ts_response.status_code == 200:
            ts_result_data = ts_response.json()
            if ts_result_data.get("status") == "ok":
                print(f"   ✅ TypeScript signature ACCEPTED by API")
                if "response" in ts_result_data and "tx" in ts_result_data["response"]:
                    tx = ts_result_data["response"]["tx"]
                    print(f"   🔗 Transaction: {tx[:32]}...")
            else:
                print(f"   ❌ TypeScript signature rejected: {ts_result_data}")
        else:
            print(f"   ❌ HTTP error: {ts_response.text}")
            
    except Exception as e:
        print(f"   ❌ TypeScript API test failed: {e}")
    
    # Test Rust signature (only if we have one and it's different)
    if rust_result and rust_result['signature'] != ts_result['signature'][0]:
        print(f"\n🟠 Testing Rust signature...")
        rust_api_request = {
            "action": payload["action"],
            "nonce": payload["nonce"],
            "signature": [rust_result["signature"]],  # Wrap in array like TypeScript
            "pubkey": rust_result["pubkey"]
        }
        
        try:
            rust_response = requests.post(
                "https://embindexer.net/ember/api/dev/v1/exchange",
                json=rust_api_request,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"   Status: {rust_response.status_code}")
            if rust_response.status_code == 200:
                rust_result_data = rust_response.json()
                if rust_result_data.get("status") == "ok":
                    print(f"   ✅ Rust signature ACCEPTED by API")
                    if "response" in rust_result_data and "tx" in rust_result_data["response"]:
                        tx = rust_result_data["response"]["tx"]
                        print(f"   🔗 Transaction: {tx[:32]}...")
                else:
                    print(f"   ❌ Rust signature rejected: {rust_result_data}")
            else:
                print(f"   ❌ HTTP error: {rust_response.text}")
                
        except Exception as e:
            print(f"   ❌ Rust API test failed: {e}")
    else:
        print(f"\n🟠 Skipping Rust API test (same signature or no Rust result)")

def main():
    """Main comparison function"""
    
    print(f"🔄 TYPESCRIPT vs RUST SIGNATURE COMPARISON")
    print(f"=" * 70)
    
    # Create test payload
    payload, fixed_nonce = create_test_payload()
    
    print(f"📋 Test Payload:")
    print(json.dumps(payload, indent=2))
    print(f"   Fixed nonce: {fixed_nonce}")
    
    # Get TypeScript signature
    ts_result = get_typescript_signature(payload)
    if not ts_result:
        print(f"❌ Failed to get TypeScript signature - cannot continue")
        return
    
    # Get Rust signature
    rust_result = get_rust_signature(fixed_nonce)
    if not rust_result:
        print(f"❌ Failed to get Rust signature - comparison incomplete")
        
        # Still test TypeScript to confirm it works
        print(f"\n🔵 Testing TypeScript signature only...")
        test_api_with_both_signatures(ts_result, None, payload)
        return
    
    # Compare signatures
    sig_match, key_match = compare_signatures(ts_result, rust_result, payload)
    
    # Test with API
    test_api_with_both_signatures(ts_result, rust_result, payload)
    
    # Final summary
    print(f"\n📊 FINAL SUMMARY")
    print(f"=" * 40)
    print(f"   TypeScript signature: ✅ Working")
    print(f"   Rust signature: {'✅ Generated' if rust_result else '❌ Failed'}")
    
    if rust_result:
        print(f"   Signatures match: {'✅ YES' if sig_match else '❌ NO'}")
        print(f"   Public keys match: {'✅ YES' if key_match else '❌ NO'}")
        
        if sig_match and key_match:
            print(f"\n🎉 PERFECT! Rust implementation produces identical signatures!")
        else:
            print(f"\n🔧 DEBUGGING NEEDED:")
            if not sig_match:
                print(f"      - Signature serialization differs")
            if not key_match:
                print(f"      - Public key derivation differs")
    else:
        print(f"\n🔧 NEXT STEPS:")
        print(f"      - Fix Rust module compilation/installation")
        print(f"      - Ensure PyO3 bindings work correctly")
        print(f"      - Test basic Rust functionality")

if __name__ == "__main__":
    main()