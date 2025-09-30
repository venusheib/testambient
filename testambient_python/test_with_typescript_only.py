#!/usr/bin/env python3
"""
Since Rust module installation is having issues, let's test with just TypeScript
to get the target signature we need to match, then figure out the Rust installation.
"""

import json
import time
import requests
import subprocess
import tempfile
import os

def create_fixed_test_payload():
    """Create the exact test payload for comparison"""
    
    fixed_nonce = 1759220000000  # Fixed timestamp for reproducible results
    
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

def get_typescript_signature_and_test(payload):
    """Get TypeScript signature and test with API"""
    
    print("🔵 TYPESCRIPT SDK TEST")
    print("=" * 50)
    
    # Write payload to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_path = f.name

    try:
        # Run TypeScript SDK signing
        print("1. Signing with TypeScript SDK...")
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
        
        # Test with API
        print(f"\n2. Testing with live API...")
        response = requests.post(
            "https://embindexer.net/ember/api/dev/v1/exchange",
            json=signed_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result_data = response.json()
            print(f"   Response: {json.dumps(result_data, indent=2)}")
            
            if result_data.get("status") == "ok":
                print(f"✅ API ACCEPTS TYPESCRIPT SIGNATURE!")
                
                if "response" in result_data and "tx" in result_data["response"]:
                    tx = result_data["response"]["tx"]
                    print(f"🔗 Transaction: {tx}")
                    print(f"   Explorer: https://explorer.solana.com/tx/{tx}?cluster=testnet")
                
                return signed_payload
        else:
            print(f"❌ API rejected: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        os.unlink(temp_path)
    
    return None

def show_rust_target():
    """Show what our Rust implementation needs to produce"""
    
    print(f"\n🎯 RUST IMPLEMENTATION TARGET")
    print(f"=" * 50)
    
    payload, fixed_nonce = create_fixed_test_payload()
    
    print(f"📋 Input Payload:")
    print(json.dumps(payload, indent=2))
    
    # Get TypeScript signature
    ts_result = get_typescript_signature_and_test(payload)
    
    if ts_result:
        ts_sig = ts_result['signature'][0]
        ts_pubkey = ts_result['pubkey']
        
        print(f"\n🎯 RUST MUST PRODUCE:")
        print(f"   Signature: {ts_sig}")
        print(f"   Public Key: {ts_pubkey}")
        print(f"   For nonce: {fixed_nonce}")
        
        # Show exact parameters for Rust
        expires_unix = fixed_nonce // 1000 + 60
        
        print(f"\n📝 EXACT RUST PARAMETERS NEEDED:")
        print(f"   program_id: '6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g'")
        print(f"   cluster: 'testnet'")
        print(f"   market_id: 0")
        print(f"   client_id: {fixed_nonce}")
        print(f"   side: 0  # Buy (b=true → side=0)")
        print(f"   qty: 5000000  # 0.00005000 * 10^8")
        print(f"   expires_unix: {expires_unix}")
        print(f"   max_fee_quote: 1000000")
        print(f"   nonce: {fixed_nonce}")
        print(f"   price: 10500000000000  # 105000.0 * 10^8")
        print(f"   tif: 'Gtc'")
        print(f"   reduce_only: false")
        
        print(f"\n🔧 DEBUGGING APPROACH:")
        print(f"   1. Fix Rust module installation")
        print(f"   2. Call with exact parameters above")
        print(f"   3. Compare signature byte-by-byte")
        print(f"   4. Debug serialization differences")
        
        return ts_sig, ts_pubkey, fixed_nonce
    else:
        print(f"❌ Could not get TypeScript signature")
        return None, None, None

def check_rust_installation_options():
    """Check different ways to get Rust working"""
    
    print(f"\n🔧 RUST INSTALLATION OPTIONS")
    print(f"=" * 50)
    
    # Check if we can import directly
    try:
        from ambient_signer import ambient_signer
        print(f"✅ Option 1: Direct import works!")
        return True
    except ImportError:
        print(f"❌ Option 1: Direct import failed")
    
    # Check maturin develop
    try:
        result = subprocess.run(['maturin', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Option 2: Maturin available ({result.stdout.strip()})")
            print(f"   Need to create virtualenv for maturin develop")
        else:
            print(f"❌ Option 2: Maturin not working")
    except:
        print(f"❌ Option 2: Maturin not found")
    
    # Check wheel
    wheel_path = "ambient_signer/target/wheels/ambient_signer-0.1.0-cp313-cp313-macosx_11_0_arm64.whl"
    if os.path.exists(wheel_path):
        print(f"✅ Option 3: Wheel exists at {wheel_path}")
        print(f"   Platform compatibility issue - need to fix installation")
    else:
        print(f"❌ Option 3: No wheel found")
    
    # Check if we can build differently
    print(f"\n💡 SUGGESTED FIXES:")
    print(f"   1. Create virtual environment and use maturin develop")
    print(f"   2. Modify wheel compatibility tags")
    print(f"   3. Build for correct Python/platform combination")
    
    return False

def main():
    """Main function"""
    
    print(f"🔬 TYPESCRIPT vs RUST SIGNATURE ANALYSIS")
    print(f"=" * 60)
    
    # Get the target signature from TypeScript
    target_sig, target_pubkey, target_nonce = show_rust_target()
    
    # Check Rust installation options
    rust_available = check_rust_installation_options()
    
    print(f"\n📊 CURRENT STATUS:")
    print(f"   TypeScript SDK: ✅ Working perfectly")
    print(f"   Target signature: {'✅ Obtained' if target_sig else '❌ Failed'}")
    print(f"   Rust module: {'✅ Available' if rust_available else '❌ Needs setup'}")
    
    if target_sig and not rust_available:
        print(f"\n🎯 NEXT STEPS:")
        print(f"   1. Fix Rust module installation")
        print(f"   2. Generate Rust signature for nonce {target_nonce}")
        print(f"   3. Compare with target: {target_sig[:32]}...{target_sig[-32:]}")
        print(f"   4. Debug any differences")
    
    if target_sig:
        print(f"\n✅ SUCCESS: We have a clear target to match!")
        return True
    else:
        print(f"\n❌ FAILURE: Could not establish baseline")
        return False

if __name__ == "__main__":
    main()