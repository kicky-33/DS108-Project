# DS108-Project: Dự báo Phụ tải Điện Việt Nam (STLF)

Dự án thu thập và tiền xử lý dữ liệu phụ tải điện từ NSMO và dữ liệu khí tượng từ Visual Crossing để xây dựng bộ dữ liệu chuẩn cho bài toán dự báo phụ tải ngắn hạn.

## 🚀 Hướng dẫn chạy Code (A-Z)

Để tái lập toàn bộ bộ dữ liệu, hãy chạy các notebook trong thư mục `notebooks/` theo thứ tự sau:

### Giai đoạn 1: Thu thập dữ liệu (Data Collection)
1. `01_crawl_nsmo.ipynb`: Thu thập Load & Price từ API NSMO $\to$ lưu vào `data/raw/NSMO/`.
2. `02_crawl_weather.ipynb`: Thu thập Weather từ Visual Crossing API $\to$ lưu vào `data/raw/Weather_*_Raw/`.

### Giai đoạn 2: Tiền xử lý (Data Preprocessing)
3. `03_merging_and_initial_eda.ipynb`: Gộp các file batch, kiểm tra gap và EDA sơ bộ $\to$ `*_raw_merged.csv`.
4. `04_cleaning.ipynb`: Xử lý missing, outlier, duplicate cho từng nguồn $\to$ `*_v1_clean.csv`.
5. `05_integration.ipynb`: Nội suy weather 1h $\to$ 30min và merge với NSMO $\to$ `unified_v1_merged.csv`.
6. `06_normalization.ipynb`: Tạo lag/rolling features và Scaling (Min-Max/Z-score) $\to$ `final_v1_dataset.csv`.

### Giai đoạn 3: Phân tích & Xác thực (Analysis & Validation)
7. `07_eda.ipynb`: EDA toàn diện sau xử lý, phân tích tương quan phi tuyến Load-Temp $\to$ `eda_report.md`.
8. `08_validation.ipynb`: Chia Train/Test, chạy 4 model độc lập để đánh giá chất lượng dataset $\to$ `model_results.md`.
9. `09_multi_horizon_validation.ipynb`: Xác thực đa tầm dự báo bằng phương pháp Direct Multi-Step Forecasting $\to$ `horizon_results.md`.

---

## 📁 Cấu trúc Thư mục
```
DS108-Project/
├── data/
│   ├── raw/                  # Dữ liệu thô gốc (Immutable)
│   │   ├── NSMO/             # Batch CSV từ NSMO
│   │   └── Weather_*_Raw/    # Batch CSV từ Visual Crossing
│   └── processed/            # Thành phẩm sau mỗi bước xử lý
├── notebooks/                # Toàn bộ pipeline (01 to 08)
├── reports/                  # Báo cáo EDA và Validation
├── src/                      # Scripts bổ trợ (utils, crawlers)
├── requirements.txt          # Thư viện cần thiết
└── README.md                 # File này
```

## 🛠️ Yêu cầu Kỹ thuật
- **Ngôn ngữ:** Python 3.10+
- **Thư viện chính:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`
- **Cài đặt:** `pip install -r requirements.txt`

## ⚠️ Lưu ý quan trọng cho Reviewer
- **Data Leakage:** Toàn bộ tham số Scaling và Imputation được tính toán trên tập **Train** và áp dụng cho tập **Test** để đảm bảo tính khách quan của mô hình.
- **Feature Engineering:** Sử dụng `lag336` và `rolling_mean_48` để bắt đặc tính mùa vụ tuần và mức nền 24h.
- **Mốc dữ liệu:** Dataset cuối cùng bắt đầu từ `2023-03-18 00:30:00`.
- **Tầm dự báo (Multi-Horizon):** Qua thực nghiệm chứng minh, mô hình Random Forest (RF) kết hợp biến thời tiết chiến thắng Naive baseline (lag48) một cách nhất quán ở toàn bộ 40 tổ hợp cấu hình từ 30 phút ($h=1$) đến 24 giờ ($h=48$), giúp giảm sai số MAE từ 19% đến 59%. Toàn bộ phạm vi 1–24h được chứng minh là cửa sổ dự báo hợp lệ và có giá trị thực tiễn cao cho bài toán STLF.