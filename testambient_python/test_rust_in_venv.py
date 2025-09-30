#!/usr/bin/env python3
"""
Test Rust signature in virtual environment
"""

import json
from exchange.ambient_trading_with_sdk import

def test_rust_signature():
    """Test Rust signature with exact target parameters"""
    
    print("🦀 TESTING RUST SIGNATURE")
    print("=" * 50)
    
    try:
        from ambient_signer import ambient_signer
        print("✅ Rust module imported successfully!")
        
        # Load private key
        with open('devkey.json', 'r') as f:
            key_data = json.load(f)
        private_key_hex = ''.join(f'{b:02x}' for b in key_data)
        
        # Create signer
        signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)
        print(f"✅ Signer created! Public key: {signer.public_key}")
        
        # Use EXACT parameters from TypeScript analysis
        target_nonce = 1759220000000
        target_expires = 1759220060
        
        print(f"\n📝 Signing with exact parameters:")
        print(f"   nonce: {target_nonce}")
        print(f"   expires_unix: {target_expires}")
        print(f"   side: 0 (buy)")
        print(f"   qty: 5000000 (0.00005000 * 10^8)")
        print(f"   price: 10500000000000 (105000.0 * 10^8)")
        
        signed_permit = signer.sign_place_order(
            program_id="6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
            cluster="testnet",
            authorizer=signer.public_key,
            market_id=0,
            client_id=target_nonce,
            side=0,  # Buy (b=true → side=0)
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
        
        rust_signature = signed_permit.signature_hex
        rust_envelope = signed_permit.bytes_hex
        rust_pubkey = signer.public_key
        
        print(f"\n✅ RUST RESULTS:")
        print(f"   Signature: {rust_signature}")
        print(f"   Envelope:  {rust_envelope[:32]}...{rust_envelope[-32:]}")
        print(f"   Pubkey:    {rust_pubkey}")
        
        # Compare with target
        target_signature = "6ac91350a226f5c68bd2e2ae83f665943919f700ded5f1e554f240640fa8cb20849f1424e58c194013ce8a2817958f0ac453ac9e999e23513edcb8465a25630a"
        target_pubkey = "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
        
        print(f"\n🎯 TARGET vs RUST COMPARISON:")
        print(f"   Target Sig:  {target_signature}")
        print(f"   Rust Sig:    {rust_signature}")
        print(f"   Signatures:  {'✅ MATCH' if rust_signature == target_signature else '❌ DIFFER'}")
        
        print(f"\n   Target Key:  {target_pubkey}")
        print(f"   Rust Key:    {rust_pubkey}")
        print(f"   Public Keys: {'✅ MATCH' if rust_pubkey == target_pubkey else '❌ DIFFER'}")
        
        if rust_signature == target_signature and rust_pubkey == target_pubkey:
            print(f"\n🎉 PERFECT MATCH! Rust implementation is working correctly!")
            return True, rust_signature, rust_envelope, rust_pubkey
        else:
            print(f"\n🔍 DIFFERENCES FOUND - need debugging")
            
            if rust_signature != target_signature:
                # Find first difference
                min_len = min(len(rust_signature), len(target_signature))
                for i in range(min_len):
                    if rust_signature[i] != target_signature[i]:
                        print(f"   First sig difference at position {i}")
                        print(f"   Context: ...{target_signature[max(0,i-8):i+8]}... vs ...{rust_signature[max(0,i-8):i+8]}...")
                        break
            
            return False, rust_signature, rust_envelope, rust_pubkey
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False, None, None, None
    except Exception as e:
        print(f"❌ Runtime error: {e}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False, None, None, None

if __name__ == "__main__":
    success, sig, env, key = test_rust_signature()
    
    if success:
        print(f"\n🏆 SUCCESS: Rust produces identical signatures to TypeScript!")
    else:
        print(f"\n🔧 DEBUGGING NEEDED: Signatures differ")
        if sig:
            print(f"   At least Rust module is working - can debug serialization")
        else:
            print(f"   Need to fix Rust module first")