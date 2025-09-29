#!/usr/bin/env python3
"""
Collect detailed responses from all Ambient Finance info endpoints
for documentation purposes.
"""

import requests
import json
from typing import Dict, Any, Optional

def test_endpoint(endpoint_type: str, user: Optional[str] = None, coin: Optional[str] = None) -> Dict[str, Any]:
    """Test an embindexer API endpoint and return detailed results"""
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
        
        return {
            "success": True,
            "status_code": response.status_code,
            "payload": payload,
            "response": data
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "payload": payload,
            "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        }

def collect_all_responses():
    """Collect responses from all endpoints"""
    
    user_address = "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
    
    endpoints = [
        # Market Data endpoints
        {"name": "Meta and Asset Contexts", "type": "metaAndAssetCtxs", "category": "Market Data"},
        {"name": "All Mids", "type": "allMids", "category": "Market Data"},
        {"name": "Meta", "type": "meta", "category": "Market Data"},
        {"name": "Funding History", "type": "fundingHistory", "category": "Market Data"},
        {"name": "Candle Snapshot", "type": "candleSnapshot", "category": "Market Data"},
        
        # User Data endpoints
        {"name": "User Fills", "type": "userFills", "user": user_address, "category": "User Data"},
        {"name": "User Fills By Time", "type": "userFillsByTime", "user": user_address, "category": "User Data"},
        {"name": "Clearing House State", "type": "clearinghouseState", "user": user_address, "category": "User Data"},
        {"name": "Historical Orders", "type": "historicalOrders", "user": user_address, "category": "User Data"},
        {"name": "User Funding", "type": "userFunding", "user": user_address, "category": "User Data"},
        {"name": "Portfolio", "type": "portfolio", "user": user_address, "category": "User Data"},
        {"name": "Active Asset Data", "type": "activeAssetData", "user": user_address, "coin": "BTC", "category": "User Data"},
        
        # Additional endpoints to try
        {"name": "Order Status", "type": "orderStatus", "user": user_address, "category": "User Data"},
        {"name": "User State", "type": "userState", "user": user_address, "category": "User Data"},
        {"name": "Market Summary", "type": "marketSummary", "category": "Market Data"},
        {"name": "L2 Book", "type": "l2Book", "coin": "BTC", "category": "Market Data"},
    ]
    
    results = {}
    
    print("🔍 Collecting responses from all Ambient Finance info endpoints...\n")
    
    for endpoint in endpoints:
        endpoint_name = endpoint["name"]
        endpoint_type = endpoint["type"]
        user = endpoint.get("user")
        coin = endpoint.get("coin")
        category = endpoint["category"]
        
        print(f"Testing {endpoint_name} ({endpoint_type})...", end=" ")
        
        result = test_endpoint(endpoint_type, user, coin)
        results[endpoint_type] = {
            "name": endpoint_name,
            "category": category,
            "result": result
        }
        
        if result["success"]:
            print("✅")
        else:
            print("❌")
    
    return results

def format_response_for_readme(endpoint_type: str, endpoint_info: Dict[str, Any]) -> str:
    """Format endpoint response for README documentation"""
    name = endpoint_info["name"]
    category = endpoint_info["category"]
    result = endpoint_info["result"]
    
    output = f"## {name} (`{endpoint_type}`)\n\n"
    output += f"**Category:** {category}\n\n"
    
    if result["success"]:
        payload = result["payload"]
        response = result["response"]
        
        output += f"**Request Payload:**\n```json\n{json.dumps(payload, indent=2)}\n```\n\n"
        output += f"**Response ({result['status_code']}):**\n```json\n{json.dumps(response, indent=2)}\n```\n\n"
        
        # Add summary
        if isinstance(response, list):
            output += f"**Summary:** Returns an array with {len(response)} items\n\n"
        elif isinstance(response, dict):
            keys = list(response.keys())
            output += f"**Summary:** Returns object with keys: {', '.join(keys[:5])}{', ...' if len(keys) > 5 else ''}\n\n"
    else:
        output += f"**Status:** Failed with error: {result['error']}\n"
        if result.get('status_code'):
            output += f"**HTTP Status Code:** {result['status_code']}\n"
        output += f"**Request Payload:**\n```json\n{json.dumps(result['payload'], indent=2)}\n```\n\n"
    
    output += "---\n\n"
    return output

if __name__ == "__main__":
    # Collect all responses
    all_results = collect_all_responses()
    
    print(f"\n📋 Collected {len(all_results)} endpoint responses")
    print("✍️  Generating README documentation...\n")
    
    # Generate README content
    readme_content = """# Ambient Finance Info API Endpoints - Complete Response Documentation

This document contains actual API responses from all Ambient Finance info endpoints for testing and integration purposes.

**Base URL:** `https://embindexer.net/ember/api/dev/v1/info`  
**Method:** POST  
**Content-Type:** application/json

**Test User Address:** `5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK`

---

"""
    
    # Add working endpoints first
    working_endpoints = []
    failed_endpoints = []
    
    for endpoint_type, info in all_results.items():
        if info["result"]["success"]:
            working_endpoints.append((endpoint_type, info))
        else:
            failed_endpoints.append((endpoint_type, info))
    
    if working_endpoints:
        readme_content += "# ✅ Working Endpoints\n\n"
        for endpoint_type, info in working_endpoints:
            readme_content += format_response_for_readme(endpoint_type, info)
    
    if failed_endpoints:
        readme_content += "# ❌ Failed/Empty Endpoints\n\n"
        for endpoint_type, info in failed_endpoints:
            readme_content += format_response_for_readme(endpoint_type, info)
    
    readme_content += """
## Usage Examples

### Python
```python
import requests

def query_ambient_info(endpoint_type, user=None, coin=None):
    url = "https://embindexer.net/ember/api/dev/v1/info"
    payload = {"type": endpoint_type}
    
    if user:
        payload["user"] = user
    if coin:
        payload["coin"] = coin
        
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    return response.json()

# Example: Get market metadata
meta = query_ambient_info("meta")

# Example: Get user's active asset data
asset_data = query_ambient_info("activeAssetData", user="5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK", coin="BTC")
```

### JavaScript
```javascript
async function queryAmbientInfo(endpointType, user = null, coin = null) {
    const payload = { type: endpointType };
    
    if (user) payload.user = user;
    if (coin) payload.coin = coin;
    
    const response = await fetch('https://embindexer.net/ember/api/dev/v1/info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    
    return await response.json();
}

// Example: Get all mids
const mids = await queryAmbientInfo('allMids');
```

### cURL
```bash
# Get meta information
curl -X POST https://embindexer.net/ember/api/dev/v1/info \\
  -H "Content-Type: application/json" \\
  -d '{"type": "meta"}'

# Get user fills
curl -X POST https://embindexer.net/ember/api/dev/v1/info \\
  -H "Content-Type: application/json" \\
  -d '{"type": "userFills", "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"}'
```

---

**Generated on:** """ + str(json.loads(json.dumps({"timestamp": "auto-generated"}))) + """
**Total Endpoints Tested:** """ + str(len(all_results)) + """
**Working Endpoints:** """ + str(len(working_endpoints)) + """
**Failed Endpoints:** """ + str(len(failed_endpoints)) + """
"""
    
    # Save to file
    with open("../docs/AMBIENT_INFO_API_RESPONSES.md", "w") as f:
        f.write(readme_content)
    
    print("✅ README generated: AMBIENT_INFO_API_RESPONSES.md")
    print(f"📊 Working endpoints: {len(working_endpoints)}")
    print(f"❌ Failed endpoints: {len(failed_endpoints)}")