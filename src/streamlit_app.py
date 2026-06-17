"""
DS108 — EDA Interactive Dashboard
Phụ tải điện Việt Nam 2023–2026

Chạy: streamlit run streamlit_app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import os

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DS108 · EDA Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── THEME COLORS (RGB Part) ──────────────────────────────────────────────────
C = {
    "bac": "rgb(55, 138, 221)",  # #378ADD
    "trung": "rgb(216, 90, 48)",  # #D85A30
    "nam": "rgb(29, 158, 117)",  # #1D9E75
    "qg": "rgb(127, 119, 221)",  # #7F77DD
    "grid": "rgba(128,128,128,0.1)",
    "bg": "rgb(250, 250, 250)",
    "red": "rgb(200, 50, 50)",
}

MIEN_COLORS = [C["bac"], C["trung"], C["nam"], C["qg"]]
MIEN_NAMES = ["Bắc", "Trung", "Nam", "Quốc gia"]
MIEN_MAP = {"Bắc": "North", "Trung": "Central", "Nam": "South", "Quốc gia": "National"}

HOURS = list(range(24))
DAYS_VN = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
MONTHS_VN = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12"]


# ─── LOAD DATA ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load real dataset từ file cùng thư mục."""
    # Đường dẫn tuyệt đối đến file CSV
    data_path = "../data/processed/final_v1_dataset.csv"

    if not os.path.exists(data_path):
        st.error(f"❌ Không tìm thấy file: {data_path}")
        st.stop()

    df = pd.read_csv(data_path, parse_dates=["Timestamp"])

    # Tạo thêm các cột hỗ trợ cho EDA
    df["hour"] = df["Timestamp"].dt.hour
    df["dayofweek"] = df["Timestamp"].dt.dayofweek
    df["month"] = df["Timestamp"].dt.month
    df["dayofweek_vn"] = df["dayofweek"].map(
        {0: "T2", 1: "T3", 2: "T4", 3: "T5", 4: "T6", 5: "T7", 6: "CN"}
    )
    df["month_vn"] = df["month"].map(
        {
            1: "T1",
            2: "T2",
            3: "T3",
            4: "T4",
            5: "T5",
            6: "T6",
            7: "T7",
            8: "T8",
            9: "T9",
            10: "T10",
            11: "T11",
            12: "T12",
        }
    )
    return df


df = load_data()


# ─── HELPERS ──────────────────────────────────────────────────────────────────
def peak_shade(fig, row=1, col=1):
    for zone in [(9, 11.5), (17, 20)]:
        fig.add_vrect(
            x0=zone[0],
            x1=zone[1],
            fillcolor="rgba(29,158,117,0.12)",
            line_width=0,
            row=row,
            col=col,
        )


def fig_layout(fig, title="", xlab="", ylab=""):
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color="rgb(51, 51, 51)"), x=0),
        xaxis_title=xlab,
        yaxis_title=ylab,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="sans-serif", size=12, color="rgb(68, 68, 68)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=20, t=60, b=40),
        height=360,
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(128,128,128,0.1)", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(128,128,128,0.1)", zeroline=False)
    return fig


def compute_mape(df, y_true, y_pred):
    """Tính MAPE cho validation."""
    return np.mean(np.abs((df[y_true] - df[y_pred]) / df[y_true])) * 100


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ DS108 Dashboard")
    st.markdown("**Đồ án cuối kỳ · UIT 2026**")
    st.markdown("La Gia Hân · 24520448  \nHuỳnh Gia Hào · 24520457")
    st.divider()
    st.markdown("### Dataset")
    st.metric("Tổng mẫu", f"{len(df):,}")
    st.metric("Đặc trưng", f"{len(df.columns)} cột")
    st.metric(
        "Giai đoạn", f"{df['Timestamp'].min().date()} → {df['Timestamp'].max().date()}"
    )
    st.metric("Tần suất", "30 phút")
    st.divider()
    st.markdown("### Anti-Leakage")
    st.success("✅ Lớp 1: Scaling params")
    st.success("✅ Lớp 2: Price exclusion")
    st.success("✅ Lớp 3: Rolling shift(1)")
    st.divider()
    st.markdown("### Kết quả tốt nhất")
    st.metric("RF · Quốc gia MAPE", "2.9%", delta="-60% vs Naive")
    st.metric("RF · Nam MAPE", "3.4%", delta="-58% vs Naive")
    st.markdown("---")
    st.caption("GitHub: kicky-33/DS108-Project")

# ─── MAIN HEADER ──────────────────────────────────────────────────────────────
st.title("⚡ EDA Dashboard — Phụ tải điện Việt Nam 2023–2026")
st.caption(
    "Dữ liệu thật · Pipeline DS108 · Medallion Architecture · 9 Notebooks · 3 lớp Anti-Leakage"
)

# ─── TOP METRICS ──────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Mẫu", f"{len(df):,}", "sau drop lag t-336")
c2.metric("Cột", f"{len(df.columns)}", "time+lag+weather")
c3.metric("Notebooks", "9", "end-to-end")
c4.metric("Anti-leakage", "3 lớp", "độc lập")
c5.metric("MAPE tốt nhất", "2.9%", "RF · Quốc gia")
c6.metric("vs. Naive", "-60%", "Quốc gia")

st.divider()

# ─── TABS ─────────────────────────────────────────────────────────────────────
tabs = st.tabs(
    [
        "📈 Daily Pattern",
        "📅 Weekly Pattern",
        "🌡 Seasonal Pattern",
        "🔥 Load–Nhiệt độ",
        "✅ Validation",
        "🕐 Multi-Horizon",
        "🌦 Weather Signal",
        "📋 Dataset Summary",
    ]
)

# ══════════════════════════════════════════════════════════════════
# TAB 1 — DAILY PATTERN
# ══════════════════════════════════════════════════════════════════
with tabs[0]:
    st.subheader("Daily Pattern — Phụ tải trung bình theo giờ")
    col_ctrl, col_info = st.columns([3, 1])
    with col_ctrl:
        mien_d = st.selectbox("Chọn miền", ["Bắc", "Trung", "Nam"], key="d_mien")
        show_we = st.toggle("Hiện cuối tuần", value=True, key="d_we")
    with col_info:
        st.info("**Justify is_peak:** Đỉnh 9–11h30 và 17–20h theo QĐ 648/QĐ-BCT")

    load_col = f"Load_{MIEN_MAP[mien_d]}"

    weekday_mean = df[df["dayofweek"] < 5].groupby("hour")[load_col].mean()
    weekend_mean = df[df["dayofweek"] >= 5].groupby("hour")[load_col].mean()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=HOURS,
            y=weekday_mean.values,
            name="Ngày thường",
            line=dict(color=C["bac"], width=2.5),
            fill="tozeroy",
            fillcolor="rgba(55, 138, 221, 0.15)",
        )
    )
    if show_we:
        fig.add_trace(
            go.Scatter(
                x=HOURS,
                y=weekend_mean.values,
                name="Cuối tuần",
                line=dict(color=C["trung"], width=2, dash="dash"),
            )
        )
    peak_shade(fig)
    fig.add_annotation(
        x=10.25,
        y=max(weekday_mean.values) * 0.97,
        text="Cao điểm sáng",
        showarrow=False,
        font=dict(size=11, color="rgb(15, 110, 86)"),
        bgcolor="rgba(255,255,255,0.7)",
    )
    fig.add_annotation(
        x=18.5,
        y=max(weekday_mean.values) * 0.97,
        text="Cao điểm chiều",
        showarrow=False,
        font=dict(size=11, color="rgb(15, 110, 86)"),
        bgcolor="rgba(255,255,255,0.7)",
    )
    fig_layout(
        fig,
        f"Daily Pattern — {mien_d} (từ dữ liệu thật)",
        "Giờ trong ngày",
        "Phụ tải (MW)",
    )
    fig.update_xaxes(tickmode="linear", dtick=2)
    st.plotly_chart(fig, use_container_width=True)

    diff = (weekday_mean.mean() - weekend_mean.mean()) / weekend_mean.mean() * 100
    st.success(
        f"📌 **Insight:** {mien_d} — ngày thường cao hơn cuối tuần **{diff:.1f}%** → justify `is_weekend` và `lag336`."
    )

# ══════════════════════════════════════════════════════════════════
# TAB 2 — WEEKLY PATTERN
# ══════════════════════════════════════════════════════════════════
with tabs[1]:
    st.subheader("Weekly Pattern — Phụ tải trung bình theo thứ")

    weekly_data = {}
    for mien, eng in MIEN_MAP.items():
        load_col = f"Load_{eng}"
        weekly_data[mien] = (
            df.groupby("dayofweek_vn")[load_col].mean().reindex(DAYS_VN).values
        )

    fig = go.Figure()
    for i, (mien, color) in enumerate(zip(["Bắc", "Trung", "Nam"], MIEN_COLORS)):
        fig.add_trace(
            go.Bar(
                x=DAYS_VN,
                y=weekly_data[mien],
                name=mien,
                marker_color=color,
                opacity=0.85,
            )
        )
    fig.add_vrect(x0=4.5, x1=6.5, fillcolor="rgba(200,0,0,0.06)", line_width=0)
    fig.add_annotation(
        x=5.5,
        y=max(weekly_data["Bắc"]) * 1.02,
        text="Cuối tuần",
        showarrow=False,
        font=dict(size=11, color="rgb(153, 60, 29)"),
    )
    fig_layout(fig, "Weekly Pattern — 3 miền (từ dữ liệu thật)", "Thứ", "Phụ tải (MW)")
    fig.update_layout(barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns(2)
    col_a.warning(
        "⚠️ **Bẫy cuối tuần (lag48):** Model dự báo Thứ Hai nhìn vào Chủ Nhật — phụ tải thấp bất thường → bị kéo sai."
    )
    col_b.success(
        "✅ **Fix với lag336:** `shift(336)` = đúng 1 tuần → tham chiếu cùng giờ, cùng thứ."
    )

# ══════════════════════════════════════════════════════════════════
# TAB 3 — SEASONAL PATTERN
# ══════════════════════════════════════════════════════════════════
with tabs[2]:
    st.subheader("Seasonal Pattern — Phụ tải trung bình theo tháng")

    seasonal_data = {}
    for mien, eng in MIEN_MAP.items():
        load_col = f"Load_{eng}"
        seasonal_data[mien] = (
            df.groupby("month_vn")[load_col].mean().reindex(MONTHS_VN).values
        )

    fig = go.Figure()
    for mien, color in zip(["Bắc", "Trung", "Nam"], MIEN_COLORS):
        fig.add_trace(
            go.Scatter(
                x=MONTHS_VN,
                y=seasonal_data[mien],
                name=mien,
                line=dict(color=color, width=2.5),
                mode="lines+markers",
                marker=dict(size=6),
            )
        )
    fig_layout(
        fig,
        "Seasonal Pattern — So sánh 3 miền (từ dữ liệu thật)",
        "Tháng",
        "Phụ tải (MW)",
    )
    st.plotly_chart(fig, use_container_width=True)

    bac_range = max(seasonal_data["Bắc"]) - min(seasonal_data["Bắc"])
    nam_range = max(seasonal_data["Nam"]) - min(seasonal_data["Nam"])

    ca, cb, cc = st.columns(3)
    ca.metric("Biên độ mùa vụ — Bắc", f"{bac_range:.0f} MW", "Lớn nhất 3 miền")
    cb.metric(
        "Biên độ mùa vụ — Trung",
        f"{max(seasonal_data['Trung'])-min(seasonal_data['Trung']):.0f} MW",
    )
    cc.metric("Biên độ mùa vụ — Nam", f"{nam_range:.0f} MW", "Gần phẳng quanh năm")

    st.info(
        f"📌 **Justify month + 3 model độc lập:** Bắc dao động ≈ **{bac_range:.0f} MW** giữa hè và đông. Nam chỉ ≈ **{nam_range:.0f} MW** — gần như phẳng. → 1 model chung không phản ánh đặc tính riêng từng miền."
    )

# ══════════════════════════════════════════════════════════════════
# TAB 4 — LOAD–TEMPERATURE
# ══════════════════════════════════════════════════════════════════
with tabs[3]:
    st.subheader("Quan hệ Load – Nhiệt độ (U-shape)")
    mien_lt = st.selectbox("Chọn miền", ["Bắc", "Trung", "Nam"], key="lt_mien")

    eng = MIEN_MAP[mien_lt]
    temp_col = f"temp_{eng}"
    load_col = f"Load_{eng}"

    df_lt = df[[temp_col, load_col]].dropna()

    if len(df_lt) > 10:
        xs = df_lt[temp_col].values
        ys = df_lt[load_col].values

        # Linear fit
        lr = LinearRegression().fit(xs.reshape(-1, 1), ys)
        r2_linear = lr.score(xs.reshape(-1, 1), ys)

        # Poly2 fit
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(xs.reshape(-1, 1))
        lr_poly = LinearRegression().fit(X_poly, ys)
        r2_poly = lr_poly.score(X_poly, ys)

        # Generate curves
        xs_dense = np.linspace(xs.min(), xs.max(), 200)
        y_lin = lr.predict(xs_dense.reshape(-1, 1))
        y_poly = lr_poly.predict(poly.transform(xs_dense.reshape(-1, 1)))

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="markers",
                name="Dữ liệu thật",
                marker=dict(
                    color="rgba(136, 135, 128, 0.5)",
                    size=6,
                    line=dict(width=0.5, color="rgb(85, 85, 85)"),
                ),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=xs_dense,
                y=y_lin,
                mode="lines",
                name=f"Linear (R²={r2_linear:.3f})",
                line=dict(color=C["bac"], width=2),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=xs_dense,
                y=y_poly,
                mode="lines",
                name=f"Poly2 (R²={r2_poly:.3f})",
                line=dict(color=C["trung"], width=2.5, dash="dash"),
            )
        )
        fig_layout(
            fig,
            f"Load vs. Nhiệt độ — {mien_lt} (từ dữ liệu thật)",
            "Nhiệt độ (°C)",
            "Phụ tải (MW)",
        )
        st.plotly_chart(fig, use_container_width=True)

        imp = (r2_poly - r2_linear) / r2_linear * 100 if r2_linear > 0 else 0
        st.success(
            f"📌 **Quan hệ U-shape xác nhận — {mien_lt}:** R² linear = **{r2_linear:.3f}** → R² poly2 = **{r2_poly:.3f}** → Cải thiện **+{imp:.1f}%** → Feature **temp²** có giá trị."
        )
    else:
        st.warning("Không đủ dữ liệu để phân tích.")

# ══════════════════════════════════════════════════════════════════
# TAB 5 — VALIDATION
# ══════════════════════════════════════════════════════════════════
with tabs[4]:
    st.subheader("Validation Framework — MAPE (%) theo kịch bản")

    MAPE_DATA = pd.DataFrame(
        {
            "Kịch bản": [
                "Naive (lag48)",
                "Linear Reg.",
                "RF (no weather)",
                "RF (with weather)",
            ],
            "Bắc": [6.6, 5.1, 4.5, 4.0],
            "Trung": [12.0, 8.3, 8.1, 8.0],
            "Nam": [8.1, 5.6, 3.5, 3.4],
            "Quốc gia": [7.2, 4.6, 3.1, 2.9],
        }
    )

    col_t, col_c = st.columns([1, 1])
    with col_t:
        st.markdown("**Bảng kết quả MAPE (%)**")
        st.dataframe(
            MAPE_DATA.style.highlight_min(
                subset=["Bắc", "Trung", "Nam", "Quốc gia"],
                color="rgb(234, 243, 222)",
                axis=0,
            ).format({c: "{:.1f}%" for c in ["Bắc", "Trung", "Nam", "Quốc gia"]}),
            use_container_width=True,
            hide_index=True,
        )
        naive = MAPE_DATA[MAPE_DATA["Kịch bản"] == "Naive (lag48)"].iloc[0]
        best = MAPE_DATA[MAPE_DATA["Kịch bản"] == "RF (with weather)"].iloc[0]
        st.success(
            f"**Cải thiện RF vs. Naive:** Bắc: **{round((best['Bắc']-naive['Bắc'])/naive['Bắc']*100)}%** · Trung: **{round((best['Trung']-naive['Trung'])/naive['Trung']*100)}%** · Nam: **{round((best['Nam']-naive['Nam'])/naive['Nam']*100)}%** · QG: **{round((best['Quốc gia']-naive['Quốc gia'])/naive['Quốc gia']*100)}%**"
        )

    with col_c:
        fig = go.Figure()
        palette = [
            "rgba(136,135,128,0.3)",
            "rgb(181,212,244)",
            "rgba(55,138,221,0.5)",
            "rgb(24,95,165)",
        ]
        for i, (scen, color) in enumerate(zip(MAPE_DATA["Kịch bản"], palette)):
            row = MAPE_DATA.iloc[i]
            fig.add_trace(
                go.Bar(
                    name=scen,
                    x=["Bắc", "Trung", "Nam", "Quốc gia"],
                    y=[row["Bắc"], row["Trung"], row["Nam"], row["Quốc gia"]],
                    marker_color=color,
                )
            )
        fig_layout(fig, "MAPE (%) — 4 kịch bản × 4 miền", "Miền", "MAPE (%)")
        fig.update_layout(barmode="group", height=340)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("**Feature Importance — Phát hiện lag1 leakage**")
    col_fi, col_note = st.columns([1, 1])
    with col_fi:
        fi_labels = [
            "lag1",
            "rolling_mean_48",
            "lag48",
            "lag336",
            "temp",
            "hour",
            "is_peak",
            "is_weekend",
            "month",
        ]
        fi_values = [96.5, 1.8, 0.7, 0.4, 0.2, 0.15, 0.1, 0.08, 0.07]
        fig_fi = go.Figure(
            go.Bar(
                x=fi_values,
                y=fi_labels,
                orientation="h",
                marker_color=[
                    C["trung"] if l == "lag1" else C["bac"] for l in fi_labels
                ],
            )
        )
        fig_fi.update_layout(
            height=300,
            margin=dict(l=120, r=20, t=30, b=30),
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title="Feature importance (%)",
        )
        fig_fi.update_xaxes(showgrid=True, gridcolor="rgba(128,128,128,0.1)")
        st.plotly_chart(fig_fi, use_container_width=True)
    with col_note:
        st.warning(
            "⚠️ lag1 chiếm 96.5% importance → Inference Leakage\n\n"
            "lag1 = Load tại t-1. Trong dataset có sẵn nên model dùng để dự báo Load_{t} — nhưng khi inference thực tế (dự báo t+1), Load_t chưa tồn tại nên không thể dùng lag1 làm feature.\n\n"
            "✅ Quyết định của pipeline: lag1 được giữ lại trong dataset để đảm bảo minh bạch và tái lập, nhưng hoàn toàn bị loại khỏi feature set khi training ở NB08. MAPE tăng từ ~2% lên 4% — đó là năng lực thực của model."
        )
        st.success(
            "✅ **Sanity check:** Load_National = Σ(3 miền) 100% chính xác → National là tổng hợp tính toán. Consistency MAE = 526 MW."
        )

# ══════════════════════════════════════════════════════════════════
# TAB 6 — MULTI-HORIZON
# ══════════════════════════════════════════════════════════════════
with tabs[5]:
    st.subheader("Multi-Horizon Validation — MAE theo horizon (NB09)")

    HZ_LABELS = ["30m", "1h", "2h", "3h", "6h", "9h", "12h", "15h", "18h", "24h"]
    HZ_RF = {
        "Bắc": [744, 806, 820, 825, 877, 980, 1083, 1210, 1348, 1041],
        "Trung": [261, 266, 272, 281, 297, 290, 294, 300, 311, 310],
        "Nam": [526, 538, 542, 550, 558, 580, 612, 665, 715, 730],
        "Quốc gia": [1172, 1257, 1265, 1274, 1198, 1310, 1440, 1560, 1685, 1672],
    }
    HZ_NAIVE = {
        "Bắc": [1200, 1350, 1500, 1600, 1800, 2000, 2200, 2500, 2800, 2600],
        "Trung": [500, 550, 600, 620, 670, 680, 700, 710, 720, 700],
        "Nam": [900, 950, 1000, 1050, 1100, 1200, 1350, 1450, 1550, 1600],
        "Quốc gia": [2200, 2400, 2600, 2800, 3000, 3200, 3500, 3700, 3900, 3800],
    }

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        mien_hz = st.selectbox("Chọn miền", MIEN_NAMES, key="hz_mien")
    with col_h2:
        show_naive_hz = st.toggle("Hiện Naive baseline", value=True, key="hz_naive")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=HZ_LABELS,
            y=HZ_RF[mien_hz],
            name="RF with weather",
            line=dict(color=C["bac"], width=2.5),
            fill="tozeroy",
            fillcolor="rgba(55, 138, 221, 0.15)",
            mode="lines+markers",
            marker=dict(size=7),
        )
    )
    if show_naive_hz:
        fig.add_trace(
            go.Scatter(
                x=HZ_LABELS,
                y=HZ_NAIVE[mien_hz],
                name="Naive (lag48)",
                line=dict(color="rgb(136, 135, 128)", width=1.5, dash="dash"),
                mode="lines+markers",
                marker=dict(size=5),
            )
        )
    fig.add_vrect(
        x0=-0.5,
        x1=3.5,
        fillcolor="rgba(29,158,117,0.08)",
        line_width=0,
        annotation_text="Sweet spot",
        annotation_position="top left",
        annotation_font_color="rgb(15, 110, 86)",
    )
    fig_layout(
        fig,
        f"MAE theo horizon — {mien_hz} (từ dữ liệu thật)",
        "Forecast Horizon",
        "MAE (MW)",
    )
    fig.update_layout(height=380)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**MAE (MW) — Tất cả miền**")
    df_hz = pd.DataFrame(HZ_RF, index=HZ_LABELS).T.reset_index()
    df_hz.columns = ["Miền"] + HZ_LABELS
    st.dataframe(df_hz, use_container_width=True, hide_index=True)
    st.caption(
        "† Bắc h=24h (1041 MW) < h=18h (1348 MW): daily periodicity alignment — không phải lỗi model."
    )

# ══════════════════════════════════════════════════════════════════
# TAB 7 — WEATHER SIGNAL
# ══════════════════════════════════════════════════════════════════
with tabs[6]:
    st.subheader(
        "Weather Signal Isolation — Đóng góp thực của weather (NB08 Section 6b)"
    )

    WEATHER_CONTRIB = pd.DataFrame(
        {
            "Miền": ["Bắc", "Trung", "Nam", "Quốc gia"],
            "MAPE Time only (%)": [11.2, 12.7, 7.0, 8.7],
            "Đóng góp weather (%)": [-0.1, 2.0, -0.0, 4.5],
        }
    )

    col_wa, col_wb = st.columns([1, 1])
    with col_wa:
        fig_w = go.Figure()
        fig_w.add_trace(
            go.Bar(
                x=WEATHER_CONTRIB["Miền"],
                y=WEATHER_CONTRIB["MAPE Time only (%)"],
                name="Time only (no lag, no weather)",
                marker_color="rgba(127, 119, 221, 0.6)",
            )
        )
        fig_w.add_trace(
            go.Bar(
                x=WEATHER_CONTRIB["Miền"],
                y=[v if v > 0 else 0 for v in WEATHER_CONTRIB["Đóng góp weather (%)"]],
                name="Đóng góp weather (+)",
                marker_color=C["nam"],
            )
        )
        fig_w.add_trace(
            go.Bar(
                x=WEATHER_CONTRIB["Miền"],
                y=[
                    abs(v) if v < 0 else 0
                    for v in WEATHER_CONTRIB["Đóng góp weather (%)"]
                ],
                name="Đóng góp weather (−)",
                marker_color="rgba(216, 90, 48, 0.5)",
            )
        )
        fig_layout(
            fig_w, "Đóng góp Weather khi không có lag (Run 6b)", "Miền", "MAPE (%)"
        )
        fig_w.update_layout(barmode="stack", height=340)
        st.plotly_chart(fig_w, use_container_width=True)

    with col_wb:
        st.markdown("**Bảng kết quả Weather Signal Isolation**")
        st.dataframe(WEATHER_CONTRIB, use_container_width=True, hide_index=True)
        st.warning(
            "⚠️ **Phát hiện quan trọng:** Bắc và Nam — hai miền phụ tải lớn nhất — weather actual cho đóng góp **gần bằng 0** (−0.1% và −0.0%) ngay cả khi không có lag. → Giới hạn đến từ **bản chất bài toán**, không phải từ số lượng trạm khí tượng."
        )
        st.info(
            "**Hướng cải thiện:** 1. `temp²` để capture U-shape · 2. NWP weather forecast cho horizon >6h · 3. Gridded data ERA5"
        )

# ══════════════════════════════════════════════════════════════════
# TAB 8 — DATASET SUMMARY
# ══════════════════════════════════════════════════════════════════
with tabs[7]:
    st.subheader("Dataset Summary — Tổng quan bộ dữ liệu")

    col_p, col_q = st.columns(2)
    with col_p:
        st.markdown("**Pipeline Medallion Architecture**")
        pipeline_data = {
            "Notebook": [
                "NB01",
                "NB02",
                "NB03",
                "NB04",
                "NB05",
                "NB06",
                "NB07",
                "NB08",
                "NB09",
            ],
            "Tên": [
                "crawl_nsmo",
                "crawl_weather",
                "merging_eda",
                "cleaning",
                "integration",
                "normalization",
                "eda",
                "validation",
                "multi_horizon",
            ],
            "Output": [
                "27 batch CSV",
                "27×3 thành phố",
                "*_raw_merged.csv",
                "*_v1_clean.csv",
                "unified (52,608×42)",
                "final (52,272×64)",
                "EDA reports",
                "model_results",
                "horizon_results",
            ],
            "Trạng thái": ["✅"] * 9,
        }
        st.dataframe(
            pd.DataFrame(pipeline_data), use_container_width=True, hide_index=True
        )

    with col_q:
        st.markdown("**Feature Groups — 64 cột**")
        feat_data = {
            "Nhóm": [
                "Time/Boolean",
                "Load gốc + scaled",
                "Lag/Rolling",
                "Weather",
                "Price (loại)",
            ],
            "Số cột": [6, 8, 12, 33, 4],
        }
        fig_feat = go.Figure(
            go.Pie(
                labels=feat_data["Nhóm"],
                values=feat_data["Số cột"],
                hole=0.45,
                marker_colors=[
                    C["bac"],
                    C["trung"],
                    C["nam"],
                    C["qg"],
                    "rgb(136, 135, 128)",
                ],
            )
        )
        fig_feat.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=20, b=0),
            showlegend=True,
            paper_bgcolor="white",
        )
        st.plotly_chart(fig_feat, use_container_width=True)
        st.caption("* lag1 giữ trong dataset, loại khỏi training (inference leakage).")

    st.markdown("---")
    st.markdown("**Anti-Leakage — 3 lớp độc lập**")
    cla, clb, clc = st.columns(3)
    cla.error(
        "**Lớp 1 — Scaling:** Scaler params fit chỉ trên Train (80%). Lưu `scaler_params.json` (24 entries). NB08/09 chỉ load JSON."
    )
    clb.error(
        "**Lớp 2 — Price:** Price_t và Load_t xác định đồng thời trong VCGM. Dùng Price_t làm feature = future leakage. → Loại toàn bộ 4 cột Price."
    )
    clc.error(
        "**Lớp 3 — Rolling:** `rolling_mean_48` dùng `shift(1)` trước `.rolling(48).mean()` → cửa sổ [t-48, t-1]. Không shift → cửa sổ chứa t → leakage tinh vi."
    )

st.divider()
st.caption(
    "DS108 · Đồ án cuối kỳ · Trường ĐH Công nghệ Thông tin - ĐHQG TP.HCM · 2026  \nLa Gia Hân (24520448) · Huỳnh Gia Hào (24520457)  \nGitHub: [kicky-33/DS108-Project](https://github.com/kicky-33/DS108-Project)"
)
