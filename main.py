#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
BÁO CÁO BÀI TẬP LỚN - NHẬP MÔN TRÍ TUỆ NHÂN TẠO
Đề tài: XÂY DỰNG HỆ CHUYÊN GIA TƯ VẤN LỰA CHỌN MÁY ẢNH
Trường Đại học Đồng Tháp - Khoa Sư phạm Toán - Tin
Ngành: Sư phạm Tin học - Lớp: ĐHSTIN24B
Giảng viên hướng dẫn: Thạc sĩ Lê Minh Thư
Nhóm thực hiện: Nhóm 22
  1. Lê Minh Đương - MSSV: 0024416868
  2. Nguyễn Hoàng Ân - MSSV: 0024416497
================================================================================
Hướng dẫn chạy chương trình:
  - Chạy Web Server + Hệ chuyên gia: python main.py
  - Sau đó mở trình duyệt tại: http://localhost:8000
  - Hoặc chạy chế độ dòng lệnh (CLI): python main.py --cli
================================================================================
"""

import json
import os
import sys
import webbrowser
from http.server import HTTPServer, ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

# ==============================================================================
# 1. TẬP SỰ KIỆN (FACT BASE) - 7 NHÓM TIÊU CHÍ ĐẦU VÀO (T, L, C, M, V, N, G)
# ==============================================================================
FACTS_META = {
    "T": {
        "name": "Thương hiệu",
        "icon": "brand",
        "items": {
            "T1": "Canon",
            "T2": "Sony",
            "T3": "Nikon",
            "T4": "Fujifilm",
            "T5": "Panasonic"
        }
    },
    "L": {
        "name": "Loại máy ảnh",
        "icon": "camera",
        "items": {
            "L1": "DSLR (Phản xạ ống kính đơn)",
            "L2": "Mirrorless (Không gương lật)"
        }
    },
    "C": {
        "name": "Kích cỡ cảm biến",
        "icon": "sensor",
        "items": {
            "C1": "Full-frame",
            "C2": "Crop (APS-C)",
            "C3": "Medium Format",
            "C4": "Micro Four Thirds / M43"
        }
    },
    "M": {
        "name": "Màn hình cảm ứng",
        "icon": "touch",
        "items": {
            "M1": "Có màn hình cảm ứng",
            "M2": "Không có màn hình cảm ứng"
        }
    },
    "V": {
        "name": "Khả năng quay video",
        "icon": "video",
        "items": {
            "V1": "Quay cơ bản (FHD / 4K 30p)",
            "V2": "Quay nâng cao (4K 60p / 10-bit / Log)",
            "V3": "Quay điện ảnh siêu nét (6K / 8K / RAW)"
        }
    },
    "N": {
        "name": "Mục đích sử dụng",
        "icon": "purpose",
        "items": {
            "N1": "Cơ bản, Du lịch, Đường phố",
            "N2": "Chân dung, Phong cảnh",
            "N3": "Đa dụng, Sự kiện",
            "N4": "Quay Vlog, Sáng tạo nội dung",
            "N5": "Thể thao, Tốc độ cao",
            "N6": "Chuyên sản xuất Video, Điện ảnh",
            "N7": "Chụp Studio, Thương mại"
        }
    },
    "G": {
        "name": "Phân khúc giá",
        "icon": "price",
        "items": {
            "G1": "Từ 0 - 10 triệu đồng",
            "G2": "Từ 10 - 20 triệu đồng",
            "G3": "Từ 20 - 30 triệu đồng",
            "G4": "Từ 30 - 40 triệu đồng",
            "G5": "Từ 40 - 50 triệu đồng",
            "G6": "Từ 50 - 60 triệu đồng",
            "G7": "Từ 60 - 70 triệu đồng",
            "G8": "Từ 70 - 80 triệu đồng",
            "G9": "Trên 80 triệu đồng"
        }
    }
}

# ==============================================================================
# 2. CƠ SỞ DỮ LIỆU TRI THỨC 50 MÁY ẢNH (K1 -> K50)
# ==============================================================================
CAMERAS = [
    {
        "id": "K1",
        "order": 1,
        "name": "Máy ảnh Canon EOS R50",
        "desc": "Canon EOS R50 là dòng máy ảnh không gương lật nhỏ gọn với trọng lượng 328g, trang bị cảm biến 24.2MP và chip DIGIC X. Máy có màn hình xoay lật cảm ứng 3 inch, hệ thống lấy nét Dual Pixel CMOS AF II và hỗ trợ các tính năng tự động thông minh. Phù hợp cho người làm sáng tạo nội dung, quay vlog và gia đình.",
        "brand": "Canon",
        "type": "Mirrorless",
        "sensor": "Crop (APS-C)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p)",
        "purpose": "Quay Vlog, Sáng tạo nội dung",
        "price_range": "10 - 20 triệu đồng (Giá tham khảo: 15.490.000 VNĐ)",
        "price_num": 15490000,
        "price_text": "15.490.000đ",
        "rules": [
            1,
            2
        ],
        "facts": [
            "C2",
            "G2",
            "L2",
            "M1",
            "N1",
            "N4",
            "T1",
            "V1"
        ],
        "mp": "24.2MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "Cảm ứng",
        "discount": 16,
        "old_price_text": "18.440.000đ",
        "smember_text": "155.000đ",
        "promo": "Tặng đèn LED mini Godox LITEMONS LED6R và thẻ nhớ SD 64GB tốc độ cao",
        "rating": "4.9",
        "reviews": 18
    },
    {
        "id": "K2",
        "order": 2,
        "name": "Máy ảnh Canon EOS R100",
        "desc": "Canon EOS R100 là dòng máy ảnh không gương lật nhỏ nhẹ với trọng lượng chỉ 309g, sở hữu cảm biến 24.1MP và chip xử lý DIGIC 8. Máy được trang bị hệ thống lấy nét Dual Pixel CMOS AF, kính ngắm điện tử EVF sắc nét cùng giao diện trực quan, dễ làm quen. Đây là lựa chọn kinh tế hàng đầu dành cho học sinh, sinh viên và người mới bước đầu tiếp cận nhiếp ảnh.",
        "brand": "Canon",
        "type": "Mirrorless",
        "sensor": "Crop (APS-C)",
        "touch": "Không",
        "video": "Quay cơ bản (4K 24p, Full HD 60p)",
        "purpose": "Cơ bản, Du lịch, Đường phố",
        "price_range": "10 - 20 triệu đồng (Giá tham khảo: 11.990.000 VNĐ)",
        "price_num": 11990000,
        "price_text": "11.990.000đ",
        "rules": [
            3,
            4
        ],
        "facts": [
            "C2",
            "G2",
            "L2",
            "M2",
            "N1",
            "N2",
            "T1",
            "V1"
        ],
        "mp": "24.1MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "EVF/OVF",
        "discount": 15,
        "old_price_text": "14.110.000đ",
        "smember_text": "120.000đ",
        "promo": "Giảm ngay 1.500.000đ khi mua kèm ống kính chính hãng & tặng túi máy ảnh",
        "rating": "4.8",
        "reviews": 25
    },
    {
        "id": "K3",
        "order": 3,
        "name": "Máy ảnh Canon EOS R10",
        "desc": "Canon EOS R10 là dòng máy ảnh không gương lật tầm trung sở hữu cảm biến APS-C 24.2MP cùng bộ xử lý DIGIC X mạnh mẽ. Máy nổi bật với khả năng chụp liên tiếp tốc độ cao lên đến 23 khung hình/giây, hệ thống Dual Pixel CMOS AF II với 651 điểm lấy nét theo pha và màn hình LCD cảm ứng xoay lật 3 inch linh hoạt. Phù hợp cho người dùng cần sự đa dụng, vừa chụp ảnh gia đình, du lịch vừa chụp thể thao nhẹ hoặc bắt khoảnh khắc nhanh.",
        "brand": "Canon",
        "type": "Mirrorless",
        "sensor": "Crop (APS-C)",
        "touch": "Có",
        "video": "Quay nâng cao (4K 30p 10-bit HDR-PQ, hỗ trợ 4K 60p crop)",
        "purpose": "Đa dụng",
        "price_range": "10 - 20 triệu đồng (Giá tham khảo: 19.790.000 VNĐ)",
        "price_num": 19790000,
        "price_text": "19.790.000đ",
        "rules": [
            5,
            6,
            7
        ],
        "facts": [
            "C2",
            "G2",
            "L2",
            "M1",
            "N3",
            "N5",
            "T1",
            "V1",
            "V2"
        ],
        "mp": "24.2MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "23 FPS",
        "discount": 18,
        "old_price_text": "24.130.000đ",
        "smember_text": "198.000đ",
        "promo": "Tặng pin dự phòng chính hãng, bộ vệ sinh cảm biến 5 món và balo chống sốc",
        "rating": "5.0",
        "reviews": 32
    },
    {
        "id": "K4",
        "order": 4,
        "name": "Máy ảnh Canon EOS 6D",
        "desc": "Canon EOS 6D là mẫu máy ảnh DSLR Full-frame huyền thoại sở hữu cảm biến CMOS 20.2 MP cùng bộ xử lý hình ảnh DIGIC 5+. Máy nổi bật với chất ảnh trong trẻo, màu da chân dung đặc trưng và khả năng khử nhiễu tốt ở ISO cao. Thân máy đầm tay, bền bỉ, tích hợp kết nối Wi-Fi và định vị GPS tiện lợi. Đây là sự lựa chọn kinh tế hàng đầu cho người muốn trải nghiệm cảm biến Full-frame để chụp ảnh chân dung và phong cảnh.",
        "brand": "Canon",
        "type": "DSLR",
        "sensor": "Full-frame",
        "touch": "Không",
        "video": "Quay cơ bản (Full HD 1080p)",
        "purpose": "Chân dung, Phong cảnh",
        "price_range": "0 - 10 triệu đồng (Giá tham khảo máy cũ: ~ 6.500.000 VNĐ)",
        "price_num": 6500000,
        "price_text": "6.500.000đ",
        "rules": [
            8,
            9
        ],
        "facts": [
            "C1",
            "G1",
            "L1",
            "M2",
            "N1",
            "N2",
            "T1",
            "V1"
        ],
        "mp": "20.2MP",
        "video_short": "FHD 60p",
        "sensor_short": "Full-frame",
        "fps": "EVF/OVF",
        "discount": 14,
        "old_price_text": "7.560.000đ",
        "smember_text": "65.000đ",
        "promo": "Trả góp 0% lãi suất qua thẻ tín dụng, tặng kèm thẻ nhớ SanDisk Extreme Pro 64GB",
        "rating": "4.9",
        "reviews": 39
    },
    {
        "id": "K5",
        "order": 5,
        "name": "Máy ảnh Canon EOS 5D Mark III",
        "desc": "Canon EOS 5D Mark III là mẫu máy ảnh DSLR Full-frame chuyên nghiệp danh tiếng với cảm biến CMOS 22.3 MP và bộ xử lý hình ảnh DIGIC 5+. Máy sở hữu thân vỏ hợp kim magie bền bỉ, hệ thống lấy nét 61 điểm mật độ cao chính xác cùng chất màu ảnh trong trẻo, nịnh mắt. Đây là dòng máy làm nghề sự kiện, chụp cưới và dịch vụ chân dung quen thuộc với độ tin cậy cao.",
        "brand": "Canon",
        "type": "DSLR",
        "sensor": "Full-frame (22.3 MP)",
        "touch": "Không",
        "video": "Quay cơ bản (Full HD 1080p)",
        "purpose": "Đa dụng, Sự kiện",
        "price_range": "10 - 20 triệu đồng (Giá tham khảo đã qua sử dụng: ~ 15.250.000 VNĐ)",
        "price_num": 15250000,
        "price_text": "15.250.000đ",
        "rules": [
            10,
            11
        ],
        "facts": [
            "C1",
            "G2",
            "L1",
            "M2",
            "N2",
            "N3",
            "T1",
            "V1"
        ],
        "mp": "22.3MP",
        "video_short": "FHD 60p",
        "sensor_short": "Full-frame",
        "fps": "EVF/OVF",
        "discount": 16,
        "old_price_text": "18.150.000đ",
        "smember_text": "152.000đ",
        "promo": "Tặng micro thu âm cài áo không dây và chân máy tripod du lịch cao cấp",
        "rating": "5.0",
        "reviews": 46
    },
    {
        "id": "K6",
        "order": 6,
        "name": "Máy ảnh Canon EOS R8",
        "desc": "Canon EOS R8 là dòng máy ảnh không gương lật Full-frame gọn nhẹ với trọng lượng chỉ 414g, trang bị cảm biến CMOS 24.2MP cùng vi xử lý DIGIC X mạnh mẽ. Máy sở hữu hệ thống lấy nét Dual Pixel CMOS AF II thông minh, tốc độ chụp liên tiếp điện tử lên đến 40 fps và màn hình LCD xoay lật cảm ứng 3 inch sắc nét. Thiết bị hỗ trợ quay video chuyên nghiệp chất lượng cao, phù hợp cho người dùng cần sự linh hoạt khi chụp chân dung, phong cảnh và du lịch.",
        "brand": "Canon",
        "type": "Mirrorless",
        "sensor": "Full-frame (24.2 MP)",
        "touch": "Có",
        "video": "Quay nâng cao (4K 60p 10-bit, Canon Log 3, HDR-PQ, Full HD 120p)",
        "purpose": "Chân dung, Phong cảnh",
        "price_range": "20 - 30 triệu đồng (Giá tham khảo: 27.790.000 VNĐ)",
        "price_num": 27790000,
        "price_text": "27.790.000đ",
        "rules": [
            12,
            13,
            14
        ],
        "facts": [
            "C1",
            "G3",
            "L2",
            "M1",
            "N1",
            "N2",
            "N4",
            "T1",
            "V2"
        ],
        "mp": "24.2MP",
        "video_short": "4K UHD",
        "sensor_short": "Full-frame",
        "fps": "40 FPS",
        "discount": 12,
        "old_price_text": "31.580.000đ",
        "smember_text": "278.000đ",
        "promo": "Tặng đèn LED mini Godox LITEMONS LED6R và thẻ nhớ SD 64GB tốc độ cao",
        "rating": "4.8",
        "reviews": 53
    },
    {
        "id": "K7",
        "order": 7,
        "name": "Máy ảnh Canon EOS R6 Mark II",
        "desc": "Canon EOS R6 Mark II là dòng máy ảnh không gương lật Full-frame đa năng cao cấp, sở hữu cảm biến CMOS 24.2 MP cùng bộ xử lý hình ảnh DIGIC X mạnh mẽ. Máy nổi bật với hệ thống lấy nét Dual Pixel CMOS AF II thông minh, tốc độ chụp liên tiếp điện tử lên tới 40 khung hình/giây và hệ thống chống rung thân máy (IBIS) lên tới 8 stops. Trang bị màn hình cảm ứng xoay lật 3 inch, 2 khe thẻ nhớ SD UHS-II và khả năng quay 4K 60p không crop, đây là cỗ máy hoàn hảo cho nhu cầu chụp và quay dịch vụ, sự kiện chuyên nghiệp.",
        "brand": "Canon",
        "type": "Mirrorless",
        "sensor": "Full-frame (24.2 MP)",
        "touch": "Có",
        "video": "Quay nâng cao (4K 60p 10-bit, C-Log 3)",
        "purpose": "Đa dụng",
        "price_range": "40 - 50 triệu đồng (Giá khuyến mãi tham khảo: 40.490.000 VNĐ)",
        "price_num": 40490000,
        "price_text": "40.490.000đ",
        "rules": [
            15,
            16,
            17
        ],
        "facts": [
            "C1",
            "G5",
            "L2",
            "M1",
            "N3",
            "N5",
            "N6",
            "T1",
            "V2"
        ],
        "mp": "24.2MP",
        "video_short": "4K UHD",
        "sensor_short": "Full-frame",
        "fps": "40 FPS",
        "discount": 16,
        "old_price_text": "48.200.000đ",
        "smember_text": "405.000đ",
        "promo": "Giảm ngay 1.500.000đ khi mua kèm ống kính chính hãng & tặng túi máy ảnh",
        "rating": "4.9",
        "reviews": 60
    },
    {
        "id": "K8",
        "order": 8,
        "name": "Máy ảnh Canon EOS R5",
        "desc": "Canon EOS R5 là dòng máy ảnh không gương lật Full-frame chuyên nghiệp cao cấp, sở hữu cảm biến CMOS độ phân giải cao 45 MP kết hợp cùng bộ xử lý hình ảnh DIGIC X mạnh mẽ. Thiết bị nổi bật với khả năng quay video 8K 30p RAW và 4K 120p 10-bit nội bộ, hệ thống lấy nét Dual Pixel CMOS AF II với 1053 điểm tự động cùng hệ thống chống rung cảm biến 5 trục. Thân máy tích hợp màn hình cảm ứng LCD 3.2 inch sắc nét 2.1 triệu điểm ảnh và khe cắm thẻ kép CFexpress/SD UHS-II, rất phù hợp cho nhu cầu chụp ảnh Studio thương mại, quảng cáo và sản xuất video chất lượng cao.",
        "brand": "Canon",
        "type": "Mirrorless",
        "sensor": "Full-frame (45 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (8K 30p RAW, 4K 120p 10-bit)",
        "purpose": "Chụp Studio, Thương mại",
        "price_range": "60 - 70 triệu đồng (Giá khuyến mãi tham khảo: 64.900.000 VNĐ)",
        "price_num": 64900000,
        "price_text": "64.900.000đ",
        "rules": [
            18,
            19,
            20
        ],
        "facts": [
            "C1",
            "G7",
            "L2",
            "M1",
            "N6",
            "N7",
            "T1",
            "V2",
            "V3"
        ],
        "mp": "45MP",
        "video_short": "8K RAW",
        "sensor_short": "Full-frame",
        "fps": "Cảm ứng",
        "discount": 15,
        "old_price_text": "76.350.000đ",
        "smember_text": "649.000đ",
        "promo": "Tặng pin dự phòng chính hãng, bộ vệ sinh cảm biến 5 món và balo chống sốc",
        "rating": "4.8",
        "reviews": 67
    },
    {
        "id": "K9",
        "order": 9,
        "name": "Máy ảnh Canon EOS 90D",
        "desc": "Canon EOS 90D là mẫu máy ảnh DSLR tầm trung mạnh mẽ, được trang bị cảm biến APS-C độ phân giải cao 32.5 MP cùng bộ xử lý hình ảnh DIGIC 8. Máy duy trì ưu điểm của dòng DSLR với kính ngắm quang học lớn, báng cầm đầm tay, pin dung lượng cực \"trâu\" và tốc độ chụp liên tiếp lên đến 10 khung hình/giây. Kết hợp với hệ thống lấy nét Dual Pixel CMOS AF linh hoạt và màn hình cảm ứng xoay lật, đây là thiết bị tuyệt vời dành cho những ai đam mê chụp ảnh thể thao, động vật hoang dã hoặc cần một chiếc DSLR đa dụng cho cả gia đình.",
        "brand": "Canon",
        "type": "DSLR",
        "sensor": "Crop (APS-C) - 32.5 MP",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p không crop)",
        "purpose": "Thể thao, Tốc độ cao",
        "price_range": "20 - 30 triệu đồng (Giá tham khảo: ~ 26.500.000 VNĐ)",
        "price_num": 26500000,
        "price_text": "26.500.000đ",
        "rules": [
            21,
            22
        ],
        "facts": [
            "C2",
            "G3",
            "L1",
            "M1",
            "N3",
            "N5",
            "T1",
            "V1"
        ],
        "mp": "32.5MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "10 FPS",
        "discount": 17,
        "old_price_text": "31.930.000đ",
        "smember_text": "265.000đ",
        "promo": "Trả góp 0% lãi suất qua thẻ tín dụng, tặng kèm thẻ nhớ SanDisk Extreme Pro 64GB",
        "rating": "5.0",
        "reviews": 74
    },
    {
        "id": "K10",
        "order": 10,
        "name": "Máy ảnh Canon EOS R3",
        "desc": "Canon EOS R3 là mẫu máy ảnh không gương lật Full-frame cao cấp hướng đến nhiếp ảnh gia thể thao, báo chí và chim thú chuyên nghiệp. Máy trang bị cảm biến Stacked BSI CMOS 24.1 MP cho tốc độ xử lý vượt trội, hệ thống lấy nét điều khiển bằng mắt (Eye Control AF) độc quyền và tốc độ chụp liên tiếp điện tử lên tới 30 khung hình/giây không chớp đen. Thân máy tích hợp báng cầm dọc đầm tay, chống chịu thời tiết khắc nghiệt cùng khả năng quay video 6K 60p RAW nội bộ chất lượng cao.",
        "brand": "Canon",
        "type": "Mirrorless",
        "sensor": "Full-frame (24.1 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (6K 60p RAW, 4K 120p 10-bit)",
        "purpose": "Thể thao, Tốc độ cao",
        "price_range": "Trên 80 triệu đồng (Giá tham khảo: ~ 125.000.000 VNĐ)",
        "price_num": 125000000,
        "price_text": "125.000.000đ",
        "rules": [
            23,
            24
        ],
        "facts": [
            "C1",
            "G9",
            "L2",
            "M1",
            "N5",
            "N6",
            "T1",
            "V3"
        ],
        "mp": "24.1MP",
        "video_short": "6K Pro",
        "sensor_short": "Full-frame",
        "fps": "30 FPS",
        "discount": 14,
        "old_price_text": "145.350.000đ",
        "smember_text": "1.250.000đ",
        "promo": "Tặng micro thu âm cài áo không dây và chân máy tripod du lịch cao cấp",
        "rating": "4.9",
        "reviews": 81
    },
    {
        "id": "K11",
        "order": 11,
        "name": "Máy ảnh Sony ZV-E10",
        "desc": "Sony ZV-E10 là mẫu máy ảnh không gương lật cảm biến APS-C 24.2 MP được thiết kế tối ưu cho vlogger và người sáng tạo nội dung số. Máy sở hữu hệ thống lấy nét ánh mắt thời gian thực (Real-time Eye AF) siêu nhạy, tính năng ưu tiên lấy nét sản phẩm (Product Showcase) độc quyền và micro định hướng 3-capsule tích hợp thu âm rõ ràng. Thân máy siêu gọn nhẹ kết hợp màn hình xoay lật cảm ứng linh hoạt rất thuận tiện cho việc tự quay vlog, livestream và du lịch.",
        "brand": "Sony",
        "type": "Mirrorless",
        "sensor": "Crop (APS-C) (24.2 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p, Full HD 120p)",
        "purpose": "Quay Vlog, Sáng tạo nội dung",
        "price_range": "10 - 20 triệu đồng (Giá tham khảo: ~ 15.500.000 VNĐ)",
        "price_num": 15500000,
        "price_text": "15.500.000đ",
        "rules": [
            25,
            26
        ],
        "facts": [
            "C2",
            "G2",
            "L2",
            "M1",
            "N1",
            "N4",
            "T2",
            "V1"
        ],
        "mp": "24.2MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "Cảm ứng",
        "discount": 16,
        "old_price_text": "18.450.000đ",
        "smember_text": "155.000đ",
        "promo": "Tặng đèn LED mini Godox LITEMONS LED6R và thẻ nhớ SD 64GB tốc độ cao",
        "rating": "5.0",
        "reviews": 88
    },
    {
        "id": "K12",
        "order": 12,
        "name": "Máy ảnh Sony Alpha A6400",
        "desc": "Sony Alpha A6400 là dòng máy ảnh không gương lật tầm trung nổi tiếng với tốc độ bắt nét cực nhanh chỉ 0.02 giây cùng 425 điểm lấy nét theo pha. Máy trang bị cảm biến APS-C 24.2 MP, bộ xử lý BIONZ X mạnh mẽ và màn hình LCD cảm ứng lật lên 180 độ tiện lợi. Với thiết kế thân vỏ hợp kim magie cứng cáp, chống bụi ẩm tốt, thiết bị đáp ứng hoàn hảo cho cả nhu cầu chụp ảnh đường phố, du lịch lẫn quay vlog hàng ngày.",
        "brand": "Sony",
        "type": "Mirrorless",
        "sensor": "Crop (APS-C) (24.2 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p HLG/S-Log3, Full HD 120p)",
        "purpose": "Quay Vlog, Sáng tạo nội dung",
        "price_range": "10 - 20 triệu đồng (Giá tham khảo: ~ 18.500.000 VNĐ)",
        "price_num": 18500000,
        "price_text": "18.500.000đ",
        "rules": [
            27,
            28
        ],
        "facts": [
            "C2",
            "G2",
            "L2",
            "M1",
            "N1",
            "N4",
            "T2",
            "V1"
        ],
        "mp": "24.2MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "Cảm ứng",
        "discount": 15,
        "old_price_text": "21.760.000đ",
        "smember_text": "185.000đ",
        "promo": "Giảm ngay 1.500.000đ khi mua kèm ống kính chính hãng & tặng túi máy ảnh",
        "rating": "4.8",
        "reviews": 95
    },
    {
        "id": "K13",
        "order": 13,
        "name": "Máy ảnh Sony Alpha A6700",
        "desc": "Sony Alpha A6700 là mẫu máy ảnh đầu bảng thuộc dòng cảm biến Crop của Sony, sở hữu cảm biến BSI CMOS 26 MP kết hợp chip xử lý AI chuyên dụng nhận diện chủ thể thông minh. Máy được tích hợp chống rung 5 trục trong thân máy (IBIS), giao diện cảm ứng hiện đại và khả năng quay video 4K 120p 10-bit 4:2:2 chuyên nghiệp thừa hưởng từ dòng Cinema Line. Đây là thiết bị đa năng vượt trội cho người dùng vừa chụp ảnh tốc độ cao vừa làm phim bán chuyên.",
        "brand": "Sony",
        "type": "Mirrorless",
        "sensor": "Crop (APS-C) (26.0 MP)",
        "touch": "Có",
        "video": "Quay nâng cao (4K 120p 10-bit, S-Cinetone)",
        "purpose": "Đa dụng",
        "price_range": "30 - 40 triệu đồng (Giá tham khảo: ~ 34.000.000 VNĐ)",
        "price_num": 34000000,
        "price_text": "34.000.000đ",
        "rules": [
            29,
            30,
            31
        ],
        "facts": [
            "C2",
            "G4",
            "L2",
            "M1",
            "N3",
            "N4",
            "N5",
            "T2",
            "V2"
        ],
        "mp": "26MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "Cảm ứng",
        "discount": 18,
        "old_price_text": "41.460.000đ",
        "smember_text": "340.000đ",
        "promo": "Tặng pin dự phòng chính hãng, bộ vệ sinh cảm biến 5 món và balo chống sốc",
        "rating": "4.9",
        "reviews": 102
    },
    {
        "id": "K14",
        "order": 14,
        "name": "Máy ảnh Sony Alpha A7 II",
        "desc": "Sony Alpha A7 II là mẫu máy ảnh không gương lật Full-frame thế hệ thứ hai của Sony, trang bị cảm biến Exmor CMOS 24.3 MP cùng hệ thống chống rung 5 trục tích hợp trực tiếp trên thân máy. Máy sở hữu thiết kế báng cầm chắc chắn, hệ thống lấy nét lai Fast Hybrid AF ổn định và khả năng tái tạo chi tiết ảnh sắc nét, dải tương phản động rộng. Đây là lựa chọn kinh tế bậc nhất cho người dùng muốn bước chân vào thế giới Full-frame để chụp chân dung và phong cảnh.",
        "brand": "Sony",
        "type": "Mirrorless",
        "sensor": "Full-frame (24.3 MP)",
        "touch": "Không",
        "video": "Quay cơ bản (Full HD 60p)",
        "purpose": "Chân dung, Phong cảnh",
        "price_range": "10 - 20 triệu đồng (Giá tham khảo: ~ 14.000.000 VNĐ)",
        "price_num": 14000000,
        "price_text": "14.000.000đ",
        "rules": [
            32,
            33
        ],
        "facts": [
            "C1",
            "G2",
            "L2",
            "M2",
            "N1",
            "N2",
            "T2",
            "V1"
        ],
        "mp": "24.3MP",
        "video_short": "FHD 60p",
        "sensor_short": "Full-frame",
        "fps": "EVF/OVF",
        "discount": 14,
        "old_price_text": "16.280.000đ",
        "smember_text": "140.000đ",
        "promo": "Trả góp 0% lãi suất qua thẻ tín dụng, tặng kèm thẻ nhớ SanDisk Extreme Pro 64GB",
        "rating": "4.8",
        "reviews": 24
    },
    {
        "id": "K15",
        "order": 15,
        "name": "Máy ảnh Sony Alpha A7 III",
        "desc": "Sony Alpha A7 III là mẫu máy ảnh không gương lật Full-frame \"quốc dân\" được giới làm nghề dịch vụ đặc biệt ưa chuộng nhờ sự cân bằng hoàn hảo. Máy sở hữu cảm biến BSI CMOS 24.2 MP chụp thiếu sáng xuất sắc, hệ thống 693 điểm lấy nét phủ kín khung hình, chống rung 5 trục, 2 khe thẻ nhớ và viên pin NP-FZ100 dung lượng lớn. Thiết bị đáp ứng bền bỉ và toàn diện mọi nhu cầu từ chụp ảnh sự kiện, phóng sự cưới cho đến quay video thương mại.",
        "brand": "Sony",
        "type": "Mirrorless",
        "sensor": "Full-frame (24.2 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p HDR, S-Log3)",
        "purpose": "Đa dụng",
        "price_range": "20 - 30 triệu đồng (Giá tham khảo: ~ 29.500.000 VNĐ)",
        "price_num": 29500000,
        "price_text": "29.500.000đ",
        "rules": [
            34,
            35,
            36
        ],
        "facts": [
            "C1",
            "G3",
            "L2",
            "M1",
            "N2",
            "N3",
            "N6",
            "T2",
            "V1"
        ],
        "mp": "24.2MP",
        "video_short": "4K UHD",
        "sensor_short": "Full-frame",
        "fps": "Cảm ứng",
        "discount": 16,
        "old_price_text": "35.120.000đ",
        "smember_text": "295.000đ",
        "promo": "Tặng micro thu âm cài áo không dây và chân máy tripod du lịch cao cấp",
        "rating": "5.0",
        "reviews": 31
    },
    {
        "id": "K16",
        "order": 16,
        "name": "Máy ảnh Sony Alpha A7C II",
        "desc": "Sony Alpha A7C II là dòng máy ảnh Full-frame mang kiểu dáng nhỏ gọn như dòng máy Crop nhưng chứa đựng sức mạnh phần cứng vượt trội với cảm biến 33 MP và chip xử lý AI. Máy được nâng cấp mạnh mẽ khả năng lấy nét nhận diện chủ thể thông minh, chống rung thân máy lên đến 7 stops và màn hình xoay lật cảm ứng đa góc. Đây là sự lựa chọn hoàn hảo cho những nhà sáng tạo nội dung cao cấp, vlogger du lịch và người yêu thích nhiếp ảnh đường phố cần sự cơ động tối đa.",
        "brand": "Sony",
        "type": "Mirrorless",
        "sensor": "Full-frame (33.0 MP)",
        "touch": "Có",
        "video": "Quay nâng cao (4K 60p 10-bit 4:2:2, S-Cinetone)",
        "purpose": "Quay Vlog, Sáng tạo nội dung",
        "price_range": "40 - 50 triệu đồng (Giá tham khảo: ~ 47.500.000 VNĐ)",
        "price_num": 47500000,
        "price_text": "47.500.000đ",
        "rules": [
            37,
            38,
            39
        ],
        "facts": [
            "C1",
            "G5",
            "L2",
            "M1",
            "N1",
            "N3",
            "N4",
            "T2",
            "V2"
        ],
        "mp": "33MP",
        "video_short": "4K UHD",
        "sensor_short": "Full-frame",
        "fps": "Cảm ứng",
        "discount": 12,
        "old_price_text": "53.980.000đ",
        "smember_text": "475.000đ",
        "promo": "Tặng đèn LED mini Godox LITEMONS LED6R và thẻ nhớ SD 64GB tốc độ cao",
        "rating": "4.9",
        "reviews": 38
    },
    {
        "id": "K17",
        "order": 17,
        "name": "Máy ảnh Sony Alpha A7 IV",
        "desc": "Sony Alpha A7 IV là chuẩn mực máy ảnh Hybrid (kết hợp Chụp và Quay) thế hệ mới, trang bị cảm biến Full-frame Exmor R 33 MP cùng bộ xử lý BIONZ XR mạnh mẽ. Máy mang lại chất lượng ảnh tĩnh độ chi tiết cao, lấy nét tự động theo thời gian thực chuẩn xác cùng màn hình cảm ứng xoay lật linh hoạt. Với khả năng quay video 4K 60p 10-bit tích hợp màu S-Cinetone điện ảnh, đây là thiết bị chủ lực dành cho các nhiếp ảnh gia dịch vụ và nhà làm phim chuyên nghiệp.",
        "brand": "Sony",
        "type": "Mirrorless",
        "sensor": "Full-frame (33.0 MP)",
        "touch": "Có",
        "video": "Quay nâng cao (4K 60p 10-bit 4:2:2, S-Cinetone)",
        "purpose": "Đa dụng",
        "price_range": "50 - 60 triệu đồng (Giá tham khảo: ~ 53.500.000 VNĐ)",
        "price_num": 53500000,
        "price_text": "53.500.000đ",
        "rules": [
            40,
            41,
            42
        ],
        "facts": [
            "C1",
            "G6",
            "L2",
            "M1",
            "N2",
            "N3",
            "N6",
            "T2",
            "V2"
        ],
        "mp": "33MP",
        "video_short": "4K UHD",
        "sensor_short": "Full-frame",
        "fps": "Cảm ứng",
        "discount": 16,
        "old_price_text": "63.690.000đ",
        "smember_text": "535.000đ",
        "promo": "Giảm ngay 1.500.000đ khi mua kèm ống kính chính hãng & tặng túi máy ảnh",
        "rating": "5.0",
        "reviews": 45
    },
    {
        "id": "K18",
        "order": 18,
        "name": "Máy ảnh Sony Alpha A7R V",
        "desc": "Sony Alpha A7R V là dòng máy ảnh chuyên chụp độ phân giải siêu cao của Sony, sở hữu cảm biến Full-frame BSI CMOS 61 MP cùng bộ vi xử lý AI chuyên biệt đầu tiên giúp nhận diện chính xác dáng người và chủ thể phức tạp. Máy được trang bị hệ thống chống rung 5 trục lên tới 8 stops, màn hình LCD cảm ứng đa góc 4 trục độc đáo và kính ngắm điện tử 9.44 triệu điểm ảnh. Thiết bị sinh ra để phục vụ công việc chụp ảnh Studio thương mại, thời trang, kiến trúc và quảng cáo.",
        "brand": "Sony",
        "type": "Mirrorless",
        "sensor": "Full-frame (61.0 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (8K 24p, 4K 60p 10-bit)",
        "purpose": "Chụp Studio, Thương mại",
        "price_range": "Trên 80 triệu đồng (Giá tham khảo: ~ 83.000.000 VNĐ)",
        "price_num": 83000000,
        "price_text": "83.000.000đ",
        "rules": [
            43,
            44,
            45
        ],
        "facts": [
            "C1",
            "G9",
            "L2",
            "M1",
            "N2",
            "N7",
            "T2",
            "V2",
            "V3"
        ],
        "mp": "61MP",
        "video_short": "8K RAW",
        "sensor_short": "Full-frame",
        "fps": "Cảm ứng",
        "discount": 15,
        "old_price_text": "97.650.000đ",
        "smember_text": "830.000đ",
        "promo": "Tặng pin dự phòng chính hãng, bộ vệ sinh cảm biến 5 món và balo chống sốc",
        "rating": "4.8",
        "reviews": 52
    },
    {
        "id": "K19",
        "order": 19,
        "name": "Máy ảnh Sony Alpha A7S III",
        "desc": "Sony Alpha A7S III là dòng máy ảnh Full-frame chuyên trị quay phim và chụp siêu thiếu sáng với cảm biến BSI CMOS 12.1 MP được tối ưu hóa kích thước điểm ảnh lớn. Máy sở hữu dải nhạy sáng ISO mở rộng lên đến 409.600, dải tương phản động hơn 15 stops và hoàn toàn không bị giới hạn thời gian ghi hình nhờ cấu trúc tản nhiệt thông minh. Đây là công cụ làm việc lý tưởng cho các ekip sản xuất video, quay MV ca nhạc, TVC và phim tài liệu chuyên nghiệp.",
        "brand": "Sony",
        "type": "Mirrorless",
        "sensor": "Full-frame (12.1 MP)",
        "touch": "Có",
        "video": "Quay nâng cao (4K 120p 10-bit 4:2:2 All-I, xuất 16-bit RAW)",
        "purpose": "Chuyên sản xuất Video, Điện ảnh",
        "price_range": "70 - 80 triệu đồng (Giá tham khảo: ~ 76.500.000 VNĐ)",
        "price_num": 76500000,
        "price_text": "76.500.000đ",
        "rules": [
            46,
            47
        ],
        "facts": [
            "C1",
            "G8",
            "L2",
            "M1",
            "N3",
            "N6",
            "T2",
            "V2"
        ],
        "mp": "12.1MP",
        "video_short": "4K UHD",
        "sensor_short": "Full-frame",
        "fps": "Cảm ứng",
        "discount": 17,
        "old_price_text": "92.170.000đ",
        "smember_text": "765.000đ",
        "promo": "Trả góp 0% lãi suất qua thẻ tín dụng, tặng kèm thẻ nhớ SanDisk Extreme Pro 64GB",
        "rating": "4.9",
        "reviews": 59
    },
    {
        "id": "K20",
        "order": 20,
        "name": "Máy ảnh Sony Alpha A1",
        "desc": "Sony Alpha A1 là mẫu máy ảnh Flagship đầu bảng hội tụ mọi công nghệ đỉnh cao nhất của Sony, kết hợp hoàn hảo giữa độ phân giải siêu cao và tốc độ siêu thanh. Máy sở hữu cảm biến Full-frame Stacked BSI CMOS 50.1 MP, cho phép chụp liên tiếp không chớp đen 30 khung hình/giây cùng khả năng tính toán lấy nét 120 lần/giây. Bên cạnh khả năng quay video 8K 30p, thiết bị còn đáp ứng xuất sắc mọi tác vụ khắt khe nhất từ chụp thể thao, động vật hoang dã cho đến thương mại cao cấp.",
        "brand": "Sony",
        "type": "Mirrorless",
        "sensor": "Full-frame (50.1 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (8K 30p 10-bit, 4K 120p)",
        "purpose": "Thể thao, Tốc độ cao",
        "price_range": "Trên 80 triệu đồng (Giá tham khảo: ~ 142.000.000 VNĐ)",
        "price_num": 142000000,
        "price_text": "142.000.000đ",
        "rules": [
            48,
            49,
            50
        ],
        "facts": [
            "C1",
            "G9",
            "L2",
            "M1",
            "N5",
            "N6",
            "N7",
            "T2",
            "V3"
        ],
        "mp": "50.1MP",
        "video_short": "8K RAW",
        "sensor_short": "Full-frame",
        "fps": "30 FPS",
        "discount": 14,
        "old_price_text": "165.120.000đ",
        "smember_text": "1.420.000đ",
        "promo": "Tặng micro thu âm cài áo không dây và chân máy tripod du lịch cao cấp",
        "rating": "4.8",
        "reviews": 66
    },
    {
        "id": "K21",
        "order": 21,
        "name": "Máy ảnh Nikon D7500",
        "desc": "Nikon D7500 là dòng máy ảnh phản xạ ống kính đơn (DSLR) tầm trung nổi bật, trang bị cảm biến CMOS APS-C 20.9 MP và bộ xử lý hình ảnh EXPEED 5. Máy sở hữu hệ thống lấy nét tự động 51 điểm Multi-CAM 3500FX II tin cậy, tốc độ chụp liên tục 8 khung hình/giây cùng khả năng quay video 4K UHD. Thiết kế thân máy bằng hợp kim carbon bền bỉ, chống chịu thời tiết tốt, đây là lựa chọn hoàn hảo cho nhu cầu chụp thể thao và đa dụng.",
        "brand": "Nikon",
        "type": "DSLR",
        "sensor": "Crop APS-C (20.9 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p, Full HD 60p)",
        "purpose": "Thể thao, Tốc độ cao",
        "price_range": "10 - 20 triệu đồng (Giá tham khảo: 18.500.000 VNĐ)",
        "price_num": 18500000,
        "price_text": "18.500.000đ",
        "rules": [
            51,
            52
        ],
        "facts": [
            "C2",
            "G2",
            "L1",
            "M1",
            "N3",
            "N5",
            "T3",
            "V1"
        ],
        "mp": "20.9MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "8 FPS",
        "discount": 16,
        "old_price_text": "22.020.000đ",
        "smember_text": "185.000đ",
        "promo": "Tặng đèn LED mini Godox LITEMONS LED6R và thẻ nhớ SD 64GB tốc độ cao",
        "rating": "5.0",
        "reviews": 73
    },
    {
        "id": "K22",
        "order": 22,
        "name": "Máy ảnh Nikon D850",
        "desc": "Nikon D850 được coi là đỉnh cao của dòng máy ảnh DSLR Full-frame chuyên nghiệp. Máy trang bị cảm biến BSI CMOS độ phân giải siêu cao 45.7 MP, bộ xử lý EXPEED 5 cùng hệ thống lấy nét 153 điểm đỉnh cao. Kính ngắm quang học rộng lớn, khả năng chống chịu thời tiết khắc nghiệt và thời lượng pin cực kỳ bền bỉ giúp D850 trở thành biểu tượng cho nhu cầu chụp phong cảnh, studio và sản phẩm độ chi tiết cao.",
        "brand": "Nikon",
        "type": "DSLR",
        "sensor": "Full-frame (45.7 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p không crop)",
        "purpose": "Chụp Studio, Thương mại",
        "price_range": "40 - 50 triệu đồng (Giá tham khảo: 49.000.000 VNĐ)",
        "price_num": 49000000,
        "price_text": "49.000.000đ",
        "rules": [
            53,
            54
        ],
        "facts": [
            "C1",
            "G5",
            "L1",
            "M1",
            "N2",
            "N7",
            "T3",
            "V1"
        ],
        "mp": "45.7MP",
        "video_short": "4K UHD",
        "sensor_short": "Full-frame",
        "fps": "Cảm ứng",
        "discount": 15,
        "old_price_text": "57.650.000đ",
        "smember_text": "490.000đ",
        "promo": "Giảm ngay 1.500.000đ khi mua kèm ống kính chính hãng & tặng túi máy ảnh",
        "rating": "4.9",
        "reviews": 80
    },
    {
        "id": "K23",
        "order": 23,
        "name": "Máy ảnh Nikon Z30",
        "desc": "Nikon Z30 là dòng máy ảnh không gương lật nhỏ gọn nhất trong hệ sinh thái Z-series của Nikon, thiết kế tối ưu hóa cho người làm sáng tạo nội dung. Trang bị cảm biến Crop APS-C 20.9 MP, máy hỗ trợ quay 4K 30p không crop, micro kép tích hợp lọc gió và đèn báo hiệu ghi hình (Tally Light). Màn hình xoay lật góc rộng giúp việc tự ghi hình Vlog trở nên vô cùng linh hoạt và đơn giản.",
        "brand": "Nikon",
        "type": "Mirrorless",
        "sensor": "Crop APS-C (20.9 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p không crop)",
        "purpose": "Quay Vlog, Sáng tạo nội dung",
        "price_range": "10 - 20 triệu đồng (Giá tham khảo: 14.900.000 VNĐ)",
        "price_num": 14900000,
        "price_text": "14.900.000đ",
        "rules": [
            55,
            56
        ],
        "facts": [
            "C2",
            "G2",
            "L2",
            "M1",
            "N1",
            "N4",
            "T3",
            "V1"
        ],
        "mp": "20.9MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "Cảm ứng",
        "discount": 18,
        "old_price_text": "18.170.000đ",
        "smember_text": "149.000đ",
        "promo": "Tặng pin dự phòng chính hãng, bộ vệ sinh cảm biến 5 món và balo chống sốc",
        "rating": "5.0",
        "reviews": 87
    },
    {
        "id": "K24",
        "order": 24,
        "name": "Máy ảnh Nikon Z50",
        "desc": "Nikon Z50 là mẫu máy ảnh Mirrorless ngàm Z phân khúc APS-C đầu tiên của Nikon. Sở hữu cảm biến CMOS 20.9 MP, bộ xử lý EXPEED 6 cùng báng cầm sâu đầm tay đặc trưng, máy cho trải nghiệm cầm nắm cực kỳ thoải mái. Khả năng chụp liên tiếp 11 khung hình/giây, lấy nét tự động vào mắt người/động vật và màn hình lật xuống 180 độ đáp ứng hoàn hảo nhu cầu chụp ảnh du lịch và gia đình.",
        "brand": "Nikon",
        "type": "Mirrorless",
        "sensor": "Crop APS-C (20.9 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p, Full HD 120p)",
        "purpose": "Cơ bản, Du lịch, Đường phố",
        "price_range": "10 - 20 triệu đồng (Giá tham khảo: 18.000.000 VNĐ)",
        "price_num": 18000000,
        "price_text": "18.000.000đ",
        "rules": [
            57,
            58
        ],
        "facts": [
            "C2",
            "G2",
            "L2",
            "M1",
            "N1",
            "N4",
            "T3",
            "V1"
        ],
        "mp": "20.9MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "11 FPS",
        "discount": 14,
        "old_price_text": "20.930.000đ",
        "smember_text": "180.000đ",
        "promo": "Trả góp 0% lãi suất qua thẻ tín dụng, tặng kèm thẻ nhớ SanDisk Extreme Pro 64GB",
        "rating": "4.8",
        "reviews": 94
    },
    {
        "id": "K25",
        "order": 25,
        "name": "Máy ảnh Nikon Z fc",
        "desc": "Nikon Z fc gây ấn tượng mạnh mẽ với thiết kế hoài cổ Classic lấy cảm hứng từ chiếc máy phim huyền thoại Nikon FM2. Bên trong ngoại hình vintage là sức mạnh hiện đại với cảm biến Crop APS-C 20.9 MP, hệ thống vòng xoay cơ học điều chỉnh ISO, tốc độ màn trập và bù trừ sáng trực quan. Máy tích hợp màn hình xoay lật đa góc và khả năng bắt nét Eye-AF nhanh chóng, hoàn hảo cho phong cách chụp Streetlife.",
        "brand": "Nikon",
        "type": "Mirrorless",
        "sensor": "Crop APS-C (20.9 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p)",
        "purpose": "Cơ bản, Du lịch, Đường phố",
        "price_range": "20 - 30 triệu đồng (Giá tham khảo: 21.500.000 VNĐ)",
        "price_num": 21500000,
        "price_text": "21.500.000đ",
        "rules": [
            59,
            60
        ],
        "facts": [
            "C2",
            "G3",
            "L2",
            "M1",
            "N1",
            "N4",
            "T3",
            "V1"
        ],
        "mp": "20.9MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "Cảm ứng",
        "discount": 16,
        "old_price_text": "25.600.000đ",
        "smember_text": "215.000đ",
        "promo": "Tặng micro thu âm cài áo không dây và chân máy tripod du lịch cao cấp",
        "rating": "4.9",
        "reviews": 101
    },
    {
        "id": "K26",
        "order": 26,
        "name": "Máy ảnh Nikon Z5",
        "desc": "Nikon Z5 là dòng máy ảnh Mirrorless Full-frame nhập môn kinh tế nhất của Nikon. Máy trang bị cảm biến Full-frame CMOS 24.3 MP, hệ thống chống rung 5 trục ngay trên thân máy (IBIS) lên tới 5 stops và 273 điểm lấy nét tự động. Điểm cộng lớn của Z5 là sở hữu 2 khe cắm thẻ nhớ SD chuẩn UHS-II và thân máy hợp kim magie chống bụi bẩn, thích hợp cho người mới bước chân vào con đường chụp ảnh Full-frame.",
        "brand": "Nikon",
        "type": "Mirrorless",
        "sensor": "Full-frame (24.3 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p crop 1.7x)",
        "purpose": "Chân dung, Phong cảnh",
        "price_range": "20 - 30 triệu đồng (Giá tham khảo: 23.000.000 VNĐ)",
        "price_num": 23000000,
        "price_text": "23.000.000đ",
        "rules": [
            61,
            62
        ],
        "facts": [
            "C1",
            "G3",
            "L2",
            "M1",
            "N2",
            "N3",
            "T3",
            "V1"
        ],
        "mp": "24.3MP",
        "video_short": "4K UHD",
        "sensor_short": "Full-frame",
        "fps": "Cảm ứng",
        "discount": 12,
        "old_price_text": "26.140.000đ",
        "smember_text": "230.000đ",
        "promo": "Tặng đèn LED mini Godox LITEMONS LED6R và thẻ nhớ SD 64GB tốc độ cao",
        "rating": "4.8",
        "reviews": 23
    },
    {
        "id": "K27",
        "order": 27,
        "name": "Máy ảnh Nikon Z6 II",
        "desc": "Nikon Z6 II là bản nâng cấp đa năng toàn diện, trang bị cảm biến Full-frame BSI CMOS 24.5 MP cùng bộ đôi vi xử lý kép Dual EXPEED 6. Máy cải thiện đáng kể tốc độ lấy nét trong điều kiện thiếu sáng, khả năng chụp liên tiếp lên đến 14 fps và hỗ trợ 2 khe thẻ nhớ (CFexpress/XQD + SD). Khả năng quay video 4K 60p mượt mà giúp Z6 II đáp ứng tốt nhu cầu làm dịch vụ sự kiện và quay chụp hỗn hợp.",
        "brand": "Nikon",
        "type": "Mirrorless",
        "sensor": "Full-frame (24.5 MP)",
        "touch": "Có",
        "video": "Quay nâng cao (4K 60p, N-Log 10-bit qua HDMI)",
        "purpose": "Đa dụng, Sự kiện",
        "price_range": "30 - 40 triệu đồng (Giá tham khảo: 38.000.000 VNĐ)",
        "price_num": 38000000,
        "price_text": "38.000.000đ",
        "rules": [
            63,
            64,
            65
        ],
        "facts": [
            "C1",
            "G4",
            "L2",
            "M1",
            "N2",
            "N3",
            "T3",
            "V1",
            "V2"
        ],
        "mp": "24.5MP",
        "video_short": "4K UHD",
        "sensor_short": "Full-frame",
        "fps": "14 FPS",
        "discount": 16,
        "old_price_text": "45.240.000đ",
        "smember_text": "380.000đ",
        "promo": "Giảm ngay 1.500.000đ khi mua kèm ống kính chính hãng & tặng túi máy ảnh",
        "rating": "5.0",
        "reviews": 30
    },
    {
        "id": "K28",
        "order": 28,
        "name": "Máy ảnh Nikon Z7 II",
        "desc": "Nikon Z7 II là dòng máy ảnh Mirrorless Full-frame độ phân giải cao phục vụ cho nhiếp ảnh gia chuyên nghiệp. Sở hữu cảm biến BSI CMOS 45.7 MP không có bộ lọc thông thấp (OLPF) cùng bộ xử lý kép Dual EXPEED 6, máy cho ra những bức ảnh với độ chi tiết xuất sắc và dải nhạy sáng (Dynamic Range) cực rộng. Hệ thống chống rung 5 trục IBIS giúp tối ưu hóa độ sắc nét khi chụp phong cảnh và thương mại.",
        "brand": "Nikon",
        "type": "Mirrorless",
        "sensor": "Full-frame (45.7 MP)",
        "touch": "Có",
        "video": "Quay nâng cao (4K 60p)",
        "purpose": "Chụp Studio, Thương mại",
        "price_range": "50 - 60 triệu đồng (Giá tham khảo: 56.000.000 VNĐ)",
        "price_num": 56000000,
        "price_text": "56.000.000đ",
        "rules": [
            66,
            67
        ],
        "facts": [
            "C1",
            "G6",
            "L2",
            "M1",
            "N2",
            "N7",
            "T3",
            "V2"
        ],
        "mp": "45.7MP",
        "video_short": "4K UHD",
        "sensor_short": "Full-frame",
        "fps": "Cảm ứng",
        "discount": 15,
        "old_price_text": "65.880.000đ",
        "smember_text": "560.000đ",
        "promo": "Tặng pin dự phòng chính hãng, bộ vệ sinh cảm biến 5 món và balo chống sốc",
        "rating": "4.9",
        "reviews": 37
    },
    {
        "id": "K29",
        "order": 29,
        "name": "Máy ảnh Nikon Z8",
        "desc": "Nikon Z8 được mệnh danh là \"Baby Z9\", sở hữu trọn vẹn sức mạnh của dòng Flagship trong một thân máy nhỏ gọn hơn 30%. Trang bị cảm biến Full-frame xếp chồng (Stacked BSI) 45.7 MP và chip EXPEED 7, máy loại bỏ hoàn toàn màn trập cơ học. Z8 hỗ trợ quay phim nội bộ 8.3K 60p N-RAW 12-bit, chụp liên tiếp 20 fps RAW và hệ thống bắt nét AI siêu việt, đáp ứng đỉnh cao nhu cầu quay phim và thể thao chuyên nghiệp.",
        "brand": "Nikon",
        "type": "Mirrorless",
        "sensor": "Full-frame (45.7 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (8.3K 60p N-RAW, 4K 120p)",
        "purpose": "Chuyên sản xuất Video, Điện ảnh",
        "price_range": "Trên 80 triệu đồng (Giá tham khảo: 92.000.000 VNĐ)",
        "price_num": 92000000,
        "price_text": "92.000.000đ",
        "rules": [
            68,
            69,
            70
        ],
        "facts": [
            "C1",
            "G9",
            "L2",
            "M1",
            "N5",
            "N6",
            "N7",
            "T3",
            "V3"
        ],
        "mp": "45.7MP",
        "video_short": "8K RAW",
        "sensor_short": "Full-frame",
        "fps": "20 FPS",
        "discount": 17,
        "old_price_text": "110.840.000đ",
        "smember_text": "920.000đ",
        "promo": "Trả góp 0% lãi suất qua thẻ tín dụng, tặng kèm thẻ nhớ SanDisk Extreme Pro 64GB",
        "rating": "5.0",
        "reviews": 44
    },
    {
        "id": "K30",
        "order": 30,
        "name": "Máy ảnh Nikon Z9",
        "desc": "Nikon Z9 là mẫu máy ảnh Mirrorless Flagship đỉnh cao nhất của Nikon dành cho các nhiếp ảnh gia thể thao, động vật hoang dã và phóng sự chiến trường. Máy trang bị cảm biến Stacked CMOS 45.7 MP, bộ xử lý EXPEED 7 và thiết kế báng cầm dọc tích hợp pin lớn. Khả năng chụp liên tiếp 20 hình/giây RAW, 120 hình/giây JPEG, chống chịu thời tiết siêu việt cùng khả năng quay 8K RAW liên tục không bị quá nhiệt biến Z9 thành cỗ máy chụp ảnh mạnh mẽ nhất.",
        "brand": "Nikon",
        "type": "Mirrorless",
        "sensor": "Full-frame (45.7 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (8.3K 60p RAW, 4K 120p)",
        "purpose": "Thể thao, Tốc độ cao",
        "price_range": "Trên 80 triệu đồng (Giá tham khảo: 122.000.000 VNĐ)",
        "price_num": 122000000,
        "price_text": "122.000.000đ",
        "rules": [
            71,
            72
        ],
        "facts": [
            "C1",
            "G9",
            "L2",
            "M1",
            "N5",
            "N6",
            "T3",
            "V3"
        ],
        "mp": "45.7MP",
        "video_short": "8K RAW",
        "sensor_short": "Full-frame",
        "fps": "20 FPS",
        "discount": 14,
        "old_price_text": "141.860.000đ",
        "smember_text": "1.220.000đ",
        "promo": "Tặng micro thu âm cài áo không dây và chân máy tripod du lịch cao cấp",
        "rating": "4.8",
        "reviews": 51
    },
    {
        "id": "K31",
        "order": 31,
        "name": "Máy ảnh Fujifilm X-T30 II",
        "desc": "Fujifilm X-T30 II là dòng máy ảnh tầm trung với ngoại hình vintage cực kỳ bắt mắt và nhỏ gọn. Máy thừa hưởng hệ thống lấy nét và cảm biến X-Trans IV 26.1 MP từ dòng X-T4 cao cấp, đi kèm 18 bộ màu phim giúp người mới chơi dễ dàng có được bức ảnh đẹp ngay khi chụp.",
        "brand": "Fujifilm",
        "type": "Mirrorless",
        "sensor": "Crop / APS-C (26.1 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p, Full HD 240p)",
        "purpose": "Cơ bản, Du lịch, Đường phố",
        "price_range": "20 - 30 triệu đồng (Giá tham khảo: 21.000.000 VNĐ)",
        "price_num": 21000000,
        "price_text": "21.000.000đ",
        "rules": [
            73,
            74
        ],
        "facts": [
            "C2",
            "G3",
            "L2",
            "M1",
            "N1",
            "N2",
            "T4",
            "V1"
        ],
        "mp": "26.1MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "Cảm ứng",
        "discount": 16,
        "old_price_text": "25.000.000đ",
        "smember_text": "210.000đ",
        "promo": "Tặng đèn LED mini Godox LITEMONS LED6R và thẻ nhớ SD 64GB tốc độ cao",
        "rating": "4.9",
        "reviews": 58
    },
    {
        "id": "K32",
        "order": 32,
        "name": "Máy ảnh Fujifilm X-E4",
        "desc": "Fujifilm X-E4 sở hữu thiết kế phẳng tối giản theo phong cách Rangefinder, vô cùng nhỏ gọn có thể bỏ túi. Dù nhỏ bé nhưng máy vẫn mang cấu hình mạnh mẽ với cảm biến 26.1 MP và bộ xử lý X-Processor 4, phù hợp cho những ai yêu thích phong cách chụp ảnh đường phố kín đáo.",
        "brand": "Fujifilm",
        "type": "Mirrorless",
        "sensor": "Crop / APS-C (26.1 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p)",
        "purpose": "Cơ bản, Du lịch, Đường phố",
        "price_range": "20 - 30 triệu đồng (Giá tham khảo: 22.000.000 VNĐ)",
        "price_num": 22000000,
        "price_text": "22.000.000đ",
        "rules": [
            75
        ],
        "facts": [
            "C2",
            "G3",
            "L2",
            "M1",
            "N1",
            "T4",
            "V1"
        ],
        "mp": "26.1MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "Cảm ứng",
        "discount": 15,
        "old_price_text": "25.880.000đ",
        "smember_text": "220.000đ",
        "promo": "Giảm ngay 1.500.000đ khi mua kèm ống kính chính hãng & tặng túi máy ảnh",
        "rating": "4.8",
        "reviews": 65
    },
    {
        "id": "K33",
        "order": 33,
        "name": "Máy ảnh Fujifilm X-S10",
        "desc": "Fujifilm X-S10 thay đổi phong cách thiết kế truyền thống bằng báng cầm lớn, kiểu dáng hiện đại dễ tiếp cận. Máy được trang bị hệ thống chống rung thân máy (IBIS) 6 stops gọn nhẹ, cảm biến 26.1 MP và màn hình xoay lật linh hoạt cho cả chụp lẫn quay.",
        "brand": "Fujifilm",
        "type": "Mirrorless",
        "sensor": "Crop / APS-C (26.1 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p, Full HD 240p)",
        "purpose": "Đa dụng, Sự kiện",
        "price_range": "20 - 30 triệu đồng (Giá tham khảo: 23.500.000 VNĐ)",
        "price_num": 23500000,
        "price_text": "23.500.000đ",
        "rules": [
            76,
            77
        ],
        "facts": [
            "C2",
            "G3",
            "L2",
            "M1",
            "N3",
            "N4",
            "T4",
            "V1"
        ],
        "mp": "26.1MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "Cảm ứng",
        "discount": 18,
        "old_price_text": "28.660.000đ",
        "smember_text": "235.000đ",
        "promo": "Tặng pin dự phòng chính hãng, bộ vệ sinh cảm biến 5 món và balo chống sốc",
        "rating": "5.0",
        "reviews": 72
    },
    {
        "id": "K34",
        "order": 34,
        "name": "Máy ảnh Fujifilm X-S20",
        "desc": "Fujifilm X-S20 là mẫu máy ảnh đa năng nhỏ gọn hướng tới người sáng tạo nội dung và Vlogger. Máy sử dụng báng cầm sâu đầm tay, viên pin dung lượng lớn W235, chống rung IBIS 7 stops cùng chế độ quay Vlog / Product Priority chuyên dụng rất dễ thao tác.",
        "brand": "Fujifilm",
        "type": "Mirrorless",
        "sensor": "Crop / APS-C (26.1 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (6.2K 30p, 4K 60p)",
        "purpose": "Quay Vlog, Sáng tạo nội dung",
        "price_range": "30 - 40 triệu đồng (Giá tham khảo: 30.500.000 VNĐ)",
        "price_num": 30500000,
        "price_text": "30.500.000đ",
        "rules": [
            78,
            79,
            80
        ],
        "facts": [
            "C2",
            "G4",
            "L2",
            "M1",
            "N3",
            "N4",
            "T4",
            "V2",
            "V3"
        ],
        "mp": "26.1MP",
        "video_short": "6K Pro",
        "sensor_short": "APS-C CMOS",
        "fps": "Cảm ứng",
        "discount": 14,
        "old_price_text": "35.470.000đ",
        "smember_text": "305.000đ",
        "promo": "Trả góp 0% lãi suất qua thẻ tín dụng, tặng kèm thẻ nhớ SanDisk Extreme Pro 64GB",
        "rating": "4.9",
        "reviews": 79
    },
    {
        "id": "K35",
        "order": 35,
        "name": "Máy ảnh Fujifilm X-T4",
        "desc": "Fujifilm X-T4 là flagship dòng Crop một thời của hãng, cân bằng hoàn hảo giữa chụp ảnh tĩnh và quay video. Máy sở hữu màn hình xoay lật đa góc, chống rung IBIS 6.5 stops, viên pin lớn và khả năng chụp liên tiếp cơ học tới 15 hình/giây.",
        "brand": "Fujifilm",
        "type": "Mirrorless",
        "sensor": "Crop / APS-C (26.1 MP)",
        "touch": "Có",
        "video": "Quay nâng cao (4K 60p 10-bit)",
        "purpose": "Đa dụng, Sự kiện",
        "price_range": "30 - 40 triệu đồng (Giá tham khảo: 33.000.000 VNĐ)",
        "price_num": 33000000,
        "price_text": "33.000.000đ",
        "rules": [
            81,
            82
        ],
        "facts": [
            "C2",
            "G4",
            "L2",
            "M1",
            "N3",
            "N6",
            "T4",
            "V2"
        ],
        "mp": "26.1MP",
        "video_short": "4K UHD",
        "sensor_short": "APS-C CMOS",
        "fps": "15 FPS",
        "discount": 16,
        "old_price_text": "39.290.000đ",
        "smember_text": "330.000đ",
        "promo": "Tặng micro thu âm cài áo không dây và chân máy tripod du lịch cao cấp",
        "rating": "5.0",
        "reviews": 86
    },
    {
        "id": "K36",
        "order": 36,
        "name": "Máy ảnh Fujifilm X-T5",
        "desc": "Fujifilm X-T5 mang thiết kế hoài cổ đặc trưng với các vòng xoay cơ học, trang bị cảm biến APS-C X-Trans CMOS 5 HR độ phân giải cao 40 MP. Máy tập trung tối đa vào trải nghiệm chụp ảnh với hệ thống lấy nét AI thông minh, chống rung IBIS 7 stops và 19 bộ lọc giả lập màu phim độc quyền.",
        "brand": "Fujifilm",
        "type": "Mirrorless",
        "sensor": "Crop / APS-C (40 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (6.2K 30p, 4K 60p)",
        "purpose": "Chân dung, Phong cảnh",
        "price_range": "40 - 50 triệu đồng (Giá tham khảo: 41.500.000 VNĐ)",
        "price_num": 41500000,
        "price_text": "41.500.000đ",
        "rules": [
            83,
            84,
            85
        ],
        "facts": [
            "C2",
            "G5",
            "L2",
            "M1",
            "N1",
            "N2",
            "N3",
            "T4",
            "V3"
        ],
        "mp": "40MP",
        "video_short": "6K Pro",
        "sensor_short": "APS-C CMOS",
        "fps": "Cảm ứng",
        "discount": 12,
        "old_price_text": "47.160.000đ",
        "smember_text": "415.000đ",
        "promo": "Tặng đèn LED mini Godox LITEMONS LED6R và thẻ nhớ SD 64GB tốc độ cao",
        "rating": "4.8",
        "reviews": 93
    },
    {
        "id": "K37",
        "order": 37,
        "name": "Máy ảnh Fujifilm X-H2",
        "desc": "Fujifilm X-H2 sở hữu cảm biến APS-C độ phân giải cao kỷ lục 40 MP, hỗ trợ tính năng Pixel Shift Multishot cho ra bức ảnh lên tới 160 MP. Đây là thiết bị tối ưu cho chụp ảnh sản phẩm, thương mại và các công việc quay phim yêu cầu độ nét tối đa.",
        "brand": "Fujifilm",
        "type": "Mirrorless",
        "sensor": "Crop / APS-C (40 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (8K 30p, 4K 60p)",
        "purpose": "Chụp Studio, Thương mại",
        "price_range": "40 - 50 triệu đồng (Giá tham khảo: 44.000.000 VNĐ)",
        "price_num": 44000000,
        "price_text": "44.000.000đ",
        "rules": [
            86,
            87
        ],
        "facts": [
            "C2",
            "G5",
            "L2",
            "M1",
            "N6",
            "N7",
            "T4",
            "V3"
        ],
        "mp": "40MP",
        "video_short": "8K RAW",
        "sensor_short": "APS-C CMOS",
        "fps": "Cảm ứng",
        "discount": 16,
        "old_price_text": "52.380.000đ",
        "smember_text": "440.000đ",
        "promo": "Giảm ngay 1.500.000đ khi mua kèm ống kính chính hãng & tặng túi máy ảnh",
        "rating": "4.9",
        "reviews": 100
    },
    {
        "id": "K38",
        "order": 38,
        "name": "Máy ảnh Fujifilm X-H2S",
        "desc": "Fujifilm X-H2S là dòng máy ảnh flagship tốc độ cao sử dụng cảm biến X-Trans CMOS 5 HS dạng Stacked BSI 26.1 MP. Máy có khả năng chụp liên tiếp siêu tốc 40 hình/giây không bị chớp đen và quay video chuyên nghiệp, đáp ứng tốt nhu cầu tác nghiệp thể thao, chim thú và sự kiện tốc độ.",
        "brand": "Fujifilm",
        "type": "Mirrorless",
        "sensor": "Crop / APS-C (26.1 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (6.2K 30p, 4K 120p ProRes)",
        "purpose": "Thể thao, Tốc độ cao",
        "price_range": "50 – 60  triệu đồng (Giá tham khảo: 54.000.000 VNĐ)",
        "price_num": 54000000,
        "price_text": "54.000.000đ",
        "rules": [
            88,
            89
        ],
        "facts": [
            "C2",
            "G6",
            "L2",
            "M1",
            "N5",
            "N6",
            "T4",
            "V3"
        ],
        "mp": "26.1MP",
        "video_short": "6K Pro",
        "sensor_short": "APS-C CMOS",
        "fps": "40 FPS",
        "discount": 15,
        "old_price_text": "63.530.000đ",
        "smember_text": "540.000đ",
        "promo": "Tặng pin dự phòng chính hãng, bộ vệ sinh cảm biến 5 món và balo chống sốc",
        "rating": "4.8",
        "reviews": 22
    },
    {
        "id": "K39",
        "order": 39,
        "name": "Máy ảnh Fujifilm GFX 50S II",
        "desc": "Fujifilm GFX 50S II là mẫu máy ảnh Medium Format tiếp cận mức giá dễ chịu hơn, trang bị cảm biến 51.4 MP cho dải tương phản động (Dynamic Range) cực rộng và màu sắc trung thực. Thân máy có chống rung IBIS 6.5 stops giúp chụp cầm tay dễ dàng, là lựa chọn lý tưởng cho chụp ảnh chân dung nghệ thuật và phong cảnh.",
        "brand": "Fujifilm",
        "type": "Mirrorless",
        "sensor": "Medium Format (51.4 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (Full HD 30p)",
        "purpose": "Chân dung, Phong cảnh",
        "price_range": "trên 80 triệu đồng (Giá tham khảo: 82.000.000 VNĐ)",
        "price_num": 82000000,
        "price_text": "82.000.000đ",
        "rules": [
            90,
            91
        ],
        "facts": [
            "C3",
            "G9",
            "L2",
            "M1",
            "N2",
            "N7",
            "T4",
            "V1"
        ],
        "mp": "51.4MP",
        "video_short": "FHD 60p",
        "sensor_short": "M.Format",
        "fps": "Cảm ứng",
        "discount": 17,
        "old_price_text": "98.800.000đ",
        "smember_text": "820.000đ",
        "promo": "Trả góp 0% lãi suất qua thẻ tín dụng, tặng kèm thẻ nhớ SanDisk Extreme Pro 64GB",
        "rating": "5.0",
        "reviews": 29
    },
    {
        "id": "K40",
        "order": 40,
        "name": "Máy ảnh Fujifilm GFX 100S",
        "desc": "Fujifilm GFX 100S sở hữu cảm biến khổ lớn Medium Format với độ phân giải lên tới 102 MP, mang lại chi tiết hình ảnh vượt trội và khả năng tái tạo màu sắc đỉnh cao. Máy tích hợp chống rung 5 trục (IBIS) trong một thân máy gọn nhẹ tương đương máy ảnh Full-frame, thích hợp cho nhiếp ảnh gia chụp thời trang, quảng cáo và studio thương mại chuyên nghiệp.",
        "brand": "Fujifilm",
        "type": "Mirrorless",
        "sensor": "Medium Format (102 MP)",
        "touch": "Có",
        "video": "Quay nâng cao (4K 30p 10-bit)",
        "purpose": "Chụp Studio, Thương mại",
        "price_range": "trên 80 triệu đồng (Giá tham khảo: 129.000.000 VNĐ)",
        "price_num": 129000000,
        "price_text": "129.000.000đ",
        "rules": [
            92,
            93
        ],
        "facts": [
            "C3",
            "G9",
            "L2",
            "M1",
            "N2",
            "N7",
            "T4",
            "V2"
        ],
        "mp": "102MP",
        "video_short": "4K UHD",
        "sensor_short": "M.Format",
        "fps": "Cảm ứng",
        "discount": 14,
        "old_price_text": "150.000.000đ",
        "smember_text": "1.290.000đ",
        "promo": "Tặng micro thu âm cài áo không dây và chân máy tripod du lịch cao cấp",
        "rating": "4.9",
        "reviews": 36
    },
    {
        "id": "K41",
        "order": 41,
        "name": "Máy ảnh Panasonic Lumix G100",
        "desc": "Panasonic Lumix G100 là dòng máy ảnh Mirrorless gọn nhẹ thiết kế tối ưu cho Vlogger và người sáng tạo nội dung cá nhân. Máy tích hợp công nghệ âm thanh OZO Audio thông minh của Nokia giúp thu âm định hướng rõ ràng, đi kèm màn hình xoay lật và giao diện quay chụp rất dễ sử dụng.",
        "brand": "Panasonic",
        "type": "Mirrorless",
        "sensor": "Micro Four Thirds / M43 (20.3 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p, Full HD 60p)",
        "purpose": "Quay Vlog, Sáng tạo nội dung",
        "price_range": "10 – 20  triệu đồng (Giá tham khảo: 12.500.000 VNĐ)",
        "price_num": 12500000,
        "price_text": "12.500.000đ",
        "rules": [
            94,
            95
        ],
        "facts": [
            "C4",
            "G2",
            "L2",
            "M1",
            "N1",
            "N4",
            "T5",
            "V1"
        ],
        "mp": "20.3MP",
        "video_short": "4K UHD",
        "sensor_short": "M4/3 CMOS",
        "fps": "Cảm ứng",
        "discount": 16,
        "old_price_text": "14.880.000đ",
        "smember_text": "125.000đ",
        "promo": "Tặng đèn LED mini Godox LITEMONS LED6R và thẻ nhớ SD 64GB tốc độ cao",
        "rating": "5.0",
        "reviews": 43
    },
    {
        "id": "K42",
        "order": 42,
        "name": "Máy ảnh Panasonic Lumix G85",
        "desc": "Panasonic Lumix G85 là mẫu máy ảnh M43 tầm trung có khả năng hoạt động bền bỉ với thân máy kháng bụi và tia nước. Máy sở hữu chống rung 5 trục Dual I.S. 2 hiệu quả, quay video 4K sắc nét, là lựa chọn kinh tế cho người mới làm quen với quay phim.",
        "brand": "Panasonic",
        "type": "Mirrorless",
        "sensor": "Micro Four Thirds / M43 (16.0 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p, Full HD 60p)",
        "purpose": "Cơ bản, Du lịch, Đường phố",
        "price_range": "10 - 20 triệu đồng (Giá tham khảo: 15.000.000 VNĐ)",
        "price_num": 15000000,
        "price_text": "15.000.000đ",
        "rules": [
            96,
            97
        ],
        "facts": [
            "C4",
            "G2",
            "L2",
            "M1",
            "N1",
            "N4",
            "T5",
            "V1"
        ],
        "mp": "16.0MP",
        "video_short": "4K UHD",
        "sensor_short": "M4/3 CMOS",
        "fps": "Cảm ứng",
        "discount": 15,
        "old_price_text": "17.650.000đ",
        "smember_text": "150.000đ",
        "promo": "Giảm ngay 1.500.000đ khi mua kèm ống kính chính hãng & tặng túi máy ảnh",
        "rating": "4.8",
        "reviews": 50
    },
    {
        "id": "K43",
        "order": 43,
        "name": "Máy ảnh Panasonic Lumix G95",
        "desc": "Panasonic Lumix G95 là bản nâng cấp toàn diện của G85, bổ sung cảm biến 20.3 MP không có bộ lọc thông thấp (OLPF) giúp hình ảnh sắc nét hơn. Máy tích hợp sẵn profile màu V-LogL giúp tối ưu hóa dải tương phản động khi quay phim và chỉnh màu hậu kỳ.",
        "brand": "Panasonic",
        "type": "Mirrorless",
        "sensor": "Micro Four Thirds / M43 (20.3 MP)",
        "touch": "Có",
        "video": "Quay cơ bản (4K 30p, Full HD 120p)",
        "purpose": "Quay Vlog, Sáng tạo nội dung",
        "price_range": "10 - 20 triệu đồng (Giá tham khảo: 18.500.000 VNĐ)",
        "price_num": 18500000,
        "price_text": "18.500.000đ",
        "rules": [
            98,
            99
        ],
        "facts": [
            "C4",
            "G2",
            "L2",
            "M1",
            "N3",
            "N4",
            "T5",
            "V1"
        ],
        "mp": "20.3MP",
        "video_short": "4K UHD",
        "sensor_short": "M4/3 CMOS",
        "fps": "Cảm ứng",
        "discount": 18,
        "old_price_text": "22.560.000đ",
        "smember_text": "185.000đ",
        "promo": "Tặng pin dự phòng chính hãng, bộ vệ sinh cảm biến 5 món và balo chống sốc",
        "rating": "4.9",
        "reviews": 57
    },
    {
        "id": "K44",
        "order": 44,
        "name": "Máy ảnh Panasonic Lumix GH5",
        "desc": "Panasonic Lumix GH5 từng là huyền thoại trong giới quay phim dịch vụ và YouTube nhờ khả năng quay 4K 10-bit nội bộ 4:2:2 vô cùng bền bỉ, không bị quá nhiệt. Thân máy hợp kim magie chắc chắn cùng hệ thống chống rung bá chủ phân khúc giúp quay cầm tay mượt mà.",
        "brand": "Panasonic",
        "type": "Mirrorless",
        "sensor": "Micro Four Thirds / M43 (20.3 MP)",
        "touch": "Có",
        "video": "Quay nâng cao (4K 60p 10-bit 4:2:2)",
        "purpose": "Chuyên sản xuất Video, Điện ảnh",
        "price_range": "20 - 30 triệu đồng (Giá tham khảo: 24.000.000 VNĐ)",
        "price_num": 24000000,
        "price_text": "24.000.000đ",
        "rules": [
            100,
            101
        ],
        "facts": [
            "C4",
            "G3",
            "L2",
            "M1",
            "N3",
            "N6",
            "T5",
            "V2"
        ],
        "mp": "20.3MP",
        "video_short": "4K UHD",
        "sensor_short": "M4/3 CMOS",
        "fps": "Cảm ứng",
        "discount": 14,
        "old_price_text": "27.910.000đ",
        "smember_text": "240.000đ",
        "promo": "Trả góp 0% lãi suất qua thẻ tín dụng, tặng kèm thẻ nhớ SanDisk Extreme Pro 64GB",
        "rating": "4.8",
        "reviews": 64
    },
    {
        "id": "K45",
        "order": 45,
        "name": "Máy ảnh Panasonic Lumix GH5 II",
        "desc": "Panasonic Lumix GH5 II nâng cấp bộ xử lý Venus Engine mới, cải thiện khả năng lấy nét tự động nhận diện khuôn mặt/mắt và hỗ trợ tính năng Livestream trực tiếp qua Wi-Fi hoặc USB cực kỳ tiện lợi cho các buổi phát sóng trực tuyến.",
        "brand": "Panasonic",
        "type": "Mirrorless",
        "sensor": "Micro Four Thirds / M43 (20.3 MP)",
        "touch": "Có",
        "video": "Quay nâng cao (C4K/4K 60p 10-bit, V-Log L)",
        "purpose": "Chuyên sản xuất Video, Điện ảnh",
        "price_range": "30 - 40 triệu đồng (Giá tham khảo: 32.000.000 VNĐ)",
        "price_num": 32000000,
        "price_text": "32.000.000đ",
        "rules": [
            102,
            103
        ],
        "facts": [
            "C4",
            "G4",
            "L2",
            "M1",
            "N4",
            "N6",
            "T5",
            "V2"
        ],
        "mp": "20.3MP",
        "video_short": "4K UHD",
        "sensor_short": "M4/3 CMOS",
        "fps": "Cảm ứng",
        "discount": 16,
        "old_price_text": "38.100.000đ",
        "smember_text": "320.000đ",
        "promo": "Tặng micro thu âm cài áo không dây và chân máy tripod du lịch cao cấp",
        "rating": "5.0",
        "reviews": 71
    },
    {
        "id": "K46",
        "order": 46,
        "name": "Máy ảnh Panasonic Lumix S5",
        "desc": "Panasonic Lumix S5 đánh dấu bước chuyển mình sang cảm biến Full-frame nhỏ gọn. Máy sở hữu dải nhạy sáng rộng (Dynamic Range 14+ stop với V-Log), chụp ảnh độ phân giải cao 96 MP nhờ cơ chế Shift-sensor, mang chất lượng điện ảnh đến với người dùng bán chuyên.",
        "brand": "Panasonic",
        "type": "Mirrorless",
        "sensor": "Full-frame (24.2 MP)",
        "touch": "Có",
        "video": "Quay nâng cao (4K 60p / 10-bit V-Log)",
        "purpose": "Chân dung, Phong cảnh",
        "price_range": "30 - 40 triệu đồng (Giá tham khảo: 33.500.000 VNĐ)",
        "price_num": 33500000,
        "price_text": "33.500.000đ",
        "rules": [
            104,
            105
        ],
        "facts": [
            "C1",
            "G4",
            "L2",
            "M1",
            "N2",
            "N6",
            "T5",
            "V2"
        ],
        "mp": "96MP",
        "video_short": "4K UHD",
        "sensor_short": "Full-frame",
        "fps": "Cảm ứng",
        "discount": 12,
        "old_price_text": "38.070.000đ",
        "smember_text": "335.000đ",
        "promo": "Tặng đèn LED mini Godox LITEMONS LED6R và thẻ nhớ SD 64GB tốc độ cao",
        "rating": "4.9",
        "reviews": 78
    },
    {
        "id": "K47",
        "order": 47,
        "name": "Máy ảnh Panasonic Lumix GH6",
        "desc": "Panasonic Lumix GH6 là chiếc máy ảnh M43 đỉnh cao chuyên dụng cho sản xuất video. Máy tích hợp quạt tản nhiệt chủ động giúp quay phim liên tục không giới hạn, hỗ trợ định dạng Apple ProRes 422 HQ nội bộ và hệ thống chống rung IBIS lên tới 7.5 stop.",
        "brand": "Panasonic",
        "type": "Mirrorless",
        "sensor": "Micro Four Thirds / M43 (25.2 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (5.7K 60p, 4K 120p ProRes).",
        "purpose": "Chuyên sản xuất Video, Điện ảnh",
        "price_range": "30 - 40 triệu đồng (Giá tham khảo: 38.000.000 VNĐ)",
        "price_num": 38000000,
        "price_text": "38.000.000đ",
        "rules": [
            106,
            107
        ],
        "facts": [
            "C4",
            "G4",
            "L2",
            "M1",
            "N6",
            "T5",
            "V2",
            "V3"
        ],
        "mp": "25.2MP",
        "video_short": "6K Pro",
        "sensor_short": "M4/3 CMOS",
        "fps": "Cảm ứng",
        "discount": 16,
        "old_price_text": "45.240.000đ",
        "smember_text": "380.000đ",
        "promo": "Giảm ngay 1.500.000đ khi mua kèm ống kính chính hãng & tặng túi máy ảnh",
        "rating": "5.0",
        "reviews": 85
    },
    {
        "id": "K48",
        "order": 48,
        "name": "Máy ảnh Panasonic Lumix G9 II",
        "desc": "Panasonic Lumix G9 II là dòng máy ảnh M43 cao cấp thế hệ mới tích hợp công nghệ lấy nét Phase Hybrid AF (lấy nét theo pha) xóa bỏ điểm yếu lấy nét trước đây. Máy hỗ trợ chụp liên tiếp siêu tốc 60fps với lấy nét liên tục, phù hợp cho cả quay video và chụp ảnh hành động.",
        "brand": "Panasonic",
        "type": "Mirrorless",
        "sensor": "Micro Four Thirds / M43 (25.2 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (5.7K 60p, 4K 120p)",
        "purpose": "Thể thao, Tốc độ cao",
        "price_range": "40 - 50 triệu đồng (Giá tham khảo: 42.000.000 VNĐ)",
        "price_num": 42000000,
        "price_text": "42.000.000đ",
        "rules": [
            108,
            109
        ],
        "facts": [
            "C4",
            "G5",
            "L2",
            "M1",
            "N5",
            "N6",
            "T5",
            "V3"
        ],
        "mp": "25.2MP",
        "video_short": "6K Pro",
        "sensor_short": "M4/3 CMOS",
        "fps": "60 FPS",
        "discount": 15,
        "old_price_text": "49.410.000đ",
        "smember_text": "420.000đ",
        "promo": "Tặng pin dự phòng chính hãng, bộ vệ sinh cảm biến 5 món và balo chống sốc",
        "rating": "4.8",
        "reviews": 92
    },
    {
        "id": "K49",
        "order": 49,
        "name": "Máy ảnh Panasonic Lumix S5 II",
        "desc": "Panasonic Lumix S5 II là bước đột phá lớn của hãng khi trang bị cảm biến Full-frame kết hợp lấy nét theo pha Phase Hybrid AF cực kỳ chính xác. Máy tích hợp quạt tản nhiệt ẩn trong gù ngắm, chống rung Active I.S. ấn tượng cho khả năng quay phim handheld mượt mà như dùng gimbal.",
        "brand": "Panasonic",
        "type": "Mirrorless",
        "sensor": "Full-frame (24.2 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (6K 30p, 4K 60p 10-bit)",
        "purpose": "Đa dụng, Sự kiện",
        "price_range": "40 - 50 triệu đồng (Giá tham khảo: 43.000.000 VNĐ)",
        "price_num": 43000000,
        "price_text": "43.000.000đ",
        "rules": [
            110,
            111
        ],
        "facts": [
            "C1",
            "G5",
            "L2",
            "M1",
            "N3",
            "N6",
            "T5",
            "V3"
        ],
        "mp": "24.2MP",
        "video_short": "6K Pro",
        "sensor_short": "Full-frame",
        "fps": "Cảm ứng",
        "discount": 17,
        "old_price_text": "51.810.000đ",
        "smember_text": "430.000đ",
        "promo": "Trả góp 0% lãi suất qua thẻ tín dụng, tặng kèm thẻ nhớ SanDisk Extreme Pro 64GB",
        "rating": "4.9",
        "reviews": 99
    },
    {
        "id": "K50",
        "order": 50,
        "name": "Máy ảnh Panasonic Lumix S1H",
        "desc": "Panasonic Lumix S1H là chiếc máy ảnh mirrorless Full-frame đầu tiên trên thế giới được Netflix công nhận đạt tiêu chuẩn quay phim điện ảnh chuyên nghiệp (Netflix Approved). Máy trang bị cảm biến Full-frame 24.2 MP với Dual Native ISO, quạt tản nhiệt công nghiệp và khả năng xuất RAW 6K ra bộ ghi ngoài.",
        "brand": "Panasonic",
        "type": "Mirrorless",
        "sensor": "Full-frame (24.2 MP)",
        "touch": "Có",
        "video": "Quay điện ảnh siêu nét (6K 24p, 4K 60p 10-bit V-Log)",
        "purpose": "Chuyên sản xuất Video, Điện ảnh",
        "price_range": "trên 80 triệu đồng (Giá tham khảo: 85.000.000 VNĐ)",
        "price_num": 85000000,
        "price_text": "85.000.000đ",
        "rules": [
            112,
            113
        ],
        "facts": [
            "C1",
            "G9",
            "L2",
            "M1",
            "N6",
            "T5",
            "V2",
            "V3"
        ],
        "mp": "24.2MP",
        "video_short": "6K Pro",
        "sensor_short": "Full-frame",
        "fps": "Cảm ứng",
        "discount": 14,
        "old_price_text": "98.840.000đ",
        "smember_text": "850.000đ",
        "promo": "Tặng micro thu âm cài áo không dây và chân máy tripod du lịch cao cấp",
        "rating": "4.8",
        "reviews": 21
    }
]

# ==============================================================================
# 3. TẬP LUẬT SUY DIỄN (RULE BASE) - 113 LUẬT CHUYÊN GIA
# Biểu diễn dưới dạng Luật sản xuất (Production Rules):
#   IF (T_i ∧ L_j ∧ C_k ∧ M_l ∧ V_m ∧ N_n ∧ G_p) THEN K_q
# ==============================================================================
RULES = [
    {
        "id": 1,
        "conditions": [
            "T1",
            "L2",
            "C2",
            "M1",
            "V1",
            "N4",
            "G2"
        ],
        "conclusion": "K1",
        "formula": "T1∧L2∧C2∧M1∧V1∧N4∧G2→K1",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Canon EOS R50."
    },
    {
        "id": 2,
        "conditions": [
            "T1",
            "L2",
            "C2",
            "M1",
            "V1",
            "N1",
            "G2"
        ],
        "conclusion": "K1",
        "formula": "T1∧L2∧C2∧M1∧V1∧N1∧G2→K1",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Canon EOS R50."
    },
    {
        "id": 3,
        "conditions": [
            "T1",
            "L2",
            "C2",
            "M2",
            "V1",
            "N1",
            "G2"
        ],
        "conclusion": "K2",
        "formula": "T1∧L2∧C2∧M2∧V1∧N1∧G2→K2",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), không có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Canon EOS R100."
    },
    {
        "id": 4,
        "conditions": [
            "T1",
            "L2",
            "C2",
            "M2",
            "V1",
            "N2",
            "G2"
        ],
        "conclusion": "K2",
        "formula": "T1∧L2∧C2∧M2∧V1∧N2∧G2→K2",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), không có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Canon EOS R100."
    },
    {
        "id": 5,
        "conditions": [
            "T1",
            "L2",
            "C2",
            "M1",
            "V2",
            "N3",
            "G2"
        ],
        "conclusion": "K3",
        "formula": "T1∧L2∧C2∧M1∧V2∧N3∧G2→K3",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Canon EOS R10."
    },
    {
        "id": 6,
        "conditions": [
            "T1",
            "L2",
            "C2",
            "M1",
            "V2",
            "N5",
            "G2"
        ],
        "conclusion": "K3",
        "formula": "T1∧L2∧C2∧M1∧V2∧N5∧G2→K3",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích thể thao, tốc độ cao với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Canon EOS R10."
    },
    {
        "id": 7,
        "conditions": [
            "T1",
            "L2",
            "C2",
            "M1",
            "V1",
            "N3",
            "G2"
        ],
        "conclusion": "K3",
        "formula": "T1∧L2∧C2∧M1∧V1∧N3∧G2→K3",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Canon EOS R10."
    },
    {
        "id": 8,
        "conditions": [
            "T1",
            "L1",
            "C1",
            "M2",
            "V1",
            "N2",
            "G1"
        ],
        "conclusion": "K4",
        "formula": "T1∧L1∧C1∧M2∧V1∧N2∧G1→K4",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy DSLR, trang bị cảm biến Full-frame, không có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 0 - 10 triệu đồng thì nên chọn Máy ảnh Canon EOS 6D."
    },
    {
        "id": 9,
        "conditions": [
            "T1",
            "L1",
            "C1",
            "M2",
            "V1",
            "N1",
            "G1"
        ],
        "conclusion": "K4",
        "formula": "T1∧L1∧C1∧M2∧V1∧N1∧G1→K4",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy DSLR, trang bị cảm biến Full-frame, không có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 0 - 10 triệu đồng thì nên chọn Máy ảnh Canon EOS 6D."
    },
    {
        "id": 10,
        "conditions": [
            "T1",
            "L1",
            "C1",
            "M2",
            "V1",
            "N3",
            "G2"
        ],
        "conclusion": "K5",
        "formula": "T1∧L1∧C1∧M2∧V1∧N3∧G2→K5",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy DSLR, trang bị cảm biến Full-frame, không có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Canon EOS 5D Mark III."
    },
    {
        "id": 11,
        "conditions": [
            "T1",
            "L1",
            "C1",
            "M2",
            "V1",
            "N2",
            "G2"
        ],
        "conclusion": "K5",
        "formula": "T1∧L1∧C1∧M2∧V1∧N2∧G2→K5",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy DSLR, trang bị cảm biến Full-frame, không có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Canon EOS 5D Mark III."
    },
    {
        "id": 12,
        "conditions": [
            "T1",
            "L2",
            "C1",
            "M1",
            "V2",
            "N2",
            "G3"
        ],
        "conclusion": "K6",
        "formula": "T1∧L2∧C1∧M1∧V2∧N2∧G3→K6",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Canon EOS R8."
    },
    {
        "id": 13,
        "conditions": [
            "T1",
            "L2",
            "C1",
            "M1",
            "V2",
            "N1",
            "G3"
        ],
        "conclusion": "K6",
        "formula": "T1∧L2∧C1∧M1∧V2∧N1∧G3→K6",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Canon EOS R8."
    },
    {
        "id": 14,
        "conditions": [
            "T1",
            "L2",
            "C1",
            "M1",
            "V2",
            "N4",
            "G3"
        ],
        "conclusion": "K6",
        "formula": "T1∧L2∧C1∧M1∧V2∧N4∧G3→K6",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Canon EOS R8."
    },
    {
        "id": 15,
        "conditions": [
            "T1",
            "L2",
            "C1",
            "M1",
            "V2",
            "N3",
            "G5"
        ],
        "conclusion": "K7",
        "formula": "T1∧L2∧C1∧M1∧V2∧N3∧G5→K7",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Canon EOS R6 Mark II."
    },
    {
        "id": 16,
        "conditions": [
            "T1",
            "L2",
            "C1",
            "M1",
            "V2",
            "N5",
            "G5"
        ],
        "conclusion": "K7",
        "formula": "T1∧L2∧C1∧M1∧V2∧N5∧G5→K7",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích thể thao, tốc độ cao với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Canon EOS R6 Mark II."
    },
    {
        "id": 17,
        "conditions": [
            "T1",
            "L2",
            "C1",
            "M1",
            "V2",
            "N6",
            "G5"
        ],
        "conclusion": "K7",
        "formula": "T1∧L2∧C1∧M1∧V2∧N6∧G5→K7",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Canon EOS R6 Mark II."
    },
    {
        "id": 18,
        "conditions": [
            "T1",
            "L2",
            "C1",
            "M1",
            "V3",
            "N7",
            "G7"
        ],
        "conclusion": "K8",
        "formula": "T1∧L2∧C1∧M1∧V3∧N7∧G7→K8",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chụp Studio, thương mại với phân khúc giá từ 60 - 70 triệu đồng thì nên chọn Máy ảnh Canon EOS R5."
    },
    {
        "id": 19,
        "conditions": [
            "T1",
            "L2",
            "C1",
            "M1",
            "V3",
            "N6",
            "G7"
        ],
        "conclusion": "K8",
        "formula": "T1∧L2∧C1∧M1∧V3∧N6∧G7→K8",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 60 - 70 triệu đồng thì nên chọn Máy ảnh Canon EOS R5."
    },
    {
        "id": 20,
        "conditions": [
            "T1",
            "L2",
            "C1",
            "M1",
            "V2",
            "N7",
            "G7"
        ],
        "conclusion": "K8",
        "formula": "T1∧L2∧C1∧M1∧V2∧N7∧G7→K8",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chụp Studio, thương mại với phân khúc giá từ 60 - 70 triệu đồng thì nên chọn Máy ảnh Canon EOS R5."
    },
    {
        "id": 21,
        "conditions": [
            "T1",
            "L1",
            "C2",
            "M1",
            "V1",
            "N5",
            "G3"
        ],
        "conclusion": "K9",
        "formula": "T1∧L1∧C2∧M1∧V1∧N5∧G3→K9",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy DSLR, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích thể thao, tốc độ cao với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Canon EOS 90D."
    },
    {
        "id": 22,
        "conditions": [
            "T1",
            "L1",
            "C2",
            "M1",
            "V1",
            "N3",
            "G3"
        ],
        "conclusion": "K9",
        "formula": "T1∧L1∧C2∧M1∧V1∧N3∧G3→K9",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy DSLR, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Canon EOS 90D."
    },
    {
        "id": 23,
        "conditions": [
            "T1",
            "L2",
            "C1",
            "M1",
            "V3",
            "N5",
            "G9"
        ],
        "conclusion": "K10",
        "formula": "T1∧L2∧C1∧M1∧V3∧N5∧G9→K10",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích thể thao, tốc độ cao với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Canon EOS R3."
    },
    {
        "id": 24,
        "conditions": [
            "T1",
            "L2",
            "C1",
            "M1",
            "V3",
            "N6",
            "G9"
        ],
        "conclusion": "K10",
        "formula": "T1∧L2∧C1∧M1∧V3∧N6∧G9→K10",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Canon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Canon EOS R3."
    },
    {
        "id": 25,
        "conditions": [
            "T2",
            "L2",
            "C2",
            "M1",
            "V1",
            "N4",
            "G2"
        ],
        "conclusion": "K11",
        "formula": "T2∧L2∧C2∧M1∧V1∧N4∧G2→K11",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Sony ZV-E10."
    },
    {
        "id": 26,
        "conditions": [
            "T2",
            "L2",
            "C2",
            "M1",
            "V1",
            "N1",
            "G2"
        ],
        "conclusion": "K11",
        "formula": "T2∧L2∧C2∧M1∧V1∧N1∧G2→K11",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Sony ZV-E10."
    },
    {
        "id": 27,
        "conditions": [
            "T2",
            "L2",
            "C2",
            "M1",
            "V1",
            "N4",
            "G2"
        ],
        "conclusion": "K12",
        "formula": "T2∧L2∧C2∧M1∧V1∧N4∧G2→K12",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Sony Alpha A6400."
    },
    {
        "id": 28,
        "conditions": [
            "T2",
            "L2",
            "C2",
            "M1",
            "V1",
            "N1",
            "G2"
        ],
        "conclusion": "K12",
        "formula": "T2∧L2∧C2∧M1∧V1∧N1∧G2→K12",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Sony Alpha A6400."
    },
    {
        "id": 29,
        "conditions": [
            "T2",
            "L2",
            "C2",
            "M1",
            "V2",
            "N3",
            "G4"
        ],
        "conclusion": "K13",
        "formula": "T2∧L2∧C2∧M1∧V2∧N3∧G4→K13",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Sony Alpha A6700."
    },
    {
        "id": 30,
        "conditions": [
            "T2",
            "L2",
            "C2",
            "M1",
            "V2",
            "N4",
            "G4"
        ],
        "conclusion": "K13",
        "formula": "T2∧L2∧C2∧M1∧V2∧N4∧G4→K13",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Sony Alpha A6700."
    },
    {
        "id": 31,
        "conditions": [
            "T2",
            "L2",
            "C2",
            "M1",
            "V2",
            "N5",
            "G4"
        ],
        "conclusion": "K13",
        "formula": "T2∧L2∧C2∧M1∧V2∧N5∧G4→K13",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích thể thao, tốc độ cao với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Sony Alpha A6700."
    },
    {
        "id": 32,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M2",
            "V1",
            "N2",
            "G2"
        ],
        "conclusion": "K14",
        "formula": "T2∧L2∧C1∧M2∧V1∧N2∧G2→K14",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, không có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7 II."
    },
    {
        "id": 33,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M2",
            "V1",
            "N1",
            "G2"
        ],
        "conclusion": "K14",
        "formula": "T2∧L2∧C1∧M2∧V1∧N1∧G2→K14",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, không có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7 II."
    },
    {
        "id": 34,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V1",
            "N3",
            "G3"
        ],
        "conclusion": "K15",
        "formula": "T2∧L2∧C1∧M1∧V1∧N3∧G3→K15",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7 III."
    },
    {
        "id": 35,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V1",
            "N2",
            "G3"
        ],
        "conclusion": "K15",
        "formula": "T2∧L2∧C1∧M1∧V1∧N2∧G3→K15",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7 III."
    },
    {
        "id": 36,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V1",
            "N6",
            "G3"
        ],
        "conclusion": "K15",
        "formula": "T2∧L2∧C1∧M1∧V1∧N6∧G3→K15",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7 III."
    },
    {
        "id": 37,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V2",
            "N4",
            "G5"
        ],
        "conclusion": "K16",
        "formula": "T2∧L2∧C1∧M1∧V2∧N4∧G5→K16",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7C II."
    },
    {
        "id": 38,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V2",
            "N1",
            "G5"
        ],
        "conclusion": "K16",
        "formula": "T2∧L2∧C1∧M1∧V2∧N1∧G5→K16",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7C II."
    },
    {
        "id": 39,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V2",
            "N3",
            "G5"
        ],
        "conclusion": "K16",
        "formula": "T2∧L2∧C1∧M1∧V2∧N3∧G5→K16",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7C II."
    },
    {
        "id": 40,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V2",
            "N3",
            "G6"
        ],
        "conclusion": "K17",
        "formula": "T2∧L2∧C1∧M1∧V2∧N3∧G6→K17",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 50 - 60 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7 IV."
    },
    {
        "id": 41,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V2",
            "N2",
            "G6"
        ],
        "conclusion": "K17",
        "formula": "T2∧L2∧C1∧M1∧V2∧N2∧G6→K17",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 50 - 60 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7 IV."
    },
    {
        "id": 42,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V2",
            "N6",
            "G6"
        ],
        "conclusion": "K17",
        "formula": "T2∧L2∧C1∧M1∧V2∧N6∧G6→K17",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 50 - 60 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7 IV."
    },
    {
        "id": 43,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V3",
            "N7",
            "G9"
        ],
        "conclusion": "K18",
        "formula": "T2∧L2∧C1∧M1∧V3∧N7∧G9→K18",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chụp Studio, thương mại với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7R V."
    },
    {
        "id": 44,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V3",
            "N2",
            "G9"
        ],
        "conclusion": "K18",
        "formula": "T2∧L2∧C1∧M1∧V3∧N2∧G9→K18",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chân dung, phong cảnh với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7R V."
    },
    {
        "id": 45,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V2",
            "N7",
            "G9"
        ],
        "conclusion": "K18",
        "formula": "T2∧L2∧C1∧M1∧V2∧N7∧G9→K18",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chụp Studio, thương mại với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7R V."
    },
    {
        "id": 46,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V2",
            "N6",
            "G8"
        ],
        "conclusion": "K19",
        "formula": "T2∧L2∧C1∧M1∧V2∧N6∧G8→K19",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 70 - 80 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7S III."
    },
    {
        "id": 47,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V2",
            "N3",
            "G8"
        ],
        "conclusion": "K19",
        "formula": "T2∧L2∧C1∧M1∧V2∧N3∧G8→K19",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 70 - 80 triệu đồng thì nên chọn Máy ảnh Sony Alpha A7S III."
    },
    {
        "id": 48,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V3",
            "N5",
            "G9"
        ],
        "conclusion": "K20",
        "formula": "T2∧L2∧C1∧M1∧V3∧N5∧G9→K20",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích thể thao, tốc độ cao với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Sony Alpha A1."
    },
    {
        "id": 49,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V3",
            "N7",
            "G9"
        ],
        "conclusion": "K20",
        "formula": "T2∧L2∧C1∧M1∧V3∧N7∧G9→K20",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chụp Studio, thương mại với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Sony Alpha A1."
    },
    {
        "id": 50,
        "conditions": [
            "T2",
            "L2",
            "C1",
            "M1",
            "V3",
            "N6",
            "G9"
        ],
        "conclusion": "K20",
        "formula": "T2∧L2∧C1∧M1∧V3∧N6∧G9→K20",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Sony, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Sony Alpha A1."
    },
    {
        "id": 51,
        "conditions": [
            "T3",
            "L1",
            "C2",
            "M1",
            "V1",
            "N5",
            "G2"
        ],
        "conclusion": "K21",
        "formula": "T3∧L1∧C2∧M1∧V1∧N5∧G2→K21",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy DSLR, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích thể thao, tốc độ cao với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Nikon D7500."
    },
    {
        "id": 52,
        "conditions": [
            "T3",
            "L1",
            "C2",
            "M1",
            "V1",
            "N3",
            "G2"
        ],
        "conclusion": "K21",
        "formula": "T3∧L1∧C2∧M1∧V1∧N3∧G2→K21",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy DSLR, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Nikon D7500."
    },
    {
        "id": 53,
        "conditions": [
            "T3",
            "L1",
            "C1",
            "M1",
            "V1",
            "N7",
            "G5"
        ],
        "conclusion": "K22",
        "formula": "T3∧L1∧C1∧M1∧V1∧N7∧G5→K22",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy DSLR, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích chụp Studio, thương mại với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Nikon D850."
    },
    {
        "id": 54,
        "conditions": [
            "T3",
            "L1",
            "C1",
            "M1",
            "V1",
            "N2",
            "G5"
        ],
        "conclusion": "K22",
        "formula": "T3∧L1∧C1∧M1∧V1∧N2∧G5→K22",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy DSLR, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Nikon D850."
    },
    {
        "id": 55,
        "conditions": [
            "T3",
            "L2",
            "C2",
            "M1",
            "V1",
            "N4",
            "G2"
        ],
        "conclusion": "K23",
        "formula": "T3∧L2∧C2∧M1∧V1∧N4∧G2→K23",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Nikon Z30."
    },
    {
        "id": 56,
        "conditions": [
            "T3",
            "L2",
            "C2",
            "M1",
            "V1",
            "N1",
            "G2"
        ],
        "conclusion": "K23",
        "formula": "T3∧L2∧C2∧M1∧V1∧N1∧G2→K23",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Nikon Z30."
    },
    {
        "id": 57,
        "conditions": [
            "T3",
            "L2",
            "C2",
            "M1",
            "V1",
            "N1",
            "G2"
        ],
        "conclusion": "K24",
        "formula": "T3∧L2∧C2∧M1∧V1∧N1∧G2→K24",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Nikon Z50."
    },
    {
        "id": 58,
        "conditions": [
            "T3",
            "L2",
            "C2",
            "M1",
            "V1",
            "N4",
            "G2"
        ],
        "conclusion": "K24",
        "formula": "T3∧L2∧C2∧M1∧V1∧N4∧G2→K24",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Nikon Z50."
    },
    {
        "id": 59,
        "conditions": [
            "T3",
            "L2",
            "C2",
            "M1",
            "V1",
            "N1",
            "G3"
        ],
        "conclusion": "K25",
        "formula": "T3∧L2∧C2∧M1∧V1∧N1∧G3→K25",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Nikon Z fc."
    },
    {
        "id": 60,
        "conditions": [
            "T3",
            "L2",
            "C2",
            "M1",
            "V1",
            "N4",
            "G3"
        ],
        "conclusion": "K25",
        "formula": "T3∧L2∧C2∧M1∧V1∧N4∧G3→K25",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Nikon Z fc."
    },
    {
        "id": 61,
        "conditions": [
            "T3",
            "L2",
            "C1",
            "M1",
            "V1",
            "N2",
            "G3"
        ],
        "conclusion": "K26",
        "formula": "T3∧L2∧C1∧M1∧V1∧N2∧G3→K26",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Nikon Z5."
    },
    {
        "id": 62,
        "conditions": [
            "T3",
            "L2",
            "C1",
            "M1",
            "V1",
            "N3",
            "G3"
        ],
        "conclusion": "K26",
        "formula": "T3∧L2∧C1∧M1∧V1∧N3∧G3→K26",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Nikon Z5."
    },
    {
        "id": 63,
        "conditions": [
            "T3",
            "L2",
            "C1",
            "M1",
            "V2",
            "N3",
            "G4"
        ],
        "conclusion": "K27",
        "formula": "T3∧L2∧C1∧M1∧V2∧N3∧G4→K27",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Nikon Z6 II."
    },
    {
        "id": 64,
        "conditions": [
            "T3",
            "L2",
            "C1",
            "M1",
            "V2",
            "N2",
            "G4"
        ],
        "conclusion": "K27",
        "formula": "T3∧L2∧C1∧M1∧V2∧N2∧G4→K27",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Nikon Z6 II."
    },
    {
        "id": 65,
        "conditions": [
            "T3",
            "L2",
            "C1",
            "M1",
            "V1",
            "N3",
            "G4"
        ],
        "conclusion": "K27",
        "formula": "T3∧L2∧C1∧M1∧V1∧N3∧G4→K27",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Nikon Z6 II."
    },
    {
        "id": 66,
        "conditions": [
            "T3",
            "L2",
            "C1",
            "M1",
            "V2",
            "N7",
            "G6"
        ],
        "conclusion": "K28",
        "formula": "T3∧L2∧C1∧M1∧V2∧N7∧G6→K28",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chụp Studio, thương mại với phân khúc giá từ 50 - 60 triệu đồng thì nên chọn Máy ảnh Nikon Z7 II."
    },
    {
        "id": 67,
        "conditions": [
            "T3",
            "L2",
            "C1",
            "M1",
            "V2",
            "N2",
            "G6"
        ],
        "conclusion": "K28",
        "formula": "T3∧L2∧C1∧M1∧V2∧N2∧G6→K28",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 50 - 60 triệu đồng thì nên chọn Máy ảnh Nikon Z7 II."
    },
    {
        "id": 68,
        "conditions": [
            "T3",
            "L2",
            "C1",
            "M1",
            "V3",
            "N6",
            "G9"
        ],
        "conclusion": "K29",
        "formula": "T3∧L2∧C1∧M1∧V3∧N6∧G9→K29",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Nikon Z8."
    },
    {
        "id": 69,
        "conditions": [
            "T3",
            "L2",
            "C1",
            "M1",
            "V3",
            "N5",
            "G9"
        ],
        "conclusion": "K29",
        "formula": "T3∧L2∧C1∧M1∧V3∧N5∧G9→K29",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích thể thao, tốc độ cao với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Nikon Z8."
    },
    {
        "id": 70,
        "conditions": [
            "T3",
            "L2",
            "C1",
            "M1",
            "V3",
            "N7",
            "G9"
        ],
        "conclusion": "K29",
        "formula": "T3∧L2∧C1∧M1∧V3∧N7∧G9→K29",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chụp Studio, thương mại với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Nikon Z8."
    },
    {
        "id": 71,
        "conditions": [
            "T3",
            "L2",
            "C1",
            "M1",
            "V3",
            "N5",
            "G9"
        ],
        "conclusion": "K30",
        "formula": "T3∧L2∧C1∧M1∧V3∧N5∧G9→K30",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích thể thao, tốc độ cao với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Nikon Z9."
    },
    {
        "id": 72,
        "conditions": [
            "T3",
            "L2",
            "C1",
            "M1",
            "V3",
            "N6",
            "G9"
        ],
        "conclusion": "K30",
        "formula": "T3∧L2∧C1∧M1∧V3∧N6∧G9→K30",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Nikon, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Nikon Z9."
    },
    {
        "id": 73,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V1",
            "N1",
            "G3"
        ],
        "conclusion": "K31",
        "formula": "T4∧L2∧C2∧M1∧V1∧N1∧G3→K31",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Fujifilm X-T30 II."
    },
    {
        "id": 74,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V1",
            "N2",
            "G3"
        ],
        "conclusion": "K31",
        "formula": "T4∧L2∧C2∧M1∧V1∧N2∧G3→K31",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Fujifilm X-T30 II."
    },
    {
        "id": 75,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V1",
            "N1",
            "G3"
        ],
        "conclusion": "K32",
        "formula": "T4∧L2∧C2∧M1∧V1∧N1∧G3→K32",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Fujifilm X-E4."
    },
    {
        "id": 76,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V1",
            "N3",
            "G3"
        ],
        "conclusion": "K33",
        "formula": "T4∧L2∧C2∧M1∧V1∧N3∧G3→K33",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Fujifilm X-S10."
    },
    {
        "id": 77,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V1",
            "N4",
            "G3"
        ],
        "conclusion": "K33",
        "formula": "T4∧L2∧C2∧M1∧V1∧N4∧G3→K33",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Fujifilm X-S10."
    },
    {
        "id": 78,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V3",
            "N4",
            "G4"
        ],
        "conclusion": "K34",
        "formula": "T4∧L2∧C2∧M1∧V3∧N4∧G4→K34",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Fujifilm X-S20."
    },
    {
        "id": 79,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V2",
            "N4",
            "G4"
        ],
        "conclusion": "K34",
        "formula": "T4∧L2∧C2∧M1∧V2∧N4∧G4→K34",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Fujifilm X-S20."
    },
    {
        "id": 80,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V3",
            "N3",
            "G4"
        ],
        "conclusion": "K34",
        "formula": "T4∧L2∧C2∧M1∧V3∧N3∧G4→K34",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Fujifilm X-S20."
    },
    {
        "id": 81,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V2",
            "N3",
            "G4"
        ],
        "conclusion": "K35",
        "formula": "T4∧L2∧C2∧M1∧V2∧N3∧G4→K35",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Fujifilm X-T4."
    },
    {
        "id": 82,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V2",
            "N6",
            "G4"
        ],
        "conclusion": "K35",
        "formula": "T4∧L2∧C2∧M1∧V2∧N6∧G4→K35",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Fujifilm X-T4."
    },
    {
        "id": 83,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V3",
            "N2",
            "G5"
        ],
        "conclusion": "K36",
        "formula": "T4∧L2∧C2∧M1∧V3∧N2∧G5→K36",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Fujifilm X-T5."
    },
    {
        "id": 84,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V3",
            "N1",
            "G5"
        ],
        "conclusion": "K36",
        "formula": "T4∧L2∧C2∧M1∧V3∧N1∧G5→K36",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Fujifilm X-T5."
    },
    {
        "id": 85,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V3",
            "N3",
            "G5"
        ],
        "conclusion": "K36",
        "formula": "T4∧L2∧C2∧M1∧V3∧N3∧G5→K36",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Fujifilm X-T5."
    },
    {
        "id": 86,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V3",
            "N7",
            "G5"
        ],
        "conclusion": "K37",
        "formula": "T4∧L2∧C2∧M1∧V3∧N7∧G5→K37",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chụp Studio, thương mại với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Fujifilm X-H2."
    },
    {
        "id": 87,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V3",
            "N6",
            "G5"
        ],
        "conclusion": "K37",
        "formula": "T4∧L2∧C2∧M1∧V3∧N6∧G5→K37",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Fujifilm X-H2."
    },
    {
        "id": 88,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V3",
            "N5",
            "G6"
        ],
        "conclusion": "K38",
        "formula": "T4∧L2∧C2∧M1∧V3∧N5∧G6→K38",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích thể thao, tốc độ cao với phân khúc giá từ 50 - 60 triệu đồng thì nên chọn Máy ảnh Fujifilm X-H2S."
    },
    {
        "id": 89,
        "conditions": [
            "T4",
            "L2",
            "C2",
            "M1",
            "V3",
            "N6",
            "G6"
        ],
        "conclusion": "K38",
        "formula": "T4∧L2∧C2∧M1∧V3∧N6∧G6→K38",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Crop (APS-C), có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 50 - 60 triệu đồng thì nên chọn Máy ảnh Fujifilm X-H2S."
    },
    {
        "id": 90,
        "conditions": [
            "T4",
            "L2",
            "C3",
            "M1",
            "V1",
            "N2",
            "G9"
        ],
        "conclusion": "K39",
        "formula": "T4∧L2∧C3∧M1∧V1∧N2∧G9→K39",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Medium Format, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích chân dung, phong cảnh với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Fujifilm GFX 50S II."
    },
    {
        "id": 91,
        "conditions": [
            "T4",
            "L2",
            "C3",
            "M1",
            "V1",
            "N7",
            "G9"
        ],
        "conclusion": "K39",
        "formula": "T4∧L2∧C3∧M1∧V1∧N7∧G9→K39",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Medium Format, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích chụp Studio, thương mại với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Fujifilm GFX 50S II."
    },
    {
        "id": 92,
        "conditions": [
            "T4",
            "L2",
            "C3",
            "M1",
            "V2",
            "N7",
            "G9"
        ],
        "conclusion": "K40",
        "formula": "T4∧L2∧C3∧M1∧V2∧N7∧G9→K40",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Medium Format, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chụp Studio, thương mại với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Fujifilm GFX 100S."
    },
    {
        "id": 93,
        "conditions": [
            "T4",
            "L2",
            "C3",
            "M1",
            "V2",
            "N2",
            "G9"
        ],
        "conclusion": "K40",
        "formula": "T4∧L2∧C3∧M1∧V2∧N2∧G9→K40",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Fujifilm, thuộc dòng máy Mirrorless, trang bị cảm biến Medium Format, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chân dung, phong cảnh với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Fujifilm GFX 100S."
    },
    {
        "id": 94,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V1",
            "N4",
            "G2"
        ],
        "conclusion": "K41",
        "formula": "T5∧L2∧C4∧M1∧V1∧N4∧G2→K41",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix G100."
    },
    {
        "id": 95,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V1",
            "N1",
            "G2"
        ],
        "conclusion": "K41",
        "formula": "T5∧L2∧C4∧M1∧V1∧N1∧G2→K41",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix G100."
    },
    {
        "id": 96,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V1",
            "N1",
            "G2"
        ],
        "conclusion": "K42",
        "formula": "T5∧L2∧C4∧M1∧V1∧N1∧G2→K42",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích cơ bản, du lịch, đường phố với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix G85."
    },
    {
        "id": 97,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V1",
            "N4",
            "G2"
        ],
        "conclusion": "K42",
        "formula": "T5∧L2∧C4∧M1∧V1∧N4∧G2→K42",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix G85."
    },
    {
        "id": 98,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V1",
            "N4",
            "G2"
        ],
        "conclusion": "K43",
        "formula": "T5∧L2∧C4∧M1∧V1∧N4∧G2→K43",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix G95."
    },
    {
        "id": 99,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V1",
            "N3",
            "G2"
        ],
        "conclusion": "K43",
        "formula": "T5∧L2∧C4∧M1∧V1∧N3∧G2→K43",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay cơ bản, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 10 - 20 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix G95."
    },
    {
        "id": 100,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V2",
            "N6",
            "G3"
        ],
        "conclusion": "K44",
        "formula": "T5∧L2∧C4∧M1∧V2∧N6∧G3→K44",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix GH5."
    },
    {
        "id": 101,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V2",
            "N3",
            "G3"
        ],
        "conclusion": "K44",
        "formula": "T5∧L2∧C4∧M1∧V2∧N3∧G3→K44",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 20 - 30 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix GH5."
    },
    {
        "id": 102,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V2",
            "N6",
            "G4"
        ],
        "conclusion": "K45",
        "formula": "T5∧L2∧C4∧M1∧V2∧N6∧G4→K45",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix GH5 II."
    },
    {
        "id": 103,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V2",
            "N4",
            "G4"
        ],
        "conclusion": "K45",
        "formula": "T5∧L2∧C4∧M1∧V2∧N4∧G4→K45",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích quay Vlog, sáng tạo nội dung với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix GH5 II."
    },
    {
        "id": 104,
        "conditions": [
            "T5",
            "L2",
            "C1",
            "M1",
            "V2",
            "N2",
            "G4"
        ],
        "conclusion": "K46",
        "formula": "T5∧L2∧C1∧M1∧V2∧N2∧G4→K46",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chân dung, phong cảnh với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix S5."
    },
    {
        "id": 105,
        "conditions": [
            "T5",
            "L2",
            "C1",
            "M1",
            "V2",
            "N6",
            "G4"
        ],
        "conclusion": "K46",
        "formula": "T5∧L2∧C1∧M1∧V2∧N6∧G4→K46",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix S5."
    },
    {
        "id": 106,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V3",
            "N6",
            "G4"
        ],
        "conclusion": "K47",
        "formula": "T5∧L2∧C4∧M1∧V3∧N6∧G4→K47",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix GH6."
    },
    {
        "id": 107,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V2",
            "N6",
            "G4"
        ],
        "conclusion": "K47",
        "formula": "T5∧L2∧C4∧M1∧V2∧N6∧G4→K47",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 30 - 40 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix GH6."
    },
    {
        "id": 108,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V3",
            "N5",
            "G5"
        ],
        "conclusion": "K48",
        "formula": "T5∧L2∧C4∧M1∧V3∧N5∧G5→K48",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích thể thao, tốc độ cao với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix G9 II."
    },
    {
        "id": 109,
        "conditions": [
            "T5",
            "L2",
            "C4",
            "M1",
            "V3",
            "N6",
            "G5"
        ],
        "conclusion": "K48",
        "formula": "T5∧L2∧C4∧M1∧V3∧N6∧G5→K48",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Micro Four Thirds / M43, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix G9 II."
    },
    {
        "id": 110,
        "conditions": [
            "T5",
            "L2",
            "C1",
            "M1",
            "V3",
            "N3",
            "G5"
        ],
        "conclusion": "K49",
        "formula": "T5∧L2∧C1∧M1∧V3∧N3∧G5→K49",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích đa dụng, sự kiện với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix S5 II."
    },
    {
        "id": 111,
        "conditions": [
            "T5",
            "L2",
            "C1",
            "M1",
            "V3",
            "N6",
            "G5"
        ],
        "conclusion": "K49",
        "formula": "T5∧L2∧C1∧M1∧V3∧N6∧G5→K49",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá từ 40 - 50 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix S5 II."
    },
    {
        "id": 112,
        "conditions": [
            "T5",
            "L2",
            "C1",
            "M1",
            "V3",
            "N6",
            "G9"
        ],
        "conclusion": "K50",
        "formula": "T5∧L2∧C1∧M1∧V3∧N6∧G9→K50",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay điện ảnh siêu nét, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix S1H."
    },
    {
        "id": 113,
        "conditions": [
            "T5",
            "L2",
            "C1",
            "M1",
            "V2",
            "N6",
            "G9"
        ],
        "conclusion": "K50",
        "formula": "T5∧L2∧C1∧M1∧V2∧N6∧G9→K50",
        "description": "Nếu bạn muốn chọn máy ảnh thương hiệu Panasonic, thuộc dòng máy Mirrorless, trang bị cảm biến Full-frame, có màn hình cảm ứng, khả năng quay nâng cao, phục vụ mục đích chuyên sản xuất Video, điện ảnh với phân khúc giá trên 80 triệu đồng thì nên chọn Máy ảnh Panasonic Lumix S1H."
    }
]


# ==============================================================================
# 4. MÁY SUY DIỄN TIẾN (FORWARD CHAINING INFERENCE ENGINE)
# ==============================================================================
class CameraExpertSystem:
    """
    Hệ chuyên gia tư vấn lựa chọn máy ảnh sử dụng thuật toán Suy diễn tiến
    (Forward Chaining) kết hợp Khả năng giải thích (Explanation Facility)
    và Khả năng thu nhận tri thức (Knowledge Acquisition).
    """

    def __init__(self, facts_meta, cameras, rules):
        self.facts_meta = facts_meta
        self.cameras = {c["id"]: c for c in cameras}
        self.rules = list(rules)
        self.fact_labels = {}
        self.fact_groups = {}
        for grp_code, grp_data in facts_meta.items():
            for f_code, f_label in grp_data["items"].items():
                self.fact_labels[f_code] = f_label
                self.fact_groups[f_code] = grp_data["name"]

    def get_fact_label(self, code):
        if code in self.fact_labels:
            return f"{code} ({self.fact_labels[code]})"
        if code in self.cameras:
            return f"{code} ({self.cameras[code]['name']})"
        return code

    def forward_chaining(self, selected_facts):
        """
        Thuật toán Suy diễn tiến (Forward Chaining):
        - Đầu vào: Tập sự kiện ban đầu trong Bộ nhớ làm việc (Working Memory).
        - Quá trình:
          1. Nạp các từ khóa sự kiện người dùng chọn vào Working Memory.
          2. Duyệt tập luật (RULES) để lập Lịch công việc (Agenda):
             + Luật khớp hoàn toàn (khi người dùng chọn đủ 7 tiêu chí và khớp 7/7,
               hoặc khi tập sự kiện người dùng chọn là tập con khớp 100% với luật).
             + Luật khớp một phần (xếp hạng theo số lượng sự kiện thỏa mãn).
          3. Kích hoạt luật ưu tiên cao nhất, bổ sung kết luận K_i vào Working Memory.
          4. Sinh lời giải thích tự động (Explanation) và vết suy diễn (Inference Trace).
        """
        working_memory = list(dict.fromkeys(selected_facts))
        selected_set = set(working_memory)

        # Phân nhóm các sự kiện người dùng đã chọn theo nhóm T, L, C, M, V, N, G
        selected_by_group = {}
        for f in working_memory:
            grp = f[0] if f else ""
            selected_by_group.setdefault(grp, []).append(f)

        inference_steps = []
        inference_steps.append({
            "step": 1,
            "title": "Khởi tạo Bộ nhớ làm việc (Working Memory)",
            "detail": (
                f"Tiếp nhận {len(working_memory)} sự kiện đầu vào từ người dùng: "
                + (", ".join(self.get_fact_label(f) for f in working_memory) if working_memory else "Chưa chọn sự kiện")
            ),
            "facts": list(working_memory)
        })

        exact_fired_rules = []
        subset_matched_rules = []
        partial_matched_rules = []

        for rule in self.rules:
            cond_set = set(rule["conditions"])
            matched_facts = [f for f in rule["conditions"] if f in selected_set]
            missing_facts = [f for f in rule["conditions"] if f not in selected_set]

            # Kiểm tra xem có nhóm nào người dùng đã chọn nhưng luật này không thỏa không
            group_conflict = False
            for grp, chosen_codes in selected_by_group.items():
                rule_code_in_grp = next((c for c in rule["conditions"] if c.startswith(grp)), None)
                if rule_code_in_grp not in chosen_codes:
                    group_conflict = True
                    break

            score = len(matched_facts) / len(rule["conditions"]) if rule["conditions"] else 0.0

            rule_eval = {
                "rule": rule,
                "matched_facts": matched_facts,
                "missing_facts": missing_facts,
                "match_count": len(matched_facts),
                "total_conditions": len(rule["conditions"]),
                "score": round(score * 100, 1),
                "group_conflict": group_conflict
            }

            if len(matched_facts) == len(rule["conditions"]) and not group_conflict:
                exact_fired_rules.append(rule_eval)
            elif not group_conflict and len(matched_facts) > 0:
                subset_matched_rules.append(rule_eval)
            elif len(matched_facts) > 0:
                partial_matched_rules.append(rule_eval)

        # Sắp xếp lịch công việc (Agenda)
        subset_matched_rules.sort(key=lambda x: (-x["match_count"], x["rule"]["id"]))
        partial_matched_rules.sort(key=lambda x: (-x["match_count"], x["rule"]["id"]))

        if exact_fired_rules:
            active_agenda = exact_fired_rules
            mode = "EXACT_MATCH"
            inference_steps.append({
                "step": 2,
                "title": "Lập Lịch công việc (Agenda) & Đối sánh Tập luật",
                "detail": (
                    f"Máy suy diễn tiến quét qua {len(self.rules)} luật và phát hiện "
                    f"{len(exact_fired_rules)} luật thỏa mãn tuyệt đối (100% điều kiện vế trái)."
                ),
                "facts": list(working_memory)
            })
        elif subset_matched_rules:
            active_agenda = subset_matched_rules
            mode = "SUBSET_MATCH"
            inference_steps.append({
                "step": 2,
                "title": "Lập Lịch công việc (Agenda) theo Tập từ khóa đã chọn",
                "detail": (
                    f"Người dùng chọn {len(working_memory)} từ khóa thuộc {len(selected_by_group)}/7 nhóm tiêu chí. "
                    f"Máy suy diễn lọc được {len(subset_matched_rules)} luật thỏa mãn toàn bộ các từ khóa đã chọn."
                ),
                "facts": list(working_memory)
            })
        else:
            active_agenda = partial_matched_rules[:10]
            mode = "PARTIAL_MATCH"
            inference_steps.append({
                "step": 2,
                "title": "Suy diễn xấp xỉ theo độ tương đồng (Partial Rule Matching)",
                "detail": (
                    "Tổ hợp từ khóa hiện tại không khớp tuyệt đối với một luật đơn lẻ. "
                    f"Hệ chuyên gia xếp hạng {len(active_agenda)} luật có số sự kiện thỏa mãn cao nhất."
                ),
                "facts": list(working_memory)
            })

        recommendations = []
        seen_cameras = set()

        for idx, item in enumerate(active_agenda):
            rule = item["rule"]
            cam_id = rule["conclusion"]
            cam = self.cameras.get(cam_id)
            if not cam:
                continue

            if cam_id not in working_memory:
                working_memory.append(cam_id)

            if idx < 5:
                inference_steps.append({
                    "step": len(inference_steps) + 1,
                    "title": f"Kích hoạt Luật #{rule['id']}: {rule['formula']}",
                    "detail": (
                        f"Luật #{rule['id']} thỏa mãn {item['match_count']}/{item['total_conditions']} sự kiện "
                        f"({', '.join(item['matched_facts'])}) → Suy ra kết luận {cam_id}: {cam['name']}."
                    ),
                    "facts": list(working_memory)
                })

            if cam_id not in seen_cameras:
                seen_cameras.add(cam_id)
                matched_desc = ", ".join(self.get_fact_label(f) for f in item["matched_facts"])
                explanation = (
                    f"Dựa trên nhu cầu của bạn ({(', '.join(self.fact_labels.get(f, f) for f in item['matched_facts']))}), MingDShop gợi ý {cam['name']} — mẫu máy ảnh rất phù hợp với tiêu chí và ngân sách bạn đã chọn."
                )
                recommendations.append({
                    "camera": cam,
                    "rule": rule,
                    "matched_facts": item["matched_facts"],
                    "missing_facts": item["missing_facts"],
                    "match_count": item["match_count"],
                    "total_conditions": item["total_conditions"],
                    "score": item["score"],
                    "mode": mode,
                    "explanation": explanation
                })

        return {
            "mode": mode,
            "selected_facts": selected_facts,
            "working_memory": working_memory,
            "inference_steps": inference_steps,
            "recommendations": recommendations,
            "total_rules_checked": len(self.rules)
        }

    def add_rule(self, conditions, conclusion, description=""):
        """Khả năng thu nhận tri thức (Knowledge Acquisition): Thêm luật mới."""
        new_id = len(self.rules) + 1
        formula = "∧".join(conditions) + "→" + conclusion
        if not description and conclusion in self.cameras:
            cam_name = self.cameras[conclusion]["name"]
            cond_names = ", ".join(self.fact_labels.get(c, c) for c in conditions)
            description = f"Nếu chọn ({cond_names}) thì nên chọn {cam_name}."
        new_rule = {
            "id": new_id,
            "conditions": conditions,
            "conclusion": conclusion,
            "formula": formula,
            "description": description
        }
        self.rules.append(new_rule)
        return new_rule


# Khởi tạo instance toàn cục của Hệ chuyên gia
expert_system = CameraExpertSystem(FACTS_META, CAMERAS, RULES)


# ==============================================================================
# 5. WEB SERVER & WSGI APP (TƯƠNG THÍCH GITHUB, RENDER, GUNICORN & LOCAL)
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def app(environ, start_response):
    """
    WSGI Application hỗ trợ chạy trực tiếp với Gunicorn trên Render:
      gunicorn main:app
    hoặc chạy trực tiếp bằng lệnh:
      python main.py
    """
    method = environ.get("REQUEST_METHOD", "GET").upper()
    path = environ.get("PATH_INFO", "/")

    cors_headers = [
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD"),
        ("Access-Control-Allow-Headers", "Content-Type, Accept"),
    ]

    if method == "OPTIONS":
        start_response("204 No Content", cors_headers)
        return [b""]

    if path in ("/", "/index.html"):
        html_path = os.path.join(BASE_DIR, "index.html")
        if os.path.exists(html_path):
            with open(html_path, "rb") as f:
                body = f.read()
            headers = [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(body)))] + cors_headers
            start_response("200 OK", headers)
            return [b""] if method == "HEAD" else [body]
        msg = "<h1>Không tìm thấy file index.html trong cùng thư mục!</h1>".encode("utf-8")
        headers = [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(msg)))] + cors_headers
        start_response("404 Not Found", headers)
        return [b""] if method == "HEAD" else [msg]

    if path in ("/api/health", "/healthz"):
        body = json.dumps({"status": "ok", "cameras": len(CAMERAS), "rules": len(RULES)}, ensure_ascii=False).encode("utf-8")
        headers = [("Content-Type", "application/json; charset=utf-8"), ("Content-Length", str(len(body)))] + cors_headers
        start_response("200 OK", headers)
        return [b""] if method == "HEAD" else [body]

    if path == "/api/kb":
        body = json.dumps({
            "facts_meta": expert_system.facts_meta,
            "cameras": list(expert_system.cameras.values()),
            "rules": expert_system.rules
        }, ensure_ascii=False).encode("utf-8")
        headers = [("Content-Type", "application/json; charset=utf-8"), ("Content-Length", str(len(body)))] + cors_headers
        start_response("200 OK", headers)
        return [b""] if method == "HEAD" else [body]

    if path == "/api/consult":
        if method == "POST":
            try:
                length = int(environ.get("CONTENT_LENGTH") or 0)
            except ValueError:
                length = 0
            raw = environ["wsgi.input"].read(length).decode("utf-8") if length > 0 else "{}"
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {}
            facts = payload.get("facts", [])
        else:
            facts = []
        result = expert_system.forward_chaining(facts)
        body = json.dumps(result, ensure_ascii=False).encode("utf-8")
        headers = [("Content-Type", "application/json; charset=utf-8"), ("Content-Length", str(len(body)))] + cors_headers
        start_response("200 OK", headers)
        return [body]

    if path == "/api/add-rule" and method == "POST":
        try:
            length = int(environ.get("CONTENT_LENGTH") or 0)
        except ValueError:
            length = 0
        raw = environ["wsgi.input"].read(length).decode("utf-8") if length > 0 else "{}"
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {}
        conditions = payload.get("conditions", [])
        conclusion = payload.get("conclusion", "K1")
        description = payload.get("description", "")
        new_rule = expert_system.add_rule(conditions, conclusion, description)
        body = json.dumps({"status": "ok", "rule": new_rule, "total_rules": len(expert_system.rules)}, ensure_ascii=False).encode("utf-8")
        headers = [("Content-Type", "application/json; charset=utf-8"), ("Content-Length", str(len(body)))] + cors_headers
        start_response("200 OK", headers)
        return [body]

    body = json.dumps({"error": "Endpoint not found"}, ensure_ascii=False).encode("utf-8")
    headers = [("Content-Type", "application/json; charset=utf-8"), ("Content-Length", str(len(body)))] + cors_headers
    start_response("404 Not Found", headers)
    return [body]


# Alias chuẩn cho các dịch vụ Cloud PaaS (Render / Gunicorn / uWSGI)
application = app


class ExpertSystemRequestHandler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Accept")
        self.end_headers()

    def do_HEAD(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html", "/api/health", "/healthz"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
        else:
            super().do_HEAD()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            html_path = os.path.join(BASE_DIR, "index.html")
            if os.path.exists(html_path):
                with open(html_path, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)
            else:
                msg = b"<h1>Khong tim thay file index.html trong cung thu muc!</h1>"
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(msg)))
                self.end_headers()
                self.wfile.write(msg)
        elif parsed.path in ("/api/health", "/healthz"):
            self._send_json({"status": "ok", "cameras": len(CAMERAS), "rules": len(RULES)})
        elif parsed.path == "/api/kb":
            self._send_json({
                "facts_meta": expert_system.facts_meta,
                "cameras": list(expert_system.cameras.values()),
                "rules": expert_system.rules
            })
        elif parsed.path == "/api/consult":
            self._send_json(expert_system.forward_chaining([]))
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        try:
            payload = json.loads(raw_body)
        except Exception:
            payload = {}

        if parsed.path == "/api/consult":
            facts = payload.get("facts", [])
            result = expert_system.forward_chaining(facts)
            self._send_json(result)
        elif parsed.path == "/api/add-rule":
            conditions = payload.get("conditions", [])
            conclusion = payload.get("conclusion", "K1")
            description = payload.get("description", "")
            new_rule = expert_system.add_rule(conditions, conclusion, description)
            self._send_json({"status": "ok", "rule": new_rule, "total_rules": len(expert_system.rules)})
        else:
            self._send_json({"error": "Endpoint not found"}, status=404)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Accept")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[ExpertSystem Server] {self.address_string()} - {fmt % args}")


def run_cli_demo():
    """Chế độ kiểm thử nhanh trên dòng lệnh (CLI)"""
    print("=" * 72)
    print("HỆ CHUYÊN GIA TƯ VẤN LỰA CHỌN MÁY ẢNH - NHÓM 22 (ĐH ĐỒNG THÁP)")
    print(f"Tổng số máy ảnh: {len(CAMERAS)} (K1 - K50) | Tổng số luật: {len(RULES)} (R1 - R113)")
    print("=" * 72)
    sample_facts = ["T1", "L2", "C2", "M1", "V1", "N4", "G2"]
    print("Thử nghiệm suy diễn tiến với tập sự kiện:", " ∧ ".join(sample_facts))
    res = expert_system.forward_chaining(sample_facts)
    for step in res["inference_steps"]:
        print(f"  [Bước {step['step']}] {step['title']}: {step['detail']}")
    print("-" * 72)
    for rec in res["recommendations"]:
        print(f"=> KẾT LUẬN: {rec['camera']['name']} ({rec['camera']['id']}) - Giá: {rec['camera']['price_text']}")
        print(f"   Giải thích: {rec['explanation']}")


if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli_demo()
    else:
        port = int(os.environ.get("PORT", 8000))
        server = ThreadingHTTPServer(("0.0.0.0", port), ExpertSystemRequestHandler)
        url = f"http://localhost:{port}"
        print("=" * 72)
        print("MINGDSHOP CAMERA AI - HỆ CHUYÊN GIA TƯ VẤN MÁY ẢNH (NHÓM 22 - ĐH ĐỒNG THÁP)")
        print(f"Server đang chạy tại: {url} (0.0.0.0:{port})")
        print("Nhấn Ctrl+C để dừng Server.")
        print("=" * 72)
        if not os.environ.get("RENDER") and not os.environ.get("PORT"):
            try:
                webbrowser.open(url)
            except Exception:
                pass
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã dừng Server.")
            server.server_close()
