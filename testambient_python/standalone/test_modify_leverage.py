#!/usr/bin/env python3
"""
Test Modify Order and Update Leverage functionality
"""

from exchange.ambient_trading_with_sdk import AmbientSDKTrader

def test_modify_and_leverage():
    """Test modify order and update leverage functionality"""
    print("🧪 Testing Modify Order and Update Leverage")
    print("=" * 60)
    
    # Initialize trader
    trader = AmbientSDKTrader()
    
    # Test 1: Update Leverage
    print("\n📈 Step 1: Update leverage to 25x")
    try:
        leverage_response = trader.update_leverage(
            asset_index=0,  # BTC
            leverage=10    #
        )
        print(f"✅ Leverage response: {leverage_response}")
        
        # Check if successful
        if leverage_response.get("status") == "ok":
            if "response" in leverage_response and "data" in leverage_response["response"]:
                print(f"🎉 Leverage updated successfully!")
                tx = leverage_response["response"].get("tx")
                if tx:
                    print(f"   TX: {tx}")
            elif "response" in leverage_response and "status" in leverage_response["response"]:
                if "error" in leverage_response["response"]["status"]:
                    print(f"⚠️ Leverage update failed: {leverage_response['response']['status']['error']}")
                else:
                    print(f"✅ Leverage update status: {leverage_response['response']['status']}")
        
    except Exception as e:
        print(f"❌ Leverage update failed: {e}")
    
    # # Test 2: Modify existing order
    # print("\n✏️ Step 2: Modify existing buy order (ID: 6000)")
    # print("   Original: Buy at $75,000 for 0.00010000 BTC")
    # print("   Modified: Buy at $76,000 for 0.00015000 BTC")
    #
    # try:
    #     modify_response = trader.modify_order(
    #         asset_index=0,           # BTC
    #         order_id=6000,          # Existing buy order
    #         new_price="76000.0",    # Raise price from $75k to $76k
    #         new_size="0.00015000",  # Increase size
    #         reduce_only=False,
    #         time_in_force="Gtc"
    #     )
    #     print(f"✅ Modify response: {modify_response}")
    #
    #     # Check if successful
    #     if modify_response.get("status") == "ok":
    #         if "response" in modify_response and "data" in modify_response["response"]:
    #             data = modify_response["response"]["data"]
    #             print(f"🎉 Order modified successfully!")
    #             print(f"   New OID: {data.get('oid')}")
    #             print(f"   New CLOID: {data.get('cloid')}")
    #             tx = modify_response["response"].get("tx")
    #             if tx:
    #                 print(f"   TX: {tx}")
    #         elif "response" in modify_response and "status" in modify_response["response"]:
    #             if "error" in modify_response["response"]["status"]:
    #                 print(f"⚠️ Order modify failed: {modify_response['response']['status']['error']}")
    #             else:
    #                 print(f"✅ Order modify status: {modify_response['response']['status']}")
    #
    # except Exception as e:
    #     print(f"❌ Order modify failed: {e}")
    #
    # # Test 3: Verify changes by checking open orders
    # print("\n👀 Step 3: Check updated orders")
    # try:
    #     import requests
    #     import json
    #
    #     client = requests.Session()
    #     client.headers.update({'Content-Type': 'application/json'})
    #     user = trader.pubkey
    #
    #     response = client.post('https://embindexer.net/ember/api/dev/v1/info',
    #                           json={'type': 'openOrders', 'user': user})
    #     orders = response.json()
    #     print("Current open orders:")
    #     for order in orders:
    #         print(f"   OID {order['oid']}: {order['side']} {order['sz']} BTC at ${order['limitPx']}")
    #
    # except Exception as e:
    #     print(f"⚠️ Could not fetch updated orders: {e}")
    #
    # print("\n🎉 Test completed!")


if __name__ == "__main__":
    test_modify_and_leverage()