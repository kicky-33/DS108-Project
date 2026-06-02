# DATA CODEBOOK — DS108 Đồ Án Tiền Xử Lý Dữ Liệu

**Nhóm:** La Gia Hân (24520448) · Huỳnh Gia Hào (24520457)  
**Giai đoạn:** 2023-03-11 → 2026-03-10  
**Cập nhật:** 05/2026

---

## Nguồn 1 — NSMO (nsmo.vn)

**Mô tả:** Dữ liệu vận hành hệ thống điện quốc gia — phụ tải và giá biên theo 3 miền và toàn hệ thống.  
**Thu thập:** Reverse engineering API `GetChartPhuTaiVM` và `GetChartGiaBienVM`, crawl tự động bằng Python.  
**Tần suất:** 30 phút/mẫu  
**Thư mục:** `data/raw/NSMO/`  
**Số file batch:** 27 file (mỗi file ~40 ngày)  
**Tổng dòng ước tính:** ~52,704 dòng (3 năm × 365 ngày × 48 chu kỳ)

### Bảng mô tả cột

| Cột | Kiểu | Đơn vị | Mô tả | Miền giá trị (mẫu) |
|---|---|---|---|---|
| `Timestamp` | datetime | — | Mốc thời gian kết thúc chu kỳ 30 phút, UTC+7 | 2023-03-11T00:30:00 |
| `Load_North` | float64 | MW | Phụ tải tiêu thụ miền Bắc | ~9,800 – 28,000 |
| `Load_Central` | float64 | MW | Phụ tải tiêu thụ miền Trung | ~1,800 – 6,000 |
| `Load_South` | float64 | MW | Phụ tải tiêu thụ miền Nam | ~10,000 – 26,000 |
| `Load_National` | float64 | MW | Tổng phụ tải toàn hệ thống | ~25,000 – 55,000 |
| `Price_North` | float64 | đ/kWh | Giá biên hệ thống miền Bắc | 0 – 3,500 |
| `Price_Central` | float64 | đ/kWh | Giá biên hệ thống miền Trung | 0 – 3,500 |
| `Price_South` | float64 | đ/kWh | Giá biên hệ thống miền Nam | 0 – 3,500 |
| `Price_National` | float64 | đ/kWh | Giá biên toàn hệ thống (bình quân) | 0 – 3,500 |

### Lưu ý kỹ thuật
- Giá trị 0 trong cột Price không phải lỗi — xảy ra khi thừa công suất (giá biên = 0 là hợp lệ trong thị trường điện).
- Timestamp bắt đầu từ `00:30:00` mỗi ngày, không phải `00:00:00`.
- Một số ngày lễ hoặc sự cố server có thể thiếu vài chu kỳ → xử lý ở notebook 04.

---

## Nguồn 2 — Visual Crossing API

**Mô tả:** Dữ liệu khí tượng lịch sử theo giờ cho 3 thành phố đại diện 3 miền.  
**Thu thập:** Visual Crossing Weather API, kỹ thuật xoay vòng API key (40 ngày/key).  
**Tần suất:** 1 giờ/mẫu  
**Mapping địa lý:**

| Thành phố | Đại diện miền | Thư mục |
|---|---|---|
| Hà Nội | Miền Bắc | `data/raw/Weather_Hanoi_Raw/` |
| Đà Nẵng | Miền Trung | `data/raw/Weather_DaNang_Raw/` |
| TP.HCM | Miền Nam | `data/raw/Weather_TPHCM_Raw/` |

**Số file batch mỗi thành phố:** 27 file  
**Tổng dòng mỗi thành phố ước tính:** ~26,304 dòng (3 năm × 365 ngày × 24 giờ)

### Bảng mô tả cột

| Cột | Kiểu | Đơn vị | Mô tả | Ghi chú |
|---|---|---|---|---|
| `name` | str | — | Tên địa điểm | Drop trước khi merge |
| `datetime` | datetime | — | Mốc thời gian theo giờ, UTC+7 | Key để merge |
| `temp` | float64 | °C | Nhiệt độ không khí | Feature chính |
| `feelslike` | float64 | °C | Nhiệt độ cảm nhận | Có thể dùng thay temp |
| `dew` | float64 | °C | Điểm sương | Liên quan humidity |
| `humidity` | float64 | % | Độ ẩm tương đối | 0–100 |
| `precip` | float64 | mm | Lượng mưa | Thường = 0, spike khi mưa |
| `precipprob` | int64 | % | Xác suất có mưa | 0–100 |
| `preciptype` | str | — | Loại kết tủa (rain/snow/...) | **Categorical** → forward fill |
| `snow` | int64 | cm | Lượng tuyết | Luôn = 0 tại VN |
| `snowdepth` | int64 | cm | Độ sâu tuyết | Luôn = 0 tại VN |
| `windgust` | float64 | km/h | Tốc độ gió giật | Có thể missing |
| `windspeed` | float64 | km/h | Tốc độ gió trung bình | — |
| `winddir` | float64 | độ | Hướng gió (0–360) | — |
| `sealevelpressure` | float64 | hPa | Áp suất khí quyển mực nước biển | — |
| `cloudcover` | float64 | % | Độ che phủ mây | 0–100 |
| `visibility` | float64 | km | Tầm nhìn xa | — |
| `solarradiation` | float64 | W/m² | Bức xạ mặt trời | = 0 ban đêm |
| `solarenergy` | float64 | MJ/m² | Năng lượng mặt trời tích lũy | Tính từ solarradiation |
| `uvindex` | int64 | — | Chỉ số UV | 0–10 |
| `severerisk` | float64 | % | Rủi ro thời tiết khắc nghiệt | Thường missing |
| `conditions` | str | — | Mô tả thời tiết tổng quát | **Categorical** → forward fill |
| `icon` | str | — | Icon thời tiết (partly-cloudy-day...) | **Categorical** → forward fill |
| `stations` | str | — | Trạm khí tượng nguồn | Drop trước khi merge |

### Cột giữ lại sau khi làm sạch (dùng trong unified dataset)
```
datetime, temp, feelslike, humidity, precip, precipprob,
windspeed, cloudcover, solarradiation, uvindex, conditions, icon
```

### Cột drop (không có giá trị phân tích)
```
name, stations, snow, snowdepth, severerisk,
dew, windgust, winddir, sealevelpressure, visibility, solarenergy, preciptype
```

---

## Cột sau khi rename (unified_v1_merged.csv)

Sau bước integration, tên cột weather được thêm hậu tố miền:

| Tên gốc | Sau rename Bắc | Sau rename Trung | Sau rename Nam |
|---|---|---|---|
| `temp` | `temp_North` | `temp_Central` | `temp_South` |
| `humidity` | `humidity_North` | `humidity_Central` | `humidity_South` |
| `precip` | `precip_North` | `precip_Central` | `precip_South` |
| `cloudcover` | `cloudcover_North` | `cloudcover_Central` | `cloudcover_South` |
| `solarradiation` | `solarradiation_North` | `solarradiation_Central` | `solarradiation_South` |
| `uvindex` | `uvindex_North` | `uvindex_Central` | `uvindex_South` |
| `conditions` | `conditions_North` | `conditions_Central` | `conditions_South` |

---

## Feature Engineering (final_v1_dataset.csv)

### Time & Boolean Features

| Cột mới | Kiểu | Mô tả | Cách tính |
|---|---|---|---|
| `hour` | int | Giờ trong ngày | `Timestamp.dt.hour` |
| `dayofweek` | int | Thứ trong tuần (0=Thứ 2) | `Timestamp.dt.dayofweek` |
| `month` | int | Tháng | `Timestamp.dt.month` |
| `is_peak` | int {0,1} | Giờ cao điểm (QĐ 648/QĐ-BCT) | 9h–11h30 và 17h–20h |
| `is_weekend` | int {0,1} | Cuối tuần | dayofweek >= 5 |
| `is_holiday` | int {0,1} | Ngày lễ Việt Nam | Theo danh sách ngày lễ cố định |

### Lag & Rolling Features

| Cột mới | Kiểu | Mô tả | Cách tính | Lý do |
|---|---|---|---|---|
| `Load_*_lag1` | float64 | Load 30 phút trước | `shift(1)` | Quán tính ngắn hạn |
| `Load_*_lag48` | float64 | Load cùng giờ hôm qua | `shift(48)` | Daily seasonality |
| `Load_*_lag336` | float64 | Load cùng giờ tuần trước | `shift(336)` | Weekly seasonality — giải quyết bẫy ngày cuối tuần |
| `Load_*_rolling_mean_48` | float64 | Trung bình 24 giờ trước | `shift(1).rolling(48).mean()` | Mức nền phụ tải — bắt xu hướng dài hạn |

*(4 cột × 4 loại = 16 lag/rolling features, áp dụng cho North, Central, South, National)*

**Lưu ý data leakage:** `rolling_mean_48` dùng `shift(1)` trước `.rolling()` để cửa sổ tính là `[t-48, t-1]`, không bao gồm `t` hiện tại.

**Lưu ý drop dòng:** 336 dòng đầu bị drop do lag t-336 → mốc bắt đầu thực tế: `2023-03-18 00:30:00`

---

## Scaling (final_v1_dataset.csv)

| Nhóm cột | Phương pháp | Lý do |
|---|---|---|
| Load (gốc + lag1 + lag48 + lag336 + rolling) | Min-Max → [0, 1] | Phân phối bounded, ổn định, ít spike |
| Price | Z-score (mean=0, std=1) | Phân phối lệch phải, có spike 0 và 3,500 đ/kWh |
| Weather numeric | Không scale | Tree-based models không cần scale |
| Time & boolean | Không scale | Đã trong khoảng nhỏ hoặc nhị phân |

Params lưu tại: `data/processed/scaler_params.json`
