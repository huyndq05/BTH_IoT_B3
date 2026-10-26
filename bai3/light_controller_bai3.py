import asyncio
import json

import aiocoap
from aiocoap.numbers import ContentFormat


URI = "coap://127.0.0.1:5683/iot/lab/light01/status"


async def main():
    context = await aiocoap.Context.create_client_context()
    try:
        while True:
            try:
                command = input(
                    "Nhap lenh (ON/OFF/STATUS/EXIT): "
                ).strip().upper()
            except EOFError:
                break

            if command == "EXIT":
                break
            if command not in ("ON", "OFF", "STATUS"):
                print("Lenh khong hop le. Hay nhap ON, OFF, STATUS hoac EXIT.")
                continue

            try:
                if command in ("ON", "OFF"):
                    payload = json.dumps(
                        {"device_id": "light01", "command": command}
                    ).encode("utf-8")
                    print("Sending PUT request...")
                    response = await context.request(
                        aiocoap.Message(
                            code=aiocoap.PUT,
                            uri=URI,
                            payload=payload,
                            content_format=ContentFormat.JSON,
                        )
                    ).response
                    print(f"Response Code: {response.code}")
                    if response.code.is_successful():
                        message = (
                            "Da bat den light01"
                            if command == "ON"
                            else "Da tat den light01"
                        )
                        print(message)
                    else:
                        print(response.payload.decode("utf-8", errors="replace"))
                else:
                    print("Sending GET request...")
                    response = await context.request(
                        aiocoap.Message(code=aiocoap.GET, uri=URI)
                    ).response
                    print("Response:")
                    print(response.payload.decode("utf-8"))
            except (aiocoap.error.NetworkError, OSError) as exc:
                print(f"Khong the ket noi toi CoAP Server: {exc}")
    finally:
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nController stopped")
