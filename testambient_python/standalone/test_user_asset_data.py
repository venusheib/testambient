#!/usr/bin/env python3
"""
Query User's Active Asset Data

Retrieves user's active asset data for a specific coin from the Ambient API.
"""

import json
import requests
import subprocess
from typing import Dict, Any

# API Configuration
AMBIENT_URL = "https://embindexer.net/ember/api/dev/v1"
SDK_PATH = "./ambient-ember-sdk"
DEVKEY_PATH = f"{SDK_PATH}/devkey.json"


class AmbientInfoClient:
    """Client for querying Ambient API info endpoints"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        
        # Get public key from devkey
        self.pubkey = self._get_pubkey_from_devkey()
        print(f"🔑 Using pubkey: {self.pubkey}")
    
    def _get_pubkey_from_devkey(self) -> str:
        """Extract public key from devkey.json using SDK"""
        try:
            result = subprocess.run([
                'node',
                '-e',
                f'''
                const fs = require('fs');
                const bs58 = require('bs58');
                const nacl = require('tweetnacl');
                
                const keyData = JSON.parse(fs.readFileSync('{DEVKEY_PATH}', 'utf8'));
                const keypair = nacl.sign.keyPair.fromSeed(new Uint8Array(keyData));
                const pubkey = bs58.encode(keypair.publicKey);
                console.log(pubkey);
                '''
            ], capture_output=True, text=True, cwd=SDK_PATH)
            
            if result.returncode != 0:
                raise RuntimeError(f"Failed to extract pubkey: {result.stderr}")
            
            return result.stdout.strip()
            
        except Exception as e:
            # Fallback to hardcoded pubkey if extraction fails
            print(f"⚠️ Could not extract pubkey from devkey: {e}")
            return "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
    
    def get_user_asset_data(self, coin: str = "BTC") -> Dict[str, Any]:
        """
        Retrieve user's active asset data for a specific coin
        
        Args:
            coin: Asset symbol (e.g., "BTC")
            
        Returns:
            User's asset data including leverage, balance, etc.
        """
        payload = {
            "type": "userAssetData",
            "user": self.pubkey,
            "coin": coin
        }
        
        print(f"📊 Querying user asset data:")
        print(f"   User: {self.pubkey}")
        print(f"   Coin: {coin}")
        
        try:
            response = self.session.post(f"{AMBIENT_URL}/info", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ User asset data query failed: {e}")
            if hasattr(e, 'response'):
                print(f"Response: {e.response.text}")
            raise


def demo_user_asset_data():
    """Demonstrate user asset data querying"""
    print("📈 User Asset Data Query Demo")
    print("=" * 50)
    
    client = AmbientInfoClient()
    
    try:
        # Query BTC asset data
        print("\n1. Querying BTC asset data...")
        btc_data = client.get_user_asset_data("BTC")
        
        print("\n✅ BTC Asset Data:")
        print(json.dumps(btc_data, indent=2))
        
        # Parse and display key information
        if isinstance(btc_data, dict):
            print(f"\n📋 Summary:")
            print(f"   Coin: {btc_data.get('coin', 'N/A')}")
            print(f"   User: {btc_data.get('user', 'N/A')}")
            print(f"   Mark Price: ${btc_data.get('markPx', 'N/A')}")
            
            leverage = btc_data.get('leverage', {})
            if leverage:
                print(f"   Leverage: {leverage.get('value', 'N/A')}x ({leverage.get('type', 'N/A')})")
            
            available = btc_data.get('availableToTrade', [])
            if available and len(available) >= 2:
                print(f"   Available to Trade: Buy={available[0]}, Sell={available[1]}")
            
            max_sizes = btc_data.get('maxTradeSzs', [])
            if max_sizes and len(max_sizes) >= 2:
                print(f"   Max Trade Sizes: Buy={max_sizes[0]}, Sell={max_sizes[1]}")
        
        # Try other coins if they exist
        print(f"\n2. Trying other potential coins...")
        for coin in ["ETH", "SOL"]:
            try:
                print(f"\n   Querying {coin} asset data...")
                coin_data = client.get_user_asset_data(coin)
                print(f"   ✅ {coin} data found:")
                print(f"      Mark Price: ${coin_data.get('markPx', 'N/A')}")
                leverage = coin_data.get('leverage', {})
                if leverage:
                    print(f"      Leverage: {leverage.get('value', 'N/A')}x ({leverage.get('type', 'N/A')})")
            except Exception as e:
                print(f"   ⚠️ {coin} data not available: {e}")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    demo_user_asset_data()