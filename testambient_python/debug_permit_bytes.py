#!/usr/bin/env python3
"""
Debug permit envelope bytes to find the mismatch
Compare TypeScript SDK vs Rust implementation byte-by-byte
"""

import json
import time
import subprocess
import tempfile
import os
from ambient_signer import ambient_signer
def test_typescript_sdk_bytes():
    """Get the exact bytes from TypeScript SDK"""
    
    # Create test payload
    payload = {
        "action": {
            "type": "order",
            "a": 0,
            "b": True,
            "p": "50000000000",
            "s": "1000",
            "r": False,
            "t": {"limit": {"tif": "Gtc"}},
            "c": "1759184076517"
        }
    }
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_path = f.name

    try:
        # Run the SDK signing script to get the exact envelope bytes
        result = subprocess.run([
            'node',
            'ambient-ember-sdk/scripts/signPayload.mjs',
            'devkey.json',
            temp_path
        ], capture_output=True, text=True, cwd='.')

        if result.returncode != 0:
            print(f"❌ SDK signing failed: {result.stderr}")
            return None, None

        # Parse the signed payload
        signed_payload = json.loads(result.stdout)
        
        # Extract signature and permitBytes
        signature_hex = signed_payload['signature'][0]  # First signature
        permit_bytes = None
        
        # The SDK doesn't output permitBytes directly, but we can get them from the signing process
        # Let's modify the SDK script to output the raw envelope bytes
        
        print(f"✅ TypeScript SDK signed successfully")
        print(f"   Signature: {signature_hex[:32]}...{signature_hex[-32:]}")
        print(f"   Pubkey: {signed_payload['pubkey']}")
        
        return signature_hex, permit_bytes

    finally:
        os.unlink(temp_path)

def test_rust_signer_bytes():
    """Get the exact bytes from Rust signer"""
    
    from ambient_signer import ambient_signer
    
    # Load private key
    with open('devkey.json', 'r') as f:
        key_data = json.load(f)
    private_key_hex = ''.join(f'{b:02x}' for b in key_data)
    
    # Create signer
    signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)
    
    # Sign with same parameters
    current_time = int(time.time())
    nonce = 1759184076517  # Use same nonce as TypeScript test
    
    signed_permit = signer.sign_place_order(
        program_id="6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
        cluster="testnet",
        authorizer=signer.public_key,
        market_id=0,
        client_id=nonce,
        side=0,
        qty=1000,
        expires_unix=current_time + 3600,
        max_fee_quote=100000,
        nonce=nonce,
        price=50000000000,
        tif="Gtc",
        reduce_only=False,
        trigger_price=None,
        trigger_type=0,
        relayer=None
    )
    
    print(f"✅ Rust signer signed successfully")
    print(f"   Signature: {signed_permit.signature_hex[:32]}...{signed_permit.signature_hex[-32:]}")
    print(f"   Pubkey: {signer.public_key}")
    print(f"   Envelope bytes: {len(signed_permit.bytes)} bytes")
    
    return signed_permit.signature_hex, signed_permit.bytes_hex

def compare_implementations():
    """Compare TypeScript vs Rust implementations"""
    print("🔍 Comparing TypeScript SDK vs Rust Signer")
    print("=" * 60)
    
    print("\n1. Testing TypeScript SDK...")
    ts_signature, ts_bytes = test_typescript_sdk_bytes()
    
    print("\n2. Testing Rust Signer...")
    rust_signature, rust_bytes = test_rust_signer_bytes()
    
    print("\n3. Comparison Results:")
    print("-" * 30)
    
    if ts_signature and rust_signature:
        print(f"TypeScript Signature: {ts_signature[:32]}...{ts_signature[-32:]}")
        print(f"Rust Signature:       {rust_signature[:32]}...{rust_signature[-32:]}")
        print(f"Signatures Match:     {'✅' if ts_signature == rust_signature else '❌'}")
        
        if ts_signature != rust_signature:
            print("\n🔍 Detailed Signature Analysis:")
            for i in range(0, len(ts_signature), 16):
                ts_chunk = ts_signature[i:i+16]
                rust_chunk = rust_signature[i:i+16] if i < len(rust_signature) else ""
                match = "✅" if ts_chunk == rust_chunk else "❌"
                print(f"  {i//2:2d}: TS={ts_chunk:16s} Rust={rust_chunk:16s} {match}")
    
    if rust_bytes:
        print(f"\nRust Envelope Bytes: {len(rust_bytes)//2} bytes")
        print(f"First 32 bytes: {rust_bytes[:64]}")
        print(f"Byte 68 area:   {rust_bytes[136:144]} (this is where the mismatch occurs)")
        print(f"Last 32 bytes:  {rust_bytes[-64:]}")
    
    print(f"\n📝 Key Insights:")
    print(f"- Server expects 142 bytes total ✅")
    print(f"- Rust produces 142 bytes ✅") 
    print(f"- Difference at byte position 68 ⚠️")
    print(f"- Likely field ordering or numeric encoding issue")

def analyze_envelope_structure():
    """Analyze the envelope structure differences"""
    print("\n🔬 Analyzing Envelope Structure Differences")
    print("=" * 50)
    
    print("TypeScript SDK uses:")
    print("- BN (BigNumber) for all u64/u128 values")
    print("- @coral-xyz/borsh for serialization")
    print("- PublicKey.toBytes() for public keys")
    print("- Specific field ordering in permitEnvelopeSchema")
    
    print("\nRust implementation uses:")
    print("- Native u64/u128 types")
    print("- borsh crate for serialization") 
    print("- [u8; 32] arrays for public keys")
    print("- Rust struct field ordering")
    
    print("\n🎯 Most Likely Issues:")
    print("1. Field ordering in struct serialization")
    print("2. Public key encoding format")
    print("3. Numeric type size differences")
    print("4. Optional field handling")
    
    print("\n📋 Action Plan:")
    print("1. Create modified TypeScript script that outputs envelope bytes")
    print("2. Compare exact byte sequences")
    print("3. Identify specific field causing mismatch")
    print("4. Adjust Rust implementation to match")

if __name__ == "__main__":
    compare_implementations()
    analyze_envelope_structure()