import asyncio
from datetime import datetime

import aiocoap
import aiocoap.resource as resource


class MessageResource(resource.Resource):
    async def render_get(self, request):
        print(f"GET request received: /{'/'.join(request.opt.uri_path)}")
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload="Xin chao tu CoAP Server".encode("utf-8"),
        )

    async def render_post(self, request):
        try:
            message = request.payload.decode("utf-8").strip()
        except UnicodeDecodeError:
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload="Payload phai duoc ma hoa UTF-8".encode("utf-8"),
            )

        if not message:
            return aiocoap.Message(
                code=aiocoap.BAD_REQUEST,
                payload="Thong diep khong duoc de trong".encode("utf-8"),
            )

        print("POST request received:")
        print(f"Payload: {message}")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        return aiocoap.Message(
            code=aiocoap.CHANGED,
            payload="Server da nhan thong diep".encode("utf-8"),
        )


async def main():
    site = resource.Site()
    site.add_resource(["iot", "lab", "message"], MessageResource())
    context = await aiocoap.Context.create_server_context(
        site, bind=("127.0.0.1", 5683)
    )
    print("CoAP Server started on port 5683")
    try:
        await asyncio.Event().wait()
    finally:
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCoAP Server stopped")
