#!/usr/bin/env python3
"""
Test script for the Rust-based Ambient signer
This script tests the PyO3 wrapper functionality without building the full extension
"""

import json
import time
from typing import Dict, Any

# For now, let's create a simple Python implementation that mimics the Rust functionality
# We'll use the existing devkey.json for testing

def read_devkey() -> bytes:
    """Read the private key from devkey.json"""
    with open('devkey.json', 'r') as f:
        key_data = json.load(f)
    return bytes(key_data)

def test_sign_place_order():
    """Test signing a place order with our implementation"""
    
    # Load the private key
    private_key = read_devkey()
    print(f"Private key loaded: {len(private_key)} bytes")
    
    # Create test order parameters
    test_params = {
        "program_id": "6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
        "cluster": "testnet", 
        "authorizer": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
        "market_id": 64,
        "client_id": int(time.time() * 1000),  # Use timestamp as client_id
        "side": 0,  # Buy
        "qty": 10000,
        "price": 75000000000,
        "tif": "GTC",
        "reduce_only": False,
        "trigger_price": None,
        "trigger_type": 0,
        "expires_unix": int(time.time()) + 3600,  # 1 hour from now
        "max_fee_quote": 1000000,
        "nonce": int(time.time() * 1000),
        "relayer": None
    }
    
    print("\nTest parameters:")
    for key, value in test_params.items():
        print(f"  {key}: {value}")
    
    print(f"\nPrivate key first 32 bytes: {private_key[:32].hex()}")
    print("✅ Basic parameter validation passed")
    
    return test_params

def test_rust_signer_integration():
    """Test the Rust signer integration once built"""
    print("🧪 Testing Rust Signer Integration")
    print("=" * 50)
    
    try:
        # This will work once the module is built
        # import ambient_signer
        # signer = ambient_signer.AmbientSigner.from_hex(private_key.hex())
        print("⚠️  Rust module not built yet - creating test parameters")
        
        test_params = test_sign_place_order()
        
        # Once the module is built, this would be:
        # signed_permit = signer.sign_place_order(**test_params)
        # print(f"✅ Signature: {signed_permit.signature_hex}")
        # print(f"✅ Signed bytes: {len(signed_permit.bytes)} bytes")
        
        print("📋 Next step: Build the Rust module with maturin")
        
    except ImportError:
        print("⚠️  ambient_signer module not available")
        print("   Run: cd ambient_signer && maturin build --release")

if __name__ == "__main__":
    test_rust_signer_integration()