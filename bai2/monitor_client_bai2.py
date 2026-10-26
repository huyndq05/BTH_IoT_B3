import asyncio
import json
from datetime import datetime

import aiocoap


URI = "coap://127.0.0.1:5683/iot/lab/sensor01/data"


async def main():
    context = await aiocoap.Context.create_client_context()
    print(f"Monitoring sensor at {URI} every 3 seconds. Press Ctrl+C to stop.")
    try:
        while True:
            try:
                response = await context.request(
                    aiocoap.Message(code=aiocoap.GET, uri=URI)
                ).response
                data = json.loads(response.payload.decode("utf-8"))
                device_id = data["device_id"]
                temperature = float(data["temperature"])
                humidity = float(data["humidity"])
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                print(f"Server tra ve JSON khong hop le: {exc}")
            except (KeyError, TypeError, ValueError) as exc:
                print(f"Du lieu cam bien khong hop le: {exc}")
            except (aiocoap.error.NetworkError, OSError) as exc:
                print(f"Khong the doc du lieu cam bien: {exc}")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Received sensor data")
                print(f"Device: {device_id}")
                print(f"Temperature: {temperature:.1f} C")
                print(f"Humidity: {humidity:.1f} %")
                warnings = []
                if temperature > 35:
                    warnings.append("CANH BAO: Nhiet do cao")
                if humidity < 40:
                    warnings.append("CANH BAO: Do am thap")
                for warning in warnings:
                    print(warning)
                if not warnings:
                    print("Trang thai: Binh thuong")
                print("------------------------------")

            await asyncio.sleep(3)
    finally:
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
