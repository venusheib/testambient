const HYPERLIQUID_URL = "https://api.hyperliquid.xyz";
const AMBIENT_URL = "https://embindexer.net/ember/api/dev/v1";

const AMBIENT_TEST_ADDRESS = "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK";
const HYPERLIQUID_TEST_ADDRESS = "0x0f6410E884F115166f82E3FFB5840BAdc20619e1";
// const HYPERLIQUID_TEST_ADDRESS = "0x5b9306593aE710a66832C4101E019E3E96f65d0a";

interface ApiPayload {
  type: string;
  coin?: string;
  user?: string;
  aggregateByTime?: boolean;
  startTime?: number;
  req?: any;
}

async function doHlInfoCall(payload: ApiPayload): Promise<any> {
  const startTime = Date.now();
  const response = await fetch(`${HYPERLIQUID_URL}/info`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  const endTime = Date.now();
  console.log(`HL info call with payload type "${payload.type}" took ${(endTime - startTime) / 1000} seconds`);
  return response.json();
}

async function doAmbientInfoCall(payload: ApiPayload): Promise<any> {
  const startTime = Date.now();
  const response = await fetch(`${AMBIENT_URL}/info`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  const endTime = Date.now();
  const text = await response.text();
  console.log(`Ambient info call with payload type "${payload.type}" took ${(endTime - startTime) / 1000} seconds`);
  console.log(text);

  console.log(payload);
  return JSON.parse(text);
}

function getTypeName(obj: any): string {
  if (obj === null) return 'null';
  if (Array.isArray(obj)) return 'array';
  return typeof obj;
}

function compareJsonShapes(obj1: any, obj2: any, path: string = "", checkIsHashmap: boolean = true): boolean {
  /**
   * Smart comparison with rules for different data types
   */
  if (getTypeName(obj1) !== getTypeName(obj2)) {
    console.log(`Type mismatch at ${path}: ${getTypeName(obj1)} vs ${getTypeName(obj2)}`);
    return false;
  }
  
  if (typeof obj1 === 'object' && obj1 !== null && !Array.isArray(obj1)) {
    // Detect if this looks like a hashmap/lookup table
    const keys = Object.keys(obj1);
    const isHashmap = checkIsHashmap && path === "" && keys.slice(0, 10).every(k => 
      typeof k === 'string' && (k.startsWith('@') || k === k.toUpperCase() || k.length <= 10)
    );
    
    if (isHashmap) {
      console.log(`Detected hashmap at ${path}, comparing value shapes only`);
      const keys1 = new Set(Object.keys(obj1));
      const keys2 = new Set(Object.keys(obj2));
      
      // Find common keys or use samples
      const commonKeys = new Set([...keys1].filter(k => keys2.has(k)));
      if (commonKeys.size > 0) {
        const sampleKey = commonKeys.values().next().value;
        return compareJsonShapes(
          obj1[sampleKey], obj2[sampleKey], `${path}.<value>`, checkIsHashmap
        );
      } else if (keys1.size > 0 && keys2.size > 0) {
        // Use samples from each
        const key1 = keys1.values().next().value;
        const key2 = keys2.values().next().value;
        console.log(`  Comparing ${key1} vs ${key2}`);
        return compareJsonShapes(
          obj1[key1], obj2[key2], `${path}.<value>`, checkIsHashmap
        );
      }
      return true; // Both empty
    } else {
      // Regular object - strict key matching
      const keys1 = new Set(Object.keys(obj1));
      const keys2 = new Set(Object.keys(obj2));
      
      if (keys1.size !== keys2.size || ![...keys1].every(k => keys2.has(k))) {
        console.log(`Key mismatch at ${path}:`);
        const onlyInFirst = [...keys1].filter(k => !keys2.has(k));
        const onlyInSecond = [...keys2].filter(k => !keys1.has(k));
        if (onlyInFirst.length > 0) console.log(`  Only in first: ${JSON.stringify(onlyInFirst)}`);
        if (onlyInSecond.length > 0) console.log(`  Only in second: ${JSON.stringify(onlyInSecond)}`);
        return false;
      }
      
      return [...keys1].every(k => 
        compareJsonShapes(obj1[k], obj2[k], `${path}.${k}`, checkIsHashmap)
      );
    }
  } else if (Array.isArray(obj1)) {
    // if (obj1.length !== obj2.length) {
    //   console.log(`Array length mismatch at ${path}: ${obj1.length} vs ${obj2.length}`);
    //   return false;
    // }
    
    if (obj1.length > 0 && obj2.length > 0) {
      return compareJsonShapes(obj1[0], obj2[0], `${path}[0]`, checkIsHashmap);
    }
  }
  
  return true;
}

async function testAllMids(): Promise<void> {
  const payload: ApiPayload = {
    type: "allMids"
  };
  console.log("Testing all mids");
  const hlResponse = await doHlInfoCall(payload);
  const ambientResponse = await doAmbientInfoCall(payload);
  if (compareJsonShapes(hlResponse, ambientResponse)) {
    console.log("JSON shapes match");
  } else {
    console.log("JSON shapes do not match");
  }
}

async function testL2Book(symbol: string): Promise<void> {
  const payload: ApiPayload = {
    type: "l2Book",
    coin: symbol
  };
  const hlResponse = await doHlInfoCall(payload);
  const ambientResponse = await doAmbientInfoCall(payload);
  if (compareJsonShapes(hlResponse, ambientResponse, "", false)) {
    console.log("JSON shapes match");
  } else {
    console.log("JSON shapes do not match");
  }
}

async function testUserState(): Promise<void> {
  const hlPayload: ApiPayload = {
    type: "clearinghouseState",
    user: HYPERLIQUID_TEST_ADDRESS
  };
  const hlResponse = await doHlInfoCall(hlPayload);
  console.log("HL response");
  orderJson(hlResponse);
  const ambientPayload: ApiPayload = {
    type: "clearinghouseState",
    user: AMBIENT_TEST_ADDRESS
  };
  const ambientResponse = await doAmbientInfoCall(ambientPayload);
  console.log("Ambient response");
  orderJson(ambientResponse);
  console.log(ambientResponse);
  if (compareJsonShapes(hlResponse, ambientResponse, "", false)) {
    console.log("JSON shapes match");
  } else {
    console.log("JSON shapes do not match");
  }
}

async function testOpenOrders(): Promise<void> {
  const hlPayload: ApiPayload = {
    type: "openOrders",
    user: HYPERLIQUID_TEST_ADDRESS
  };
  const hlResponse = await doHlInfoCall(hlPayload);
  const ambientPayload: ApiPayload = {
    type: "openOrders",
    user: AMBIENT_TEST_ADDRESS
  };
  console.log("HL response");
  orderJson(hlResponse);
  const ambientResponse = await doAmbientInfoCall(ambientPayload);
  console.log("Ambient response");
  orderJson(ambientResponse);
  if (compareJsonShapes(hlResponse, ambientResponse, "", false)) {
    console.log("JSON shapes match");
  } else {
    console.log("JSON shapes do not match");
  }
}

async function testHistoricalOrders(): Promise<void> {
  const hlPayload: ApiPayload = {
    type: "historicalOrders",
    user: HYPERLIQUID_TEST_ADDRESS
  };
  const hlResponse = await doHlInfoCall(hlPayload);
  const ambientPayload: ApiPayload = {
    type: "historicalOrders",
    user: AMBIENT_TEST_ADDRESS
  };
  const ambientResponse = await doAmbientInfoCall(ambientPayload);
  console.log("HL response");
  orderJson(hlResponse);
  console.log("Ambient response");
  orderJson(ambientResponse);
  if (compareJsonShapes(hlResponse, ambientResponse, "", false)) {
    console.log("JSON shapes match");
  } else {
    console.log("JSON shapes do not match");
  }
}

async function testUserFills(): Promise<void> {
  const hlPayload: ApiPayload = {
    type: "userFills",
    user: HYPERLIQUID_TEST_ADDRESS,
    aggregateByTime: false,
  };
  const hlResponse = await doHlInfoCall(hlPayload);
  const ambientPayload: ApiPayload = {
    type: "userFills",
    user: AMBIENT_TEST_ADDRESS
  };
  const ambientResponse = await doAmbientInfoCall(ambientPayload);
  console.log("HL response");
  orderJson(hlResponse);
  console.log("Ambient response");
  orderJson(ambientResponse);
  if (compareJsonShapes(hlResponse, ambientResponse, "", false)) {
    console.log("JSON shapes match");
  } else {
    console.log("JSON shapes do not match");
  }
}

async function testUserFillsByTime(): Promise<void> {
  const hlPayload: ApiPayload = {
    type: "userFillsByTime",
    user: HYPERLIQUID_TEST_ADDRESS,
    startTime: 1758546945000 - 86400000,
    aggregateByTime: true,
  };
  const hlResponse = await doHlInfoCall(hlPayload);
  const ambientPayload: ApiPayload = {
    type: "userFillsByTime",
    user: AMBIENT_TEST_ADDRESS,
    startTime: 1758546945000 - 86400000,
    aggregateByTime: true,
  };
  const ambientResponse = await doAmbientInfoCall(ambientPayload);
  console.log("HL response");
  orderJson(hlResponse);
  console.log("Ambient response");
  orderJson(ambientResponse);
  if (compareJsonShapes(hlResponse, ambientResponse, "", false)) {
    console.log("JSON shapes match");
  } else {
    console.log("JSON shapes do not match");
  }
}

async function testMeta(): Promise<void> {
  const hlPayload: ApiPayload = {
    type: "meta"
  };
  const hlResponse = await doHlInfoCall(hlPayload);
  const ambientPayload: ApiPayload = {
    type: "meta"
  };
  const ambientResponse = await doAmbientInfoCall(ambientPayload);
  console.log("HL response");
  orderJson(hlResponse);
  console.log("Ambient response");
  orderJson(ambientResponse);
  if (compareJsonShapes(hlResponse, ambientResponse, "", false)) {
    console.log("JSON shapes match");
  } else {
    console.log("JSON shapes do not match");
  }
}

async function testmetaAndAssetCtxs(): Promise<void> {
  const hlPayload: ApiPayload = {
    type: "metaAndAssetCtxs"
  };
  const hlResponse = await doHlInfoCall(hlPayload);
  const ambientPayload: ApiPayload = {
    type: "metaAndAssetCtxs"
  };
  const ambientResponse = await doAmbientInfoCall(ambientPayload);
  console.log("HL response");
  orderJson(hlResponse);
  console.log("Ambient response");
  orderJson(ambientResponse);
  if (compareJsonShapes(hlResponse, ambientResponse, "", false)) {
    console.log("JSON shapes match");
  } else {
    console.log("JSON shapes do not match");
  }
}

async function testUserFunding(): Promise<void> {
  const hlPayload: ApiPayload = {
    type: "userFunding",
    user: HYPERLIQUID_TEST_ADDRESS
  };
  const hlResponse = await doHlInfoCall(hlPayload);

  const ambientPayload: ApiPayload = {
    type: "userFunding",
    user: AMBIENT_TEST_ADDRESS
  };
  const ambientResponse = await doAmbientInfoCall(ambientPayload);
  console.log("HL response");
  orderJson(hlResponse);
  console.log("Ambient response");
  orderJson(ambientResponse);
  if (compareJsonShapes(hlResponse, ambientResponse, "", false)) {
    console.log("JSON shapes match");
  } else {
    console.log("JSON shapes do not match");
  }
}

async function testFundingHistory(): Promise<void> {
  const hlPayload: ApiPayload = {
    type: "fundingHistory",
    coin: "BTC",
    startTime: 1758546945000 - 86400000
  };
  const hlResponse = await doHlInfoCall(hlPayload);

  const ambientPayload: ApiPayload = {
    type: "fundingHistory",
    coin: "BTC",
    startTime: 1758546945000 - 86400000
  };
  const ambientResponse = await doAmbientInfoCall(ambientPayload);
  console.log("HL response");
  orderJson(hlResponse);
  console.log("Ambient response");
  orderJson(ambientResponse);
  if (compareJsonShapes(hlResponse, ambientResponse, "", false)) {
    console.log("JSON shapes match");
  } else {
    console.log("JSON shapes do not match");
  }
}

async function testPortfolio(): Promise<void> {
  const hlPayload: ApiPayload = {
    type: "portfolio",
    user: HYPERLIQUID_TEST_ADDRESS
  };
  const hlResponse = await doHlInfoCall(hlPayload);
  const ambientPayload: ApiPayload = {
    type: "portfolio",
    user: AMBIENT_TEST_ADDRESS
  };
  const ambientResponse = await doAmbientInfoCall(ambientPayload);
  console.log("HL response");
  orderJson(hlResponse);
  console.log("Ambient response");
  orderJson(ambientResponse);
  if (compareJsonShapes(hlResponse, ambientResponse, "", false)) {
    console.log("JSON shapes match");
  } else {
    console.log("JSON shapes do not match");
  }
}

async function testCandleSnapshot(): Promise<void> {
  const payload: ApiPayload = {
    type: "candleSnapshot",
    req: {
      coin: "BTC",
      interval: "1m",
      startTime: 1758546945000 - 86400000,
      endTime: 1758546945000,
    }
  };

  const hlResponse = await doHlInfoCall(payload);
  const ambientResponse = await doAmbientInfoCall(payload);
  console.log("HL response");
  orderJson(hlResponse);
  console.log("Ambient response");
  orderJson(ambientResponse);
  if (compareJsonShapes(hlResponse, ambientResponse, "", false)) {
    console.log("JSON shapes match");
  } else {
    console.log("JSON shapes do not match");
  }
}



async function main(): Promise<void> {
  // await testAllMids();
  // await testL2Book("BTC");
  // await testUserState();
  // await testOpenOrders();
  // await testHistoricalOrders();
  // await testUserFills();
  // await testUserFillsByTime();
  // await testMeta();
  // await testmetaAndAssetCtxs();
  // await testUserFunding();
  // await testFundingHistory();
  // await testPortfolio();
  await testCandleSnapshot();
}

/**
 * Helper function to order object keys recursively and log formatted JSON
 * @param obj - The object to order and log
 * @param sortKeys - Whether to sort keys alphabetically (default: true)
 */
const orderJson = (obj: any, sortKeys: boolean = true): void => {
  const orderObject = (input: any): any => {
    if (input === null || typeof input !== 'object') {
      return input;
    }
    
    if (Array.isArray(input)) {
      return input.map(orderObject);
    }
    
    const keys = Object.keys(input);
    if (sortKeys) {
      keys.sort();
    }
    
    const orderedObj: any = {};
    keys.forEach(key => {
      orderedObj[key] = orderObject(input[key]);
    });
    
    return orderedObj;
  };
  
  const orderedObj = orderObject(obj);
  console.log(JSON.stringify(orderedObj, null, 2));
};

// Run the main function if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}