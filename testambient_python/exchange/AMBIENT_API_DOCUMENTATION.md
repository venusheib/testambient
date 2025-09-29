# Ambient API Documentation

Complete documentation for placing orders, canceling orders, and canceling by client order ID using the Ambient Ember API with proper SDK signing.

## Base Configuration

```
API Base URL: https://embindexer.net/ember/api/dev/v1
Exchange Endpoint: {BASE_URL}/exchange
Content-Type: application/json
Method: POST
```

## Authentication & Signing

All exchange requests must be signed using the Ambient Ember SDK. The SDK handles:
- Permit-based signatures compatible with Solana
- Automatic nonce generation
- Proper expiry alignment
- Hex signature formatting

### SDK Signing Process
```bash
# Sign payload using SDK
echo '{"action": {...}}' | node scripts/signPayload.mjs devkey.json --stdin
```

## Asset Indexing

Assets are referenced by their **universe index** from the meta response:
- **BTC**: Universe index `0`
- Use `GET {BASE_URL}/info` with `{"type": "meta"}` to get current universe mapping

---

## 1. Place Order

### Request Headers
```
Content-Type: application/json
```

### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | object | ✅ | Order action details |
| `action.type` | string | ✅ | Must be `"order"` |
| `action.a` | integer | ✅ | Asset universe index (0 for BTC) |
| `action.b` | boolean | ✅ | Order side (`true` = buy, `false` = sell) |
| `action.p` | string | ✅ | Price as string (e.g., "112000.0") |
| `action.s` | string | ✅ | Size as string (e.g., "0.00010000") |
| `action.r` | boolean | ✅ | Reduce only flag |
| `action.t` | object | ✅ | Time in force configuration |
| `action.t.limit.tif` | string | ✅ | Time in force: "Gtc", "Ioc", "Alo" |
| `action.c` | string | ❌ | Client order ID (auto-generated if omitted) |
| `nonce` | integer | ✅ | Millisecond timestamp (SDK generates) |
| `signature` | array | ✅ | Hex signature array (SDK generates) |
| `pubkey` | string | ✅ | Base58 public key (SDK generates) |

### Example Request Body
```json
{
  "action": {
    "type": "order",
    "a": 0,
    "b": false,
    "p": "112000.0",
    "s": "0.00010000",
    "r": false,
    "t": {
      "limit": {
        "tif": "Gtc"
      }
    },
    "c": "1758796565225"
  },
  "nonce": 1758796565225,
  "signature": [
    "b8b5130775205fcc6cea8d4e4a8f9d5c7e3f2a1b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b"
  ],
  "pubkey": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

### Success Response (Status: 200)
```json
{
  "status": "ok",
  "response": {
    "status": "ok",
    "data": {
      "type": "limit",
      "oid": 1758796565225,
      "cloid": "1758796565225",
      "filled": {
        "totalSz": "0",
        "avgPx": "0"
      }
    },
    "tx": "5h8Q421bt4TFUhWddg21AYMKuphuaSpyKU7BptMhU3hiKzN9Hy3mcvTmc9o7pPW9TUGJ4gMXdwY71pFaPvvSynJm"
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Overall status: "ok" or "err" |
| `response.status` | string | Transaction status: "ok" or error object |
| `response.data.type` | string | Order type: "limit", "market", etc. |
| `response.data.oid` | integer | Order ID assigned by exchange |
| `response.data.cloid` | string | Client order ID (echo or generated) |
| `response.data.filled.totalSz` | string | Total filled size |
| `response.data.filled.avgPx` | string | Average fill price |
| `response.tx` | string | Transaction hash on blockchain |

---

## 2. Cancel Order (by Order ID)

### Request Headers
```
Content-Type: application/json
```

### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | object | ✅ | Cancel action details |
| `action.type` | string | ✅ | Must be `"cancel"` |
| `action.cancels` | array | ✅ | Array of orders to cancel |
| `action.cancels[].a` | integer | ✅ | Asset universe index (0 for BTC) |
| `action.cancels[].o` | integer | ✅ | Order ID to cancel |
| `nonce` | integer | ✅ | Millisecond timestamp (SDK generates) |
| `signature` | array | ✅ | Hex signature array (SDK generates) |
| `pubkey` | string | ✅ | Base58 public key (SDK generates) |

### Example Request Body
```json
{
  "action": {
    "type": "cancel",
    "cancels": [
      {
        "a": 0,
        "o": 1758796565225
      }
    ]
  },
  "nonce": 1758796566961,
  "signature": [
    "eb86ddb0af000aee80b0c4f8d9e2a1b3c5d7e9f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c5d7e9f1a3b5c7d9e1f3a5b7c9d1e3f5"
  ],
  "pubkey": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

### Success Response (Status: 200)
```json
{
  "status": "ok",
  "response": {
    "status": "ok",
    "data": {
      "type": "cancel",
      "cancelled": [
        {
          "oid": 1758796565225,
          "status": "cancelled"
        }
      ]
    },
    "tx": "2nB8vKq3xYz9LmN4pO6rS8tU1wE5iH7jK9mP2qR5sT8vY1zA3bC6dF9gH2kM5nP8qT1wE4iH7jK0mP3qR6sU9vY2zA"
  }
}
```

---

## 3. Cancel Order (by Client Order ID)

### Request Headers
```
Content-Type: application/json
```

### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | object | ✅ | Cancel by cloid action details |
| `action.type` | string | ✅ | Must be `"cancelByCloid"` |
| `action.cancels` | array | ✅ | Array of orders to cancel by cloid |
| `action.cancels[].asset` | string | ✅ | Asset symbol (e.g., "BTC") |
| `action.cancels[].cloid` | string | ✅ | Client order ID to cancel |
| `nonce` | integer | ✅ | Millisecond timestamp (SDK generates) |
| `signature` | array | ✅ | Hex signature array (SDK generates) |
| `pubkey` | string | ✅ | Base58 public key (SDK generates) |

### Example Request Body
```json
{
  "action": {
    "type": "cancelByCloid",
    "cancels": [
      {
        "asset": "BTC",
        "cloid": "my_order_001"
      }
    ]
  },
  "nonce": 1758796567123,
  "signature": [
    "3f7a9c1e5b8d2f6a0c4e8b2f6a9c3e7b1d5f9a2c6e0b4f8a1c5e9b3f7a0d4e8b2f6a9c3e7b1d5f9a2c6e0b4f8a1c5"
  ],
  "pubkey": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

### Success Response (Status: 200)
```json
{
  "status": "ok",
  "response": {
    "status": "ok",
    "data": {
      "type": "cancelByCloid",
      "cancelled": [
        {
          "cloid": "my_order_001",
          "oid": 1758796565225,
          "status": "cancelled"
        }
      ]
    },
    "tx": "4oD9wLs4yA0bN5qP7rS9tV2xF6jI8kL1nO4rR6sU9vY3zA5bC8eG1hK4mN7pQ0sT3wF6jI9kL2nO5rR8sV1yA4bD"
  }
}
```

---

## 4. Update Leverage

### Request Headers
```
Content-Type: application/json
```

### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | object | ✅ | Update leverage action details |
| `action.type` | string | ✅ | Must be `"updateLeverage"` |
| `action.asset` | integer | ✅ | Asset universe index (0 for BTC) |
| `action.leverage` | integer | ✅ | New leverage value (e.g., 25 for 25x) |
| `action.isCross` | boolean | ✅ | Cross margin flag (true for cross margin) |
| `nonce` | integer | ✅ | Millisecond timestamp (SDK generates) |
| `signature` | array | ✅ | Hex signature array (SDK generates) |
| `pubkey` | string | ✅ | Base58 public key (SDK generates) |

### Example Request Body
```json
{
  "action": {
    "type": "updateLeverage",
    "asset": 0,
    "leverage": 25,
    "isCross": true
  },
  "nonce": 1758814353694,
  "signature": [
    "23fabbf1c2c0a388cbdec7a5f9b1d4e8a2c6f0b5c9d3e7a1b4f8c2d6e0a9b3c7e1f5a8d2b6c0e4f8a3c7b1d5e9f2a6"
  ],
  "pubkey": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

### Success Response (Status: 200)
```json
{
  "status": "ok",
  "response": {
    "status": "ok",
    "tx": "4FbpSQyEEZ1qYpZ321NRcjERR2yAC3to361BopTAtkKq9ScyDvuVgXAZ8ttp9yj5XUhqnGdugKyNr2nEWfntnShP"
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Overall status: "ok" or "err" |
| `response.status` | string | Transaction status: "ok" or error object |
| `response.tx` | string | Transaction hash on blockchain |

---

## 5. Modify Order ✅

### Request Headers
```
Content-Type: application/json
```

### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | object | ✅ | Modify action details |
| `action.type` | string | ✅ | Must be `"modify"` |
| `action.oid` | integer | ✅ | Existing order ID to modify |
| `action.order` | object | ✅ | New order specification |
| `action.order.a` | integer | ✅ | Asset universe index (0 for BTC) |
| `action.order.b` | boolean | ✅ | Order side (true = buy, false = sell) |
| `action.order.p` | string | ✅ | New price as string |
| `action.order.s` | string | ✅ | New size as string |
| `action.order.r` | boolean | ✅ | Reduce only flag |
| `action.order.t` | object | ✅ | Time in force configuration |
| `action.order.t.limit.tif` | string | ✅ | Time in force: "Gtc", "Ioc", "Alo" |
| `action.order.c` | string | ❌ | New client order ID |
| `nonce` | integer | ✅ | Millisecond timestamp (SDK generates) |
| `signature` | array | ✅ | Hex signature array (SDK generates) |
| `pubkey` | string | ✅ | Base58 public key (SDK generates) |

### Example Request Body
```json
{
  "action": {
    "type": "modify",
    "oid": 6000,
    "order": {
      "a": 0,
      "b": true,
      "p": "76000.0",
      "s": "0.00015000",
      "r": false,
      "t": {
        "limit": {
          "tif": "Gtc"
        }
      },
      "c": "1758814355386"
    }
  },
  "nonce": 1758814355569,
  "signature": [
    "c85181308abf9345cfd6a7b2e9f3c8d1e4a7b0c3f6e9d2a5f8b1c4e7d0a3b6c9f2e5a8d1b4f7c0a3e6f9b2c5d8a1b4"
  ],
  "pubkey": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

### Success Response (Status: 200)
```json
{
  "status": "ok",
  "response": {
    "status": "ok",
    "data": {
      "type": "modify",
      "oid": 1758819984591,
      "cloid": "1758819984591",
      "filled": {
        "totalSz": "0",
        "avgPx": "0"
      }
    },
    "tx": "4qAWr9Ly3BRHzHZaaFuRLCmLrKnuBQ6ZqLtEkqUX8RBogWxNK1HR7sJ8qeFGP72TTAiXwGEaB2rZh5m1uYfkt1bg"
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Overall status: "ok" or "err" |
| `response.status` | string | Transaction status: "ok" or error object |
| `response.data.type` | string | Action type: "modify" |
| `response.data.oid` | integer | New order ID (different from original) |
| `response.data.cloid` | string | New client order ID |
| `response.data.filled` | object | Fill information (usually empty for new orders) |
| `response.tx` | string | Transaction hash on blockchain |

### Important Notes
✅ **Modify orders work successfully with fresh orders**  
⚠️ **Creates a new order with new OID** - The modify operation cancels the original order and creates a new one atomically  
⚠️ **May fail on older orders** - Orders in certain states may not be modifiable

---

## 6. Query Order Status ✅

Query order status by Order ID (OID) or Client Order ID (CLOID). Similar to Hyperliquid's orderStatus API.

### Request Headers
```
Content-Type: application/json
```

### Endpoint
```
POST {BASE_URL}/info
```

### Request Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✅ | Must be `"orderStatus"` |
| `user` | string | ✅ | Base58 public key of the user |
| `orderId` | integer/string | ✅ | Order ID (integer) or Client Order ID (string) |

### Example Request Body (Query by OID)
```json
{
  "type": "orderStatus",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
  "orderId": 1758872506411
}
```

### Example Request Body (Query by CLOID)
```json
{
  "type": "orderStatus", 
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
  "orderId": "custom_order_123"
}
```

### Success Response - Order Found (Status: 200)
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

### Success Response - Order Not Found (Status: 200)
```json
{
  "order": null,
  "status": "notFound",
  "statusTimestamp": 1758872482787
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `order` | object/null | Order details (null if not found) |
| `order.avgFillPx` | string | Average fill price |
| `order.coin` | string | Asset symbol (e.g., "BTC") |
| `order.filledSz` | string | Total filled size |
| `order.limitPx` | string | Order limit price |
| `order.orderId` | integer | Order ID |
| `order.orderType` | string | Order type: "limit", "market", etc. |
| `order.postOnly` | boolean | Post-only flag |
| `order.reduceOnly` | boolean | Reduce-only flag |
| `order.side` | string | Order side: "B" (buy) or "A" (sell) |
| `order.sz` | string | Order size |
| `order.timestamp` | integer | Order timestamp |
| `status` | string | Order status (see status values below) |
| `statusTimestamp` | integer | Status timestamp |

### Order Status Values

Similar to Hyperliquid API status values:

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

### Important Notes
✅ **No signing required** - This is an info endpoint, not an exchange endpoint  
✅ **Supports both OID and CLOID** - Can query by either identifier  
⚠️ **Indexing delay** - New orders may show "notFound" briefly while being indexed  
⚠️ **User verification** - Must provide correct user pubkey that owns the order  

---

## Error Responses

### Invalid Action (Status: 400)
```json
{
  "status": "err",
  "response": {
    "code": "INVALID_ACTION",
    "message": "Unknown asset: Symbol(\"BTC\")"
  }
}
```

### Transaction Simulation Failed (Status: 200)
```json
{
  "status": "ok",
  "response": {
    "status": {
      "error": "Transaction simulation failed: InstructionError(2, Custom(2))"
    }
  }
}
```

### Common Error Codes

| Error | Description | Solution |
|-------|-------------|----------|
| `Unknown asset: Symbol("BTC")` | Using coin name instead of index | Use universe index (0 for BTC) |
| `Unknown asset: Index(50)` | Using wrong index | Use universe index from meta response |
| `InstructionError(2, Custom(2))` | Business logic validation failed | Check price, size, balance, market conditions |
| `UninitializedAccount` | Account/order not found | Verify order ID exists and is owned by signer |

---

## Python Implementation Example

```python
from exchange.ambient_trading_with_sdk import AmbientSDKTrader, OrderParams

trader = AmbientSDKTrader()

# Place order
order_params = OrderParams(
    asset_index=0,  # BTC universe index
    is_buy=False,  # Sell order
    price="112000.0",  # Price as string
    size="0.00010000",  # Size as string
    reduce_only=False,
    time_in_force="Gtc"
)

response = trader.place_order(order_params)
oid = response["response"]["data"]["oid"]
cloid = response["response"]["data"]["cloid"]

# Query order status by OID
status_response = trader.query_order_status(oid)
print(f"Order status: {status_response['status']}")
if status_response['order']:
    order_info = status_response['order']
    print(f"Side: {'BUY' if order_info['side'] == 'B' else 'SELL'}")
    print(f"Size: {order_info['sz']}, Filled: {order_info['filledSz']}")

# Query order status by CLOID (if different from OID)
status_response = trader.query_order_status(cloid)

# Cancel by order ID  
trader.cancel_order(0, oid)  # asset_index=0, order_id=oid

# Update leverage to 25x
trader.update_leverage(0, 25)  # asset_index=0, leverage=25x

# Modify existing order (works best with fresh orders)
modify_response = trader.modify_order(0, oid, "111500.0", "0.00020000")  # new_price, new_size
new_oid = modify_response["response"]["data"]["oid"]  # Gets new order ID
```

---

## Notes

1. **Signing Required**: All exchange requests must be signed with the Ambient Ember SDK (info requests do not require signing)
2. **Asset Format**: Always use universe index (0 for BTC), not coin names or margin table IDs
3. **String Types**: Prices and sizes must be strings, not numbers
4. **Nonce**: SDK automatically generates millisecond timestamp nonces
5. **Permits**: SDK handles permit envelope generation and expiry alignment
6. **Idempotency**: Same nonce = same transaction, preventing double execution
7. **Order Status**: Query order status via info endpoint using OID or CLOID - no signing required