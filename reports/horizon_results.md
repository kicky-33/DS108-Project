# NB09 — Multi-Horizon Validation Results

**Nhom:** La Gia Han (24520448) · Huynh Gia Hao (24520457)
**Dataset:** final_v1_dataset.csv — 52,272 dong x 104 cot

## MAE (MW) theo Horizon

| Region | 30m | 1h | 2h | 3h | 4h | 6h | 8h | 12h | 18h | 24h |
|---|---|---|---|---|---|---|---|---|---|---|
| North | 743.6 | 805.7 | 828.6 | 825.4 | 871.0 | 877.5 | 947.7 | 1083.4 | 1348.6 | 1040.4 |
| Central | 260.9 | 266.3 | 272.6 | 280.8 | 284.3 | 296.5 | 294.5 | 293.7 | 310.9 | 309.3 |
| South | 525.5 | 537.8 | 541.8 | 549.6 | 546.3 | 557.9 | 567.8 | 612.3 | 714.7 | 729.6 |
| National | 1171.6 | 1257.5 | 1216.6 | 1274.2 | 1292.4 | 1197.9 | 1244.6 | 1439.9 | 1684.5 | 1671.3 |

## MAPE (%) theo Horizon

| Region | 30m | 1h | 2h | 3h | 4h | 6h | 8h | 12h | 18h | 24h |
|---|---|---|---|---|---|---|---|---|---|---|
| North | 4.26 | 4.56 | 4.66 | 4.62 | 4.85 | 4.91 | 5.32 | 6.10 | 7.57 | 6.12 |
| Central | 7.99 | 8.12 | 8.27 | 8.50 | 8.59 | 8.92 | 8.87 | 8.87 | 9.39 | 9.35 |
| South | 3.50 | 3.60 | 3.65 | 3.67 | 3.65 | 3.73 | 3.77 | 4.13 | 4.96 | 5.15 |
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