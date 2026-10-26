import asyncio

import aiocoap


URI = "coap://127.0.0.1:5683/iot/lab/message"


async def main():
    student_name = input("Nhap ho ten sinh vien: ").strip()
    student_id = input("Nhap ma sinh vien: ").strip()
    if not student_name or not student_id:
        raise ValueError("Ho ten va ma sinh vien khong duoc de trong.")

    context = await aiocoap.Context.create_client_context()
    try:
        print("Sending GET request...")
        print(f"URI: {URI}")
        get_response = await context.request(
            aiocoap.Message(code=aiocoap.GET, uri=URI)
        ).response
        print("Response:")
        print(f"Code: {get_response.code}")
        print(f"Payload: {get_response.payload.decode('utf-8')}")

        payload = (
            f"Xin chao tu CoAP Client - {student_id} - {student_name}"
        ).encode("utf-8")
        print("Sending POST request...")
        print(f"Payload: {payload.decode('utf-8')}")
        post_response = await context.request(
            aiocoap.Message(code=aiocoap.POST, uri=URI, payload=payload)
        ).response
        print("Response:")
        print(f"Code: {post_response.code}")
        print(f"Payload: {post_response.payload.decode('utf-8')}")
    except (aiocoap.error.NetworkError, OSError) as exc:
        print(f"Khong the ket noi toi CoAP Server: {exc}")
    finally:
        await context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCoAP Client stopped")
