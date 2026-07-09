# Sử dụng Python phiên bản nhẹ để tiết kiệm tài nguyên
FROM python:3.9-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy toàn bộ code từ máy tính của bạn vào trong container
COPY . .

# Đây là lệnh sẽ chạy khi container khởi động
# Sau này chúng ta sẽ thay đổi nó thành lệnh chấm bài
CMD ["python", "main.py"]


