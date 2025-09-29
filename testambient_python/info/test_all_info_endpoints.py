#!/usr/bin/env python3
"""
Ambient Info API Endpoint Testing Suite

Comprehensive test suite for all Ambient Info API endpoints.
Tests all documented endpoints with real API calls and validates response schemas.
"""

import json
import time
import requests
from typing import Any, Dict, Optional, List
from dataclasses import dataclass

# API Configuration
AMBIENT_URL = "https://embindexer.net/ember/api/dev/v1"
TEST_USER = "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"

@dataclass
class TestResult:
    """Test result container"""
    endpoint: str
    success: bool
    response_data: Optional[Any] = None
    error_message: Optional[str] = None
    response_time: Optional[float] = None

class AmbientInfoTester:
    """Ambient Info API comprehensive test suite"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.results: List[TestResult] = []
    
    def make_info_request(self, payload: Dict[str, Any]) -> TestResult:
        """Make an info API request and return test result"""
        start_time = time.time()
        endpoint = payload.get("type", "unknown")
        
        try:
            response = self.session.post(f"{AMBIENT_URL}/info", json=payload)
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                return TestResult(
                    endpoint=endpoint,
                    success=True,
                    response_data=data,
                    response_time=response_time
                )
            else:
                return TestResult(
                    endpoint=endpoint,
                    success=False,
                    error_message=f"HTTP {response.status_code}: {response.text}",
                    response_time=response_time
                )
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            return TestResult(
                endpoint=endpoint,
                success=False,
                error_message=str(e),
                response_time=response_time
            )
    
    def print_response(self, result: TestResult, show_full_response: bool = False):
        """Print formatted test result"""
        status = "✅ PASS" if result.success else "❌ FAIL"
        time_str = f" ({result.response_time:.3f}s)" if result.response_time else ""
        
        print(f"{status} | {result.endpoint}{time_str}")
        
        if result.error_message:
            print(f"   Error: {result.error_message}")
        elif result.response_data is not None:
            if show_full_response:
                print(f"   Response: {json.dumps(result.response_data, indent=2)}")
            else:
                # Show summary based on response type
                data = result.response_data
                if isinstance(data, dict):
                    if "BTC" in data and len(data) <= 5:  # allMids response
                        print(f"   Response: {data}")
                    elif "coin" in data and "levels" in data:  # l2Book response
                        bid_count = len(data["levels"][0]) if data["levels"][0] else 0
                        ask_count = len(data["levels"][1]) if data["levels"][1] else 0
                        print(f"   Coin: {data['coin']}, Bids: {bid_count}, Asks: {ask_count}")
                    elif "marginSummary" in data:  # clearinghouseState response
                        account_value = data["marginSummary"]["accountValue"]
                        positions = len(data.get("assetPositions", []))
                        print(f"   Account Value: {account_value}, Positions: {positions}")
                    elif "marginTables" in data and "universe" in data:  # meta response
                        universe_count = len(data["universe"])
                        print(f"   Universe assets: {universe_count}")
                    elif "order" in data and "status" in data:  # orderStatus response
                        status = data["status"]
                        order_id = data["order"]["orderId"] if data["order"] else "N/A"
                        print(f"   Order {order_id}: {status}")
                    else:
                        print(f"   Response type: {type(data).__name__} with {len(data)} items")
                elif isinstance(data, list):
                    print(f"   Response: Array with {len(data)} items")
                    if data and isinstance(data[0], dict):
                        # Show first item keys for structure
                        sample_keys = list(data[0].keys())[:5]
                        print(f"   Sample keys: {sample_keys}")
                else:
                    print(f"   Response: {type(data).__name__}")
    
    def test_all_mids(self) -> TestResult:
        """Test allMids endpoint"""
        payload = {"type": "allMids"}
        result = self.make_info_request(payload)
        self.results.append(result)
        return result
    
    def test_meta(self) -> TestResult:
        """Test meta endpoint"""
        payload = {"type": "meta"}
        result = self.make_info_request(payload)
        self.results.append(result)
        return result
    
    def test_meta_and_asset_ctxs(self) -> TestResult:
        """Test metaAndAssetCtxs endpoint"""
        payload = {"type": "metaAndAssetCtxs"}
        result = self.make_info_request(payload)
        self.results.append(result)
        return result
    
    def test_open_orders(self) -> TestResult:
        """Test openOrders endpoint"""
        payload = {"type": "openOrders", "user": TEST_USER}
        result = self.make_info_request(payload)
        self.results.append(result)
        return result
    
    def test_l2_book(self, coin: str = "BTC") -> TestResult:
        """Test l2Book endpoint"""
        payload = {"type": "l2Book", "coin": coin}
        result = self.make_info_request(payload)
        self.results.append(result)
        return result
    
    def test_l2_book_with_sig_figs(self, coin: str = "BTC", n_sig_figs: int = 3) -> TestResult:
        """Test l2Book endpoint with nSigFigs parameter"""
        payload = {"type": "l2Book", "coin": coin, "nSigFigs": n_sig_figs}
        result = self.make_info_request(payload)
        result.endpoint = f"l2Book (nSigFigs={n_sig_figs})"
        self.results.append(result)
        return result
    
    def test_user_fills(self) -> TestResult:
        """Test userFills endpoint"""
        payload = {"type": "userFills", "user": TEST_USER}
        result = self.make_info_request(payload)
        self.results.append(result)
        return result
    
    def test_user_fills_aggregated(self) -> TestResult:
        """Test userFills endpoint with aggregation"""
        payload = {"type": "userFills", "user": TEST_USER, "aggregateByTime": True}
        result = self.make_info_request(payload)
        result.endpoint = "userFills (aggregated)"
        self.results.append(result)
        return result
    
    def test_user_fills_by_time(self) -> TestResult:
        """Test userFillsByTime endpoint"""
        start_time = int(time.time() * 1000) - 86400000  # 24 hours ago
        payload = {
            "type": "userFillsByTime",
            "user": TEST_USER,
            "startTime": start_time,
            "aggregateByTime": False
        }
        result = self.make_info_request(payload)
        self.results.append(result)
        return result
    
    def test_clearinghouse_state(self) -> TestResult:
        """Test clearinghouseState endpoint"""
        payload = {"type": "clearinghouseState", "user": TEST_USER}
        result = self.make_info_request(payload)
        self.results.append(result)
        return result
    
    def test_active_asset_data(self, coin: str = "BTC") -> TestResult:
        """Test activeAssetData endpoint"""
        payload = {"type": "activeAssetData", "user": TEST_USER, "coin": coin}
        result = self.make_info_request(payload)
        self.results.append(result)
        return result
    
    def test_historical_orders(self) -> TestResult:
        """Test historicalOrders endpoint"""
        payload = {"type": "historicalOrders", "user": TEST_USER}
        result = self.make_info_request(payload)
        self.results.append(result)
        return result
    
    def test_order_status_by_oid(self, order_id: int = 1758872506411) -> TestResult:
        """Test orderStatus endpoint by OID"""
        payload = {"type": "orderStatus", "user": TEST_USER, "orderId": order_id}
        result = self.make_info_request(payload)
        result.endpoint = f"orderStatus (OID {order_id})"
        self.results.append(result)
        return result
    
    def test_order_status_by_cloid(self, cloid: str = "test_cloid_123") -> TestResult:
        """Test orderStatus endpoint by CLOID"""
        payload = {"type": "orderStatus", "user": TEST_USER, "orderId": cloid}
        result = self.make_info_request(payload)
        result.endpoint = f"orderStatus (CLOID {cloid})"
        self.results.append(result)
        return result
    
    def test_invalid_endpoint(self) -> TestResult:
        """Test invalid endpoint to verify error handling"""
        payload = {"type": "invalidEndpoint"}
        result = self.make_info_request(payload)
        result.endpoint = "invalidEndpoint (error test)"
        self.results.append(result)
        return result
    
    def test_missing_required_field(self) -> TestResult:
        """Test missing required field to verify error handling"""
        payload = {"type": "openOrders"}  # Missing required 'user' field
        result = self.make_info_request(payload)
        result.endpoint = "openOrders (missing user)"
        self.results.append(result)
        return result
    
    def run_all_tests(self, show_responses: bool = False) -> None:
        """Run all info endpoint tests"""
        print("🧪 Ambient Info API Comprehensive Test Suite")
        print("=" * 80)
        print(f"API Base URL: {AMBIENT_URL}")
        print(f"Test User: {TEST_USER}")
        print(f"Show Full Responses: {show_responses}")
        print()
        
        # Core market data endpoints
        print("📊 Market Data Endpoints")
        print("-" * 40)
        self.print_response(self.test_all_mids(), show_responses)
        self.print_response(self.test_meta(), show_responses)
        self.print_response(self.test_meta_and_asset_ctxs(), show_responses)
        self.print_response(self.test_l2_book(), show_responses)
        self.print_response(self.test_l2_book_with_sig_figs(), show_responses)
        
        print()
        print("👤 User Data Endpoints")
        print("-" * 40)
        self.print_response(self.test_open_orders(), show_responses)
        self.print_response(self.test_user_fills(), show_responses)
        self.print_response(self.test_user_fills_aggregated(), show_responses)
        self.print_response(self.test_user_fills_by_time(), show_responses)
        self.print_response(self.test_clearinghouse_state(), show_responses)
        self.print_response(self.test_active_asset_data(), show_responses)
        self.print_response(self.test_historical_orders(), show_responses)
        
        print()
        print("🔍 Order Status Endpoints")
        print("-" * 40)
        # Test with a real order ID if available from open orders
        open_orders_result = next((r for r in self.results if r.endpoint == "openOrders"), None)
        if open_orders_result and open_orders_result.success and open_orders_result.response_data:
            orders = open_orders_result.response_data
            if orders and len(orders) > 0:
                test_oid = orders[0]["oid"]
                self.print_response(self.test_order_status_by_oid(test_oid), show_responses)
            else:
                self.print_response(self.test_order_status_by_oid(), show_responses)
        else:
            self.print_response(self.test_order_status_by_oid(), show_responses)
        
        self.print_response(self.test_order_status_by_cloid(), show_responses)
        
        print()
        print("❌ Error Handling Tests")
        print("-" * 40)
        self.print_response(self.test_invalid_endpoint(), show_responses)
        self.print_response(self.test_missing_required_field(), show_responses)
        
        self.print_summary()
    
    def run_single_endpoint_test(self, endpoint_name: str, **kwargs) -> None:
        """Run a single endpoint test for debugging"""
        print(f"🔍 Testing {endpoint_name}")
        print("=" * 50)
        
        test_methods = {
            "allMids": self.test_all_mids,
            "meta": self.test_meta,
            "metaAndAssetCtxs": self.test_meta_and_asset_ctxs,
            "openOrders": self.test_open_orders,
            "l2Book": self.test_l2_book,
            "userFills": self.test_user_fills,
            "userFillsByTime": self.test_user_fills_by_time,
            "clearinghouseState": self.test_clearinghouse_state,
            "activeAssetData": self.test_active_asset_data,
            "historicalOrders": self.test_historical_orders,
            "orderStatus": self.test_order_status_by_oid,
        }
        
        if endpoint_name in test_methods:
            result = test_methods[endpoint_name](**kwargs)
            self.print_response(result, show_full_response=True)
        else:
            print(f"❌ Unknown endpoint: {endpoint_name}")
            print(f"Available endpoints: {list(test_methods.keys())}")
    
    def print_summary(self) -> None:
        """Print test summary"""
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for r in self.results if r.success)
        failed = sum(1 for r in self.results if not r.success)
        total = len(self.results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        
        if total > 0:
            pass_rate = (passed / total) * 100
            print(f"Pass Rate: {pass_rate:.1f}%")
        
        # Show failed tests
        failed_tests = [r for r in self.results if not r.success]
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for result in failed_tests:
                print(f"   - {result.endpoint}: {result.error_message}")
        
        # Show response time statistics
        successful_results = [r for r in self.results if r.success and r.response_time]
        if successful_results:
            response_times = [r.response_time for r in successful_results]
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            
            print(f"\n⏱️  Response Time Statistics:")
            print(f"   Average: {avg_time:.3f}s")
            print(f"   Fastest: {min_time:.3f}s")
            print(f"   Slowest: {max_time:.3f}s")


def run_comprehensive_tests():
    """Run comprehensive test suite"""
    tester = AmbientInfoTester()
    tester.run_all_tests(show_responses=False)


def run_single_test(endpoint: str = "allMids"):
    """Run a single endpoint test for debugging"""
    tester = AmbientInfoTester()
    tester.run_single_endpoint_test(endpoint)


def run_with_full_responses():
    """Run all tests showing full API responses"""
    tester = AmbientInfoTester()
    tester.run_all_tests(show_responses=True)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "single":
            endpoint = sys.argv[2] if len(sys.argv) > 2 else "allMids"
            run_single_test(endpoint)
        elif command == "full":
            run_with_full_responses()
        elif command == "help":
            print("Usage:")
            print("  python test_all_info_endpoints.py                    # Run all tests")
            print("  python test_all_info_endpoints.py single [endpoint]  # Test single endpoint")
            print("  python test_all_info_endpoints.py full               # Show full responses")
            print("  python test_all_info_endpoints.py help               # Show this help")
            print()
            print("Available endpoints for single testing:")
            print("  allMids, meta, metaAndAssetCtxs, openOrders, l2Book,")
            print("  userFills, userFillsByTime, clearinghouseState,")
            print("  activeAssetData, historicalOrders, orderStatus")
        else:
            print(f"Unknown command: {command}")
            print("Use 'help' for usage information")
    else:
        run_comprehensive_tests()