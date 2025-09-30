#!/usr/bin/env python3
"""
Byte-by-byte comparison of TypeScript vs Rust envelope serialization
"""

import json
import time

def compare_envelope_bytes():
    """Compare the envelope bytes from both implementations"""
    
    # TypeScript envelope bytes from the debug output
    ts_hex = "53f1c7daafd01531f2020755f3cc03ff08549ca465a4ec33024c13bb04c69dc901013e685bda70d1e5c4cf8ee99d4a45fbd74c05786919803456651e124079d0a77800004000000000000000e5be8a979901000000000000000000000000e8764817000000010000c52ebca2b100020000000003800805db680000000040420f000000000000e5be8a9799010000"
    
    # Get Rust envelope bytes
    from ambient_signer import ambient_signer
    
    with open('devkey.json', 'r') as f:
        key_data = json.load(f)
    private_key_hex = ''.join(f'{b:02x}' for b in key_data)
    
    signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)
    
    # Sign with exact same parameters as TypeScript
    signed_permit = signer.sign_place_order(
        program_id="6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
        cluster="testnet",
        authorizer=signer.public_key,
        market_id=64,  # This should be 64, not 0!
        client_id=1759184076517,
        side=0,
        qty=100000000000,  # This should match TypeScript qty!
        expires_unix=1759184136,  # Use exact same expiry!
        max_fee_quote=1000000,
        nonce=1759184076517,
        price=50000000000000000,  # Use exact same price!
        tif="Gtc",
        reduce_only=False,
        trigger_price=None,
        trigger_type=0,
        relayer=None
    )
    
    rust_hex = signed_permit.bytes_hex
    
    print("🔍 Byte-by-Byte Comparison")
    print("=" * 70)
    print(f"TypeScript: {len(ts_hex)//2} bytes")
    print(f"Rust:       {len(rust_hex)//2} bytes")
    print()
    
    # Compare byte by byte
    ts_bytes = bytes.fromhex(ts_hex)
    rust_bytes = bytes.fromhex(rust_hex)
    
    min_len = min(len(ts_bytes), len(rust_bytes))
    first_diff = None
    
    print("Pos | TS   | Rust | Match | ASCII")
    print("-" * 40)
    
    for i in range(min_len):
        ts_byte = ts_bytes[i]
        rust_byte = rust_bytes[i]
        match = "✅" if ts_byte == rust_byte else "❌"
        
        if ts_byte != rust_byte and first_diff is None:
            first_diff = i
        
        ascii_ts = chr(ts_byte) if 32 <= ts_byte <= 126 else '.'
        ascii_rust = chr(rust_byte) if 32 <= rust_byte <= 126 else '.'
        
        if i < 20 or (first_diff and abs(i - first_diff) <= 10) or i >= min_len - 10:
            print(f"{i:3d} | {ts_byte:02x}   | {rust_byte:02x}   | {match}  | {ascii_ts}{ascii_rust}")
        elif i == 20 and first_diff and first_diff > 30:
            print("... (identical bytes skipped)")
    
    if len(ts_bytes) != len(rust_bytes):
        print(f"\n⚠️  Length difference: TS={len(ts_bytes)}, Rust={len(rust_bytes)}")
    
    if first_diff is not None:
        print(f"\n🎯 First difference at byte {first_diff}")
        print(f"   TypeScript: 0x{ts_bytes[first_diff]:02x}")
        print(f"   Rust:       0x{rust_bytes[first_diff]:02x}")
        
        # Show context around the difference
        start = max(0, first_diff - 4)
        end = min(len(ts_bytes), first_diff + 5)
        
        print(f"\n📍 Context around byte {first_diff}:")
        ts_context = ts_hex[start*2:end*2]
        rust_context = rust_hex[start*2:end*2]
        print(f"   TS:   {ts_context}")
        print(f"   Rust: {rust_context}")
        
        # Mark the difference
        diff_pos = (first_diff - start) * 2
        marker = " " * diff_pos + "^^"
        print(f"         {marker}")
    else:
        print("\n✅ All bytes match perfectly!")
    
    print(f"\n🔐 Signature Comparison:")
    ts_signature = "127d5fc61a595fd145fd9ff4b1a5e617ebef82d5f9e036b67aed5fe359b5dc474476ff6043b473e0d3d5a75320f2b9b87da37546a01d71e854013ed15fff9809"
    rust_signature = signed_permit.signature_hex
    
    print(f"TypeScript: {ts_signature}")
    print(f"Rust:       {rust_signature}")
    print(f"Match:      {'✅' if ts_signature == rust_signature else '❌'}")

if __name__ == "__main__":
    compare_envelope_bytes()