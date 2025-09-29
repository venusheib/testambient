# Ambient Finance Info API Endpoints - Complete Response Documentation

This document contains actual API responses from all Ambient Finance info endpoints for testing and integration purposes.

**Base URL:** `https://embindexer.net/ember/api/dev/v1/info`  
**Method:** POST  
**Content-Type:** application/json

**Test User Address:** `5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK`

---

# ✅ Working Endpoints

## Meta and Asset Contexts (`metaAndAssetCtxs`)

**Category:** Market Data

**Request Payload:**
```json
{
  "type": "metaAndAssetCtxs"
}
```

**Response (200):**
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
      "markPx": "114100.500000",
      "midPx": "114100.500000",
      "openInterest": "0.01853032",
      "oraclePx": "114100.500000",
      "premium": "0",
      "prevDayPx": "0"
    }
  ]
]
```

**Summary:** Returns an array with 2 items

---

## All Mids (`allMids`)

**Category:** Market Data

**Request Payload:**
```json
{
  "type": "allMids"
}
```

**Response (200):**
```json
{
  "BTC": "114100.50000000"
}
```

**Summary:** Returns object with keys: BTC

---

## Meta (`meta`)

**Category:** Market Data

**Request Payload:**
```json
{
  "type": "meta"
}
```

**Response (200):**
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

**Summary:** Returns object with keys: marginTables, universe

---

## Funding History (`fundingHistory`)

**Category:** Market Data

**Request Payload:**
```json
{
  "type": "fundingHistory"
}
```

**Response (200):**
```json
[]
```

**Summary:** Returns an array with 0 items

---

## User Fills (`userFills`)

**Category:** User Data

**Request Payload:**
```json
{
  "type": "userFills",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

**Response (200):**
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
  },
  {
    "closedPnl": "0.000699",
    "coin": "BTC",
    "crossed": false,
    "dir": "Close Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000000000001772",
    "oid": 6002,
    "px": "112910.999975",
    "side": "A",
    "startPosition": "0.00010000",
    "sz": "0.00010000",
    "tid": 381449530,
    "time": 1758633848000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000000000001773",
    "oid": 6003,
    "px": "112716.000025",
    "side": "B",
    "startPosition": "0.00000000",
    "sz": "0.00010000",
    "tid": 381483128,
    "time": 1758635152000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x000000000000000000000000000000000000000000000000000000000000177a",
    "oid": 6010,
    "px": "112173.000025",
    "side": "B",
    "startPosition": "0.00010000",
    "sz": "0.00010000",
    "tid": 382880305,
    "time": 1758690765000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x000000000000000000000000000000000000000000000000000000000000177b",
    "oid": 6011,
    "px": "112173.000025",
    "side": "B",
    "startPosition": "0.00020000",
    "sz": "0.00010000",
    "tid": 382882161,
    "time": 1758690800000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019981f9315b",
    "oid": 1758822216027,
    "px": "109369.000025",
    "side": "B",
    "startPosition": "0.00030000",
    "sz": "0.00005000",
    "tid": 1758822596182197,
    "time": 1758822216000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019981fc2759",
    "oid": 1758822410073,
    "px": "109335.000025",
    "side": "B",
    "startPosition": "0.00035000",
    "sz": "0.00005000",
    "tid": 1758822790233049,
    "time": 1758822410000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019985b54ecd",
    "oid": 1758884875981,
    "px": "108742.000025",
    "side": "B",
    "startPosition": "0.00040000",
    "sz": "0.00092000",
    "tid": 1758885257702542,
    "time": 1758884876000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000001",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019985d3e2a4",
    "oid": 1758886879908,
    "px": "109006.000025",
    "side": "B",
    "startPosition": "0.00132000",
    "sz": "0.00220000",
    "tid": 1758887261679817,
    "time": 1758886887000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000002",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019985d4d3a4",
    "oid": 1758886941604,
    "px": "109042.000025",
    "side": "B",
    "startPosition": "0.00352000",
    "sz": "0.00370000",
    "tid": 1758887323377419,
    "time": 1758886951000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000001",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019985d601a9",
    "oid": 1758887018921,
    "px": "109044.000025",
    "side": "B",
    "startPosition": "0.00722000",
    "sz": "0.00118032",
    "tid": 1758887400696116,
    "time": 1758887019000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x000000000000000000000000000000000000000000000000000001999490d332",
    "oid": 1759134143282,
    "px": "112023.000025",
    "side": "B",
    "startPosition": "0.00840032",
    "sz": "0.00036000",
    "tid": 1759134531234584,
    "time": 1759134143000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019995e5eb02",
    "oid": 1759156497154,
    "px": "113761.000025",
    "side": "B",
    "startPosition": "0.00876032",
    "sz": "0.00036000",
    "tid": 1759156885665376,
    "time": 1759156497000
  },
  {
    "closedPnl": "3.862963",
    "coin": "BTC",
    "crossed": false,
    "dir": "Close Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019995e60dfa",
    "oid": 1759156506106,
    "px": "113759.999975",
    "side": "A",
    "startPosition": "0.00912032",
    "sz": "0.00089000",
    "tid": 1759156894617602,
    "time": 1759156506000
  }
]
```

**Summary:** Returns an array with 14 items

---

## User Fills By Time (`userFillsByTime`)

**Category:** User Data

**Request Payload:**
```json
{
  "type": "userFillsByTime",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

**Response (200):**
```json
[
  {
    "closedPnl": "3.862963",
    "coin": "BTC",
    "crossed": false,
    "dir": "Close Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019995e60dfa",
    "oid": 1759156506106,
    "px": "113759.999975",
    "side": "A",
    "startPosition": "0.00912032",
    "sz": "0.00089000",
    "tid": 1759156894617602,
    "time": 1759156506000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019995e5eb02",
    "oid": 1759156497154,
    "px": "113761.000025",
    "side": "B",
    "startPosition": "0.00876032",
    "sz": "0.00036000",
    "tid": 1759156885665376,
    "time": 1759156497000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x000000000000000000000000000000000000000000000000000001999490d332",
    "oid": 1759134143282,
    "px": "112023.000025",
    "side": "B",
    "startPosition": "0.00840032",
    "sz": "0.00036000",
    "tid": 1759134531234584,
    "time": 1759134143000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000001",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019985d601a9",
    "oid": 1758887018921,
    "px": "109044.000025",
    "side": "B",
    "startPosition": "0.00722000",
    "sz": "0.00118032",
    "tid": 1758887400696116,
    "time": 1758887019000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000002",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019985d4d3a4",
    "oid": 1758886941604,
    "px": "109042.000025",
    "side": "B",
    "startPosition": "0.00352000",
    "sz": "0.00370000",
    "tid": 1758887323377419,
    "time": 1758886951000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000001",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019985d3e2a4",
    "oid": 1758886879908,
    "px": "109006.000025",
    "side": "B",
    "startPosition": "0.00132000",
    "sz": "0.00220000",
    "tid": 1758887261679817,
    "time": 1758886887000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019985b54ecd",
    "oid": 1758884875981,
    "px": "108742.000025",
    "side": "B",
    "startPosition": "0.00040000",
    "sz": "0.00092000",
    "tid": 1758885257702542,
    "time": 1758884876000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019981fc2759",
    "oid": 1758822410073,
    "px": "109335.000025",
    "side": "B",
    "startPosition": "0.00035000",
    "sz": "0.00005000",
    "tid": 1758822790233049,
    "time": 1758822410000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000019981f9315b",
    "oid": 1758822216027,
    "px": "109369.000025",
    "side": "B",
    "startPosition": "0.00030000",
    "sz": "0.00005000",
    "tid": 1758822596182197,
    "time": 1758822216000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x000000000000000000000000000000000000000000000000000000000000177b",
    "oid": 6011,
    "px": "112173.000025",
    "side": "B",
    "startPosition": "0.00020000",
    "sz": "0.00010000",
    "tid": 382882161,
    "time": 1758690800000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x000000000000000000000000000000000000000000000000000000000000177a",
    "oid": 6010,
    "px": "112173.000025",
    "side": "B",
    "startPosition": "0.00010000",
    "sz": "0.00010000",
    "tid": 382880305,
    "time": 1758690765000
  },
  {
    "closedPnl": "0.000000",
    "coin": "BTC",
    "crossed": false,
    "dir": "Open Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000000000001773",
    "oid": 6003,
    "px": "112716.000025",
    "side": "B",
    "startPosition": "0.00000000",
    "sz": "0.00010000",
    "tid": 381483128,
    "time": 1758635152000
  },
  {
    "closedPnl": "0.000699",
    "coin": "BTC",
    "crossed": false,
    "dir": "Close Long",
    "fee": "0.000000",
    "feeToken": "USDC",
    "hash": "0x0000000000000000000000000000000000000000000000000000000000001772",
    "oid": 6002,
    "px": "112910.999975",
    "side": "A",
    "startPosition": "0.00010000",
    "sz": "0.00010000",
    "tid": 381449530,
    "time": 1758633848000
  },
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

**Summary:** Returns an array with 14 items

---

## Clearing House State (`clearinghouseState`)

**Category:** User Data

**Request Payload:**
```json
{
  "type": "clearinghouseState",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

**Response (200):**
```json
make t
```

**Summary:** Returns object with keys: assetPositions, crossMaintenanceMarginUsed, crossMarginSummary, marginSummary, time, ...

---

## Historical Orders (`historicalOrders`)

**Category:** User Data

**Request Payload:**
```json
{
  "type": "historicalOrders",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

**Response (200):**
```json
[
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "103082.000000",
      "oid": 1759156506106,
      "orderType": "Limit",
      "origSz": "0.00089000",
      "reduceOnly": false,
      "side": "A",
      "sz": "0.00089000",
      "tif": "Gtc",
      "timestamp": 1759156506000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1759156506000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "121010.000000",
      "oid": 1759156497154,
      "orderType": "Limit",
      "origSz": "0.00036000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00036000",
      "tif": "Gtc",
      "timestamp": 1759156497000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1759156497000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "108000.000000",
      "oid": 1759134907388,
      "orderType": "Limit",
      "origSz": "0.00006000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00006000",
      "tif": "Gtc",
      "timestamp": 1759134907000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1759134907000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "121010.000000",
      "oid": 1759134143282,
      "orderType": "Limit",
      "origSz": "0.00036000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00036000",
      "tif": "Gtc",
      "timestamp": 1759134143000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1759134143000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "108000.000000",
      "oid": 1759124917376,
      "orderType": "Limit",
      "origSz": "0.00006000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00006000",
      "tif": "Gtc",
      "timestamp": 1759124918000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1759124921000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "107500.000000",
      "oid": 1759124920628,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1759124921000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1759124921000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "117769.000000",
      "oid": 1758887018921,
      "orderType": "Limit",
      "origSz": "0.00118032",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00118032",
      "tif": "Gtc",
      "timestamp": 1758887019000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758887019000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "117763.000000",
      "oid": 1758886941604,
      "orderType": "Limit",
      "origSz": "0.00370000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00370000",
      "tif": "Gtc",
      "timestamp": 1758886951000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758886951000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "117743.000000",
      "oid": 1758886879908,
      "orderType": "Limit",
      "origSz": "0.00220000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00220000",
      "tif": "Gtc",
      "timestamp": 1758886887000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758886887000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "117402.000000",
      "oid": 1758884875981,
      "orderType": "Limit",
      "origSz": "0.00092000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00092000",
      "tif": "Gtc",
      "timestamp": 1758884876000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758884876000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "107500.000000",
      "oid": 1758874330712,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758874331000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758874331000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "108000.000000",
      "oid": 1758874327369,
      "orderType": "Limit",
      "origSz": "0.00006000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00006000",
      "tif": "Gtc",
      "timestamp": 1758874327000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1758874331000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "107500.000000",
      "oid": 1758873899315,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758873900000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758873900000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "108000.000000",
      "oid": 1758873895840,
      "orderType": "Limit",
      "origSz": "0.00006000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00006000",
      "tif": "Gtc",
      "timestamp": 1758873896000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1758873900000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "107500.000000",
      "oid": 1758873683695,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758873684000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1758873686000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "108000.000000",
      "oid": 1758873680443,
      "orderType": "Limit",
      "origSz": "0.00006000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00006000",
      "tif": "Gtc",
      "timestamp": 1758873681000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1758873684000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "105000.000000",
      "oid": 1758872506411,
      "orderType": "Limit",
      "origSz": "0.00004000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00004000",
      "tif": "Gtc",
      "timestamp": 1758872507000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1758872510000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "105000.000000",
      "oid": 1758872473431,
      "orderType": "Limit",
      "origSz": "0.00004000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00004000",
      "tif": "Gtc",
      "timestamp": 1758872473000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758872473000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "105000.000000",
      "oid": 1758872452218,
      "orderType": "Limit",
      "origSz": "0.00004000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00004000",
      "tif": "Gtc",
      "timestamp": 1758872453000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758872453000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "108000.000000",
      "oid": 1758872286813,
      "orderType": "Limit",
      "origSz": "0.00005000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00005000",
      "tif": "Gtc",
      "timestamp": 1758872287000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758872287000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "110000.000000",
      "oid": 1758822410073,
      "orderType": "Limit",
      "origSz": "0.00005000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00005000",
      "tif": "Gtc",
      "timestamp": 1758822410000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758822410000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "107500.000000",
      "oid": 1758822380478,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758822390000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1758822392000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "108000.000000",
      "oid": 1758822376755,
      "orderType": "Limit",
      "origSz": "0.00006000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00006000",
      "tif": "Gtc",
      "timestamp": 1758822377000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1758822390000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "108000.000000",
      "oid": 1758822362988,
      "orderType": "Limit",
      "origSz": "0.00006000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00006000",
      "tif": "Gtc",
      "timestamp": 1758822363000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1758822376000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "107500.000000",
      "oid": 1758822365675,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758822376000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758822376000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "107500.000000",
      "oid": 1758822366410,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758822375000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758822375000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "108000.000000",
      "oid": 1758822363726,
      "orderType": "Limit",
      "origSz": "0.00006000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00006000",
      "tif": "Gtc",
      "timestamp": 1758822363000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1758822375000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "110000.000000",
      "oid": 1758822216027,
      "orderType": "Limit",
      "origSz": "0.00005000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00005000",
      "tif": "Gtc",
      "timestamp": 1758822216000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758822216000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "109500.000000",
      "oid": 1758819984591,
      "orderType": "Limit",
      "origSz": "0.00008000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00008000",
      "tif": "Gtc",
      "timestamp": 1758819985000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758819985000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "110000.000000",
      "oid": 1758819979999,
      "orderType": "Limit",
      "origSz": "0.00005000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00005000",
      "tif": "Gtc",
      "timestamp": 1758819980000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1758819985000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "112000.000000",
      "oid": 1758796669713,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "A",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758796670000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1758796672000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "112000.000000",
      "oid": 1758796565225,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "A",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758796565000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758796565000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "75000.000000",
      "oid": 1758786052805,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758786088000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1758786952000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "75000.000000",
      "oid": 3748278,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758786151000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "cancelled",
    "statusTimestamp": 1758786797000
  },
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
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "150000.000000",
      "oid": 6010,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758690765000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758690765000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "150000.000000",
      "oid": 6003,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758635152000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758635152000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "100000.000000",
      "oid": 6002,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": true,
      "side": "A",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758633848000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758633848000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "150000.000000",
      "oid": 6001,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758632269000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758632269000
  },
  {
    "order": {
      "children": [],
      "cloid": null,
      "coin": "BTC",
      "isPositionTpsl": false,
      "isTrigger": false,
      "limitPx": "75000.000000",
      "oid": 6000,
      "orderType": "Limit",
      "origSz": "0.00010000",
      "reduceOnly": false,
      "side": "B",
      "sz": "0.00010000",
      "tif": "Gtc",
      "timestamp": 1758631358000,
      "triggerCondition": "N/A",
      "triggerPx": "0.0"
    },
    "status": "open",
    "statusTimestamp": 1758631358000
  }
]
```

**Summary:** Returns an array with 40 items

---

## User Funding (`userFunding`)

**Category:** User Data

**Request Payload:**
```json
{
  "type": "userFunding",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

**Response (200):**
```json
[]
```

**Summary:** Returns an array with 0 items

---

## Active Asset Data (`activeAssetData`)

**Category:** User Data

**Request Payload:**
```json
{
  "type": "activeAssetData",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
  "coin": "BTC"
}
```

**Response (200):**
```json
{
  "availableToTrade": [
    "0.08851846",
    "0.08851846"
  ],
  "coin": "BTC",
  "leverage": {
    "type": "cross",
    "value": 101
  },
  "markPx": "114100.500000",
  "maxTradeSzs": [
    "0.08851846",
    "0.08851846"
  ],
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

**Summary:** Returns object with keys: availableToTrade, coin, leverage, markPx, maxTradeSzs, ...

---

## L2 Book (`l2Book`)

**Category:** Market Data

**Request Payload:**
```json
{
  "type": "l2Book",
  "coin": "BTC"
}
```

**Response (200):**
```json
{
  "coin": "BTC",
  "levels": [
    [
      {
        "n": 3,
        "px": "114100.000000",
        "sz": "2.00822000"
      },
      {
        "n": 1,
        "px": "114099.000000",
        "sz": "0.00011000"
      },
      {
        "n": 1,
        "px": "114098.000000",
        "sz": "0.00011000"
      },
      {
        "n": 1,
        "px": "114097.000000",
        "sz": "0.00011000"
      },
      {
        "n": 1,
        "px": "114096.000000",
        "sz": "0.00011000"
      },
      {
        "n": 2,
        "px": "114095.000000",
        "sz": "2.65000000"
      },
      {
        "n": 1,
        "px": "114094.000000",
        "sz": "0.00011000"
      },
      {
        "n": 1,
        "px": "114093.000000",
        "sz": "0.00011000"
      },
      {
        "n": 2,
        "px": "114092.000000",
        "sz": "0.03578000"
      },
      {
        "n": 1,
        "px": "114091.000000",
        "sz": "0.00011000"
      },
      {
        "n": 1,
        "px": "114090.000000",
        "sz": "0.00011000"
      },
      {
        "n": 2,
        "px": "114089.000000",
        "sz": "0.87595000"
      },
      {
        "n": 2,
        "px": "114088.000000",
        "sz": "0.20011000"
      },
      {
        "n": 1,
        "px": "114087.000000",
        "sz": "0.00011000"
      },
      {
        "n": 3,
        "px": "114086.000000",
        "sz": "0.00250000"
      },
      {
        "n": 1,
        "px": "114085.000000",
        "sz": "0.00011000"
      },
      {
        "n": 3,
        "px": "114084.000000",
        "sz": "1.32095000"
      },
      {
        "n": 1,
        "px": "114083.000000",
        "sz": "0.53570000"
      },
      {
        "n": 5,
        "px": "114082.000000",
        "sz": "2.05242000"
      },
      {
        "n": 3,
        "px": "114081.000000",
        "sz": "1.75403000"
      }
    ],
    [
      {
        "n": 53,
        "px": "114101.000000",
        "sz": "23.45672000"
      },
      {
        "n": 3,
        "px": "114102.000000",
        "sz": "11.38172000"
      },
      {
        "n": 8,
        "px": "114103.000000",
        "sz": "17.03407000"
      },
      {
        "n": 2,
        "px": "114105.000000",
        "sz": "0.56927000"
      },
      {
        "n": 7,
        "px": "114106.000000",
        "sz": "11.66381000"
      },
      {
        "n": 2,
        "px": "114107.000000",
        "sz": "3.94096000"
      },
      {
        "n": 12,
        "px": "114108.000000",
        "sz": "6.13488000"
      },
      {
        "n": 1,
        "px": "114109.000000",
        "sz": "4.57466000"
      },
      {
        "n": 3,
        "px": "114110.000000",
        "sz": "7.66024000"
      },
      {
        "n": 1,
        "px": "114111.000000",
        "sz": "0.08763000"
      },
      {
        "n": 1,
        "px": "114112.000000",
        "sz": "1.73446000"
      },
      {
        "n": 4,
        "px": "114113.000000",
        "sz": "2.72528000"
      },
      {
        "n": 4,
        "px": "114114.000000",
        "sz": "2.67049000"
      },
      {
        "n": 3,
        "px": "114115.000000",
        "sz": "4.77864000"
      },
      {
        "n": 6,
        "px": "114116.000000",
        "sz": "1.55481000"
      },
      {
        "n": 10,
        "px": "114117.000000",
        "sz": "4.52368000"
      },
      {
        "n": 4,
        "px": "114118.000000",
        "sz": "0.38580000"
      },
      {
        "n": 5,
        "px": "114119.000000",
        "sz": "8.96236000"
      },
      {
        "n": 7,
        "px": "114120.000000",
        "sz": "2.79318000"
      },
      {
        "n": 2,
        "px": "114121.000000",
        "sz": "2.18925000"
      }
    ]
  ],
  "time": 1759168443349
}
```

**Summary:** Returns object with keys: coin, levels, time

---

# ❌ Failed/Empty Endpoints

## Candle Snapshot (`candleSnapshot`)

**Category:** Market Data

**Status:** Failed with error: 400 Client Error: Bad Request for url: https://embindexer.net/ember/api/dev/v1/info
**HTTP Status Code:** 400
**Request Payload:**
```json
{
  "type": "candleSnapshot"
}
```

---

## Portfolio (`portfolio`)

**Category:** User Data

**Status:** Failed with error: 400 Client Error: Bad Request for url: https://embindexer.net/ember/api/dev/v1/info
**HTTP Status Code:** 400
**Request Payload:**
```json
{
  "type": "portfolio",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

---

## Order Status (`orderStatus`)

**Category:** User Data

**Status:** Failed with error: 500 Server Error: Internal Server Error for url: https://embindexer.net/ember/api/dev/v1/info
**HTTP Status Code:** 500
**Request Payload:**
```json
{
  "type": "orderStatus",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

---

## User State (`userState`)

**Category:** User Data

**Status:** Failed with error: 400 Client Error: Bad Request for url: https://embindexer.net/ember/api/dev/v1/info
**HTTP Status Code:** 400
**Request Payload:**
```json
{
  "type": "userState",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

---

## Market Summary (`marketSummary`)

**Category:** Market Data

**Status:** Failed with error: 400 Client Error: Bad Request for url: https://embindexer.net/ember/api/dev/v1/info
**HTTP Status Code:** 400
**Request Payload:**
```json
{
  "type": "marketSummary"
}
```

---


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
curl -X POST https://embindexer.net/ember/api/dev/v1/info \
  -H "Content-Type: application/json" \
  -d '{"type": "meta"}'

# Get user fills
curl -X POST https://embindexer.net/ember/api/dev/v1/info \
  -H "Content-Type: application/json" \
  -d '{"type": "userFills", "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"}'
```

---

**Generated on:** {'timestamp': 'auto-generated'}
**Total Endpoints Tested:** 16
**Working Endpoints:** 11
**Failed Endpoints:** 5
