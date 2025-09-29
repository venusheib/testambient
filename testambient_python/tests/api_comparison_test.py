#!/usr/bin/env python3
"""
API Comparison Test Suite

Converts the TypeScript API comparison script to Python and runs comprehensive
tests comparing Hyperliquid and Ambient API responses for shape compatibility.
"""

import json
import time
import requests
from typing import Any, Dict, Optional, Union, List
from dataclasses import dataclass

# API Configuration
HYPERLIQUID_URL = "https://api.hyperliquid.xyz"
AMBIENT_URL = "https://embindexer.net/ember/api/dev/v1"

AMBIENT_TEST_ADDRESS = "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
HYPERLIQUID_TEST_ADDRESS = "0x0f6410E884F115166f82E3FFB5840BAdc20619e1"

@dataclass
class ApiPayload:
    """API payload structure"""
    type: str
    coin: Optional[str] = None
    user: Optional[str] = None
    aggregateByTime: Optional[bool] = None
    startTime: Optional[int] = None
    endTime: Optional[int] = None
    req: Optional[Dict[str, Any]] = None

class ApiTester:
    """API comparison testing class"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def do_hl_info_call(self, payload: ApiPayload) -> Any:
        """Make a Hyperliquid API call"""
        start_time = time.time()
        
        payload_dict = {
            "type": payload.type
        }
        if payload.coin is not None:
            payload_dict["coin"] = payload.coin
        if payload.user is not None:
            payload_dict["user"] = payload.user
        if payload.aggregateByTime is not None:
            payload_dict["aggregateByTime"] = payload.aggregateByTime
        if payload.startTime is not None:
            payload_dict["startTime"] = payload.startTime
        if payload.endTime is not None:
            payload_dict["endTime"] = payload.endTime
        if payload.req is not None:
            payload_dict["req"] = payload.req
        
        try:
            response = self.session.post(
                f"{HYPERLIQUID_URL}/info",
                json=payload_dict
            )
            end_time = time.time()
            print(f'HL info call with payload type "{payload.type}" took {end_time - start_time:.3f} seconds')
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"HL API Error: {e}")
            return None
    
    def do_ambient_info_call(self, payload: ApiPayload) -> Any:
        """Make an Ambient API call"""
        start_time = time.time()
        
        payload_dict = {
            "type": payload.type
        }
        if payload.coin is not None:
            payload_dict["coin"] = payload.coin
        if payload.user is not None:
            payload_dict["user"] = payload.user
        if payload.aggregateByTime is not None:
            payload_dict["aggregateByTime"] = payload.aggregateByTime
        if payload.startTime is not None:
            payload_dict["startTime"] = payload.startTime
        if payload.endTime is not None:
            payload_dict["endTime"] = payload.endTime
        if payload.req is not None:
            payload_dict["req"] = payload.req
        
        try:
            response = self.session.post(
                f"{AMBIENT_URL}/info",
                json=payload_dict
            )
            end_time = time.time()
            text = response.text
            print(f'Ambient info call with payload type "{payload.type}" took {end_time - start_time:.3f} seconds')
            print(text)
            print(payload_dict)
            
            if response.status_code != 200:
                print(f"Ambient API HTTP {response.status_code}: {text}")
                return None
                
            return response.json()
        except Exception as e:
            print(f"Ambient API Error: {e}")
            return None
    
    def get_type_name(self, obj: Any) -> str:
        """Get the type name of an object"""
        if obj is None:
            return 'null'
        if isinstance(obj, list):
            return 'array'
        return type(obj).__name__
    
    def compare_json_shapes(self, obj1: Any, obj2: Any, path: str = "", check_is_hashmap: bool = True) -> bool:
        """Smart comparison with rules for different data types"""
        
        if self.get_type_name(obj1) != self.get_type_name(obj2):
            print(f"Type mismatch at {path}: {self.get_type_name(obj1)} vs {self.get_type_name(obj2)}")
            return False
        
        if isinstance(obj1, dict) and obj1 is not None:
            # Detect if this looks like a hashmap/lookup table
            keys = list(obj1.keys())
            is_hashmap = (check_is_hashmap and 
                         path == "" and 
                         len(keys) > 0 and
                         all(isinstance(k, str) and 
                             (k.startswith('@') or k.isupper() or len(k) <= 10) 
                             for k in keys[:10]))
            
            if is_hashmap:
                print(f"Detected hashmap at {path}, comparing value shapes only")
                keys1 = set(obj1.keys())
                keys2 = set(obj2.keys())
                
                # Find common keys or use samples
                common_keys = keys1.intersection(keys2)
                if common_keys:
                    sample_key = next(iter(common_keys))
                    return self.compare_json_shapes(
                        obj1[sample_key], obj2[sample_key], f"{path}.<value>", check_is_hashmap
                    )
                elif keys1 and keys2:
                    # Use samples from each
                    key1 = next(iter(keys1))
                    key2 = next(iter(keys2))
                    print(f"  Comparing {key1} vs {key2}")
                    return self.compare_json_shapes(
                        obj1[key1], obj2[key2], f"{path}.<value>", check_is_hashmap
                    )
                return True  # Both empty
            else:
                # Regular object - strict key matching
                keys1 = set(obj1.keys())
                keys2 = set(obj2.keys())
                
                if keys1 != keys2:
                    print(f"Key mismatch at {path}:")
                    only_in_first = keys1 - keys2
                    only_in_second = keys2 - keys1
                    if only_in_first:
                        print(f"  Only in first: {list(only_in_first)}")
                    if only_in_second:
                        print(f"  Only in second: {list(only_in_second)}")
                    return False
                
                return all(
                    self.compare_json_shapes(obj1[k], obj2[k], f"{path}.{k}", check_is_hashmap)
                    for k in keys1
                )
        
        elif isinstance(obj1, list):
            # Compare array shapes - don't require same length
            if len(obj1) > 0 and len(obj2) > 0:
                return self.compare_json_shapes(obj1[0], obj2[0], f"{path}[0]", check_is_hashmap)
        
        return True
    
    def order_json(self, obj: Any, sort_keys: bool = True) -> None:
        """Helper function to order object keys recursively and log formatted JSON"""
        
        def order_object(input_obj: Any) -> Any:
            if input_obj is None or not isinstance(input_obj, (dict, list)):
                return input_obj
            
            if isinstance(input_obj, list):
                return [order_object(item) for item in input_obj]
            
            keys = list(input_obj.keys())
            if sort_keys:
                keys.sort()
            
            ordered_obj = {}
            for key in keys:
                ordered_obj[key] = order_object(input_obj[key])
            
            return ordered_obj
        
        ordered_obj = order_object(obj)
        print(json.dumps(ordered_obj, indent=2))
    
    def test_endpoint(self, test_name: str, hl_payload: ApiPayload, ambient_payload: ApiPayload, 
                     check_hashmap: bool = False) -> bool:
        """Generic test method for comparing endpoint responses"""
        print(f"\n{'='*60}")
        print(f"Testing {test_name}")
        print(f"{'='*60}")
        
        hl_response = self.do_hl_info_call(hl_payload)
        ambient_response = self.do_ambient_info_call(ambient_payload)
        
        if hl_response is None or ambient_response is None:
            print("❌ One or both API calls failed")
            return False
        
        print("\n--- HL Response ---")
        self.order_json(hl_response)
        print("\n--- Ambient Response ---")
        self.order_json(ambient_response)
        
        if self.compare_json_shapes(hl_response, ambient_response, "", not check_hashmap):
            print("✅ JSON shapes match")
            return True
        else:
            print("❌ JSON shapes do not match")
            return False

# Test Methods
def test_all_mids(tester: ApiTester) -> bool:
    """Test all mids endpoint"""
    payload = ApiPayload(type="allMids")
    return tester.test_endpoint("All Mids", payload, payload, check_hashmap=True)

def test_l2_book(tester: ApiTester, symbol: str = "BTC") -> bool:
    """Test L2 book endpoint"""
    payload = ApiPayload(type="l2Book", coin=symbol)
    return tester.test_endpoint(f"L2 Book ({symbol})", payload, payload)

def test_user_state(tester: ApiTester) -> bool:
    """Test clearinghouse state endpoint"""
    hl_payload = ApiPayload(type="clearinghouseState", user=HYPERLIQUID_TEST_ADDRESS)
    ambient_payload = ApiPayload(type="clearinghouseState", user=AMBIENT_TEST_ADDRESS)
    return tester.test_endpoint("User State", hl_payload, ambient_payload)

def test_open_orders(tester: ApiTester) -> bool:
    """Test open orders endpoint"""
    hl_payload = ApiPayload(type="openOrders", user=HYPERLIQUID_TEST_ADDRESS)
    ambient_payload = ApiPayload(type="openOrders", user=AMBIENT_TEST_ADDRESS)
    return tester.test_endpoint("Open Orders", hl_payload, ambient_payload)

def test_historical_orders(tester: ApiTester) -> bool:
    """Test historical orders endpoint"""
    hl_payload = ApiPayload(type="historicalOrders", user=HYPERLIQUID_TEST_ADDRESS)
    ambient_payload = ApiPayload(type="historicalOrders", user=AMBIENT_TEST_ADDRESS)
    return tester.test_endpoint("Historical Orders", hl_payload, ambient_payload)

def test_user_fills(tester: ApiTester) -> bool:
    """Test user fills endpoint"""
    hl_payload = ApiPayload(type="userFills", user=HYPERLIQUID_TEST_ADDRESS, aggregateByTime=False)
    ambient_payload = ApiPayload(type="userFills", user=AMBIENT_TEST_ADDRESS)
    return tester.test_endpoint("User Fills", hl_payload, ambient_payload)

def test_user_fills_by_time(tester: ApiTester) -> bool:
    """Test user fills by time endpoint"""
    start_time = int(time.time() * 1000) - 86400000  # 24 hours ago
    hl_payload = ApiPayload(
        type="userFillsByTime", 
        user=HYPERLIQUID_TEST_ADDRESS,
        startTime=start_time,
        aggregateByTime=True
    )
    ambient_payload = ApiPayload(
        type="userFillsByTime",
        user=AMBIENT_TEST_ADDRESS,
        startTime=start_time,
        aggregateByTime=True
    )
    return tester.test_endpoint("User Fills By Time", hl_payload, ambient_payload)

def test_meta(tester: ApiTester) -> bool:
    """Test meta endpoint"""
    payload = ApiPayload(type="meta")
    return tester.test_endpoint("Meta", payload, payload)

def test_meta_and_asset_ctxs(tester: ApiTester) -> bool:
    """Test metaAndAssetCtxs endpoint"""
    payload = ApiPayload(type="metaAndAssetCtxs")
    return tester.test_endpoint("Meta and Asset Contexts", payload, payload)

def test_user_funding(tester: ApiTester) -> bool:
    """Test user funding endpoint"""
    hl_payload = ApiPayload(type="userFunding", user=HYPERLIQUID_TEST_ADDRESS)
    ambient_payload = ApiPayload(type="userFunding", user=AMBIENT_TEST_ADDRESS)
    return tester.test_endpoint("User Funding", hl_payload, ambient_payload)

def test_funding_history(tester: ApiTester) -> bool:
    """Test funding history endpoint"""
    start_time = int(time.time() * 1000) - 86400000  # 24 hours ago
    payload = ApiPayload(type="fundingHistory", coin="BTC", startTime=start_time)
    return tester.test_endpoint("Funding History", payload, payload)

def test_portfolio(tester: ApiTester) -> bool:
    """Test portfolio endpoint"""
    hl_payload = ApiPayload(type="portfolio", user=HYPERLIQUID_TEST_ADDRESS)
    ambient_payload = ApiPayload(type="portfolio", user=AMBIENT_TEST_ADDRESS)
    return tester.test_endpoint("Portfolio", hl_payload, ambient_payload)

def test_candle_snapshot(tester: ApiTester) -> bool:
    """Test candle snapshot endpoint"""
    start_time = int(time.time() * 1000) - 86400000  # 24 hours ago
    end_time = int(time.time() * 1000)
    
    payload = ApiPayload(
        type="candleSnapshot",
        req={
            "coin": "BTC",
            "interval": "1m",
            "startTime": start_time,
            "endTime": end_time,
        }
    )
    return tester.test_endpoint("Candle Snapshot", payload, payload)

def run_all_tests() -> None:
    """Run all API comparison tests"""
    tester = ApiTester()
    
    # Define all tests
    tests = [
        ("All Mids", lambda: test_all_mids(tester)),
        ("L2 Book", lambda: test_l2_book(tester)),
        ("User State", lambda: test_user_state(tester)),
        ("Open Orders", lambda: test_open_orders(tester)),
        ("Historical Orders", lambda: test_historical_orders(tester)),
        ("User Fills", lambda: test_user_fills(tester)),
        ("User Fills By Time", lambda: test_user_fills_by_time(tester)),
        ("Meta", lambda: test_meta(tester)),
        ("Meta and Asset Contexts", lambda: test_meta_and_asset_ctxs(tester)),
        ("User Funding", lambda: test_user_funding(tester)),
        ("Funding History", lambda: test_funding_history(tester)),
        ("Portfolio", lambda: test_portfolio(tester)),
        ("Candle Snapshot", lambda: test_candle_snapshot(tester)),
    ]
    
    results = []
    
    print("🧪 Running API Comparison Tests")
    print("=" * 80)
    print(f"Hyperliquid API: {HYPERLIQUID_URL}")
    print(f"Ambient API: {AMBIENT_URL}")
    print(f"HL Test Address: {HYPERLIQUID_TEST_ADDRESS}")
    print(f"Ambient Test Address: {AMBIENT_TEST_ADDRESS}")
    
    for test_name, test_func in tests:
        try:
            print(f"\n🔍 Running {test_name}...")
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Test {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Results: {passed} passed, {failed} failed out of {len(results)} tests")
    pass_rate = (passed / len(results)) * 100 if results else 0
    print(f"📊 Pass rate: {pass_rate:.1f}%")

def run_single_test() -> None:
    """Run a single test for debugging"""
    tester = ApiTester()
    
    # Uncomment the test you want to run:
    # test_all_mids(tester)
    # test_l2_book(tester)
    # test_user_state(tester)
    # test_open_orders(tester)
    # test_historical_orders(tester)
    # test_user_fills(tester)
    # test_user_fills_by_time(tester)
    # test_meta(tester)
    # test_meta_and_asset_ctxs(tester)
    # test_user_funding(tester)
    # test_funding_history(tester)
    # test_portfolio(tester)
    test_candle_snapshot(tester)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "single":
        run_single_test()
    else:
        run_all_tests()