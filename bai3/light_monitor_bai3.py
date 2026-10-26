import asyncio
import json
from datetime import datetime

import aiocoap


URI = "coap://127.0.0.1:5683/iot/lab/light01/status"


def display_state(response, is_initial):
    try:
        data = json.loads(response.payload.decode("utf-8"))
        device_id = data["device_id"]
        status = data["status"]
        if status not in ("ON", "OFF"):
            raise ValueError("status must be ON or OFF")
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Observe payload is invalid: {exc}")
        return False

    label = "Initial State" if is_initial else "State Updated"
    if is_initial:
        print("Observe registration successful")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {label}")
    print(f"Device: {device_id}")
    print(f"Status: {status}")
    return True


async def main():
    context = await aiocoap.Context.create_client_context()
    request = aiocoap.Message(code=aiocoap.GET, uri=URI, observe=0)
    requester = context.request(request)
    print("Registering CoAP Observe...")
    try:
        initial_response = await requester.response
        display_state(initial_response, is_initial=True)
        async for response in requester.observation:
            display_state(response, is_initial=False)
    except (aiocoap.error.NetworkError, OSError) as exc:
        print(f"Observe connection failed: {exc}")
    finally:
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
