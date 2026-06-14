# Model Results — DS108 Validation Framework

Generated: 2026-06-11 11:23

## MAPE (%)

| run                            |   North |   Central |   South |   National |
|:-------------------------------|--------:|----------:|--------:|-----------:|
| Naive (lag48)                  |     6.6 |      12   |     8.1 |        7.2 |
| Linear Regression (no weather) |     5.1 |       8.3 |     5.6 |        4.6 |
| RF (no weather)                |     4.5 |       8.1 |     3.5 |        3.1 |
| RF (with weather)              |     4   |       8   |     3.4 |        2.9 |

## RMSE (MW)

| run                            |   North |   Central |   South |   National |
|:-------------------------------|--------:|----------:|--------:|-----------:|
| Naive (lag48)                  |  1531.7 |     524.7 |  1772.6 |     3391.5 |
| Linear Regression (no weather) |  1174.4 |     375.3 |  1134.5 |     2216.4 |
| RF (no weather)                |  1098.6 |     361.5 |   730.1 |     1580.1 |
| RF (with weather)              |   960.7 |     359   |   727.5 |     1501.8 |

## Cải thiện MAPE: RF (with weather) vs Naive (lag48)

- North: +39.9%
- Central: +33.6%
- South: +57.7%
- National: +59.2%

## Đóng góp weather features: RF-withW vs RF-noW

- North: +11.6%
- Central: +1.2%
- South: +1.3%
- National: +5.2%

## Sanity Check

Consistency MAE (pred_National vs sum pred_3 miền): 526.1 MW
Số điểm kiểm tra: 10,455