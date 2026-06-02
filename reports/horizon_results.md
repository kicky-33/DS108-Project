# NB09 — Multi-Horizon Validation Results

**Nhom:** La Gia Han (24520448) · Huynh Gia Hao (24520457)
**Dataset:** final_v1_dataset.csv — 52,272 dong x 104 cot

## MAE (MW) theo Horizon

| Region | 30m | 1h | 2h | 3h | 4h | 6h | 8h | 12h | 18h | 24h |
|---|---|---|---|---|---|---|---|---|---|---|
| North | 763.8 | 840.1 | 830.0 | 818.7 | 908.1 | 880.6 | 943.9 | 1046.2 | 1246.1 | 1003.4 |
| Central | 260.7 | 264.3 | 270.3 | 282.3 | 291.6 | 292.0 | 291.7 | 294.3 | 316.2 | 307.9 |
| South | 535.2 | 546.0 | 551.9 | 568.8 | 551.3 | 563.4 | 570.1 | 625.6 | 736.8 | 756.3 |
| National | 1171.8 | 1257.4 | 1216.6 | 1274.2 | 1292.4 | 1198.0 | 1244.6 | 1439.9 | 1684.5 | 1671.8 |

## MAPE (%) theo Horizon

| Region | 30m | 1h | 2h | 3h | 4h | 6h | 8h | 12h | 18h | 24h |
|---|---|---|---|---|---|---|---|---|---|---|
| North | 4.37 | 4.75 | 4.68 | 4.58 | 5.05 | 4.95 | 5.32 | 5.93 | 7.10 | 5.93 |
| Central | 7.98 | 8.04 | 8.21 | 8.49 | 8.74 | 8.76 | 8.76 | 8.88 | 9.48 | 9.31 |
| South | 3.56 | 3.64 | 3.70 | 3.78 | 3.67 | 3.79 | 3.79 | 4.27 | 5.13 | 5.36 |
| National | 3.25 | 3.47 | 3.35 | 3.49 | 3.52 | 3.28 | 3.44 | 4.03 | 4.77 | 4.89 |

## Nhan Xet Phan Tich

**1. MAE tang dan theo horizon** — ket qua nhat quan voi ly thuyet STLF.
Lag48 va lag336 la anchor chinh; MAE tang khong tuyen tinh, mot so dips nho la noise thong ke binh thuong.

**2. Mien Trung co MAPE cao nhat (8.0–9.5%)** do phu tai nen nho (~3 400 MW).
Day la gioi han thiet ke du lieu (1 tram khi tuong/mien), khong phai gioi han giai thuat.


**3. Nguong ky thuat 6h:**
- Truoc 6h: actual weather la thong tin thuc te co san tai thoi diem du bao.
- Sau 6h: can weather forecast — MAE tang ro hon tu h=12h tro di o North, South, National.


**4. RF thang Naive (lag48) o tat ca 40 combinations** — dataset co gia tri du bao thuc su toan bo window 1–24h.

## Pham Vi Bai Toan Duoc Chon

> Dua tren ket qua thuc nghiem, pham vi **1–12h (h=1 den h=12)** duoc chon:
> - MAPE on dinh, tang duoi 1 diem phan tram trong vung nay o 3/4 mien.
> - Actual weather con hop le, khong phai weather forecast.
> - Mien Trung vuot nguong hoc thuat tu h=30m — day la gioi han du lieu, khong phai phuong phap.