#!/usr/bin/env python3
"""
Compare TypeScript and Rust signatures using the same nonce and expiry
"""

import json
import subprocess
import tempfile
import os

def get_typescript_signature_for_nonce(nonce, expires):
    """Get TypeScript signature for specific nonce and expires"""
    
    print(f"🔵 Getting TypeScript signature for nonce: {nonce}, expires: {expires}")
    
    # Create payload with exact nonce and expires
    payload = {
        "action": {
            "type": "order",
            "a": 0,  # Asset index (BTC)
            "b": True,  # isBuy = true (buy order)
            "p": "105000.0",  # Price
            "s": "0.00005000",  # Size
            "r": False,  # reduce_only
            "t": {"limit": {"tif": "Gtc"}},  # Good till cancelled
            "c": str(nonce)  # Client order ID
        },
        "nonce": nonce
    }
    
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
        
        ts_signature = signed_payload['signature'][0]
        ts_pubkey = signed_payload['pubkey']
        
        print(f"✅ TypeScript signature: {ts_signature}")
        print(f"✅ TypeScript pubkey: {ts_pubkey}")
        
        return ts_signature, ts_pubkey

    except Exception as e:
        print(f"❌ TypeScript error: {e}")
        return None
        
    finally:
        os.unlink(temp_path)

def get_rust_signature_for_nonce(nonce, expires):
    """Get Rust signature for specific nonce and expires"""
    
    print(f"🦀 Getting Rust signature for nonce: {nonce}, expires: {expires}")
    
    try:
        from ambient_signer import ambient_signer
        
        # Load private key
        with open('devkey.json', 'r') as f:
            key_data = json.load(f)
        private_key_hex = ''.join(f'{b:02x}' for b in key_data)
        
        # Create signer
        signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)
        
        # Sign with exact nonce and expires
        signed_permit = signer.sign_place_order(
            program_id="6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
            cluster="testnet",
            authorizer=signer.public_key,
            market_id=0,
            client_id=nonce,
            side=0,  # Buy
            qty=5000000,  # 0.00005000 * 10^8
            expires_unix=expires,
            max_fee_quote=1000000,
            nonce=nonce,
            price=10500000000000,  # 105000.0 * 10^8
            tif="Gtc",
            reduce_only=False,
            trigger_price=None,
            trigger_type=0,
            relayer=None
        )
        
        rust_signature = signed_permit.signature_hex
        rust_pubkey = signer.public_key
        rust_envelope = signed_permit.bytes_hex
        
        print(f"✅ Rust signature: {rust_signature}")
        print(f"✅ Rust pubkey: {rust_pubkey}")
        print(f"✅ Rust envelope: {rust_envelope[:32]}...{rust_envelope[-32:]}")
        
        return rust_signature, rust_pubkey, rust_envelope
        
    except ImportError as e:
        print(f"❌ Rust import failed: {e}")
        return None, None, None
    except Exception as e:
        print(f"❌ Rust error: {e}")
        return None, None, None

def test_rust_signature():
    """Test the Rust signature implementation with same nonce/expires as TypeScript"""
    
    print("🔬 TYPESCRIPT vs RUST SIGNATURE COMPARISON")
    print("=" * 60)
    
    # Use fixed nonce and expires for exact comparison
    test_nonce = 1759230000000  # Fixed timestamp
    test_expires = 1759230060   # 60 seconds later
    
    print(f"📋 Test Parameters:")
    print(f"   Nonce: {test_nonce}")
    print(f"   Expires: {test_expires}")
    print(f"   Price: 105000.0 (10500000000000 in base units)")
    print(f"   Size: 0.00005000 (5000000 in base units)")
    print()
    
    # Get TypeScript signature first
    ts_result = get_typescript_signature_for_nonce(test_nonce, test_expires)
    if not ts_result:
        print("❌ Failed to get TypeScript signature")
        return None, None, None
    
    ts_signature, ts_pubkey = ts_result
    print()
    
    # Get Rust signature with same parameters
    rust_result = get_rust_signature_for_nonce(test_nonce, test_expires)
    if not rust_result or not rust_result[0]:
        print("❌ Failed to get Rust signature")
        return ts_signature, ts_pubkey, None
    
    rust_signature, rust_pubkey, rust_envelope = rust_result
    
    return ts_signature, ts_pubkey, rust_signature, rust_pubkey, rust_envelope

def test_rust_signature_old():
    """Old test method - keeping for backwards compatibility"""
    
    print("🦀 TESTING RUST SIGNATURE IMPLEMENTATION")
    print("=" * 60)
    
    # Try multiple ways to get the Rust signature
    
    # Method 1: Try direct import
    try:
        print("Method 1: Trying direct import...")
        from ambient_signer import ambient_signer
        
        # Load private key
        with open('devkey.json', 'r') as f:
            key_data = json.load(f)
        private_key_hex = ''.join(f'{b:02x}' for b in key_data)
        
        # Create signer
        signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)
        
        # Target parameters
        target_nonce = 1759220000000
        target_expires = 1759220060
        
        # Sign with exact parameters
        signed_permit = signer.sign_place_order(
            program_id="6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
            cluster="testnet",
            authorizer=signer.public_key,
            market_id=0,
            client_id=target_nonce,
            side=0,  # Buy
            qty=5000000,  # 0.00005000 * 10^8
            expires_unix=target_expires,
            max_fee_quote=1000000,
            nonce=target_nonce,
            price=10500000000000,  # 105000.0 * 10^8
            tif="Gtc",
            reduce_only=False,
            trigger_price=None,
            trigger_type=0,
            relayer=None
        )
        
        print("✅ METHOD 1 SUCCESS - Direct import worked!")
        print(f"   Rust Signature: {signed_permit.signature_hex}")
        print(f"   Rust Public Key: {signer.public_key}")
        print(f"   Rust Envelope: {signed_permit.bytes_hex[:32]}...{signed_permit.bytes_hex[-32:]}")
        
        return signed_permit.signature_hex, signer.public_key, signed_permit.bytes_hex
        
    except ImportError as e:
        print(f"❌ Method 1 failed: {e}")
    except Exception as e:
        print(f"❌ Method 1 error: {e}")
    
    # Method 2: Try with venv
    print("\nMethod 2: Trying with venv...")
    venv_paths = [
        "venv/bin/python",
        "../venv/bin/python", 
        "ambient_signer/venv/bin/python"
    ]
    
    for venv_path in venv_paths:
        if os.path.exists(venv_path):
            print(f"   Found venv at: {venv_path}")
            try:
                test_script = f'''
import json
from ambient_signer import ambient_signer

with open('devkey.json', 'r') as f:
    key_data = json.load(f)
private_key_hex = ''.join(f'{{b:02x}}' for b in key_data)

signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)

signed_permit = signer.sign_place_order(
    program_id="6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
    cluster="testnet",
    authorizer=signer.public_key,
    market_id=0,
    client_id=1759220000000,
    side=0,
    qty=5000000,
    expires_unix=1759220060,
    max_fee_quote=1000000,
    nonce=1759220000000,
    price=10500000000000,
    tif="Gtc",
    reduce_only=False,
    trigger_price=None,
    trigger_type=0,
    relayer=None
)

print(f"RUST_SIGNATURE:{{signed_permit.signature_hex}}")
print(f"RUST_PUBKEY:{{signer.public_key}}")
print(f"RUST_ENVELOPE:{{signed_permit.bytes_hex}}")
'''
                
                # Write and run test script
                with open('temp_rust_test.py', 'w') as f:
                    f.write(test_script)
                
                result = subprocess.run([venv_path, 'temp_rust_test.py'], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ METHOD 2 SUCCESS - Venv worked!")
                    print(result.stdout)
                    
                    # Parse output
                    rust_sig = None
                    rust_key = None
                    rust_env = None
                    
                    for line in result.stdout.strip().split('\n'):
                        if line.startswith('RUST_SIGNATURE:'):
                            rust_sig = line.split(':', 1)[1]
                        elif line.startswith('RUST_PUBKEY:'):
                            rust_key = line.split(':', 1)[1]
                        elif line.startswith('RUST_ENVELOPE:'):
                            rust_env = line.split(':', 1)[1]
                    
                    os.unlink('temp_rust_test.py')
                    return rust_sig, rust_key, rust_env
                else:
                    print(f"❌ Venv test failed: {result.stderr}")
                
                os.unlink('temp_rust_test.py')
                
            except Exception as e:
                print(f"❌ Venv method error: {e}")
    
    # Method 3: Show installation fix
    print("\nMethod 3: Installation guidance...")
    print("To fix the Rust installation, run:")
    print("   cd ambient_signer")
    print("   python -m venv venv")
    print("   source venv/bin/activate  # or venv\\Scripts\\activate on Windows")
    print("   pip install maturin")
    print("   maturin develop --release")
    print("   cd ..")
    print("   venv/bin/python test_rust_signature.py")
    
    return None, None, None

def compare_with_target(rust_sig, rust_key, rust_env):
    """Compare Rust results with TypeScript target"""
    
    print("\n🔍 COMPARISON WITH TYPESCRIPT TARGET")
    print("=" * 60)
    
    target_signature = "6ac91350a226f5c68bd2e2ae83f665943919f700ded5f1e554f240640fa8cb20849f1424e58c194013ce8a2817958f0ac453ac9e999e23513edcb8465a25630a"
    target_pubkey = "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
    
    print(f"🎯 TARGET (TypeScript):")
    print(f"   Signature: {target_signature}")
    print(f"   Pubkey:    {target_pubkey}")
    
    if rust_sig and rust_key:
        print(f"\n🦀 RUST RESULTS:")
        print(f"   Signature: {rust_sig}")
        print(f"   Pubkey:    {rust_key}")
        
        sig_match = rust_sig == target_signature
        key_match = rust_key == target_pubkey
        
        print(f"\n📊 COMPARISON:")
        print(f"   Signatures match: {'✅ YES' if sig_match else '❌ NO'}")
        print(f"   Public keys match: {'✅ YES' if key_match else '❌ NO'}")
        
        if sig_match and key_match:
            print(f"\n🎉 PERFECT MATCH! Rust implementation is working correctly!")
            print(f"🚀 Ready to replace TypeScript SDK!")
        else:
            print(f"\n🔧 DEBUGGING NEEDED:")
            if not sig_match:
                print(f"      - Signature serialization differs")
                # Show first difference
                min_len = min(len(rust_sig), len(target_signature))
                for i in range(min_len):
                    if rust_sig[i] != target_signature[i]:
                        print(f"      - First difference at position {i}")
                        print(f"      - Target: ...{target_signature[max(0,i-8):i+8]}...")
                        print(f"      - Rust:   ...{rust_sig[max(0,i-8):i+8]}...")
                        break
            if not key_match:
                print(f"      - Public key derivation differs")
    else:
        print(f"\n❌ NO RUST RESULTS - Fix installation first")
        print(f"\n📋 Once fixed, you should see:")
        print(f"   Rust signature: {target_signature[:32]}...{target_signature[-32:]}")
        print(f"   Rust pubkey: {target_pubkey}")

if __name__ == "__main__":
    rust_sig, rust_key, rust_env = test_rust_signature()
    compare_with_target(rust_sig, rust_key, rust_env)
    
    print(f"\n📝 SUMMARY:")
    if rust_sig:
        print(f"   ✅ Rust implementation generated signature")
        print(f"   🔍 Check comparison results above")
    else:
        print(f"   ❌ Rust implementation needs installation fix")
        print(f"   🔧 Follow the installation guidance above")