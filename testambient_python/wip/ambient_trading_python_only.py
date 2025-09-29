#!/usr/bin/env python3
"""
Ambient Trading Client - Pure Python Implementation

Python-only implementation that handles permit signing without the SDK.
Implements Borsh serialization and Ed25519 signing for Ambient protocol.
"""

import json
import time
import struct
import hashlib
import requests
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
from solders.keypair import Keypair
from solders.pubkey import Pubkey
import borsh_construct as borsh
from construct import Container

# API Configuration
AMBIENT_URL = "https://embindexer.net/ember/api/dev/v1"

# Permit Constants
class ClusterType:
    MAINNET = 0
    TESTNET = 1
    DEVNET = 2
    LOCALNET = 3

class PermitActionType:
    PLACE = 0
    CANCEL_BY_ID = 1
    CANCEL_BY_CLIENT_ID = 2
    CANCEL_ALL = 3
    MODIFY = 4
    WITHDRAW = 5
    SET_LEVERAGE = 6
    NOOP = 7
    FAUCET = 8

class TimeInForceCode:
    IOC = 0
    FOK = 1
    GTC = 2
    ALO = 3
    GTT = 4

class ReplayModeType:
    SEQUENCE = 0
    NONCE = 1
    ALLOWANCE = 2
    HL_WINDOW = 3

@dataclass 
class OrderParams:
    """Order parameters for placing trades"""
    asset_index: int  # Universe index (0 for BTC)
    is_buy: bool
    price: str
    size: str
    reduce_only: bool = False
    time_in_force: str = "Gtc"  # "Alo", "Ioc", "Gtc"
    cloid: Optional[str] = None

class AmbientPythonTrader:
    """
    Pure Python Ambient trading client with permit signing
    """
    
    def __init__(self, keypair_file: str = "devkey.json"):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        
        # Load keypair from file
        with open(keypair_file, 'r') as f:
            keypair_bytes = json.load(f)
        
        # Convert list to bytes and create Keypair
        keypair_array = bytes(keypair_bytes)
        self.keypair = Keypair.from_bytes(keypair_array)
        self.pubkey = str(self.keypair.pubkey())
        
        # Program ID for Ambient on testnet
        self.program_id = Pubkey.from_string("6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g")
        
        print(f"🔑 Initialized Python-only trader with pubkey: {self.pubkey}")
    
    def _create_permit_domain(self):
        """Create permit domain structure"""
        return {
            "programId": bytes(self.program_id),
            "cluster": ClusterType.TESTNET,
            "version": 1
        }
    
    def _create_replay_mode(self, nonce: int):
        """Create HL window replay mode"""
        return {
            "type": ReplayModeType.HL_WINDOW,
            "k": 60  # 60 second window
        }
    
    def _create_place_action(self, order_params: OrderParams, market_id: int = 64):
        """Create place order permit action"""
        # Convert price and size to appropriate format
        # For BTC: szDecimals=8, so size needs to be in base units
        size_base_units = int(float(order_params.size) * 10**8)  # 8 decimals for BTC
        price_base_units = int(float(order_params.price) * 10**6)  # 6 decimals for quote (USDC)
        
        # Generate client ID if not provided
        client_id = int(order_params.cloid) if order_params.cloid else int(time.time() * 1000)
        
        # Map time in force
        tif_map = {
            "Ioc": TimeInForceCode.IOC,
            "Gtc": TimeInForceCode.GTC, 
            "Alo": TimeInForceCode.ALO
        }
        tif_code = tif_map.get(order_params.time_in_force, TimeInForceCode.GTC)
        
        return {
            "type": PermitActionType.PLACE,
            "marketId": market_id,
            "clientId": client_id,
            "side": 0 if order_params.is_buy else 1,  # 0 = Bid, 1 = Ask
            "qty": size_base_units,
            "price": price_base_units,
            "tif": {"type": tif_code},
            "reduceOnly": order_params.reduce_only,
            "triggerPrice": None,
            "triggerType": 0,
            "healthFloor": None
        }
    
    def _create_cancel_action(self, asset_index: int, order_id: int, market_id: int = 64):
        """Create cancel order permit action"""
        return {
            "type": PermitActionType.CANCEL_BY_ID,
            "marketId": market_id,
            "orderId": order_id
        }
    
    def _create_faucet_action(self, amount: float, market_id: int = 0):
        """Create faucet permit action"""
        # Convert amount to base units (6 decimals for USDC)
        amount_base_units = int(amount * 10**6)
        
        return {
            "type": PermitActionType.FAUCET,
            "marketId": market_id,
            "amount": amount_base_units,
            "recipient": bytes(self.keypair.pubkey())
        }
    
    def _create_permit_envelope(self, action: Dict[str, Any], nonce: int):
        """Create complete permit envelope"""
        expires_unix = int(time.time()) + 60  # 60 seconds from now
        
        return {
            "domain": self._create_permit_domain(),
            "authorizer": bytes(self.keypair.pubkey()),
            "keyType": 0,  # Ed25519
            "action": action,
            "mode": self._create_replay_mode(nonce),
            "expiresUnix": expires_unix,
            "maxFeeQuote": 1000000,  # 1 USDC max fee
            "relayer": None,
            "nonce": nonce
        }
    
    def _serialize_permit_envelope(self, envelope: Dict[str, Any]) -> bytes:
        """
        Serialize permit envelope using Borsh
        This is a simplified version - full implementation would need complete Borsh schemas
        """
        # For now, use a simplified JSON-based approach for testing
        # In production, this would need proper Borsh serialization matching the TypeScript schema
        
        # Create a deterministic serialization
        serializable = {
            "domain": {
                "programId": envelope["domain"]["programId"].hex(),
                "cluster": envelope["domain"]["cluster"],
                "version": envelope["domain"]["version"]
            },
            "authorizer": envelope["authorizer"].hex(),
            "keyType": envelope["keyType"],
            "action": envelope["action"],
            "mode": envelope["mode"],
            "expiresUnix": envelope["expiresUnix"],
            "maxFeeQuote": envelope["maxFeeQuote"],
            "nonce": envelope["nonce"]
        }
        
        # Convert to JSON bytes (deterministic ordering)
        json_str = json.dumps(serializable, separators=(',', ':'), sort_keys=True)
        return json_str.encode('utf-8')
    
    def _sign_permit_envelope(self, envelope: Dict[str, Any]) -> str:
        """Sign permit envelope and return hex signature"""
        # Serialize envelope
        message_bytes = self._serialize_permit_envelope(envelope)
        
        # Sign with keypair
        signature = self.keypair.sign_message(message_bytes)
        
        # Convert to hex string
        return bytes(signature).hex()
    
    def _create_signed_payload(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Create a fully signed payload for the exchange endpoint"""
        nonce = int(time.time() * 1000)
        
        # Create permit envelope
        envelope = self._create_permit_envelope(action, nonce)
        
        # Sign envelope
        signature_hex = self._sign_permit_envelope(envelope)
        
        # The API payload needs to match the original action format
        # This is where we bridge between permits (internal) and API format (external)
        return {
            "action": self._convert_action_to_api_format(action),
            "nonce": nonce,
            "signature": [signature_hex],
            "pubkey": self.pubkey
        }
    
    def _convert_action_to_api_format(self, permit_action: Dict[str, Any]) -> Dict[str, Any]:
        """Convert internal permit action to API format"""
        action_type = permit_action["type"]
        
        if action_type == PermitActionType.PLACE:
            # Convert back from base units to decimal strings
            qty_decimal = permit_action["qty"] / 10**8  # BTC has 8 decimals
            price_decimal = permit_action["price"] / 10**6  # USDC has 6 decimals
            
            # Map TIF back
            tif_map = {
                TimeInForceCode.IOC: "Ioc",
                TimeInForceCode.GTC: "Gtc", 
                TimeInForceCode.ALO: "Alo"
            }
            tif_str = tif_map.get(permit_action["tif"]["type"], "Gtc")
            
            return {
                "type": "order",
                "a": 0,  # Asset universe index (BTC)
                "b": permit_action["side"] == 0,  # Convert side: 0=buy, 1=sell
                "p": f"{price_decimal:.1f}",
                "s": f"{qty_decimal:.8f}",
                "r": permit_action["reduceOnly"],
                "t": {"limit": {"tif": tif_str}},
                "c": str(permit_action["clientId"])
            }
        
        elif action_type == PermitActionType.CANCEL_BY_ID:
            return {
                "type": "cancel",
                "cancels": [{
                    "a": 0,  # Asset universe index
                    "o": permit_action["orderId"]
                }]
            }
        
        elif action_type == PermitActionType.FAUCET:
            amount_decimal = permit_action["amount"] / 10**6  # USDC decimals
            return {
                "type": "faucet",
                "amount": str(amount_decimal),
                "marketId": permit_action["marketId"]
            }
        
        else:
            raise ValueError(f"Unsupported action type: {action_type}")
    
    def _make_exchange_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send signed payload to exchange endpoint"""
        print(f"🚀 Making Python-signed exchange request:")
        print(f"   Action: {payload['action']['type']}")
        print(f"   Nonce: {payload['nonce']}")
        print(f"   Pubkey: {payload['pubkey']}")
        print(f"   Signature: {payload['signature'][0][:20]}...")
        
        try:
            response = self.session.post(f"{AMBIENT_URL}/exchange", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Exchange request failed: {e}")
            if hasattr(e, 'response'):
                print(f"Response: {e.response.text}")
            raise
    
    def place_order(self, order_params: OrderParams) -> Dict[str, Any]:
        """Place a limit order using pure Python signing"""
        # Create permit action
        permit_action = self._create_place_action(order_params)
        
        # Create signed payload
        payload = self._create_signed_payload(permit_action)
        
        print(f"📋 Placing order (Python-only signing):")
        print(f"   Asset Index: {order_params.asset_index}")
        print(f"   Side: {'BUY' if order_params.is_buy else 'SELL'}")
        print(f"   Price: {order_params.price}")
        print(f"   Size: {order_params.size}")
        print(f"   TIF: {order_params.time_in_force}")
        
        return self._make_exchange_request(payload)
    
    def cancel_order(self, asset_index: int, order_id: int) -> Dict[str, Any]:
        """Cancel order using pure Python signing"""
        # Create permit action
        permit_action = self._create_cancel_action(asset_index, order_id)
        
        # Create signed payload  
        payload = self._create_signed_payload(permit_action)
        
        print(f"❌ Cancelling order (Python-only signing):")
        print(f"   Asset Index: {asset_index}")
        print(f"   Order ID: {order_id}")
        
        return self._make_exchange_request(payload)
    
    def request_faucet(self, amount: float, market_id: int = 0) -> Dict[str, Any]:
        """Request faucet using pure Python signing"""
        # Create permit action
        permit_action = self._create_faucet_action(amount, market_id)
        
        # Create signed payload
        payload = self._create_signed_payload(permit_action)
        
        print(f"💰 Requesting faucet (Python-only signing):")
        print(f"   Amount: {amount}")
        print(f"   Market ID: {market_id}")
        
        return self._make_exchange_request(payload)


def demo_python_trading():
    """Demonstrate pure Python trading functionality"""
    print("🐍 Ambient Trading Demo (Pure Python Signing)")
    print("=" * 70)
    
    # Initialize trader
    trader = AmbientPythonTrader()
    
    # Test 1: Place a limit order
    print("\n📋 Step 1: Place limit buy order (Python signing)")
    order_params = OrderParams(
        asset_index=0,      # BTC universe index
        is_buy=True,        # Buy order
        price="111000.0",   # Below market
        size="0.00010000",  # Standard size format
        reduce_only=False,
        time_in_force="Gtc"
    )
    
    try:
        order_response = trader.place_order(order_params)
        print(f"✅ Order response: {order_response}")
        
        # Check if order was successful
        if (order_response.get("status") == "ok" and 
            "response" in order_response and 
            "data" in order_response["response"]):
            oid = order_response["response"]["data"].get("oid")
            cloid = order_response["response"]["data"].get("cloid")
            tx = order_response["response"].get("tx")
            print(f"🎉 Order placed successfully!")
            print(f"   OID: {oid}")
            print(f"   CLOID: {cloid}")
            print(f"   TX: {tx}")
        else:
            print(f"⚠️ Order response: {order_response}")
            
    except Exception as e:
        print(f"❌ Order placement failed: {e}")
    
    print("\n🎉 Python-only demo completed!")


if __name__ == "__main__":
    # Install required dependency first:
    # pip install borsh-construct
    demo_python_trading()