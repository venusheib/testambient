# Embindexer API Documentation

API for accessing exchange and user-specific information on Embindexer.

**Base URL:** `https://embindexer.net/ember/api/dev/v1`

## Working Endpoints

### Retrieve meta and asset contexts

Returns margin tables and asset context information including funding rates, mark prices, and open interest.

**POST** `https://embindexer.net/ember/api/dev/v1/info`

#### Headers
| Name | Type | Description |
|------|------|-------------|
| Content-Type* | String | "application/json" |

#### Request Body
| Name | Type | Description |
|------|------|-------------|
| type* | String | "metaAndAssetCtxs" |

#### Response Sample
```json
[
  {
    "marginTables": [
      [
        50,
        {
          "description": "BTC",
          "marginTiers": [
            {
              "lowerBound": "0.0",
              "maxLeverage": 50
            }
          ]
        }
      ]
    ],
    "universe": [
      {
        "marginTableId": 50,
        "maxLeverage": 50,
        "name": "BTC",
        "szDecimals": 8
      }
    ]
  },
  [
    {
      "dayNtlVlm": "0",
      "funding": "0",
      "impactPxs": ["0", "0"],
      "markPx": "113799.500000",
      "midPx": "113799.500000",
      "openInterest": "0.01060000",
      "oraclePx": "113799.500000",
      "premium": "0",
      "prevDayPx": "0"
    }
  ]
]
```

---

### Retrieve all mid prices

Returns mid prices for all available trading pairs.

**POST** `https://embindexer.net/ember/api/dev/v1/info`

#### Headers
| Name | Type | Description |
|------|------|-------------|
| Content-Type* | String | "application/json" |

#### Request Body
| Name | Type | Description |
|------|------|-------------|
| type* | String | "allMids" |

#### Response Sample
```json
{
  "BTC": "113799.50000000"
}
```

---

### Retrieve perpetuals metadata

Returns universe and margin tables for perpetuals.

**POST** `https://embindexer.net/ember/api/dev/v1/info`

#### Headers
| Name | Type | Description |
|------|------|-------------|
| Content-Type* | String | "application/json" |

#### Request Body
| Name | Type | Description |
|------|------|-------------|
| type* | String | "meta" |

#### Response Sample
```json
{
  "marginTables": [
    [
      50,
      {
        "description": "BTC",
        "marginTiers": [
          {
            "lowerBound": "0.0",
            "maxLeverage": 50
          }
        ]
      }
    ]
  ],
  "universe": [
    {
      "marginTableId": 50,
      "maxLeverage": 50,
      "name": "BTC",
      "szDecimals": 8
    }
  ]
}
```

---

### Retrieve user's active asset data

Returns user's active asset data for a specific coin.

**POST** `https://embindexer.net/ember/api/dev/v1/info`

#### Headers
| Name | Type | Description |
|------|------|-------------|
| Content-Type* | String | "application/json" |

#### Request Body
| Name | Type | Description |
|------|------|-------------|
| type* | String | "activeAssetData" |
| user* | String | Address in Solana format (base58 encoded); e.g. AywrXuWFGa8Z9RMyum2BxeXpYL7kqGRFJDDXXJoxtw3e |
| coin* | String | Coin symbol, e.g. "BTC" |

#### Response Sample
```json
{
  "activeAssetData": "Sample response data"
}
```

---

## Endpoints with Empty Responses

The following endpoints are available but return empty responses for the tested user address:

### Retrieve historical funding rates

**POST** `https://embindexer.net/ember/api/dev/v1/info`

#### Headers
| Name | Type | Description |
|------|------|-------------|
| Content-Type* | String | "application/json" |

#### Request Body
| Name | Type | Description |
|------|------|-------------|
| type* | String | "fundingHistory" |

#### Response Sample
```json
null
```

---

### Retrieve a user's fills

Returns at most 2000 fills per response and only the 10000 most recent fills are available.

**POST** `https://embindexer.net/ember/api/dev/v1/info`

#### Headers
| Name | Type | Description |
|------|------|-------------|
| Content-Type* | String | "application/json" |

#### Request Body
| Name | Type | Description |
|------|------|-------------|
| type* | String | "userFills" |
| user* | String | Address in Solana format (base58 encoded); e.g. AywrXuWFGa8Z9RMyum2BxeXpYL7kqGRFJDDXXJoxtw3e |

#### Response Sample
```json
[]
```

---

### Retrieve a user's fills by time

Returns at most 2000 fills per response and only the 10000 most recent fills are available, filtered by time range.

**POST** `https://embindexer.net/ember/api/dev/v1/info`

#### Headers
| Name | Type | Description |
|------|------|-------------|
| Content-Type* | String | "application/json" |

#### Request Body
| Name | Type | Description |
|------|------|-------------|
| type* | String | "userFillsByTime" |
| user* | String | Address in Solana format (base58 encoded); e.g. AywrXuWFGa8Z9RMyum2BxeXpYL7kqGRFJDDXXJoxtw3e |
| startTime* | Integer | Start time in milliseconds, inclusive |
| endTime | Integer | End time in milliseconds, inclusive. Defaults to current time. |
| aggregateByTime | Boolean | When true, partial fills are combined when a crossing order gets filled by multiple different resting orders |

#### Response Sample
```json
[]
```

---

### Retrieve historical orders

Returns user's historical orders with status information.

**POST** `https://embindexer.net/ember/api/dev/v1/info`

#### Headers
| Name | Type | Description |
|------|------|-------------|
| Content-Type* | String | "application/json" |

#### Request Body
| Name | Type | Description |
|------|------|-------------|
| type* | String | "historicalOrders" |
| user* | String | Address in Solana format (base58 encoded); e.g. AywrXuWFGa8Z9RMyum2BxeXpYL7kqGRFJDDXXJoxtw3e |

#### Response Sample
```json
[]
```

---

### Retrieve user's funding history

Returns user's funding history.

**POST** `https://embindexer.net/ember/api/dev/v1/info`

#### Headers
| Name | Type | Description |
|------|------|-------------|
| Content-Type* | String | "application/json" |

#### Request Body
| Name | Type | Description |
|------|------|-------------|
| type* | String | "userFunding" |
| user* | String | Address in Solana format (base58 encoded); e.g. AywrXuWFGa8Z9RMyum2BxeXpYL7kqGRFJDDXXJoxtw3e |

#### Response Sample
```json
[]
```

---

## Failed Endpoints

The following endpoints returned errors and may require additional parameters or different configuration:

### Retrieve candle snapshot
- **Error:** 400 Client Error: Bad Request
- **Likely cause:** Missing required parameters (coin, interval, etc.)

### Retrieve clearing house state
- **Error:** Account with no activity
- **Likely cause:** User has no positions or trading activity

### Query user's portfolio
- **Error:** 400 Client Error: Bad Request  
- **Likely cause:** Missing required parameters or endpoint not supported

---

## Usage Examples

### Python

```python
import requests
import json

def call_embindexer_api(endpoint_type, user=None):
    url = "https://embindexer.net/ember/api/dev/v1/info"
    headers = {"Content-Type": "application/json"}
    payload = {"type": endpoint_type}
    
    if user:
        payload["user"] = user
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Get all mid prices
mids = call_embindexer_api("allMids")
print(json.dumps(mids, indent=2))

# Get user fills
user_address = "AywrXuWFGa8Z9RMyum2BxeXpYL7kqGRFJDDXXJoxtw3e"
fills = call_embindexer_api("userFills", user_address)
print(json.dumps(fills, indent=2))
```

### cURL

```bash
# Get meta and asset contexts
curl -X POST https://embindexer.net/ember/api/dev/v1/info \
  -H "Content-Type: application/json" \
  -d '{"type": "metaAndAssetCtxs"}'

# Get user fills
curl -X POST https://embindexer.net/ember/api/dev/v1/info \
  -H "Content-Type: application/json" \
  -d '{
    "type": "userFills",
    "user": "AywrXuWFGa8Z9RMyum2BxeXpYL7kqGRFJDDXXJoxtw3e"
  }'
```

---

## API Reference

For a complete interactive API reference with the ability to test endpoints, view the OpenAPI specification using:

- **Redocly Viewer:** `http://localhost:8000/redocly-viewer.html` (when running local server)
- **OpenAPI Spec:** `embindexer-redocly-spec.json`

## Testing

Run the comprehensive test suite to check all endpoints:

```bash
python test_all_endpoints.py
```

This will test all endpoints and provide a summary of working, empty, and failed endpoints.