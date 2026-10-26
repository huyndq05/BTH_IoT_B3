import asyncio
import json

import aiocoap
import aiocoap.resource as resource
from aiocoap.numbers import ContentFormat


JSON_FORMAT = ContentFormat.JSON


class LightStatusResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.status = "OFF"

    def _response(self, code=aiocoap.CONTENT, payload=None):
        if payload is None:
            payload = {
                "device_id": "light01",
                "status": self.status,
            }
        return aiocoap.Message(
            code=code,
            payload=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            content_format=JSON_FORMAT,
        )

    async def render_get(self, request):
        return self._response()

    async def render_put(self, request):
        try:
            data = json.loads(request.payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload=b"Payload must be valid UTF-8 JSON",
            )

        if not isinstance(data, dict):
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload=b"Payload must be a JSON object",
            )
        if data.get("device_id") != "light01":
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload=b"device_id must be light01",
            )
        command = data.get("command")
        if command not in ("ON", "OFF"):
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload=b"command must be ON or OFF",
            )

        previous_status = self.status
        print("PUT request received:")
        print("Device: light01")
        print(f"Command: {command}")
        self.status = command
        if self.status != previous_status:
            print(f"Light state changed: {previous_status} -> {self.status}")
            self.updated_state()
            print(f"Notify observers: {self.status}")

        return self._response(
            code=aiocoap.CHANGED,
            payload={
                "device_id": "light01",
                "status": self.status,
                "message": "Da cap nhat trang thai den",
            },
        )

    def update_observation_count(self, count):
        if count:
            print("New Observe registration received")


async def main():
    site = resource.Site()
    site.add_resource(
        ["iot", "lab", "light01", "status"], LightStatusResource()
    )
    context = await aiocoap.Context.create_server_context(
        site, bind=("127.0.0.1", 5683)
    )
    print("CoAP Smart Light Server started...")
    print("Resource: /iot/lab/light01/status")
    try:
        await asyncio.Event().wait()
    finally:
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSmart Light Server stopped")
