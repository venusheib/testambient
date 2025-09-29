import requests
import json


def call_embindexer_api(endpoint_type, user=None):
    """
    Call the embindexer API with specified endpoint type
    
    Args:
        endpoint_type (str): The type of endpoint to call
        user (str, optional): User address for user-specific endpoints
    
    Returns:
        dict: API response data
    """
    url = "https://embindexer.net/ember/api/dev/v1/info"
    headers = {"Content-Type": "application/json"}
    payload = {"type": endpoint_type}

    if user:
        payload["user"] = user

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return None


# Example usage
if __name__ == "__main__":
    user_address = "AywrXuWFGa8Z9RMyum2BxeXpYL7kqGRFJDDXXJoxtw3e"

    # Call metaAndAssetCtxs endpoint
    meta_data = call_embindexer_api("metaAndAssetCtxs")
    if meta_data:
        print("Meta and Asset Contexts:")
        print(json.dumps(meta_data, indent=2))

    # Call allMids endpoint
    mids_data = call_embindexer_api("allMids")
    if mids_data:
        print("\nAll Mids:")
        print(json.dumps(mids_data, indent=2))

    # Call userFills endpoint
    user_fills = call_embindexer_api("userFills", user_address)
    if user_fills:
        print("\nUser Fills:")
        print(json.dumps(user_fills, indent=2))

    # Call userFillsByTime endpoint
    user_fills_by_time = call_embindexer_api("userFillsByTime", user_address)
    if user_fills_by_time:
        print("\nUser Fills By Time:")
        print(json.dumps(user_fills_by_time, indent=2))

    # Call clearinghouseState endpoint
    clearing_house_state = call_embindexer_api("clearinghouseState", user_address)
    if clearing_house_state:
        print("\nClearing House State:")
        print(json.dumps(clearing_house_state, indent=2))

    # Call historicalOrders endpoint
    historical_orders = call_embindexer_api("historicalOrders", user_address)
    if historical_orders:
        print("\nHistorical Orders:")
        print(json.dumps(historical_orders, indent=2))
    
    # Call meta endpoint
    meta_data = call_embindexer_api("meta")
    if meta_data:
        print("\nMeta:")
        print(json.dumps(meta_data, indent=2))
    
    # Call userFunding endpoint
    user_funding = call_embindexer_api("userFunding", user_address)
    if user_funding:
        print("\nUser Funding:")
        print(json.dumps(user_funding, indent=2))
    
    # Call fundingHistory endpoint
    funding_history = call_embindexer_api("fundingHistory")
    if funding_history:
        print("\nFunding History:")
        print(json.dumps(funding_history, indent=2))
    
    # Call activeAssetData endpoint (needs coin parameter)
    # Note: This would need additional parameters in a real implementation
    
    # Call candleSnapshot endpoint
    candle_snapshot = call_embindexer_api("candleSnapshot")
    if candle_snapshot:
        print("\nCandle Snapshot:")
        print(json.dumps(candle_snapshot, indent=2))
    
    # Call portfolio endpoint
    portfolio = call_embindexer_api("portfolio", user_address)
    if portfolio:
        print("\nPortfolio:")
        print(json.dumps(portfolio, indent=2))
