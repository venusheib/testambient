# Ambient Finance Exchange Operations - Complete Response Documentation

This document contains actual API responses from all Ambient Finance exchange operations for testing and integration purposes.

**Base URL:** `https://embindexer.net/ember/api/dev/v1/exchange`  
**Method:** POST  
**Content-Type:** application/json

**Test User Address:** `5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK`  
**Test Asset:** BTC (Universe Index: 0)

---

## 1. Update Leverage (20x)

**Timestamp:** 2025-09-30T02:15:55.233670

**HTTP Status:** 200

**Request Payload:**
```json
{
  "action": {
    "type": "updateLeverage",
    "asset": 0,
    "leverage": 20,
    "isCross": true
  }
}
```

**Signed Payload:**
```json
{
  "action": {
    "type": "updateLeverage",
    "asset": 0,
    "leverage": 20,
    "isCross": true
  },
  "nonce": 1759173352951,
  "signature": [
    "51e30a1f26449abf77862c3ab17317eace8d5974e0c975fbb75b08e16f9cc7a63d246cc80a787f3082e54b32417b05ffaadff7881c8dd8f1b96ff4d6ea30c600"
  ],
  "pubkey": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

**Response:**
```json
{
  "status": "ok",
  "response": {
    "status": "ok",
    "tx": "5KB9DQV2NV8ZCLmZkthT6LwXyMs26VVMbQgXwv8XFeJb6WxvN1yg5MFHrigk5D5PvXq29aartuh5Y77r6ukR3mS1"
  }
}
```

---

## 2. Place Limit Order

**Timestamp:** 2025-09-30T02:15:57.005937

**HTTP Status:** 200

**Request Payload:**
```json
{
  "action": {
    "type": "order",
    "a": 0,
    "b": true,
    "p": "110000.0",
    "s": "0.00008000",
    "r": false,
    "t": {
      "limit": {
        "tif": "Gtc"
      }
    }
  }
}
```

**Signed Payload:**
```json
{
  "action": {
    "type": "order",
    "a": 0,
    "b": true,
    "p": "110000.0",
    "s": "0.00008000",
    "r": false,
    "t": {
      "limit": {
        "tif": "Gtc"
      }
    },
    "c": "1759173355567"
  },
  "nonce": 1759173355567,
  "signature": [
    "24e694574d917018b6bbea7d7af751e9ebb19c6808f0afda2e9005795e55beb04e09d652b60eaa886d1afc4244d558ad28a6cfbd026f5ac4a6d8463f7314cb0a"
  ],
  "pubkey": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

**Response:**
```json
{
  "status": "ok",
  "response": {
    "status": "ok",
    "data": {
      "type": "limit",
      "oid": 1759173355567,
      "cloid": "1759173355567",
      "filled": {
        "totalSz": "0",
        "avgPx": "0"
      }
    },
    "tx": "526vVDdyuhRcRZ2oe6fZobaKrLGhApx7PGWgvhUuqXxEhwq9kusmjzkzMzuaLA2ZnvtPsK2HPHxUEWqa68GW2KuX"
  }
}
```

---

## 3. Check Order Status

**Timestamp:** 2025-09-30T02:15:59.106798

**HTTP Status:** 200

**Request Payload:**
```json
{
  "type": "orderStatus",
  "user": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK",
  "orderId": 1759173355567
}
```

**Response:**
```json
{
  "order": {
    "avgFillPx": "0",
    "coin": "BTC",
    "filledSz": "0.00000000",
    "limitPx": "110000.000000",
    "orderId": 1759173355567,
    "orderType": "limit",
    "postOnly": false,
    "reduceOnly": false,
    "side": "B",
    "sz": "0.00008000",
    "timestamp": 1759173359103
  },
  "status": "open",
  "statusTimestamp": 1759173356000
}
```

---

## 4. Modify Order

**Timestamp:** 2025-09-30T02:16:01.534000

**HTTP Status:** 200

**Request Payload:**
```json
{
  "action": {
    "type": "modify",
    "oid": 1759173355567,
    "order": {
      "a": 0,
      "b": true,
      "p": "109500.0",
      "s": "0.00010000",
      "r": false,
      "t": {
        "limit": {
          "tif": "Gtc"
        }
      }
    }
  }
}
```

**Signed Payload:**
```json
{
  "action": {
    "type": "modify",
    "oid": 1759173355567,
    "order": {
      "a": 0,
      "b": true,
      "p": "109500.0",
      "s": "0.00010000",
      "r": false,
      "t": {
        "limit": {
          "tif": "Gtc"
        }
      },
      "c": "1759173359775"
    }
  },
  "nonce": 1759173359774,
  "signature": [
    "acfa5c89229ae8450b14eb5fd8e055188c5a2b07858bc3cbbba40bebf70b5fc22e6b29df5857aa3fb38305296d275818d6d5f7086d30e956b6e29c4211751b0e"
  ],
  "pubkey": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

**Response:**
```json
{
  "status": "ok",
  "response": {
    "status": "ok",
    "data": {
      "type": "modify",
      "oid": 1759173359775,
      "cloid": "1759173359775",
      "filled": {
        "totalSz": "0",
        "avgPx": "0"
      }
    },
    "tx": "5rPUAhymTWm5bhbgayKPf43ugAxQECLLEXFasEULZnNH5pMtE4ZxAB7y4StYEBhu9pb6AzSTigbvGZZyevK3VgJy"
  }
}
```

---

## 5. Cancel Order by ID

**Timestamp:** 2025-09-30T02:16:05.056564

**HTTP Status:** 200

**Request Payload:**
```json
{
  "action": {
    "type": "cancel",
    "cancels": [
      {
        "a": 0,
        "o": 1759173359775
      }
    ]
  }
}
```

**Signed Payload:**
```json
{
  "action": {
    "type": "cancel",
    "cancels": [
      {
        "a": 0,
        "o": 1759173359775
      }
    ]
  },
  "nonce": 1759173363753,
  "signature": [
    "62e307eecbf29ca72435d8b61ca6b3ebd7e2bbdd85d81580e67730e26176760ff7b2c4f2004594a59df69f383e33864af130e8bb17a976253b3999830ffc9c01"
  ],
  "pubkey": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

**Response:**
```json
{
  "status": "ok",
  "response": {
    "status": "ok",
    "data": {
      "type": "cancel",
      "oid": 1759173359775,
      "cloid": null,
      "filled": {
        "totalSz": "0",
        "avgPx": "0"
      }
    },
    "tx": "DRyMWeqYr8Jy9k2Z54dJmSmv2hpnxKTNrzFXzBBoVVCNQj2Es87xv9ji4nk2DsBGvowTHo7rm2EKAgS7SASA9Ju"
  }
}
```

---


## Response Schema Summary

### Successful Exchange Response
```json
{
  "status": "ok",
  "response": {
    "status": "ok",
    "data": {
      "type": "limit",
      "oid": 1234567890,
      "cloid": "custom_client_id",
      "filled": {
        "totalSz": "0",
        "avgPx": "0"
      }
    },
    "tx": "solana_transaction_hash"
  }
}
```

### Order Status Response
```json
{
  "status": "open",
  "order": {
    "asset": 0,
    "side": "B",
    "limitPx": "110000.0",
    "sz": "0.00008000",
    "filledSz": "0",
    "cloid": "1234567890",
    "oid": 1234567890,
    "timestamp": 1234567890
  }
}
```

## Usage Examples

### Python with SDK Signing
```python
import subprocess
import json
import tempfile
import os

def sign_and_send_order(action):
    # Sign with SDK
    payload = {"action": action}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_path = f.name
    
    try:
        result = subprocess.run([
            'node', 'ambient-ember-sdk/scripts/signPayload.mjs',
            'devkey.json', temp_path
        ], capture_output=True, text=True)
        
        signed_payload = json.loads(result.stdout)
    finally:
        os.unlink(temp_path)
    
    # Send to exchange
    response = requests.post(
        'https://embindexer.net/ember/api/dev/v1/exchange',
        json=signed_payload,
        headers={'Content-Type': 'application/json'}
    )
    return response.json()

# Place order
order_action = {
    "type": "order",
    "a": 0,
    "b": True,
    "p": "110000.0",
    "s": "0.00008000",
    "r": False,
    "t": {"limit": {"tif": "Gtc"}}
}
result = sign_and_send_order(order_action)
```

---

**Generated on:** 2025-09-30T02:16:05.471655
**Total Operations Tested:** 5
