#!/usr/bin/env python3
"""
Test script to verify the Rust extension was built successfully
"""

import sys
import os
import subprocess
import json
import time

def test_wheel_build():
    """Test that the wheel was built successfully"""
    wheel_dir = "/Users/home/Desktop/testambient/testambient_python/ambient_signer/target/wheels"
    
    if os.path.exists(wheel_dir):
        wheels = [f for f in os.listdir(wheel_dir) if f.endswith('.whl')]
        if wheels:
            print(f"✅ Wheel built successfully: {wheels[0]}")
            wheel_path = os.path.join(wheel_dir, wheels[0])
            wheel_size = os.path.getsize(wheel_path)
            print(f"✅ Wheel size: {wheel_size:,} bytes")
            return wheel_path
        else:
            print("❌ No wheel files found")
    else:
        print("❌ Wheel directory not found")
    return None

def test_compilation():
    """Test that the Rust code compiles"""
    try:
        result = subprocess.run(
            ["cargo", "check"], 
            cwd="/Users/home/Desktop/testambient/testambient_python/ambient_signer",
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            print("✅ Rust code compiles successfully")
            return True
        else:
            print(f"❌ Compilation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running cargo check: {e}")
        return False

def read_devkey():
    """Read the private key for testing"""
    try:
        with open('devkey.json', 'r') as f:
            key_data = json.load(f)
        return ''.join(f'{b:02x}' for b in key_data)
    except Exception as e:
        print(f"❌ Error reading devkey: {e}")
        return None

def test_manual_import():
    """Try to manually test the import"""
    try:
        # This would fail since we can't install the wheel
        import ambient_signer
        print("✅ Module imported successfully")
        return True
    except ImportError as e:
        print(f"⚠️  Module import failed (expected): {e}")
        return False

def main():
    print("🧪 Testing Rust Signer Build")
    print("=" * 40)
    
    # Test compilation
    compilation_ok = test_compilation()
    
    # Test wheel build
    wheel_path = test_wheel_build()
    
    # Test parameters
    private_key = read_devkey()
    if private_key:
        print(f"✅ Private key loaded: {len(private_key)} hex chars")
    
    # Test manual import
    import_ok = test_manual_import()
    
    print("\n📋 Summary:")
    print(f"  Compilation: {'✅' if compilation_ok else '❌'}")
    print(f"  Wheel Build: {'✅' if wheel_path else '❌'}")
    print(f"  Private Key: {'✅' if private_key else '❌'}")
    print(f"  Module Import: {'⚠️  Expected to fail' if not import_ok else '✅'}")
    
    if compilation_ok and wheel_path and private_key:
        print("\n🎉 Rust Signer Successfully Built!")
        print("\n📦 Next Steps:")
        print("1. Set up a Python virtual environment")
        print("2. Install the wheel in the virtual environment")
        print("3. Test the actual signing functionality")
        
        print(f"\n💾 Wheel location: {wheel_path}")
        
        print("\n🔧 Sample usage (once installed):")
        print("""
import ambient_signer
import time

# Load signer
signer = ambient_signer.AmbientSigner.from_hex(private_key_hex)

# Sign order
signed = signer.sign_place_order(
    program_id="6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g",
    cluster="testnet",
    authorizer="5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
    market_id=64,
    client_id=int(time.time() * 1000),
    side=0,
    qty=10000,
    expires_unix=int(time.time()) + 3600,
    max_fee_quote=1000000,
    nonce=int(time.time() * 1000)
)

print(f"Signature: {signed.signature_hex}")
""")
    else:
        print("\n❌ Build verification failed")

if __name__ == "__main__":
    main()