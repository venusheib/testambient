#!/usr/bin/env python3
"""
Simple test to build and use Rust signer
"""

import subprocess
import json
import os

def test_rust_signer():
    """Test the Rust signer with maturin develop"""
    
    print("🦀 Testing Rust Signer")
    print("=" * 40)
    
    # Try to build and install with maturin develop
    print("1. Building with maturin develop...")
    
    try:
        # Use maturin develop to build and install in development mode
        result = subprocess.run([
            'maturin', 'develop', '--release'
        ], cwd='ambient_signer', capture_output=True, text=True)
        
        print(f"   Return code: {result.returncode}")
        if result.stdout:
            print(f"   Stdout: {result.stdout}")
        if result.stderr:
            print(f"   Stderr: {result.stderr}")
        
        if result.returncode != 0:
            print("❌ Maturin develop failed")
            return False
            
    except Exception as e:
        print(f"❌ Maturin develop error: {e}")
        return False
    
    # Test the import
    print("\n2. Testing import...")
    try:
        from ambient_signer import ambient_signer
        print("✅ Import successful!")
        
        # Test basic functionality
        print("\n3. Testing basic functionality...")
        
        # Load key
        with open('devkey.json', 'r') as f:
            key_data = json.load(f)
        private_key_hex = ''.join(f'{b:02x}' for b in key_data)
        
        # Create signer
        signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)
        print(f"✅ Signer created! Public key: {signer.public_key}")
        
        # Test signing with fixed parameters
        print("\n4. Testing signing...")
        fixed_nonce = 1759220000000
        expires_unix = fixed_nonce // 1000 + 60
        
        signed_permit = signer.sign_place_order(
            program_id="6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
            cluster="testnet",
            authorizer=signer.public_key,
            market_id=0,
            client_id=fixed_nonce,
            side=0,  # Buy
            qty=5000000,  # 0.00005000 BTC in base units
            expires_unix=expires_unix,
            max_fee_quote=1000000,
            nonce=fixed_nonce,
            price=10500000000000,  # 105000.0 * 10^8
            tif="Gtc",
            reduce_only=False,
            trigger_price=None,
            trigger_type=0,
            relayer=None
        )
        
        print(f"✅ Signing successful!")
        print(f"   Signature: {signed_permit.signature_hex}")
        print(f"   Envelope: {signed_permit.bytes_hex[:32]}...{signed_permit.bytes_hex[-32:]}")
        
        return {
            'signature': signed_permit.signature_hex,
            'envelope': signed_permit.bytes_hex,
            'pubkey': signer.public_key
        }
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Runtime error: {e}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    result = test_rust_signer()
    
    if result:
        print(f"\n🎉 Rust signer working!")
        print(f"Now we can compare with TypeScript signature...")
    else:
        print(f"\n❌ Rust signer needs fixing")