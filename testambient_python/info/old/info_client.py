#!/usr/bin/env python3
"""
Embindexer API Client

A comprehensive Python client for interacting with the Embindexer API.
Includes all working endpoints with proper error handling and response formatting.
"""

import requests
import json
from typing import Optional, Dict, Any, List
from datetime import datetime


class EmbindexerClient:
    """
    Python client for the Embindexer API
    
    Usage:
        client = EmbindexerClient()
        mids = client.get_all_mids()
        print(mids)
    """
    
    def __init__(self, base_url: str = "https://embindexer.net/ember/api/dev/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def _make_request(self, endpoint_type: str, **kwargs) -> Dict[str, Any]:
        """
        Make a request to the Embindexer API
        
        Args:
            endpoint_type: The API endpoint type
            **kwargs: Additional parameters for the request
            
        Returns:
            API response as dictionary
            
        Raises:
            requests.RequestException: If the API request fails
        """
        url = f"{self.base_url}/info"
        payload = {"type": endpoint_type}
        payload.update(kwargs)
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Error calling {endpoint_type}: {e}")
            raise
    
    # ==========================================
    # WORKING ENDPOINTS
    # ==========================================
    
    def get_meta_and_asset_contexts(self) -> List[Dict[str, Any]]:
        """
        Retrieve meta and asset contexts
        
        Returns margin tables and asset context information including 
        funding rates, mark prices, and open interest.
        
        Returns:
            List containing margin tables and asset contexts
        """
        return self._make_request("metaAndAssetCtxs")
    
    def get_all_mids(self) -> Dict[str, str]:
        """
        Retrieve all mid prices
        
        Returns mid prices for all available trading pairs.
        
        Returns:
            Dictionary mapping coin symbols to mid prices
        """
        return self._make_request("allMids")
    
    def get_meta(self) -> Dict[str, Any]:
        """
        Retrieve perpetuals metadata
        
        Returns universe and margin tables for perpetuals.
        
        Returns:
            Dictionary containing margin tables and universe data
        """
        return self._make_request("meta")
    
    def get_active_asset_data(self, user: str, coin: str) -> Dict[str, Any]:
        """
        Retrieve user's active asset data
        
        Returns user's active asset data for a specific coin.
        
        Args:
            user: Solana address (base58 encoded)
            coin: Coin symbol (e.g., "BTC")
            
        Returns:
            Dictionary containing active asset data
        """
        return self._make_request("activeAssetData", user=user, coin=coin)
    
    # ==========================================
    # ENDPOINTS WITH EMPTY RESPONSES
    # ==========================================
    
    def get_funding_history(self) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieve historical funding rates
        
        Note: Currently returns empty response for tested addresses.
        
        Returns:
            List of funding history data or None if empty
        """
        try:
            result = self._make_request("fundingHistory")
            return result if result else None
        except requests.RequestException:
            return None
    
    def get_user_fills(self, user: str) -> List[Dict[str, Any]]:
        """
        Retrieve a user's fills
        
        Returns at most 2000 fills per response and only the 10000 most recent fills are available.
        
        Args:
            user: Solana address (base58 encoded)
            
        Returns:
            List of user fills (may be empty)
        """
        try:
            return self._make_request("userFills", user=user)
        except requests.RequestException:
            return []
    
    def get_user_fills_by_time(self, user: str, start_time: int, 
                              end_time: Optional[int] = None, 
                              aggregate_by_time: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieve a user's fills by time
        
        Returns at most 2000 fills per response and only the 10000 most recent fills are available,
        filtered by time range.
        
        Args:
            user: Solana address (base58 encoded)
            start_time: Start time in milliseconds, inclusive
            end_time: End time in milliseconds, inclusive. Defaults to current time.
            aggregate_by_time: When true, partial fills are combined when a crossing order 
                             gets filled by multiple different resting orders
            
        Returns:
            List of user fills (may be empty)
        """
        params = {"user": user, "startTime": start_time, "aggregateByTime": aggregate_by_time}
        if end_time is not None:
            params["endTime"] = end_time
            
        try:
            return self._make_request("userFillsByTime", **params)
        except requests.RequestException:
            return []
    
    def get_historical_orders(self, user: str) -> List[Dict[str, Any]]:
        """
        Retrieve historical orders
        
        Returns user's historical orders with status information.
        
        Args:
            user: Solana address (base58 encoded)
            
        Returns:
            List of historical orders (may be empty)
        """
        try:
            return self._make_request("historicalOrders", user=user)
        except requests.RequestException:
            return []
    
    def get_user_funding(self, user: str) -> List[Dict[str, Any]]:
        """
        Retrieve user's funding history
        
        Returns user's funding history.
        
        Args:
            user: Solana address (base58 encoded)
            
        Returns:
            List of funding history (may be empty)
        """
        try:
            return self._make_request("userFunding", user=user)
        except requests.RequestException:
            return []


def demo_client():
    """Demonstrate the EmbindexerClient with all working endpoints"""
    
    print("🚀 Embindexer API Client Demo")
    print("=" * 50)
    
    # Initialize client
    client = EmbindexerClient()
    user_address = "AywrXuWFGa8Z9RMyum2BxeXpYL7kqGRFJDDXXJoxtw3e"
    
    # Test working endpoints
    print("\n✅ WORKING ENDPOINTS")
    print("-" * 30)
    
    try:
        print("📊 Getting all mid prices...")
        mids = client.get_all_mids()
        print(f"Found {len(mids)} trading pairs")
        for coin, price in mids.items():
            print(f"  {coin}: ${price}")
        
        print("\n📋 Getting meta and asset contexts...")
        meta_ctx = client.get_meta_and_asset_contexts()
        print(f"Received {len(meta_ctx)} data sections")
        
        print("\n📈 Getting perpetuals metadata...")
        meta = client.get_meta()
        universe = meta.get("universe", [])
        print(f"Found {len(universe)} assets in universe:")
        for asset in universe:
            print(f"  {asset['name']}: {asset['maxLeverage']}x max leverage")
        
        print("\n👤 Getting active asset data for BTC...")
        active_data = client.get_active_asset_data(user_address, "BTC")
        print(active_data)
        print(f"Active asset data keys: {list(active_data.keys()) if active_data else 'None'}")
        
    except Exception as e:
        print(f"❌ Error in working endpoints: {e}")
    
    # Test endpoints with empty responses
    print("\n⚪ ENDPOINTS WITH EMPTY RESPONSES")
    print("-" * 40)
    
    print("💰 Checking user fills...")
    fills = client.get_user_fills(user_address)
    print(f"User fills: {len(fills)} found")
    
    print("📊 Checking funding history...")
    funding_history = client.get_funding_history()
    print(f"Funding history: {'Available' if funding_history else 'Empty'}")
    
    print("📝 Checking historical orders...")
    orders = client.get_historical_orders(user_address)
    print(f"Historical orders: {len(orders)} found")
    
    print("💸 Checking user funding...")
    user_funding = client.get_user_funding(user_address)
    print(f"User funding: {len(user_funding)} entries")
    
    # Test time-based fills (last 30 days)
    end_time = int(datetime.now().timestamp() * 1000)
    start_time = end_time - (30 * 24 * 60 * 60 * 1000)  # 30 days ago
    
    print(f"\n⏰ Checking fills from last 30 days...")
    time_fills = client.get_user_fills_by_time(user_address, start_time, end_time)
    print(f"Fills in last 30 days: {len(time_fills)} found")
    
    print("\n🎉 Demo completed!")


def interactive_client():
    """Interactive mode for testing different endpoints"""
    
    client = EmbindexerClient()
    user_address = "AywrXuWFGa8Z9RMyum2BxeXpYL7kqGRFJDDXXJoxtw3e"
    
    print("🔧 Interactive Embindexer API Client")
    print("=" * 40)
    print("Available commands:")
    print("1. mids - Get all mid prices")
    print("2. meta - Get perpetuals metadata")
    print("3. context - Get meta and asset contexts")
    print("4. active <coin> - Get active asset data")
    print("5. fills - Get user fills")
    print("6. orders - Get historical orders")
    print("7. funding - Get user funding")
    print("8. quit - Exit")
    print()
    
    while True:
        try:
            command = input("embindexer> ").strip().lower()
            
            if command == "quit" or command == "exit":
                print("👋 Goodbye!")
                break
            elif command == "mids":
                result = client.get_all_mids()
                print(json.dumps(result, indent=2))
            elif command == "meta":
                result = client.get_meta()
                print(json.dumps(result, indent=2))
            elif command == "context":
                result = client.get_meta_and_asset_contexts()
                print(json.dumps(result, indent=2))
            elif command.startswith("active "):
                coin = command.split()[1].upper()
                result = client.get_active_asset_data(user_address, coin)
                print(json.dumps(result, indent=2))
            elif command == "fills":
                result = client.get_user_fills(user_address)
                print(json.dumps(result, indent=2))
            elif command == "orders":
                result = client.get_historical_orders(user_address)
                print(json.dumps(result, indent=2))
            elif command == "funding":
                result = client.get_user_funding(user_address)
                print(json.dumps(result, indent=2))
            elif command == "help":
                print("Available commands: mids, meta, context, active <coin>, fills, orders, funding, quit")
            else:
                print("❓ Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_client()
    else:
        demo_client()