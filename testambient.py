# Reference initial implementation for testing ambient APIs. Use testambient.ts instead

import asyncio
import httpx
import time

HYPERLIQUID_URL = "https://api.hyperliquid.xyz"
AMBIENT_URL = "https://embindexer.net/ember/api/dev/v1"

AMBIENT_TEST_ADDRESS = "5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"
# HYPERLIQUID_TEST_ADDRESS = "0x0f6410E884F115166f82E3FFB5840BAdc20619e1"
HYPERLIQUID_TEST_ADDRESS = "0x5b9306593aE710a66832C4101E019E3E96f65d0a"



async def do_hl_info_call(payload):
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        response = await client.post(HYPERLIQUID_URL + "/info", json=payload)
        end_time = time.time()
        print(f"HL info call with payload type \"{payload['type']}\" took {end_time - start_time:.3f} seconds")
        return response.json()

async def do_ambient_info_call(payload):
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        response = await client.post(AMBIENT_URL + "/info", json=payload)
        end_time = time.time()
        print(f"Ambient info call with payload type \"{payload['type']}\" took {end_time - start_time:.3f} seconds")
        print(payload)
        print(response.text)
        return response.json()

def compare_json_shapes(obj1, obj2, path="", check_is_hashmap=True):
    """Smart comparison with rules for different data types"""
    if type(obj1) != type(obj2):
        print(f"Type mismatch at {path}: {type(obj1).__name__} vs {type(obj2).__name__}")
        return False
    
    if isinstance(obj1, dict):
        # Detect if this looks like a hashmap/lookup table
        is_hashmap = check_is_hashmap and path == "" and all(
            isinstance(k, str) and (k.startswith('@') or k.isupper() or len(k) <= 10)
            for k in list(obj1.keys())[:10]  # Sample first 10 keys
        )
        
        if is_hashmap:
            print(f"Detected hashmap at {path}, comparing value shapes only")
            keys1, keys2 = set(obj1.keys()), set(obj2.keys())
            
            # Find common keys or use samples
            common_keys = keys1 & keys2
            if common_keys:
                sample_key = next(iter(common_keys))
                return compare_json_shapes(
                    obj1[sample_key], obj2[sample_key], f"{path}.<value>", check_is_hashmap
                )
            elif keys1 and keys2:
                # Use samples from each
                key1, key2 = next(iter(keys1)), next(iter(keys2))
                print(f"  Comparing {key1} vs {key2}")
                return compare_json_shapes(
                    obj1[key1], obj2[key2], f"{path}.<value>", check_is_hashmap
                )
            return True  # Both empty
        else:
            # Regular object - strict key matching
            keys1, keys2 = set(obj1.keys()), set(obj2.keys())
            if keys1 != keys2:
                print(f"Key mismatch at {path}:")
                if keys1 - keys2: print(f"  Only in first: {keys1 - keys2}")
                if keys2 - keys1: print(f"  Only in second: {keys2 - keys1}")
                return False
            
            return all(
                compare_json_shapes(obj1[k], obj2[k], f"{path}.{k}", check_is_hashmap)
                for k in keys1
            )
    
    elif isinstance(obj1, list):
        if len(obj1) != len(obj2):
            print(f"Array length mismatch at {path}: {len(obj1)} vs {len(obj2)}")
            return False
        
        if obj1 and obj2:
            return compare_json_shapes(obj1[0], obj2[0], f"{path}[0]", check_is_hashmap)
    
    return True


async def test_all_mids():
    payload = {
        "type": "allMids"
    }
    print("Testing all mids")
    hl_response = await do_hl_info_call(payload)
    ambient_response = await do_ambient_info_call(payload)
    if compare_json_shapes(hl_response, ambient_response):
        print("JSON shapes match")
    else:
        print("JSON shapes do not match")


async def test_l2_book(symbol):
    payload = {
        "type": "l2Book",
        "coin": symbol
    }
    hl_response = await do_hl_info_call(payload)
    ambient_response = await do_ambient_info_call(payload)
    if compare_json_shapes(hl_response, ambient_response, check_is_hashmap=False):
        print("JSON shapes match")
    else:
        print("JSON shapes do not match")


async def test_user_state():
    hl_payload = {
        "type": "clearinghouseState",
        "user": HYPERLIQUID_TEST_ADDRESS
    }
    hl_response = await do_hl_info_call(hl_payload)
    ambient_payload = {
        "type": "clearinghouseState",
        "user": AMBIENT_TEST_ADDRESS
    }
    ambient_response = await do_ambient_info_call(ambient_payload)
    if compare_json_shapes(hl_response, ambient_response, check_is_hashmap=False):
        print("JSON shapes match")
    else:
        print("JSON shapes do not match")


async def main():
    # await test_all_mids()
    # await test_l2_book("BTC")
    await test_user_state()

if __name__ == "__main__":
    asyncio.run(main())
