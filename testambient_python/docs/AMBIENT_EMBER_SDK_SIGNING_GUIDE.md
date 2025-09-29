# Ambient Ember SDK Signing Guide

Complete guide for using the [Ambient Ember SDK](https://github.com/CrocSwap/ambient-ember-sdk) to sign payloads for the Ambient Finance API.

## Overview

The Ambient Ember SDK provides cryptographic signing functionality for Ambient Finance's perpetual futures exchange. This guide covers both the existing CLI approach and a programmatic implementation for direct integration.

## Prerequisites

1. **Install the Ambient Ember SDK**:
   ```bash
   git clone https://github.com/CrocSwap/ambient-ember-sdk.git
   cd ambient-ember-sdk
   npm install
   npm run build
   ```

2. **Create a Solana keypair file** (`devkey.json`):
   ```json
   [64,118,23,45,67,89,12,234,...]  // Array of 64 bytes representing your private key
   ```

## Method 1: Using the SDK's CLI Script (Recommended)

The SDK includes a ready-to-use signing script at `scripts/signPayload.mjs`.

### Basic Usage

```bash
# Sign a payload from a file
node scripts/signPayload.mjs devkey.json payload.json

# Sign a payload from stdin
echo '{"action": {...}}' | node scripts/signPayload.mjs devkey.json --stdin
```

### Example: Signing an Order

1. **Create payload file** (`order_payload.json`):
   ```json
   {
     "action": {
       "type": "order",
       "a": 0,
       "b": true,
       "p": "108000.0",
       "s": "0.00006000",
       "r": false,
       "t": {
         "limit": {
           "tif": "Gtc"
         }
       }
     }
   }
   ```

2. **Sign the payload**:
   ```bash
   node scripts/signPayload.mjs devkey.json order_payload.json
   ```

3. **Output** (signed payload ready for API):
   ```json
   {
     "action": {
       "type": "order",
       "a": 0,
       "b": true,
       "p": "108000.0",
       "s": "0.00006000",
       "r": false,
       "t": {
         "limit": {
           "tif": "Gtc"
         }
       },
       "c": "1759132034800"
     },
     "nonce": 1759132034800,
     "signature": [
       "0c1190ba43fde20c5bdb496d91359cc432fbd1254551060092cf9209dfff84b63552ece7310f54b2c6ec0af077eaf13f30e1109b4a0ab5e123f0f9750dc90804"
     ],
     "pubkey": "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
   }
   ```

## Method 2: Programmatic Integration

For direct integration into your application, you can use the SDK's core functions programmatically.

### Implementation

```typescript
import { Keypair, PublicKey } from "@solana/web3.js";
import {
  createHyperliquidContext,
  buildPermitEnvelopesFromExchangeRequest,
  signPermits,
  ClusterType,
  HyperliquidExchangeAction,
  HyperliquidExchangeRequest
} from "ambient-ember-sdk";

let ambientKeypair: Keypair | null = null;

function mapTifForAmbient(tif: "Gtc" | "Ioc" | "FrontendMarket"): "Gtc" | "Ioc" | "Alo" {
  // Map HL FrontendMarket to IOC for ambient REST semantics
  if (tif === "Ioc" || tif === "FrontendMarket") return "Ioc";
  return "Gtc";
}

function normalizeToHexArray(value: string | string[]) {
  if (Array.isArray(value)) {
    return value.map((item) =>
      typeof item === "string" ? item : Buffer.from(item).toString("hex"),
    );
  }
  if (typeof value === "string") {
    return [value];
  }
  return [Buffer.from(value).toString("hex")];
}

function alignEnvelopeExpiry(envelope: PermitEnvelopeV1) {
  const thousand = 1000n;
  const sixty = 60n;
  const nonce = envelope.nonce;
  const baseNonce = nonce - (nonce % thousand);
  const nonceSeconds = baseNonce / thousand;
  envelope.expiresUnix = nonceSeconds + sixty;
}

/**
 * Sign a payload using the Solana keypair
 * Based on the SDK's permit envelope signing approach
 */
function signPayloadWithKeypair(action: HyperliquidExchangeAction, signer: Keypair) {
  const nonce = Date.now();

  // Create the payload to sign (similar to SDK approach)
  const payload = {
    action,
    nonce,
    pubkey: signer.publicKey.toString(),
  };

  if (!payload?.action) {
    throw new Error("Payload must include 'action'");
  }
  if (payload.nonce == null) {
    payload.nonce = Date.now();
  }

  const markets = [
    { index: 0, symbol: "BTC-PERP", marketId: 64n, baseDecimals: 8, quoteDecimals: 6 },
  ];
  const programId = new PublicKey("6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g");
  const context = createHyperliquidContext(markets, programId, signer.publicKey, {
    clusterType: ClusterType.Testnet,
  });

  const envelopes = buildPermitEnvelopesFromExchangeRequest(
    payload as HyperliquidExchangeRequest,
    context,
  );
  envelopes.forEach(alignEnvelopeExpiry);

  const signResult = signPermits(envelopes, signer, "hex");
  const signatureHex = normalizeToHexArray(signResult.signatureList ?? signResult.signatures);

  const output = JSON.parse(JSON.stringify(payload)) as SignedHyperliquidExchangeRequest;
  output.signature = signatureHex;
  output.pubkey = payload.pubkey ?? payload.action?.recipient ?? signer.publicKey.toBase58();

  return output;
}
```

### Usage Example

```typescript
// Load your keypair
const secret = JSON.parse(fs.readFileSync('devkey.json', 'utf8'));
const signer = Keypair.fromSecretKey(Uint8Array.from(secret));

// Create an action
const action = {
  type: "order",
  a: 0,
  b: true,
  p: "108000.0",
  s: "0.00006000",
  r: false,
  t: {
    limit: {
      tif: "Gtc"
    }
  }
};

// Sign the payload
const signedPayload = signPayloadWithKeypair(action, signer);

// Send to Ambient API
const response = await fetch('https://embindexer.net/ember/api/dev/v1/exchange', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(signedPayload)
});
```

## Supported Action Types

The SDK supports all Ambient Finance action types:

### Order Operations
- **`order`** - Place a limit order
- **`cancel`** - Cancel orders by ID
- **`cancelByCloid`** - Cancel orders by client order ID
- **`modify`** - Modify an existing order
- **`batchOrder`** - Place multiple orders
- **`modifyBatch`** - Modify multiple orders

### Account Operations
- **`updateLeverage`** - Update leverage for an asset
- **`faucet`** - Request testnet funds
- **`withdraw`** - Withdraw funds
- **`noop`** - No-operation (for testing)

## Configuration Details

### Market Configuration
The SDK is configured for BTC-PERP trading:
```typescript
const markets = [
  { 
    index: 0, 
    symbol: "BTC-PERP", 
    marketId: 64n, 
    baseDecimals: 8, 
    quoteDecimals: 6 
  }
];
```

### Program ID
```typescript
const programId = new PublicKey("6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g");
```

### Context Options
```typescript
{
  clusterType: ClusterType.Testnet,
  expirySeconds: 60,
  hlWindowK: 128,
  maxFeeQuote: 1_000_000n
}
```

## Key Features

1. **Permit-based Signing**: Uses Solana's permit system for secure transaction authorization
2. **Automatic Nonce Generation**: Generates millisecond timestamps for replay protection
3. **Expiry Management**: Automatically sets 60-second expiry windows
4. **Multiple Action Support**: Handles all Ambient Finance action types
5. **Hex Signature Encoding**: Returns signatures in hex format for API compatibility

## Python Integration

For Python applications, use subprocess to call the CLI script:

```python
import subprocess
import json
import tempfile

def sign_payload_with_sdk(payload, devkey_path="devkey.json", sdk_path="ambient-ember-sdk"):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f)
        temp_path = f.name

    try:
        result = subprocess.run([
            'node',
            f'{sdk_path}/scripts/signPayload.mjs',
            devkey_path,
            temp_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"SDK signing failed: {result.stderr}")

        return json.loads(result.stdout)
    finally:
        os.unlink(temp_path)
```

## Security Considerations

1. **Keypair Protection**: Keep your `devkey.json` file secure and never commit it to version control
2. **Nonce Uniqueness**: The SDK automatically generates unique nonces to prevent replay attacks
3. **Expiry Windows**: Signed payloads expire after 60 seconds for security
4. **Testnet Only**: This configuration is for testnet usage; adjust for mainnet deployment

## Troubleshooting

### Common Issues

1. **"SDK not found"**: Ensure the SDK is properly installed and built
2. **"Invalid signature"**: Check that your keypair file is correctly formatted
3. **"Unknown market"**: Verify the asset index (0 for BTC-PERP)
4. **"Expired payload"**: Ensure signed payloads are sent within 60 seconds

### Debug Mode

Add logging to see the signing process:

```typescript
console.log("Payload before signing:", payload);
console.log("Envelopes:", envelopes);
console.log("Sign result:", signResult);
```

## API Endpoint

Send signed payloads to:
```
POST https://embindexer.net/ember/api/dev/v1/exchange
Content-Type: application/json
```

## Additional Resources

- [Ambient Ember SDK Repository](https://github.com/CrocSwap/ambient-ember-sdk)
- [Ambient Finance Documentation](https://docs.ambient.finance/)
- [Solana Web3.js Documentation](https://solana-labs.github.io/solana-web3.js/)