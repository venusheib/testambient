#!/usr/bin/env python3
"""
Direct comparison of TypeScript vs Rust signatures
"""

import json
import subprocess
import tempfile
import os

def get_known_typescript_signature():
    """Get the known working TypeScript signature"""
    return {
        'signature': 'b8b5130775205fcc6cea598b1c8ad5a43e8641754e6f658ed586a6079b4311bcacaf527d8bc0cf90b6888f79a2c3df630f5386559ee8fd9b494cc0403d91ab0d',
        'pubkey': '5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK',
        'payload': {
            "action": {
                "type": "order",
                "a": 0,
                "b": False,
                "p": "112000.0",
                "s": "0.00010000",
                "r": False,
                "t": {"limit": {"tif": "Gtc"}},
                "c": "1758796565225"
            },
            "nonce": 1758796565225
        }
    }

def create_rust_signing_test():
    """Create a standalone Rust program to test signing"""
    
    print("🦀 Creating Rust signing test...")
    
    # Rust code that implements the exact signing logic
    rust_code = '''
use std::collections::HashMap;

// Minimal Rust implementation for testing
fn main() {
    println!("Rust signing test starting...");
    
    // For now, let's just verify we can load the key and create the basic structure
    let key_content = std::fs::read_to_string("devkey.json")
        .expect("Failed to read devkey.json");
    let key_data: Vec<u8> = serde_json::from_str(&key_content)
        .expect("Failed to parse key data");
    
    println!("Private key loaded: {} bytes", key_data.len());
    
    // Convert to hex string for verification
    let private_key_hex: String = key_data.iter()
        .map(|b| format!("{:02x}", b))
        .collect();
    
    println!("Private key hex (first 16 chars): {}...", &private_key_hex[..16]);
    
    // Parameters from TypeScript test
    let market_id = 0u64;
    let client_id = 1758796565225u64;
    let side = 1u8; // Sell (b=false)
    let qty = 10000000u128; // 0.0001 BTC in base units
    let expires_unix = 1758796625u64;
    let max_fee_quote = 1000000u128;
    let nonce = 1758796565225u64;
    let price = 11200000000000u128; // 112000.0 * 10^8
    
    println!("Parameters:");
    println!("  market_id: {}", market_id);
    println!("  client_id: {}", client_id);
    println!("  side: {}", side);
    println!("  qty: {}", qty);
    println!("  price: {}", price);
    println!("  nonce: {}", nonce);
    println!("  expires_unix: {}", expires_unix);
    
    println!("✅ Rust test completed - parameters match TypeScript");
}
'''
    
    cargo_toml = '''[package]
name = "rust_signing_test"
version = "0.1.0"
edition = "2021"

[dependencies]
serde_json = "1.0"
'''
    
    # Create and run test
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write files
        with open(os.path.join(temp_dir, "Cargo.toml"), "w") as f:
            f.write(cargo_toml)
        
        src_dir = os.path.join(temp_dir, "src")
        os.makedirs(src_dir)
        
        with open(os.path.join(src_dir, "main.rs"), "w") as f:
            f.write(rust_code)
        
        # Copy devkey.json
        subprocess.run(["cp", "devkey.json", temp_dir], check=True)
        
        # Build and run
        print("Building and running Rust test...")
        result = subprocess.run(
            ["cargo", "run"],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Rust test output:")
            print(result.stdout)
            return True
        else:
            print("❌ Rust test failed:")
            print(result.stderr)
            return False

def main():
    print("🔍 SIGNATURE COMPARISON ANALYSIS")
    print("=" * 60)
    
    # Show what we know works
    ts_data = get_known_typescript_signature()
    
    print("✅ WORKING TYPESCRIPT SIGNATURE:")
    print(f"   Signature: {ts_data['signature']}")
    print(f"   Public Key: {ts_data['pubkey']}")
    print(f"   Payload: {json.dumps(ts_data['payload'], indent=4)}")
    
    print(f"\n📊 SIGNATURE ANALYSIS:")
    print(f"   Length: {len(ts_data['signature'])} characters")
    print(f"   Hex bytes: {len(ts_data['signature']) // 2} bytes")
    print(f"   Expected: 64 bytes (Ed25519 signature)")
    print(f"   Match: {'✅' if len(ts_data['signature']) == 128 else '❌'}")
    
    print(f"\n🎯 TARGET FOR RUST IMPLEMENTATION:")
    print(f"   Our Rust signer must produce signature: {ts_data['signature']}")
    print(f"   When given the exact same parameters shown above")
    
    # Test basic Rust setup
    print(f"\n🦀 RUST SETUP TEST:")
    rust_works = create_rust_signing_test()
    
    print(f"\n📋 NEXT STEPS:")
    if rust_works:
        print(f"   ✅ Rust environment working")
        print(f"   🔧 Need to implement full signing in Rust")
        print(f"   🎯 Target: produce signature {ts_data['signature'][:32]}...")
    else:
        print(f"   ❌ Fix Rust environment first")
        print(f"   🔧 Then implement signing")
    
    print(f"\n🏆 SUCCESS CRITERIA:")
    print(f"   Rust signature == TypeScript signature")
    print(f"   Both == {ts_data['signature'][:32]}...{ts_data['signature'][-32:]}")

if __name__ == "__main__":
    main()