# Model Results — DS108 Validation Framework

Generated: 2026-06-02 17:08

## MAE (MW)

| run                            |   Central |   National |   North |   South |
|:-------------------------------|----------:|-----------:|--------:|--------:|
| Naive (lag48)                  |     319.9 |     2149.1 |  1003.9 |  1205.5 |
| Linear Regression (no weather) |     269.2 |     1592   |   854   |   821.6 |
| RF (no weather)                |     261   |     1087.1 |   769.3 |   512.9 |
| RF (with weather)              |     257   |     1045.3 |   685.5 |   510   |

## RMSE (MW)

| run                            |   Central |   National |   North |   South |
|:-------------------------------|----------:|-----------:|--------:|--------:|
| Naive (lag48)                  |     452.3 |     3142.8 |  1439.2 |  1772.6 |
| Linear Regression (no weather) |     375.3 |     2216.4 |  1174.4 |  1134.5 |
| RF (no weather)                |     361.4 |     1580.2 |  1098.4 |   730.1 |
| RF (with weather)              |     359.1 |     1501.8 |   960.8 |   727.5 |

## Cải thiện MAE: RF (with weather) vs Naive (lag48)

- Central: +19.7%
- National: +51.4%
- North: +31.7%
- South: +57.7%

## Đóng góp weather features: RF-withW vs RF-noW

- Central: +1.5%
- National: +3.8%
- North: +10.9%
- South: +0.6%

## Sanity Check

Consistency MAE (pred_National vs sum pred_3 miền): 526.0 MW
Số điểm kiểm tra: 10,455