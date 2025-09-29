import requests
import json

def test_embindexer_endpoint(endpoint_type, user=None, coin=None):
    """
    Test an embindexer API endpoint
    
    Returns:
        tuple: (success: bool, data: dict/list/None, error: str/None)
    """
    url = "https://embindexer.net/ember/api/dev/v1/info"
    headers = {"Content-Type": "application/json"}
    payload = {"type": endpoint_type}
    
    if user:
        payload["user"] = user
    if coin:
        payload["coin"] = coin
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Check if response is empty or contains no meaningful data
        if data == [] or data == {} or data is None:
            return False, data, "Empty response"
        
        # Check for common empty patterns
        if isinstance(data, list) and len(data) == 0:
            return False, data, "Empty array"
        
        if isinstance(data, dict):
            # Check if it's an account with no activity (all zeros)
            if endpoint_type in ["clearinghouseState"] and all(
                value in ["0.00", "0", 0, []] for value in data.get("crossMarginSummary", {}).values()
            ):
                return False, data, "Account with no activity"
        
        return True, data, None
        
    except requests.exceptions.RequestException as e:
        return False, None, str(e)

def run_comprehensive_test():
    """Test all available endpoints and provide a summary"""
    user_address = "AywrXuWFGa8Z9RMyum2BxeXpYL7kqGRFJDDXXJoxtw3e"
    
    # Define all endpoints to test
    endpoints = [
        # Market Data endpoints (no user required)
        {"name": "Meta and Asset Contexts", "type": "metaAndAssetCtxs", "category": "Market Data"},
        {"name": "All Mids", "type": "allMids", "category": "Market Data"},
        {"name": "Meta", "type": "meta", "category": "Market Data"},
        {"name": "Funding History", "type": "fundingHistory", "category": "Market Data"},
        {"name": "Candle Snapshot", "type": "candleSnapshot", "category": "Market Data"},
        
        # User Data endpoints (user required)
        {"name": "User Fills", "type": "userFills", "user": user_address, "category": "User Data"},
        {"name": "User Fills By Time", "type": "userFillsByTime", "user": user_address, "category": "User Data"},
        {"name": "Clearing House State", "type": "clearinghouseState", "user": user_address, "category": "User Data"},
        {"name": "Historical Orders", "type": "historicalOrders", "user": user_address, "category": "User Data"},
        {"name": "User Funding", "type": "userFunding", "user": user_address, "category": "User Data"},
        {"name": "Portfolio", "type": "portfolio", "user": user_address, "category": "User Data"},
        {"name": "Active Asset Data", "type": "activeAssetData", "user": user_address, "coin": "BTC", "category": "User Data"},
    ]
    
    results = {
        "working": [],
        "empty": [],
        "failed": []
    }
    
    print("🧪 Testing all Embindexer API endpoints...\n")
    
    for endpoint in endpoints:
        endpoint_name = endpoint["name"]
        endpoint_type = endpoint["type"]
        user = endpoint.get("user")
        coin = endpoint.get("coin")
        category = endpoint["category"]
        
        print(f"Testing {endpoint_name} ({endpoint_type})...", end=" ")
        
        success, data, error = test_embindexer_endpoint(endpoint_type, user, coin)
        
        if success:
            print("✅ WORKING")
            results["working"].append({
                "name": endpoint_name,
                "type": endpoint_type,
                "category": category,
                "data_sample": str(data)[:100] + "..." if len(str(data)) > 100 else str(data)
            })
        elif error and "Empty" in error:
            print("⚪ EMPTY")
            results["empty"].append({
                "name": endpoint_name,
                "type": endpoint_type,
                "category": category,
                "reason": error
            })
        else:
            print("❌ FAILED")
            results["failed"].append({
                "name": endpoint_name,
                "type": endpoint_type,
                "category": category,
                "error": error
            })
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    print(f"\n✅ WORKING ENDPOINTS ({len(results['working'])})")
    print("-" * 40)
    for endpoint in results["working"]:
        print(f"• {endpoint['name']} ({endpoint['category']})")
    
    print(f"\n⚪ EMPTY/NO DATA ENDPOINTS ({len(results['empty'])})")
    print("-" * 40)
    for endpoint in results["empty"]:
        print(f"• {endpoint['name']} ({endpoint['category']}) - {endpoint['reason']}")
    
    print(f"\n❌ FAILED ENDPOINTS ({len(results['failed'])})")
    print("-" * 40)
    for endpoint in results["failed"]:
        print(f"• {endpoint['name']} ({endpoint['category']}) - {endpoint['error']}")
    
    # Statistics
    total = len(endpoints)
    working_pct = round((len(results['working']) / total) * 100, 1)
    
    print(f"\n📈 STATISTICS")
    print("-" * 40)
    print(f"Total endpoints tested: {total}")
    print(f"Working endpoints: {len(results['working'])} ({working_pct}%)")
    print(f"Empty responses: {len(results['empty'])}")
    print(f"Failed requests: {len(results['failed'])}")
    
    return results

if __name__ == "__main__":
    results = run_comprehensive_test()