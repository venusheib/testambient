# Ambient Info API Documentation

Complete documentation for all Ambient Info API endpoints with response schemas.

## Base Configuration

```
API Base URL: https://embindexer.net/ember/api/dev/v1
Info Endpoint: {BASE_URL}/info
Content-Type: application/json
Method: POST
```

## Authentication

Info endpoints are **read-only** and do **NOT** require signing or authentication.

---

## 1. All Mids

Get mid prices for all available coins.

### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ | Must be `"allMids"` |

### Example Request
```json
{
  "type": "allMids"
}
```

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `{COIN}` | string | Mid price for each coin (e.g., "BTC": "109476.50000000") |

### Example Response
```json
{
  "BTC": "109476.50000000"
}
```

---

## 2. User Open Orders

Get all open orders for a specific user.

### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ | Must be `"openOrders"` |
| `user` | string | ✅ | Base58 Solana wallet public key |

### Example Request
```json
{
  "type": "openOrders",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

### Response Schema

Array of order objects:

| Field | Type | Description |
|-------|------|-------------|
| `coin` | string | Asset symbol (e.g., "BTC") |
| `limitPx` | string | Order limit price |
| `oid` | integer | Order ID |
| `origSz` | string | Original order size |
| `side` | string | Order side: "B" (buy) or "A" (sell) |
| `sz` | string | Current remaining size |
| `timestamp` | integer | Order timestamp in milliseconds |

### Example Response
```json
[
  {
    "coin": "BTC",
    "limitPx": "112000.000000",
    "oid": 1758796565225,
    "origSz": "0.00010000",
    "side": "A",
    "sz": "0.00010000",
    "timestamp": 1758796565000
  }
]
```

---

## 3. L2 Book State

Get order book levels for a specific coin.

### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ | Must be `"l2Book"` |
| `coin` | string | ✅ | Coin symbol (e.g., "BTC") |
| `nSigFigs` | integer | ❌ | Aggregate to N significant figures (2-5, null for full precision) |

### Example Request
```json
{
  "type": "l2Book",
  "coin": "BTC"
}
```

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `coin` | string | Asset symbol |
| `levels` | array | Two-element array: [bids, asks] |
| `levels[0]` | array | Bid levels (buy orders) |
| `levels[1]` | array | Ask levels (sell orders) |
| `levels[0/1][].n` | integer | Number of orders at this level |
| `levels[0/1][].px` | string | Price level |
| `levels[0/1][].sz` | string | Total size at this level |
| `time` | integer | Timestamp in milliseconds |

### Example Response
```json
{
  "coin": "BTC",
  "levels": [
    [
      {
        "n": 3,
        "px": "109476.000000",
        "sz": "0.96865000"
      }
    ],
    [
      {
        "n": 71,
        "px": "109477.000000",
        "sz": "39.25326000"
      }
    ]
  ],
  "time": 1758913979250
}
```

---

## 4. User Fills

Get user's trading fills (executions).

### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ | Must be `"userFills"` |
| `user` | string | ✅ | Base58 Solana wallet public key |
| `aggregateByTime` | boolean | ❌ | Combine partial fills when crossing order filled by multiple resting orders |

### Example Request
```json
{
  "type": "userFills",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
  "aggregateByTime": false
}
```

### Response Schema

Array of fill objects (max 2000):

| Field | Type | Description |
|-------|------|-------------|
| `closedPnl` | string | Closed PnL from this fill |
| `coin` | string | Asset symbol |
| `crossed` | boolean | Whether this was a crossing order |
| `dir` | string | Position direction: "Open Long", "Close Long", etc. |
| `fee` | string | Fee paid |
| `feeToken` | string | Fee token symbol (e.g., "USDC") |
| `hash` | string | Transaction hash |
| `oid` | integer | Order ID |
| `px` | string | Fill price |
| `side` | string | Order side: "B" (buy) or "A" (sell) |
| `startPosition` | string | Position size before this fill |
| `sz` | string | Fill size |
| `tid` | integer | Trade ID |
| `time` | integer | Fill timestamp in milliseconds |

### Example Response
```json
[
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000000000001771",
    "oid": 6001,
    "px": "112904.000025",
    "side": "B",
    "startPosition": "0.00000000",
    "sz": "0.00010000",
    "tid": 381409047,
    "time": 1758632269000
  }
]
```

---

## 5. User Fills By Time

Get user's fills within a specific time range.

### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ | Must be `"userFillsByTime"` |
| `user` | string | ✅ | Base58 Solana wallet public key |
| `startTime` | integer | ✅ | Start time in milliseconds (inclusive) |
| `endTime` | integer | ❌ | End time in milliseconds (inclusive, defaults to current time) |
| `aggregateByTime` | boolean | ❌ | Combine partial fills |

### Example Request
```json
{
  "type": "userFillsByTime",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
  "startTime": 1758827558523,
  "endTime": 1758913958523,
  "aggregateByTime": true
}
```

### Response Schema

Same as `userFills` (max 2000 fills, only 10000 most recent fills available).

---

## 6. User Perpetuals Summary

Get user's perpetuals summary including positions and margin information.

### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ | Must be `"clearinghouseState"` |
| `user` | string | ✅ | Base58 Solana wallet public key |

### Example Request
```json
{
  "type": "clearinghouseState",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `assetPositions` | array | Array of asset position objects |
| `assetPositions[].position` | object | Position details |
| `assetPositions[].position.coin` | string | Asset symbol |
| `assetPositions[].position.cumFunding` | object | Cumulative funding |
| `assetPositions[].position.cumFunding.allTime` | string | All-time cumulative funding |
| `assetPositions[].position.cumFunding.sinceChange` | string | Funding since last change |
| `assetPositions[].position.cumFunding.sinceOpen` | string | Funding since position opened |
| `assetPositions[].position.entryPx` | string | Average entry price |
| `assetPositions[].position.leverage` | object | Leverage configuration |
| `assetPositions[].position.leverage.type` | string | Leverage type: "cross" or "isolated" |
| `assetPositions[].position.leverage.value` | integer | Leverage value |
| `assetPositions[].position.liquidationPx` | string | Liquidation price |
| `assetPositions[].position.marginUsed` | string | Margin used for this position |
| `assetPositions[].position.maxLeverage` | integer | Maximum allowed leverage |
| `assetPositions[].position.positionValue` | string | Current position value |
| `assetPositions[].position.returnOnEquity` | string | ROE percentage |
| `assetPositions[].position.szi` | string | Position size (signed) |
| `assetPositions[].position.unrealizedPnl` | string | Unrealized PnL |
| `assetPositions[].type` | string | Position type (e.g., "oneWay") |
| `crossMaintenanceMarginUsed` | string | Cross maintenance margin used |
| `crossMarginSummary` | object | Cross margin summary |
| `crossMarginSummary.accountValue` | string | Total account value |
| `crossMarginSummary.totalMarginUsed` | string | Total margin used |
| `crossMarginSummary.totalNtlPos` | string | Total notional position |
| `crossMarginSummary.totalRawUsd` | string | Total raw USD |
| `marginSummary` | object | Overall margin summary (same structure as crossMarginSummary) |
| `time` | integer | Timestamp in milliseconds |
| `withdrawable` | string | Amount available for withdrawal |

### Example Response
```json
{
  "assetPositions": [
    {
      "position": {
        "coin": "BTC",
        "cumFunding": {
          "allTime": "0",
          "sinceChange": "0",
          "sinceOpen": "0"
        },
        "entryPx": "109210.000824",
        "leverage": {
          "type": "cross",
          "value": 50
        },
        "liquidationPx": "98288.578199",
        "marginUsed": "18.39",
        "maxLeverage": 50,
        "positionValue": "919.64",
        "returnOnEquity": "12.17%",
        "szi": "0.00840032",
        "unrealizedPnl": "2.24"
      },
      "type": "oneWay"
    }
  ],
  "crossMaintenanceMarginUsed": "9.20",
  "crossMarginSummary": {
    "accountValue": "102.24",
    "totalMarginUsed": "18.39",
    "totalNtlPos": "919.64",
    "totalRawUsd": "100.00"
  },
  "marginSummary": {
    "accountValue": "102.24",
    "totalMarginUsed": "18.39",
    "totalNtlPos": "919.64",
    "totalRawUsd": "100.00"
  },
  "time": 1758913985939,
  "withdrawable": "83.85"
}
```

---

## 7. Perpetuals Asset Contexts

Get perpetuals metadata including mark price, funding, open interest, etc.

### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ | Must be `"metaAndAssetCtxs"` |

### Example Request
```json
{
  "type": "metaAndAssetCtxs"
}
```

### Response Schema

Two-element array: [meta, assetCtxs]

**Meta (index 0):**
| Field | Type | Description |
|-------|------|-------------|
| `marginTables` | array | Array of [tableId, tableConfig] pairs |
| `marginTables[][0]` | integer | Margin table ID |
| `marginTables[][1].description` | string | Asset description |
| `marginTables[][1].marginTiers` | array | Margin tier configurations |
| `marginTables[][1].marginTiers[].lowerBound` | string | Lower bound for this tier |
| `marginTables[][1].marginTiers[].maxLeverage` | integer | Max leverage for this tier |
| `universe` | array | Universe asset definitions |
| `universe[].marginTableId` | integer | Reference to margin table |
| `universe[].maxLeverage` | integer | Maximum leverage |
| `universe[].name` | string | Asset name |
| `universe[].szDecimals` | integer | Size decimal precision |

**Asset Contexts (index 1):**
| Field | Type | Description |
|-------|------|-------------|
| `dayNtlVlm` | string | 24h notional volume |
| `funding` | string | Current funding rate |
| `impactPxs` | array | Impact prices [bid, ask] |
| `markPx` | string | Mark price |
| `midPx` | string | Mid price |
| `openInterest` | string | Open interest |
| `oraclePx` | string | Oracle price |
| `premium` | string | Premium |
| `prevDayPx` | string | Previous day price |

### Example Response
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
      "impactPxs": [
        "0",
        "0"
      ],
      "markPx": "112645.500000",
      "midPx": "112645.500000",
      "openInterest": "0.01060000",
      "oraclePx": "112645.500000",
      "premium": "0",
      "prevDayPx": "0"
    }
  ]
]
```

---

## 8. Perpetuals Metadata

Get universe and margin tables for perpetuals.

### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ | Must be `"meta"` |

### Example Request
```json
{
  "type": "meta"
}
```

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `marginTables` | array | Array of [tableId, tableConfig] pairs |
| `marginTables[][0]` | integer | Margin table ID |
| `marginTables[][1].description` | string | Asset description |
| `marginTables[][1].marginTiers` | array | Margin tier configurations |
| `marginTables[][1].marginTiers[].lowerBound` | string | Lower bound for this tier |
| `marginTables[][1].marginTiers[].maxLeverage` | integer | Max leverage for this tier |
| `universe` | array | Universe asset definitions |
| `universe[].marginTableId` | integer | Reference to margin table |
| `universe[].maxLeverage` | integer | Maximum leverage |
| `universe[].name` | string | Asset name |
| `universe[].szDecimals` | integer | Size decimal precision |

### Example Response
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

## 9. User Active Asset Data

Get user's active asset data for a specific coin.

### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ | Must be `"activeAssetData"` |
| `user` | string | ✅ | Base58 Solana wallet public key |
| `coin` | string | ✅ | Coin symbol (e.g., "BTC") |

### Example Request
```json
{
  "type": "activeAssetData",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
  "coin": "BTC"
}
```

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `availableToTrade` | array | Available amounts to trade [long, short] |
| `coin` | string | Asset symbol |
| `leverage` | object | Leverage configuration |
| `leverage.type` | string | Leverage type: "cross" or "isolated" |
| `leverage.value` | integer | Leverage value |
| `markPx` | string | Current mark price |
| `maxTradeSzs` | array | Maximum trade sizes [long, short] |
| `user` | string | User public key |

### Example Response
```json
{
  "availableToTrade": [
    "0.00000000",
    "0.00000000"
  ],
  "coin": "BTC",
  "leverage": {
    "type": "cross",
    "value": 101
  },
  "markPx": "113840.500000",
  "maxTradeSzs": [
    "0.00000000",
    "0.00000000"
  ],
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

---

## 10. User Historical Orders

Get user's historical orders.

### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ | Must be `"historicalOrders"` |
| `user` | string | ✅ | Base58 Solana wallet public key |

### Example Request
```json
{
  "type": "historicalOrders",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

### Response Schema

Array of historical order objects:

| Field | Type | Description |
|-------|------|-------------|
| `order` | object | Order details |
| `order.children` | array | Child orders (usually empty) |
| `order.cloid` | string/null | Client order ID |
| `order.coin` | string | Asset symbol |
| `order.isPositionTpsl` | boolean | Is position TP/SL order |
| `order.isTrigger` | boolean | Is trigger order |
| `order.limitPx` | string | Limit price |
| `order.oid` | integer | Order ID |
| `order.orderType` | string | Order type (e.g., "Limit") |
| `order.origSz` | string | Original order size |
| `order.reduceOnly` | boolean | Reduce only flag |
| `order.side` | string | Order side: "B" (buy) or "A" (sell) |
| `order.sz` | string | Current remaining size |
| `order.tif` | string | Time in force |
| `order.timestamp` | integer | Order timestamp |
| `order.triggerCondition` | string | Trigger condition |
| `order.triggerPx` | string | Trigger price |
| `status` | string | Order status |
| `statusTimestamp` | integer | Status timestamp |

### Example Response
```json
[
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "150000.000000",
      "oid": 6011,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758690800000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758690800000
  }
]
```

---

## 11. Query Order Status

Query order status by Order ID (OID) or Client Order ID (CLOID).

### Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ | Must be `"orderStatus"` |
| `user` | string | ✅ | Base58 Solana wallet public key |
| `orderId` | integer/string | ✅ | Order ID (integer) or Client Order ID (string) |

### Example Request (by OID)
```json
{
  "type": "orderStatus",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
  "orderId": 1758872506411
}
```

### Example Request (by CLOID)
```json
{
  "type": "orderStatus",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
  "orderId": "custom_order_123"
}
```

### Response Schema

**Order Found:**
| Field | Type | Description |
|-------|------|-------------|
| `order` | object | Order details |
| `order.avgFillPx` | string | Average fill price |
| `order.coin` | string | Asset symbol |
| `order.filledSz` | string | Total filled size |
| `order.limitPx` | string | Order limit price |
| `order.orderId` | integer | Order ID |
| `order.orderType` | string | Order type: "limit", "market", etc. |
| `order.postOnly` | boolean | Post-only flag |
| `order.reduceOnly` | boolean | Reduce-only flag |
| `order.side` | string | Order side: "B" (buy) or "A" (sell) |
| `order.sz` | string | Order size |
| `order.timestamp` | integer | Order timestamp |
| `status` | string | Order status |
| `statusTimestamp` | integer | Status timestamp |

**Order Not Found:**
| Field | Type | Description |
|-------|------|-------------|
| `order` | null | null when order not found |
| `status` | string | "notFound" |
| `statusTimestamp` | integer | Query timestamp |

### Order Status Values

| Status | Description |
|--------|-------------|
| `open` | Order is active and working |
| `filled` | Order completely filled |
| `canceled` | Order canceled by user |
| `triggered` | Trigger order activated |
| `rejected` | Order rejected at placement |
| `notFound` | Order not found in system |
| `marginCanceled` | Canceled due to insufficient margin |
| `reduceOnlyCanceled` | Reduce-only order that doesn't reduce position |

### Example Response (Found)
```json
{
  "order": {
    "avgFillPx": "0",
    "coin": "BTC",
    "filledSz": "0.00000000",
    "limitPx": "105000.000000",
    "orderId": 1758872506411,
    "orderType": "limit",
    "postOnly": false,
    "reduceOnly": false,
    "side": "B",
    "sz": "0.00004000",
    "timestamp": 1758872459760
  },
  "status": "open",
  "statusTimestamp": 1758872453000
}
```

### Example Response (Not Found)
```json
{
  "order": null,
  "status": "notFound",
  "statusTimestamp": 1758872482787
}
```

---

## Error Responses

### Invalid Request Type (400)
```json
{
  "error": "Unknown request type: invalidType"
}
```

### Invalid User Format (400)
```json
{
  "error": "Invalid request"
}
```

### Common Error Codes

| Error | Description | Solution |
|-------|-------------|----------|
| `Unknown request type: {type}` | Invalid endpoint type | Use valid type from documentation |
| `Invalid request` | Malformed request | Check required fields and formats |
| Missing user field | User parameter required but missing | Include valid Base58 public key |

---

## Important Notes

1. **No Authentication**: Info endpoints are read-only and don't require signing
2. **Rate Limits**: Standard rate limits apply
3. **Data Freshness**: Market data is real-time, user data may have slight delays
4. **Pagination**: Some endpoints return limited results (e.g., max 2000 fills)
5. **Time Ranges**: Historical data availability varies by endpoint
6. **Address Format**: Always use Base58 Solana public keys for user addresses
7. **Decimal Precision**: Prices and sizes returned as strings to preserve precision
8. **Empty Results**: Endpoints return empty arrays when no data is available

---

## Python Implementation Example

```python
import requests

AMBIENT_URL = "https://embindexer.net/ember/api/dev/v1"
TEST_USER = "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"

def ambient_info_request(payload):
    response = requests.post(f"{AMBIENT_URL}/info", json=payload)
    response.raise_for_status()
    return response.json()

# Get all mid prices
mids = ambient_info_request({"type": "allMids"})
print(f"BTC mid price: {mids['BTC']}")

# Get user's open orders
orders = ambient_info_request({"type": "openOrders", "user": TEST_USER})
print(f"User has {len(orders)} open orders")

# Get L2 book for BTC
book = ambient_info_request({"type": "l2Book", "coin": "BTC"})
print(f"Best bid: {book['levels'][0][0]['px'] if book['levels'][0] else 'N/A'}")
print(f"Best ask: {book['levels'][1][0]['px'] if book['levels'][1] else 'N/A'}")

# Get user's perpetuals summary
state = ambient_info_request({"type": "clearinghouseState", "user": TEST_USER})
print(f"Account value: {state['marginSummary']['accountValue']}")

# Query order status
status = ambient_info_request({
    "type": "orderStatus", 
    "user": TEST_USER, 
    "orderId": 1758872506411
})
print(f"Order status: {status['status']}")
```