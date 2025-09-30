#!/usr/bin/env python3
"""
Create a standalone Rust test that can generate the signature
without relying on PyO3 installation issues
"""

import subprocess
import tempfile
import os
import json

def create_standalone_rust_test():
    """Create a standalone Rust binary to test our signing logic"""
    
    print("🦀 Creating standalone Rust signature test...")
    
    # Our target parameters
    target_nonce = 1759220000000
    target_expires = 1759220060
    
    # Create a standalone Rust program
    rust_code = f'''
use serde_json;
use std::fs;

// Copy the exact same structures from our ambient_signer
#[derive(Debug)]
pub struct PermitEnvelopeV1 {{
    pub program_id: String,
    pub cluster: String,
    pub permit: PermitAction,
    pub signature: [u8; 64],
}}

#[derive(Debug)]
pub struct PermitAction {{
    pub authorizer: String,
    pub market_id: u64,
    pub client_id: u64,
    pub side: u8,
    pub qty: u128,
    pub expires_unix: u64,
    pub max_fee_quote: u128,
    pub nonce: u64,
    pub price: u128,
    pub tif: String,
    pub reduce_only: bool,
    pub trigger_price: Option<u128>,
    pub trigger_type: u8,
    pub relayer: Option<String>,
}}

fn main() {{
    println!("🦀 Standalone Rust Signature Test");
    println!("================================");
    
    // Load private key
    let key_content = fs::read_to_string("devkey.json")
        .expect("Failed to read devkey.json");
    let key_data: Vec<u8> = serde_json::from_str(&key_content)
        .expect("Failed to parse key data");
    
    let private_key_hex: String = key_data.iter()
        .map(|b| format!("{{:02x}}", b))
        .collect();
    
    println!("✅ Private key loaded: {{}} bytes", key_data.len());
    println!("   Hex (first 16): {{}}...", &private_key_hex[..16]);
    
    // Create permit action with EXACT same parameters as TypeScript
    let permit = PermitAction {{
        authorizer: "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK".to_string(),
        market_id: 0,
        client_id: {target_nonce},
        side: 0,  // Buy (b=true → side=0)
        qty: 5000000,  // 0.00005000 * 10^8
        expires_unix: {target_expires},
        max_fee_quote: 1000000,
        nonce: {target_nonce},
        price: 10500000000000,  // 105000.0 * 10^8
        tif: "Gtc".to_string(),
        reduce_only: false,
        trigger_price: None,
        trigger_type: 0,
        relayer: None,
    }};
    
    println!("\\n📋 Permit Parameters:");
    println!("   Market ID: {{}}", permit.market_id);
    println!("   Client ID: {{}}", permit.client_id);
    println!("   Side: {{}}", permit.side);
    println!("   Qty: {{}}", permit.qty);
    println!("   Price: {{}}", permit.price);
    println!("   Nonce: {{}}", permit.nonce);
    println!("   Expires: {{}}", permit.expires_unix);
    
    // For now, show that we can create the structure
    // Next step would be to implement the actual signing
    println!("\\n✅ Permit structure created successfully");
    println!("\\n🎯 Target signature to match:");
    println!("   6ac91350a226f5c68bd2e2ae83f665943919f700ded5f1e554f240640fa8cb20849f1424e58c194013ce8a2817958f0ac453ac9e999e23513edcb8465a25630a");
    
    println!("\\n🔧 Next steps:");
    println!("   1. Add ed25519 and borsh dependencies");
    println!("   2. Implement permit serialization");
    println!("   3. Generate signature");
    println!("   4. Compare with target");
}}
'''
    
    # Cargo.toml for the standalone test
    cargo_toml = '''[package]
name = "ambient_signature_test"
version = "0.1.0"
edition = "2021"

[dependencies]
serde_json = "1.0"
'''
    
    # Create temporary directory and test
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"   Created temp directory: {temp_dir}")
        
        # Write Cargo.toml
        with open(os.path.join(temp_dir, "Cargo.toml"), "w") as f:
            f.write(cargo_toml)
        
        # Create src directory
        src_dir = os.path.join(temp_dir, "src")
        os.makedirs(src_dir)
        
        # Write main.rs
        with open(os.path.join(src_dir, "main.rs"), "w") as f:
            f.write(rust_code)
        
        # Copy devkey.json
        subprocess.run(["cp", "devkey.json", temp_dir], check=True)
        
        # Build and run
        print(f"   Building and running Rust test...")
        result = subprocess.run(
            ["cargo", "run"],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )
        
        print(f"\\n📤 RUST OUTPUT:")
        print(result.stdout)
        
        if result.stderr:
            print(f"\\n⚠️ RUST STDERR:")
            print(result.stderr)
        
        return result.returncode == 0

def show_comparison_summary():
    """Show what we know so far"""
    
    print(f"\\n📊 SIGNATURE COMPARISON SUMMARY")
    print(f"=" * 60)
    
    print(f"✅ WORKING TYPESCRIPT SIGNATURE:")
    print(f"   Signature: 6ac91350a226f5c68bd2e2ae83f665943919f700ded5f1e554f240640fa8cb20849f1424e58c194013ce8a2817958f0ac453ac9e999e23513edcb8465a25630a")
    print(f"   Public Key: 5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK")
    print(f"   Nonce: 1759220000000")
    print(f"   API Status: ✅ ACCEPTED (TX: 2TaScY9YRWHo8YykmCDjJrQBZRYyqJLH57qZdbRKb9DnJZ5cLJFtDkyFoWHNxpbU2H2wL17TzDH3Br7xayAz76jv)")
    
    print(f"\\n🔧 RUST IMPLEMENTATION STATUS:")
    print(f"   PyO3 Module: ❌ Installation issues")
    print(f"   Standalone Test: 🔄 In progress")
    print(f"   Core Logic: ✅ Ready to implement")
    
    print(f"\\n🎯 NEXT STEPS:")
    print(f"   1. Fix Rust signing implementation")
    print(f"   2. Generate signature for exact same parameters")
    print(f"   3. Compare byte-by-byte with TypeScript")
    print(f"   4. Debug any serialization differences")
    
    print(f"\\n🏆 SUCCESS CRITERIA:")
    print(f"   Rust signature == TypeScript signature")
    print(f"   Both must equal: 6ac91350a226f5c68bd2e2ae83f665943919f700ded5f1e554f240640fa8cb20...")

if __name__ == "__main__":
    print(f"🔬 RUST SIGNATURE DEBUGGING")
    print(f"=" * 50)
    
    success = create_standalone_rust_test()
    
    show_comparison_summary()
    
    if success:
        print(f"\\n✅ Rust environment working - ready for signing implementation")
    else:
        print(f"\\n❌ Rust environment needs fixing")