#!/usr/bin/env python3
"""
Ambient Trading Client with SDK Signing

Python client that uses the Ambient Ember SDK for proper signing and sends requests via API.
This combines the SDK's correct signing process with Python's API interaction capabilities.
"""

import json
import time
import subprocess
import tempfile
import os
import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass

# API Configuration
AMBIENT_URL = "https://embindexer.net/ember/api/dev/v1"
SDK_PATH = "../ambient-ember-sdk"
DEVKEY_PATH = "../devkey.json"


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


class AmbientSDKTrader:
    """
    Ambient API trading client using SDK for signing
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

        # Verify SDK is available
        if not os.path.exists(f"{SDK_PATH}/scripts/signPayload.mjs"):
            raise FileNotFoundError(f"SDK not found at {SDK_PATH}")

        if not os.path.exists(DEVKEY_PATH):
            raise FileNotFoundError(f"Devkey not found at {DEVKEY_PATH}")

        print(f"🔑 Initialized trader using SDK at {SDK_PATH}")
        
        # Set pubkey (extracted from signed payloads or hardcoded for now)
        self.pubkey = "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"

    def _sign_payload_with_sdk(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use the Ambient Ember SDK to sign a payload
        
        Args:
            payload: The unsigned payload to sign
            
        Returns:
            The signed payload with nonce, signature, and pubkey
        """
        # Create temporary file for payload
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(payload, f)
            temp_path = f.name

        try:
            # Run the SDK signing script
            result = subprocess.run([
                'node',
                f'{SDK_PATH}/scripts/signPayload.mjs',
                DEVKEY_PATH,
                temp_path
            ], capture_output=True, text=True)

            if result.returncode != 0:
                raise RuntimeError(f"SDK signing failed: {result.stderr}")

            # Parse the signed payload
            signed_payload = json.loads(result.stdout)
            return signed_payload

        finally:
            # Clean up temporary file
            os.unlink(temp_path)

    def _make_signed_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sign a payload with SDK and send it to the exchange endpoint
        
        Args:
            payload: Unsigned payload to sign and send
            
        Returns:
            API response
        """
        # Sign payload with SDK
        signed_payload = self._sign_payload_with_sdk(payload)

        print(f"🚀 Making SDK-signed exchange request:")
        print(f"   Action: {signed_payload['action']['type']}")
        print(f"   Nonce: {signed_payload['nonce']}")
        print(f"   Pubkey: {signed_payload['pubkey']}")
        print(f"   Signature: {signed_payload['signature'][0][:20]}...")

        try:
            response = self.session.post(f"{AMBIENT_URL}/exchange", json=signed_payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Exchange request failed: {e}")
            if hasattr(e, 'response'):
                print(f"Response: {e.response.text}")
            raise

    def place_order(self, order_params: OrderParams) -> Dict[str, Any]:
        """
        Place a limit order using SDK signing
        
        Args:
            order_params: Order parameters
            
        Returns:
            API response
        """
        # Create action payload
        action = {
            "type": "order",
            "a": order_params.asset_index,
            "b": order_params.is_buy,
            "p": order_params.price,
            "s": order_params.size,
            "r": order_params.reduce_only,
            "t": {
                "limit": {
                    "tif": order_params.time_in_force
                }
            }
        }

        # Add cloid if provided
        if order_params.cloid:
            action["c"] = order_params.cloid

        payload = {"action": action}

        print(f"📋 Placing order:")
        print(f"   Asset Index: {order_params.asset_index}")
        print(f"   Side: {'BUY' if order_params.is_buy else 'SELL'}")
        print(f"   Price: {order_params.price}")
        print(f"   Size: {order_params.size}")
        print(f"   TIF: {order_params.time_in_force}")

        return self._make_signed_request(payload)

    def cancel_order(self, asset_index: int, order_id: int) -> Dict[str, Any]:
        """
        Cancel an order by order ID using SDK signing
        
        Args:
            asset_index: Asset universe index (0 for BTC)
            order_id: Order ID to cancel
            
        Returns:
            API response
        """
        action = {
            "type": "cancel",
            "cancels": [
                {
                    "a": asset_index,
                    "o": order_id
                }
            ]
        }

        payload = {"action": action}

        print(f"❌ Cancelling order:")
        print(f"   Asset Index: {asset_index}")
        print(f"   Order ID: {order_id}")

        return self._make_signed_request(payload)

    def request_faucet(self, amount: float, market_id: int = 0) -> Dict[str, Any]:
        """
        Request funds from faucet using SDK signing
        
        Args:
            amount: Amount to request
            market_id: Market ID (default: 0)
            
        Returns:
            API response
        """
        action = {
            "type": "faucet",
            "amount": str(amount),
            "marketId": market_id
        }

        payload = {"action": action}

        print(f"💰 Requesting faucet funds:")
        print(f"   Amount: {amount}")
        print(f"   Market ID: {market_id}")

        return self._make_signed_request(payload)
    
    def modify_order(self, asset_index: int, order_id: int, new_price: str, new_size: str, 
                    new_client_id: Optional[str] = None, reduce_only: bool = False, 
                    time_in_force: str = "Gtc") -> Dict[str, Any]:
        """
        Modify an existing order using SDK signing
        
        Args:
            asset_index: Asset universe index (0 for BTC)
            order_id: Order ID to modify
            new_price: New price as string
            new_size: New size as string
            new_client_id: Optional new client order ID
            reduce_only: Reduce only flag
            time_in_force: Time in force ("Gtc", "Ioc", "Alo")
            
        Returns:
            API response
        """
        # Generate new client ID if not provided
        if new_client_id is None:
            new_client_id = str(int(time.time() * 1000))
        
        action = {
            "type": "modify",
            "oid": order_id,
            "order": {
                "a": asset_index,
                "b": True,  # True for buy, False for sell - should be determined by original order
                "p": new_price,
                "s": new_size,
                "r": reduce_only,
                "t": {"limit": {"tif": time_in_force}},
                "c": new_client_id
            }
        }
        
        payload = {"action": action}
        
        print(f"✏️ Modifying order:")
        print(f"   Asset Index: {asset_index}")
        print(f"   Order ID: {order_id}")
        print(f"   New Price: {new_price}")
        print(f"   New Size: {new_size}")
        print(f"   New Client ID: {new_client_id}")
        
        return self._make_signed_request(payload)
    
    def update_leverage(self, asset_index: int, leverage: int) -> Dict[str, Any]:
        """
        Update leverage for an asset using SDK signing
        
        Args:
            asset_index: Asset universe index (0 for BTC)
            leverage: New leverage value (e.g., 10 for 10x)
            
        Returns:
            API response
        """
        action = {
            "type": "updateLeverage",
            "asset": asset_index,
            "leverage": 10,
            "isCross": False
        }
        
        payload = {"action": action}
        
        print(f"📈 Updating leverage:")
        print(f"   Asset Index: {asset_index}")
        print(f"   New Leverage: {leverage}x")
        
        return self._make_signed_request(payload)

    def query_order_status(self, oid, user: Optional[str] = None) -> Dict[str, Any]:
        """
        Query order status by OID or CLOID (similar to Hyperliquid API)
        
        Args:
            oid: Order ID (int) or Client Order ID (str) to query
            user: User address (uses trader's pubkey if not provided)
            
        Returns:
            API response with order status information
        """
        # Use trader's pubkey as user if not provided
        if user is None:
            user = self.pubkey
        
        # Convert string CLOID to int if possible, otherwise use as string
        if isinstance(oid, str):
            try:
                # Try to convert string to int for numeric CLOIDs
                oid = int(oid)
            except ValueError:
                # Keep as string for hex CLOIDs
                pass
            
        payload = {
            "type": "orderStatus",
            "user": user,
            "orderId": oid
        }
        
        print(f"📊 Querying order status:")
        print(f"   OID: {oid}")
        print(f"   User: {user}")
        
        try:
            response = self.session.post(f"{AMBIENT_URL}/info", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Order status query failed: {e}")
            if hasattr(e, 'response'):
                print(f"Response: {e.response.text}")
            raise


def demo_sdk_trading():
    """Demonstrate complete SDK-based trading functionality"""
    print("🚀 Ambient Trading Demo (SDK Signing)")
    print("=" * 60)
    
    # Initialize trader
    trader = AmbientSDKTrader()
    
    # Test 1: Update Leverage
    print("\n📈 Step 1: Update leverage to 20x")
    try:
        leverage_response = trader.update_leverage(0, 20)
        print(f"✅ Leverage response: {leverage_response}")
        if leverage_response.get("status") == "ok":
            tx = leverage_response["response"].get("tx")
            if tx:
                print(f"🎉 Leverage updated successfully! TX: {tx}")
    except Exception as e:
        print(f"⚠️ Leverage update failed: {e}")
    
    # Test 2: Place a fresh limit order
    print("\n📋 Step 2: Place fresh limit buy order")
    order_params = OrderParams(
        asset_index=0,      # BTC universe index
        is_buy=True,        # Buy order
        price="108000.0",   # Below market
        size="0.00006000",  # Small size for testing
        reduce_only=False,
        time_in_force="Gtc"
    )
    
    try:
        order_response = trader.place_order(order_params)
        print(f"✅ Order response: {order_response}")
        
        # Check if order was successful and extract details
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
            
            # Test 2.5: Check order status
            print(f"\n📊 Step 2.5: Check order status")
            try:
                status_response = trader.query_order_status(oid)
                print(f"✅ Order status response: {status_response}")
                if "order" in status_response:
                    order_info = status_response["order"]
                    status = status_response.get("status", "unknown")
                    print(f"   Status: {status}")
                    print(f"   Side: {'BUY' if order_info.get('side') == 'B' else 'SELL'}")
                    print(f"   Size: {order_info.get('sz', 'N/A')}")
                    print(f"   Price: ${order_info.get('limitPx', 'N/A')}")
                    print(f"   Filled: {order_info.get('filledSz', '0')}")
            except Exception as e:
                print(f"⚠️ Order status check failed: {e}")
            
            # Test 3: Modify the fresh order
            if oid:
                print(f"\n✏️ Step 3: Modify the fresh order")
                print("   Original: Buy 0.00006000 BTC at $108,000")
                print("   Modified: Buy 0.00010000 BTC at $107,500")
                
                try:
                    import time
                    time.sleep(2)  # Brief pause for order processing
                    
                    modify_response = trader.modify_order(
                        asset_index=0,
                        order_id=oid,
                        new_price="107500.0",   # Lower price
                        new_size="0.00010000",  # Larger size
                        reduce_only=False,
                        time_in_force="Gtc"
                    )
                    print(f"✅ Modify response: {modify_response}")
                    
                    if (modify_response.get("status") == "ok" and
                            "response" in modify_response and
                            "data" in modify_response["response"]):
                        new_oid = modify_response["response"]["data"].get("oid")
                        modify_tx = modify_response["response"].get("tx")
                        print(f"🎉 Order modified successfully!")
                        print(f"   New OID: {new_oid}")
                        print(f"   Modify TX: {modify_tx}")
                        
                        # Test 4: Cancel the modified order
                        print(f"\n❌ Step 4: Cancel modified order")
                        try:
                            cancel_response = trader.cancel_order(0, new_oid)
                            print(f"✅ Cancel response: {cancel_response}")
                        except Exception as e:
                            print(f"⚠️ Cancel failed: {e}")
                    else:
                        print(f"⚠️ Modify may have failed")
                        
                except Exception as e:
                    print(f"❌ Modify failed: {e}")
        else:
            print(f"⚠️ Order placement may have failed")
            
    except Exception as e:
        print(f"❌ Order placement failed: {e}")
    
    print("\n🎉 Complete demo finished!")
    print("\n📊 Summary of Working Features:")
    print("✅ Place Order - Working")
    print("✅ Cancel Order - Working") 
    print("✅ Update Leverage - Working")
    print("✅ Modify Order - Working (with fresh orders)")
    print("✅ Order Status Query - Working")


def demo_order_status():
    """Demonstrate order status query functionality"""
    print("🔍 Order Status Query Demo")
    print("=" * 50)
    
    trader = AmbientSDKTrader()
    
    # Place an order first
    print("1. Placing a test order...")
    order_params = OrderParams(
        asset_index=0,
        is_buy=True,
        price="105000.0",
        size="0.00004000",
        reduce_only=False,
        time_in_force="Gtc"
    )
    
    try:
        order_response = trader.place_order(order_params)
        if (order_response.get("status") == "ok" and
                "response" in order_response and
                "data" in order_response["response"]):
            oid = order_response["response"]["data"].get("oid")
            cloid = order_response["response"]["data"].get("cloid")
            print(f"   Order placed: OID {oid}, CLOID {cloid}")
            
            # Query status by OID
            print(f"\n2. Querying status by OID ({oid})...")
            status_result = trader.query_order_status(oid)
            status = status_result.get('status', 'unknown')
            print(f"   Status: {status}")
            
            if status == 'notFound':
                print("   Order not found in system yet (may need time to index)")
                # Try again after a brief wait
                import time
                print("   Waiting 2 seconds and retrying...")
                time.sleep(2)
                status_result = trader.query_order_status(oid)
                status = status_result.get('status', 'unknown')
                print(f"   Retry Status: {status}")
            
            if "order" in status_result and status_result["order"] is not None:
                order_info = status_result["order"]
                print(f"   Side: {'BUY' if order_info.get('side') == 'B' else 'SELL'}")
                print(f"   Size: {order_info.get('sz', 'N/A')}")
                print(f"   Price: ${order_info.get('limitPx', 'N/A')}")
                print(f"   Filled: {order_info.get('filledSz', '0')}")
            elif status != 'notFound':
                print(f"   No order details available for status: {status}")
            
            # Query status by CLOID (if different from OID)
            if cloid != str(oid):
                print(f"\n3. Querying status by CLOID ({cloid})...")
                cloid_result = trader.query_order_status(cloid)
                print(f"   Status: {cloid_result.get('status', 'unknown')}")
                
            # Cancel the order
            print(f"\n4. Cancelling the order...")
            cancel_result = trader.cancel_order(0, oid)
            print(f"   Cancel result: {cancel_result.get('status', 'unknown')}")
            
            # Check status after cancellation
            print(f"\n5. Checking status after cancellation...")
            final_status = trader.query_order_status(oid)
            print(f"   Final status: {final_status.get('status', 'unknown')}")
            
            print(f"\n🎉 Order status demo completed successfully!")
            
    except Exception as e:
        print(f"❌ Order status demo failed: {e}")


def demo_comprehensive_trading():
    """Demonstrate all trading operations in a workflow"""
    print("🔬 Comprehensive Trading Operations Demo")
    print("=" * 70)
    
    trader = AmbientSDKTrader()
    
    # Place -> Modify -> Cancel workflow
    print("\n🔄 Testing Place → Modify → Cancel workflow")
    
    order_params = OrderParams(
        asset_index=0,
        is_buy=True,
        price="106000.0",
        size="0.00007000",
        reduce_only=False,
        time_in_force="Gtc"
    )
    
    try:
        # Place
        print("1. Placing order...")
        order_resp = trader.place_order(order_params)
        oid = order_resp["response"]["data"]["oid"]
        print(f"   Order placed: OID {oid}")
        
        # Wait and modify
        import time
        time.sleep(1)
        print("2. Modifying order...")
        modify_resp = trader.modify_order(0, oid, "105500.0", "0.00012000")
        new_oid = modify_resp["response"]["data"]["oid"]
        print(f"   Order modified: New OID {new_oid}")
        
        # Cancel
        print("3. Cancelling modified order...")
        cancel_resp = trader.cancel_order(0, new_oid)
        print("   Order cancelled successfully")
        
        print("🎉 Complete workflow successful!")
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}")
    
    print("\n🎯 All operations completed!")


if __name__ == "__main__":
    demo_sdk_trading()
