# Ambient Finance Batch Order Operations - Response Documentation

This document contains actual API responses from Ambient Finance batch order operations.

**Base URL:** `https://embindexer.net/ember/api/dev/v1/exchange`  
**Method:** POST  
**Content-Type:** application/json

**Test User Address:** `5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK`  
**Test Asset:** BTC (Universe Index: 0)

---

## 1. Batch Order - Place 3 Orders

**Timestamp:** 2025-09-30T03:07:20.831427

**HTTP Status:** 200

**Request Payload:**
```json
{
  "action": {
    "type": "batchOrder",
    "orders": [
      {
        "a": 0,
        "b": true,
        "p": "109000.0",
        "s": "0.00005000",
        "r": false,
        "t": {
          "limit": {
            "tif": "Gtc"
          }
        },
        "c": "1759176435"
      },
      {
        "a": 0,
        "b": true,
        "p": "108500.0",
        "s": "0.00006000",
        "r": false,
        "t": {
          "limit": {
            "tif": "Gtc"
          }
        },
        "c": "1759176436"
      },
      {
        "a": 0,
        "b": false,
        "p": "116000.0",
        "s": "0.00004000",
        "r": false,
        "t": {
          "limit": {
            "tif": "Gtc"
          }
        },
        "c": "1759176437"
      }
    ]
  }
}
```

**Signed Payload:**
```json
{
  "action": {
    "type": "batchOrder",
    "orders": [
      {
        "a": 0,
        "b": true,
        "p": "109000.0",
        "s": "0.00005000",
        "r": false,
        "t": {
          "limit": {
            "tif": "Gtc"
          }
        },
        "c": "1759176435"
      },
      {
        "a": 0,
        "b": true,
        "p": "108500.0",
        "s": "0.00006000",
        "r": false,
        "t": {
          "limit": {
            "tif": "Gtc"
          }
        },
        "c": "1759176436"
      },
      {
        "a": 0,
        "b": false,
        "p": "116000.0",
        "s": "0.00004000",
        "r": false,
        "t": {
          "limit": {
            "tif": "Gtc"
          }
        },
        "c": "1759176437"
      }
    ]
  },
  "nonce": 1759176434592,
  "signature": [
    "0838aa828a2bcdf1f52c15c3d83e90b8ec1c1bd885388d366d247ab4102cee36f395d4b135acce27615fb09063c46992a1fd29825fc9794e3bf6259a6b0ebe00",
    "eb5e6cf8509178a1b998c04ae682d58d8ba975c6f967f4d54bd0973f831f7a172f1437bbbebdb7e3b18b083a3cd0eeb23ae638fc36f5214982b0485c9b985103",
    "4ffad7dac7732c34a4021aae8fdb7bb36ea11e45aca59b5bb88b3b1018b5a2e0b17b7b0f9d1bd9d555e2c8b772c6df713823baf3f4bd587091487dca1cb9a80d"
  ],
  "pubkey": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

**Response:**
```json
{
  "status": "ok",
  "response": [
    {
      "status": "ok",
      "data": {
        "type": "limit",
        "oid": 1759176435,
        "cloid": "1759176435",
        "filled": {
          "totalSz": "0",
          "avgPx": "0"
        }
      },
      "tx": "4cNr6Q1KSEEXjYdDe4aahv1gW3EBAvgZdQ6JsqXpvCLG7q1X7vjh95cEDvELipXtxjen3HhxbiFftgcgzPfdNNSW"
    },
    {
      "status": "ok",
      "data": {
        "type": "limit",
        "oid": 1759176436,
        "cloid": "1759176436",
        "filled": {
          "totalSz": "0",
          "avgPx": "0"
        }
      },
      "tx": "4QFBdHxu9R6gCHFXM3J9R1kyh78BCPYWBQJBRiLiuk1jjVDaMnKfmAzMxGwjN7V6qeMoFGvX4WYzrANaCeU3oY8j"
    },
    {
      "status": "ok",
      "data": {
        "type": "limit",
        "oid": 1759176437,
        "cloid": "1759176437",
        "filled": {
          "totalSz": "0",
          "avgPx": "0"
        }
      },
      "tx": "W9ejWju4JYRLCsaU5oH1F77otxGGLkThAxkFB2oNw6sv7Sk9Euexw1MtwZLDGgkmaUUQtnTzhR8GmdEyQd428eR"
    }
  ]
}
```

---

## 2. Batch Order for CLOID Cancel Test

**Timestamp:** 2025-09-30T03:07:26.196680

**HTTP Status:** 200

**Request Payload:**
```json
{
  "action": {
    "type": "batchOrder",
    "orders": [
      {
        "a": 0,
        "b": true,
        "p": "107000.0",
        "s": "0.00003000",
        "r": false,
        "t": {
          "limit": {
            "tif": "Gtc"
          }
        },
        "c": "1759176544"
      },
      {
        "a": 0,
        "b": false,
        "p": "118000.0",
        "s": "0.00003000",
        "r": false,
        "t": {
          "limit": {
            "tif": "Gtc"
          }
        },
        "c": "1759176545"
      }
    ]
  }
}
```

**Signed Payload:**
```json
{
  "action": {
    "type": "batchOrder",
    "orders": [
      {
        "a": 0,
        "b": true,
        "p": "107000.0",
        "s": "0.00003000",
        "r": false,
        "t": {
          "limit": {
            "tif": "Gtc"
          }
        },
        "c": "1759176544"
      },
      {
        "a": 0,
        "b": false,
        "p": "118000.0",
        "s": "0.00003000",
        "r": false,
        "t": {
          "limit": {
            "tif": "Gtc"
          }
        },
        "c": "1759176545"
      }
    ]
  },
  "nonce": 1759176444885,
  "signature": [
    "069f1712e8742f60ef76ed8e9c5ca5361fe31002495401870f39587a108dd32da85623e77ec46fc568294713e45c8aa3b106a9b52837df26a20ec623ddc2fa09",
    "0b9651126df2e5d73b2f0ef823db2bcf00bb30b624e487e9150d9568f56d9d46ef6182b1da60cfb3857cc32b92b34395867afc94fec677d82abd7fae16d3300b"
  ],
  "pubkey": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

**Response:**
```json
{
  "status": "ok",
  "response": [
    {
      "status": "ok",
      "data": {
        "type": "limit",
        "oid": 1759176544,
        "cloid": "1759176544",
        "filled": {
          "totalSz": "0",
          "avgPx": "0"
        }
      },
      "tx": "2HFahzD9JKYcscPb1v2QAxeNEsdAnavY4LsP7ZSc2Y18u5n2CzqomUY1Em3ExxtFPT4ZaGxQpfrdSQ6e7yx5SR3"
    },
    {
      "status": "ok",
      "data": {
        "type": "limit",
        "oid": 1759176545,
        "cloid": "1759176545",
        "filled": {
          "totalSz": "0",
          "avgPx": "0"
        }
      },
      "tx": "3KkwfnWsXRD6Uuft6kiV7MLq62yQWPqxgntpwkdwQ9bpYBmtPPDB6kAdL9TBBTMRFnV3d7nY2jGJEV731u24m8Fj"
    }
  ]
}
```

---

## 3. Cancel Multiple Orders by CLOID

**Timestamp:** 2025-09-30T03:07:31.509733

**HTTP Status:** 200

**Request Payload:**
```json
{
  "action": {
    "type": "cancelByCloid",
    "cancels": [
      {
        "asset": 0,
        "cloid": "1759176544"
      },
      {
        "asset": 0,
        "cloid": "1759176545"
      }
    ]
  }
}
```

**Signed Payload:**
```json
{
  "action": {
    "type": "cancelByCloid",
    "cancels": [
      {
        "asset": 0,
        "cloid": "1759176544"
      },
      {
        "asset": 0,
        "cloid": "1759176545"
      }
    ]
  },
  "nonce": 1759176448525,
  "signature": [
    "3a38e9481e0e9622c1330c366321b8f976aca643d5c2ab8405b0851926452f514763de8beeada9cab4184bd9e7f26c9ed3c66c349e424d56f01f0c6f06d03c0f",
    "373e84396d807d1ebdc66e509b25fcd57b9289473432b9c16f37770221759ac24c96dc6d2a78eece97ae895867d4c25898b0f44aeac51e582c3509955648040f"
  ],
  "pubkey": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
}
```

**Response:**
```json
{
  "status": "ok",
  "response": [
    {
      "status": "ok",
      "tx": "28TJCG8drMNPBNHLncB5izTyJd8ruMWC6oNPqsGNb49yv6fDrNcyLHRimtqNDSMWJB6BmyvP92JTDTi9LjBvTYvC"
    },
    {
      "status": "ok",
      "tx": "ykbyQaHVbnQ4H2fLoU8CvxUq9Y3tndqv6im6gyX3ftf8h5LVWMMVfvdSDnPWDP7SNkuRa1gsfTZYYXzhf7Wv3e5"
    }
  ]
}
```

---


## Batch Operations Summary

### Supported Batch Actions

1. **`batchOrder`** - Place multiple limit orders in single transaction
2. **`cancel`** - Cancel multiple orders by Order ID  
3. **`cancelByCloid`** - Cancel multiple orders by Client Order ID

### Request Schema

#### Batch Order Placement
```json
{
  "action": {
    "type": "batchOrder",
    "orders": [
      {
        "a": 0,
        "b": true,
        "p": "109000.0", 
        "s": "0.00005000",
        "r": false,
        "t": {"limit": {"tif": "Gtc"}},
        "c": "optional_cloid"
      }
    ]
  }
}
```

#### Multiple Cancel by Order ID
```json
{
  "action": {
    "type": "cancel",
    "cancels": [
      {"a": 0, "o": order_id_1},
      {"a": 0, "o": order_id_2}
    ]
  }
}
```

#### Multiple Cancel by Client Order ID  
```json
{
  "action": {
    "type": "cancelByCloid",
    "cancels": [
      {"asset": 0, "cloid": "client_id_1"},
      {"asset": 0, "cloid": "client_id_2"}
    ]
  }
}
```

---

**Generated on:** 2025-09-30T03:07:31.512173  
**Total Operations:** 3
