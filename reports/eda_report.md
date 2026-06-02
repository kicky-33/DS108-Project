# EDA Report — DS108 NB07
**Nhom:** La Gia Han (24520448) . Huynh Gia Hao (24520457)
**Moc:** 2023-03-11 00:30 -> 2026-03-10 23:30

---

## 1. Thong ke mo ta

### Load (MW)
                   mean       50%      std    cv%  min       max      iqr  skew
Load_North     16589.55  16566.60  3144.57  18.96  0.0  29048.42  4219.00  0.05
Load_Central    3473.34   3471.40   653.27  18.81  0.0   7871.79   919.61  0.08
Load_South     15276.49  15331.92  2577.89  16.87  0.0  22670.70  3785.00 -0.29
Load_National  35339.24  35596.60  5759.11  16.30  0.0  55580.70  8340.55 -0.24

### Price (d/kWh)
                  mean     50%     std  min     max  zero_rate%  spike_rate%  skew
Price_North     726.96  870.81  727.35  0.0  1778.6       39.79          0.0  0.19
Price_Central   499.21    0.95  655.25  0.0  1778.6       49.12          0.0  0.76
Price_South     583.40    1.00  671.07  0.0  1778.6       39.35          0.0  0.50
Price_National  835.65  968.24  710.85  0.0  1778.6       28.41          0.0 -0.09

### So sanh truoc/sau xu ly
               missing_before  missing_after  mean_before  mean_after  std_before  std_after  delta_mean%  delta_std%
Load_North                  0              0     16589.50    16589.55     3144.56    3144.57        0.000       0.000
Load_Central                0              0      3473.32     3473.34      653.27     653.27        0.001       0.000
Load_South                  0              0     15276.50    15276.49     2577.86    2577.89       -0.000       0.001
Load_National               0              0     35339.19    35339.24     5759.07    5759.11        0.000       0.001

---

## 2. Phan phoi (Univariate)
- Load: co the bimodal, skewness duong
- Price: lech phai manh -> justify Z-score scaling

---

## 3. Tuong quan Load-Temperature
| Mien | R2(linear) | R2(poly2) | Cai thien |
|---|---|---|---|
| Miền Bắc | 0.273 | 0.310 | +13.4% |
| Miền Trung | 0.138 | 0.142 | +2.7% |
| Miền Nam | 0.261 | 0.269 | +2.9% |

---

## 4. Time Series Patterns
- Daily: 2 dinh cao diem sang & chieu -> justify hour, is_peak
- Weekly: ngay thuong > cuoi tuan -> justify is_weekend
- Seasonal: Bac bien do lon nhat -> justify month
- Holiday: ngay le thap hon ro ret -> justify is_holiday

---

## 5. So sanh 3 mien
             Miền Bắc  Miền Trung  Miền Nam
Mean (MW)     16589.5      3473.3   15276.5
Median (MW)   16566.6      3471.4   15331.9
Std (MW)       3144.6       653.3    2577.9
IQR (MW)       4219.0       919.6    3785.0
Min (MW)          0.0         0.0       0.0
Max (MW)      29048.4      7871.8   22670.7
CV%              19.0        18.8      16.9

---

## 6. Bieu do da luu (reports/eda_after/)
- hist_load.png . hist_price.png
- scatter_load_temp.png . heatmap_load_features.png
- daily_pattern.png . weekly_pattern.png . seasonal_pattern.png
- holiday_effect.png . boxplot_3mien.png . price_spike_timeline.png
