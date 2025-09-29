#!/usr/bin/env python3
"""
Test placing a fresh order and immediately modifying it
"""

import time
from exchange.ambient_trading_with_sdk import AmbientSDKTrader, OrderParams

def test_fresh_order_modify():
    """Place a new order and immediately try to modify it"""
    print("🧪 Testing Fresh Order + Modify")
    print("=" * 50)
    
    # Initialize trader
    trader = AmbientSDKTrader()
    
    # Step 1: Place a new limit order
    print("\n📋 Step 1: Place a fresh limit order")
    order_params = OrderParams(
        asset_index=0,           # BTC
        is_buy=True,            # Buy order
        price="110000.0",       # Price below current market
        size="0.00005000",      # Small size
        reduce_only=False,
        time_in_force="Gtc"
    )
    
    try:
        print("Placing new order...")
        order_response = trader.place_order(order_params)
        print(f"✅ Order response: {order_response}")
        
        # Extract order details
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
            
            # Wait a moment for order to be processed
            print("\n⏳ Waiting 3 seconds for order to be processed...")
            time.sleep(3)
            
            # Step 2: Modify the order
            print(f"\n✏️ Step 2: Modify the fresh order (OID: {oid})")
            print("   Original: Buy 0.00005000 BTC at $110,000")
            print("   Modified: Buy 0.00008000 BTC at $109,500")
            
            try:
                modify_response = trader.modify_order(
                    asset_index=0,           # BTC
                    order_id=oid,           # Use the fresh order ID
                    new_price="109500.0",   # Lower the price slightly
                    new_size="0.00008000",  # Increase the size
                    reduce_only=False,
                    time_in_force="Gtc"
                )
                print(f"✅ Modify response: {modify_response}")
                
                # Check modify result
                if modify_response.get("status") == "ok":
                    if "response" in modify_response and "data" in modify_response["response"]:
                        data = modify_response["response"]["data"]
                        print(f"🎉 Order modified successfully!")
                        print(f"   New OID: {data.get('oid')}")
                        print(f"   New CLOID: {data.get('cloid')}")
                        modify_tx = modify_response["response"].get("tx")
                        if modify_tx:
                            print(f"   Modify TX: {modify_tx}")
                    elif "response" in modify_response and "status" in modify_response["response"]:
                        status = modify_response["response"]["status"]
                        if isinstance(status, dict) and "error" in status:
                            print(f"⚠️ Modify failed: {status['error']}")
                        else:
                            print(f"✅ Modify status: {status}")
                
            except Exception as e:
                print(f"❌ Modify failed: {e}")
            
            # Step 3: Check current orders
            print(f"\n👀 Step 3: Check current orders")
            try:
                import requests
                import json
                
                client = requests.Session()
                client.headers.update({'Content-Type': 'application/json'})
                
                response = client.post('https://embindexer.net/ember/api/dev/v1/info', 
                                      json={'type': 'openOrders', 'user': trader.pubkey})
                orders = response.json()
                print("Current open orders:")
                for order in orders:
                    print(f"   OID {order['oid']}: {order['side']} {order['sz']} BTC at ${order['limitPx']}")
                    if str(order['oid']) == str(oid):
                        print(f"     ↑ This is our test order")
                
            except Exception as e:
                print(f"⚠️ Could not fetch orders: {e}")
        else:
            print(f"❌ Order placement failed: {order_response}")
            return
            
    except Exception as e:
        print(f"❌ Order placement failed: {e}")
        return
    
    print("\n🎉 Fresh order + modify test completed!")


if __name__ == "__main__":
    test_fresh_order_modify()