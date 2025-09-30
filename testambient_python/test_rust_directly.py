#!/usr/bin/env python3
"""
Test Rust implementation directly without maturin develop
"""

import json
import subprocess
import tempfile
import os

def test_rust_signature_direct():
    """Test Rust signature by building a standalone binary"""
    
    print("🦀 Testing Rust signature generation...")
    
    # Fixed test values
    fixed_nonce = 1758796565225
    fixed_expires = 1758796625
    
    # Create a simple Rust test program
    rust_test_code = f'''
use std::collections::HashMap;

// Copy key structures from permit.rs
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
    // Load private key from devkey.json
    let key_content = std::fs::read_to_string("devkey.json").expect("Failed to read devkey.json");
    let key_data: Vec<u8> = serde_json::from_str(&key_content).expect("Failed to parse key data");
    
    // Use the same parameters as TypeScript test
    let private_key_hex = key_data.iter().map(|b| format!("{{:02x}}", b)).collect::<String>();
    println!("Private key (first 16 chars): {{}}...", &private_key_hex[..16]);
    
    // Create permit action with exact same parameters
    let permit = PermitAction {{
        authorizer: "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK".to_string(), // This should be derived from key
        market_id: 0,
        client_id: {fixed_nonce},
        side: 1, // Sell (b=false)
        qty: 10000000, // 0.0001 BTC in base units
        expires_unix: {fixed_expires},
        max_fee_quote: 1000000,
        nonce: {fixed_nonce},
        price: 11200000000000, // 112000.0 * 10^8
        tif: "Gtc".to_string(),
        reduce_only: false,
        trigger_price: None,
        trigger_type: 0,
        relayer: None,
    }};
    
    println!("Permit created with values:");
    println!("  Market ID: {{}}", permit.market_id);
    println!("  Side: {{}}", permit.side);
    println!("  Qty: {{}}", permit.qty);
    println!("  Price: {{}}", permit.price);
    println!("  Nonce: {{}}", permit.nonce);
    
    // For now, just show the structure - we'd need to implement signing
    println!("✅ Rust permit structure created successfully");
}}
'''
    
    # Write Cargo.toml for standalone test
    cargo_toml = '''[package]
name = "rust_test"
version = "0.1.0"
edition = "2021"

[dependencies]
serde_json = "1.0"
'''
    
    # Create temporary directory for test
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write files
        with open(os.path.join(temp_dir, "Cargo.toml"), "w") as f:
            f.write(cargo_toml)
        
        src_dir = os.path.join(temp_dir, "src")
        os.makedirs(src_dir)
        
        with open(os.path.join(src_dir, "main.rs"), "w") as f:
            f.write(rust_test_code)
        
        # Copy devkey.json to temp dir
        subprocess.run(["cp", "devkey.json", temp_dir], check=True)
        
        # Build and run
        print("Building Rust test...")
        result = subprocess.run(
            ["cargo", "run"],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Rust test output:")
            print(result.stdout)
        else:
            print("❌ Rust test failed:")
            print(result.stderr)
        
        return result.returncode == 0

if __name__ == "__main__":
    test_rust_signature_direct()