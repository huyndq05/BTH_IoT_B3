import asyncio
import json
import random

import aiocoap
import aiocoap.resource as resource
from aiocoap.numbers import ContentFormat


JSON_FORMAT = ContentFormat.JSON


class SensorResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.data = self._generate_data()

    @staticmethod
    def _generate_data():
        return {
            "device_id": "sensor01",
            "temperature": round(random.uniform(20.0, 40.0), 1),
            "humidity": round(random.uniform(30.0, 80.0), 1),
        }

    async def update_sensor(self):
        while True:
            await asyncio.sleep(3)
            self.data = self._generate_data()

    async def render_get(self, request):
        payload = json.dumps(self.data, ensure_ascii=False).encode("utf-8")
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=payload,
            content_format=JSON_FORMAT,
        )


async def main():
    sensor = SensorResource()
    site = resource.Site()
    site.add_resource(["iot", "lab", "sensor01", "data"], sensor)
    context = await aiocoap.Context.create_server_context(
        site, bind=("127.0.0.1", 5683)
    )
    updater = asyncio.create_task(sensor.update_sensor())
    print("Sensor CoAP Server started on port 5683")
    print("Resource: /iot/lab/sensor01/data")
    try:
        await asyncio.Event().wait()
    finally:
        updater.cancel()
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSensor CoAP Server stopped")
