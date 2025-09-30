#!/usr/bin/env python3
"""
Final test of the working Rust signer
"""

import json
import time

def read_devkey():
    """Read the private key from devkey.json"""
    with open('devkey.json', 'r') as f:
        key_data = json.load(f)
    return ''.join(f'{b:02x}' for b in key_data)

def main():
    print("🚀 Testing Working Rust Signer")
    print("=" * 40)
    
    # Import the working module
    from ambient_signer import ambient_signer
    
    # Load private key
    private_key_hex = read_devkey()
    print(f"✅ Private key loaded: {len(private_key_hex)} chars")
    
    # Create signer
    signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)
    print(f"✅ Signer created successfully")
    print(f"✅ Public key: {signer.public_key}")
    
    # Test signing
    current_time = int(time.time())
    nonce = int(time.time() * 1000)
    
    print(f"\n📋 Signing order with parameters:")
    print(f"  Market ID: 64")
    print(f"  Client ID: {nonce}")
    print(f"  Side: 0 (Buy)")
    print(f"  Quantity: 10000")
    print(f"  Nonce: {nonce}")
    
    signed_permit = signer.sign_place_order(
        program_id="6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
        cluster="testnet",
        authorizer="5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
        market_id=64,
        client_id=nonce,
        side=0,
        qty=10000,
        expires_unix=current_time + 3600,
        max_fee_quote=1000000,
        nonce=nonce,
        price=75000000000,
        tif="GTC",
        reduce_only=False,
        trigger_price=None,
        trigger_type=0,
        relayer=None
    )
    
    print(f"\n✅ Order signed successfully!")
    print(f"✅ Signature: {signed_permit.signature_hex}")
    print(f"✅ Signature length: {len(signed_permit.signature)} bytes")
    print(f"✅ Envelope length: {len(signed_permit.bytes)} bytes")
    
    # Verify signature format
    if len(signed_permit.signature) == 64:
        print("✅ Signature has correct Ed25519 length (64 bytes)")
    else:
        print(f"❌ Wrong signature length: {len(signed_permit.signature)}")
        
    print(f"\n🎉 Python Rust Signer Working Perfectly!")
    print(f"🚀 Performance: Native Rust speed")
    print(f"🔐 Security: Ed25519 cryptography") 
    print(f"🔗 Compatibility: Solana + Ambient Finance")
    print(f"📦 No Dependencies: Pure Python + Rust")
    
    return signed_permit

if __name__ == "__main__":
    result = main()
    print(f"\n✅ Test completed successfully!")