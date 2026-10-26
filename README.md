# Thực hành buổi 3 - Lập trình Python với giao thức CoAP

## Thông tin sinh viên/nhóm

- Họ tên sinh viên 1: Phạm Chí Hiếu
- Mã sinh viên: B23DCCN309
- Họ tên sinh viên 2: Nguyễn Đình Quang Huy
- Mã sinh viên: B23DCCN393
- Nhóm: 15

## Môi trường

- Python 3.10 trở lên
- Thư viện: `aiocoap`
- CoAP sử dụng UDP, cổng mặc định `5683`

Cài đặt trong thư mục `CoAP_Lab`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Nếu PowerShell chặn kích hoạt môi trường ảo, có thể chạy trực tiếp bằng
`.\.venv\Scripts\python.exe`.

Server và client mặc định dùng `127.0.0.1:5683` trên cùng máy. Nếu chạy client
trên máy khác, đổi địa chỉ bind `127.0.0.1` trong file server tương ứng thành
địa chỉ IP LAN của máy server, đồng thời sửa địa chỉ trong biến `URI` của
client từ `127.0.0.1` thành địa chỉ IP đó. Cần cho phép UDP cổng `5683` trên
tường lửa.

## Bài 1 - Gửi và nhận thông điệp

Tài nguyên: `coap://127.0.0.1:5683/iot/lab/message`

Mở hai terminal tại thư mục `CoAP_Lab`.

Terminal 1 - chạy server:

```powershell
python .\bai1\coap_server_bai1.py
```

Terminal 2 - chạy client:

```powershell
python .\bai1\coap_client_bai1.py
```

Client gửi yêu cầu GET để nhận lời chào, sau đó yêu cầu nhập họ tên và mã sinh
viên để gửi thông điệp POST. Server in nội dung và thời điểm nhận, rồi trả về
mã phản hồi `2.04 Changed`.

## Bài 2 - Giám sát cảm biến

Tài nguyên: `coap://127.0.0.1:5683/iot/lab/sensor01/data`

Terminal 1 - chạy server:

```powershell
python .\bai2\sensor_server_bai2.py
```

Terminal 2 - chạy client giám sát:

```powershell
python .\bai2\monitor_client_bai2.py
```

Server tạo lại nhiệt độ và độ ẩm sau mỗi 3 giây. Yêu cầu GET trả về dữ liệu
JSON với Content-Format `application/json`. Client truy vấn mỗi 3 giây, hiển thị
thời điểm nhận và cảnh báo khi nhiệt độ trên 35°C hoặc độ ẩm dưới 40%. Nhấn
Ctrl+C để dừng chương trình.

## Bài 3 - Điều khiển và giám sát đèn thông minh bằng Observe

Tài nguyên: `coap://127.0.0.1:5683/iot/lab/light01/status`

Mở ba terminal. Chạy server trước:

```powershell
python .\bai3\light_server_bai3.py
```

Terminal 2 - chạy client giám sát Observe:

```powershell
python .\bai3\light_monitor_bai3.py
```

Terminal 3 - chạy client điều khiển:

```powershell
python .\bai3\light_controller_bai3.py
```

Nhập `ON`, `OFF`, `STATUS` hoặc `EXIT` trong client điều khiển. Client giám sát
đăng ký CoAP Observe và nhận thông báo từ server khi trạng thái thay đổi; client
này không dùng GET định kỳ để phát hiện thay đổi. Nhấn Ctrl+C để dừng client
giám sát.

## Kết quả và minh chứng

- Bài 1: GET nhận lời chào; POST gửi thông điệp, server hiển thị nội dung và
  thời điểm nhận rồi client nhận phản hồi xác nhận.
- Bài 2: GET nhận dữ liệu JSON của `sensor01`; client hiển thị dữ liệu và cảnh
  báo theo các ngưỡng trong đề bài.
- Bài 3: GET đọc được trạng thái; PUT `ON`/`OFF` cập nhật trạng thái; các client
  Observe nhận được thông báo khi trạng thái thay đổi.


## Cấu trúc thư mục

```text
BTH_IoT_B3/
|-- bai1/
|   |-- coap_server_bai1.py
|   `-- coap_client_bai1.py
|-- bai2/
|   |-- sensor_server_bai2.py
|   `-- monitor_client_bai2.py
|-- bai3/
|   |-- light_server_bai3.py
|   |-- light_controller_bai3.py
|   `-- light_monitor_bai3.py
|-- requirements.txt
`-- README.md
```
