import streamlit as st
import pandas as pd
import sqlite3
import datetime as dt
import base64
from pathlib import Path
import plotly.express as px

st.set_page_config(
    page_title="Mumbai Local Train Analytics",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data" / "cleaned" / "timetables_cleaned.csv"
DB_FILE = BASE_DIR / "data" / "mumbai_local.db"
HERO_IMG_PATH = BASE_DIR / "image" / "mumbai_train.png"

LINE_NAMES = {
    "CR": "Central Railway",
    "WR": "Western Railway",
    "HR": "Harbour Line",
    "TH": "Trans-Harbour",
    "PL": "Port Line",
}

NAV_ITEMS = [
    ("Overview", ""),
    ("Train Operations", ""),
    ("Route Intelligence", ""),
    ("Station Analysis", ""),
    ("Travel Performance", ""),
    ("SQL Insights", ""),
    ("Data Explorer", ""),
]

GREENS = ["#1f4d3a", "#3d7a56", "#6fa383", "#a8c9a8", "#dcb45a"]


# ------------------------------------------------------------------
# styling
# ------------------------------------------------------------------

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

:root{
  --bg:#f7f4ea; --surface:#ffffff; --border:#e7e1d0;
  --ink:#152018; --ink-soft:#5b6459; --muted:#8b8d7f;
  --forest:#1f4d3a; --forest-deep:#123024; --sage:#dfeadd; --sage-soft:#eef3e7;
  --gold:#c99a3f; --gold-soft:#f8ecd2;
  --shadow:0 6px 20px rgba(20,35,25,.06);
}

.stApp{background:var(--bg);color:var(--ink);font-family:'DM Sans',sans-serif}
.block-container{padding:1.1rem 2rem 2rem;max-width:1450px}

section[data-testid="stSidebar"]{background:#fdfcf8;border-right:1px solid var(--border)}
section[data-testid="stSidebar"]>div{padding-top:1.2rem}
.brand{display:flex;align-items:center;gap:11px;padding:4px 8px 22px;font-size:22px}
.brand-title{font-size:21px;font-weight:800;color:var(--forest-deep);line-height:1.05}
.brand-sub{font-size:13px;color:var(--forest);font-weight:600;margin-top:3px}

section[data-testid="stSidebar"] div[role="radiogroup"] label{padding:11px 14px;border-radius:11px;margin:3px 0;width:100%;transition:background .15s ease}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{background:var(--sage-soft)}
section[data-testid="stSidebar"] div[role="radiogroup"] label>div:first-child{display:none}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){background:var(--forest);box-shadow:var(--shadow)}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{color:#fff!important;font-weight:700}
section[data-testid="stSidebar"] div[role="radiogroup"] p{font-size:14px;color:#2b382d}

div[data-testid="stExpander"]{border:1px solid var(--border);border-radius:14px;background:var(--surface)}

.hero{background:linear-gradient(135deg,#f0ede0 0%,#e8ecdf 100%);border:1px solid var(--border);border-radius:24px;padding:34px 38px;display:flex;justify-content:space-between;align-items:center;gap:28px;margin:6px 0 22px;overflow:hidden}
.hero-title{font-family:'Playfair Display',Georgia,serif;font-size:46px;font-weight:700;color:var(--forest-deep);line-height:1.08;letter-spacing:-.5px}
.hero-sub{font-size:15px;color:var(--ink-soft);margin-top:13px;max-width:520px;line-height:1.55}
.hero-tag{font-size:12px;color:var(--forest);margin-top:15px;font-weight:700;letter-spacing:.02em}
.hero-img{border-radius:18px;height:230px;object-fit:cover;width:430px;box-shadow:0 12px 34px rgba(18,48,36,.18)}

.kpi-card{background:var(--surface);border:1px solid var(--border);border-radius:18px;padding:16px 17px;min-height:130px;box-shadow:var(--shadow);transition:transform .15s ease,box-shadow .15s ease}
.kpi-card:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(20,35,25,.10)}
.kpi-icon{width:38px;height:38px;border-radius:12px;background:var(--sage);color:var(--forest);display:flex;align-items:center;justify-content:center;font-size:17px;margin-bottom:10px}
.kpi-label{font-size:10px;letter-spacing:.09em;color:var(--muted);font-weight:800}
.kpi-value{font-size:25px;font-weight:800;color:var(--forest-deep);margin-top:4px}
.kpi-note{font-size:11px;color:var(--forest);opacity:.8;margin-top:4px}

.panel,.info-card{background:var(--surface);border:1px solid var(--border);border-radius:18px;box-shadow:var(--shadow)}
.panel{padding:20px 21px;margin-bottom:20px}
.panel-title{font-size:16px;font-weight:700;color:var(--forest-deep);margin-bottom:10px}
.info-card{padding:17px 18px;min-height:100px}
.info-title{font-weight:700;color:var(--forest-deep);font-size:14px;margin-bottom:5px}
.info-text{font-size:12px;color:var(--ink-soft);line-height:1.45}

.route-row{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid #f1eee2}
.route-row:last-child{border-bottom:0}
.route-num{width:25px;height:25px;border-radius:8px;background:var(--sage);color:var(--forest);font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center}
.route-name{flex:1;font-size:13px;color:var(--ink);font-weight:600}
.route-count{font-size:12px;color:var(--forest);font-weight:700}

.section-heading{font-size:25px;font-weight:800;color:var(--forest-deep);margin:8px 0 18px;letter-spacing:-.3px}
.note-box{background:var(--gold-soft);border-left:4px solid var(--gold);border-radius:10px;padding:12px 16px;color:#5e4620;font-size:13px;margin-top:14px}
.footer{text-align:center;color:var(--muted);font-size:11px;padding:30px 0 5px}

div[data-baseweb="select"]>div,div[data-baseweb="input"]>div{border-color:var(--border)!important;border-radius:10px!important;background:var(--surface)!important}
div[data-baseweb="tag"]{background:var(--forest)!important}
button[kind="secondary"]{border-radius:10px!important;border-color:var(--border)!important;color:var(--forest-deep)!important}
button[kind="secondary"]:hover{border-color:var(--forest)!important;color:var(--forest)!important}
.stDownloadButton button{width:100%;border-radius:10px;background:var(--forest)!important;color:#fff!important;border:none!important}
.stDownloadButton button:hover{background:var(--forest-deep)!important}

@media(max-width:900px){
  .block-container{padding-left:1rem;padding-right:1rem}
  .hero{padding:25px;align-items:flex-start}
  .hero-title{font-size:36px}
  .hero-img{width:340px;height:190px}
}
</style>
""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------
# data loading
# ------------------------------------------------------------------


@st.cache_data
def load_data():
    df = pd.read_csv(CSV_FILE)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    for col in [
        "distance_km",
        "train_no",
        "cars",
        "travel_time_minutes",
        "departure_hour",
        "departure_minute",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "departure_time" in df.columns:
        df["departure_time"] = pd.to_datetime(
            df["departure_time"], format="%H:%M", errors="coerce"
        )
    if "arrival_time" in df.columns:
        df["arrival_time"] = pd.to_datetime(
            df["arrival_time"], format="%H:%M", errors="coerce"
        )

    if "route" not in df.columns:
        df["route"] = (
            df["from_station"].astype(str) + " → " + df["to_station"].astype(str)
        )

    return df


@st.cache_data
def load_sql(query):
    conn = sqlite3.connect(DB_FILE)
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result


@st.cache_data
def load_hero_image():
    if HERO_IMG_PATH.exists():
        return base64.b64encode(HERO_IMG_PATH.read_bytes()).decode()
    return None


hero_b64 = load_hero_image()
hero_img_html = (
    f'<img class="hero-img" src="data:image/png;base64,{hero_b64}">'
    if hero_b64
    else '<div class="hero-img" style="display:flex;align-items:center;justify-content:center;'
    'background:#e3e0d5;color:#667066;">🚆 Mumbai Local Train</div>'
)


try:
    df = load_data()
except Exception as e:
    st.error("Unable to load cleaned dataset.")
    st.code(str(e))
    st.stop()

lines = sorted(df["line"].dropna().unique())
train_types = sorted(df["train_type"].dropna().unique())
origins = sorted(df["origin"].dropna().unique())
destinations = sorted(df["destination"].dropna().unique())


# ------------------------------------------------------------------
# sidebar - brand, nav, filters
# ------------------------------------------------------------------

with st.sidebar:
    st.markdown(
        '<div class="brand">🚆<div><div class="brand-title">Mumbai Rail</div>'
        '<div class="brand-sub">Analytics</div></div></div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "nav",
        [f"{icon}  {name}" for name, icon in NAV_ITEMS],
        label_visibility="collapsed",
    )
    page = page.split("  ", 1)[1]

    with st.expander("🎛️ Filters", expanded=True):
        if "filter_reset" not in st.session_state:
            st.session_state.filter_reset = 0
        selected_lines = st.multiselect(
            "Railway Line",
            lines,
            default=lines,
            key=f"lines_{st.session_state.filter_reset}",
        )
        selected_types = st.multiselect(
            "Train Type",
            train_types,
            default=train_types,
            key=f"types_{st.session_state.filter_reset}",
        )
        selected_origins = st.multiselect(
            "Origin",
            origins,
            default=origins,
            key=f"origins_{st.session_state.filter_reset}",
        )
        selected_destinations = st.multiselect(
            "Destination",
            destinations,
            default=destinations,
            key=f"destinations_{st.session_state.filter_reset}",
        )
        if st.button("↻ Reset all filters", width="stretch"):
            st.session_state.filter_reset += 1
            st.rerun()

filtered_df = df.copy()
if selected_lines:
    filtered_df = filtered_df[filtered_df["line"].isin(selected_lines)]
if selected_types:
    filtered_df = filtered_df[filtered_df["train_type"].isin(selected_types)]
if selected_origins:
    filtered_df = filtered_df[filtered_df["origin"].isin(selected_origins)]
if selected_destinations:
    filtered_df = filtered_df[filtered_df["destination"].isin(selected_destinations)]

if filtered_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()


# ------------------------------------------------------------------
# top bar
# ------------------------------------------------------------------

top_l, top_r = st.columns([3, 1])
with top_l:
    st.markdown("**Welcome back, Analyst 🌿**", unsafe_allow_html=True)
with top_r:
    st.markdown(
        f"<div style='text-align:right;padding-top:6px;color:#667066;font-size:13px'>📅 Data view · {dt.date.today():%b %d, %Y}</div>",
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------
# kpis (shared across pages)
# ------------------------------------------------------------------

total_records = len(filtered_df)
unique_trains = filtered_df["train_no"].nunique()
unique_routes = filtered_df["route"].nunique()
unique_lines = filtered_df["line"].nunique()
avg_travel_time = filtered_df["travel_time_minutes"].mean()
avg_distance = filtered_df["distance_km"].mean()


def kpi_card(col, icon, label, value, note):
    col.markdown(
        f'<div class="kpi-card"><div class="kpi-icon">{icon}</div>'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-note">{note} ↗</div></div>',
        unsafe_allow_html=True,
    )


# ==================================================================
# OVERVIEW
# ==================================================================

if page == "Overview":

    st.markdown(
        f'<div class="hero"><div><div class="hero-title">Mumbai Local<br>Train Analytics</div>'
        f'<div class="hero-sub">Data-driven insights on Mumbai Local Train network '
        f"operations, routes, travel time and more.</div>"
        f'<div class="hero-tag"></div></div>'
        f"{hero_img_html}</div>",
        unsafe_allow_html=True,
    )

    k = st.columns(6)
    kpi_card(
        k[0], "📄", "TOTAL RECORDS", f"{total_records:,}", "Train timetable records"
    )
    kpi_card(k[1], "🚆", "UNIQUE TRAINS", f"{unique_trains:,}", "Train services")
    kpi_card(k[2], "🔀", "ROUTES", f"{unique_routes:,}", "Unique routes")
    kpi_card(k[3], "🏛️", "RAILWAY LINES", f"{unique_lines}", ", ".join(lines))
    kpi_card(
        k[4], "⏱️", "AVG TRAVEL TIME", f"{avg_travel_time:.2f} min", "Across all routes"
    )
    kpi_card(k[5], "📏", "AVG DISTANCE", f"{avg_distance:.2f} km", "Across all routes")

    st.write("")
    c1, c2, c3 = st.columns([1.1, 1, 1])

    with c1:
        st.markdown(
            '<div class="panel"><div class="panel-title">Train Records by Railway Line</div>',
            unsafe_allow_html=True,
        )
        line_data = filtered_df["line"].value_counts().reset_index()
        line_data.columns = ["line", "train_records"]
        line_data["line_name"] = line_data["line"].map(LINE_NAMES)
        fig = px.bar(
            line_data,
            x="line_name",
            y="train_records",
            text="train_records",
            color_discrete_sequence=[GREENS[0]],
        )
        fig.update_layout(
            template="plotly_white",
            height=360,
            xaxis_title="",
            yaxis_title="",
            showlegend=False,
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(
            '<div class="panel"><div class="panel-title">Train Type Distribution</div>',
            unsafe_allow_html=True,
        )
        type_data = filtered_df["train_type"].value_counts().reset_index()
        type_data.columns = ["train_type", "count"]
        fig = px.pie(
            type_data,
            names="train_type",
            values="count",
            hole=0.6,
            color_discrete_sequence=GREENS,
        )
        fig.update_layout(
            template="plotly_white",
            height=360,
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown(
            '<div class="panel"><div class="panel-title">Top 5 Busiest Routes</div>',
            unsafe_allow_html=True,
        )
        top_routes = filtered_df["route"].value_counts().head(5).reset_index()
        top_routes.columns = ["route", "train_count"]
        for i, row in enumerate(top_routes.itertuples(), start=1):
            st.markdown(
                f'<div class="route-row"><div class="route-num">{i}</div>'
                f'<div class="route-name">{row.route}</div>'
                f'<div class="route-count">{row.train_count} trains</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    i1, i2, i3, i4 = st.columns(4)
    with i1:
        st.markdown(
            '<div class="info-card"><div class="info-title">🗃️ Data Source</div>'
            '<div class="info-text">Collected from Mumbai Local Timetable API</div>'
            "</div>",
            unsafe_allow_html=True,
        )
    with i2:
        st.markdown(
            f'<div class="info-card"><div class="info-title">💾 Database</div>'
            f'<div class="info-text">Stored in SQLite database ({len(df):,} records)</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
    with i3:
        updated = dt.datetime.fromtimestamp(CSV_FILE.stat().st_mtime)
        st.markdown(
            f'<div class="info-card"><div class="info-title">📅 Last Updated</div>'
            f'<div class="info-text">{updated:%b %d, %Y · %I:%M %p}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
    with i4:
        st.markdown(
            '<div class="info-card"><div class="info-title">📈 Dashboard</div>'
            '<div class="info-text">Interactive analytics dashboard with real-time insights</div>'
            "</div>",
            unsafe_allow_html=True,
        )


# ==================================================================
# TRAIN OPERATIONS
# ==================================================================

elif page == "Train Operations":
    st.markdown(
        '<div class="section-heading">🚉 Train Operations</div>', unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)
    with c1:
        dest_data = filtered_df["destination"].value_counts().head(10).reset_index()
        dest_data.columns = ["destination", "train_count"]
        dest_data = dest_data.sort_values("train_count")
        fig = px.bar(
            dest_data,
            x="train_count",
            y="destination",
            orientation="h",
            text="train_count",
            title="Top 10 Destinations",
            color_discrete_sequence=[GREENS[0]],
        )
        fig.update_layout(template="plotly_white", height=430, paper_bgcolor="white")
        st.plotly_chart(fig, width="stretch")

    with c2:
        if "time_period" in filtered_df.columns:
            time_data = filtered_df["time_period"].value_counts().reset_index()
            time_data.columns = ["time_period", "train_count"]
            fig = px.bar(
                time_data,
                x="time_period",
                y="train_count",
                text="train_count",
                title="Train Frequency by Time Period",
                color_discrete_sequence=[GREENS[1]],
            )
            fig.update_layout(
                template="plotly_white", height=430, paper_bgcolor="white"
            )
            st.plotly_chart(fig, width="stretch")


# ==================================================================
# ROUTE INTELLIGENCE
# ==================================================================

elif page == "Route Intelligence":
    st.markdown(
        '<div class="section-heading">🔀 Route Intelligence</div>',
        unsafe_allow_html=True,
    )

    route_data = filtered_df["route"].value_counts().head(10).reset_index()
    route_data.columns = ["route", "train_count"]
    route_data = route_data.sort_values("train_count")
    fig = px.bar(
        route_data,
        x="train_count",
        y="route",
        orientation="h",
        text="train_count",
        title="Top 10 Busiest Routes",
        color_discrete_sequence=[GREENS[0]],
    )
    fig.update_layout(template="plotly_white", height=460, paper_bgcolor="white")
    st.plotly_chart(fig, width="stretch")

# STATION ANALYSIS

elif page == "Station Analysis":
    st.markdown(
        '<div class="section-heading">🏛️ Station Activity</div>', unsafe_allow_html=True
    )

    station_data = (
        pd.concat([filtered_df["from_station"], filtered_df["to_station"]])
        .value_counts()
        .reset_index()
    )
    station_data.columns = ["station", "scheduled_services"]
    station_data = station_data.head(15).sort_values("scheduled_services")

    fig = px.bar(
        station_data,
        x="scheduled_services",
        y="station",
        orientation="h",
        text="scheduled_services",
        title="Top 15 Stations by Scheduled Services",
        color_discrete_sequence=[GREENS[0]],
    )
    fig.update_layout(template="plotly_white", height=550, paper_bgcolor="white")
    st.plotly_chart(fig, width="stretch")

    st.markdown(
        '<div class="note-box">⚠️ This is station activity based on scheduled train services, '
        "not actual passenger crowd data. Real crowd analysis would require passenger counts, "
        "ticket data or station footfall data.</div>",
        unsafe_allow_html=True,
    )

# TRAVEL PERFORMANCE

elif page == "Travel Performance":
    st.markdown(
        '<div class="section-heading">⏱️ Travel Performance</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(
            filtered_df,
            x="distance_km",
            y="travel_time_minutes",
            color="line",
            hover_data=["from_station", "to_station", "train_type"],
            title="Distance vs Travel Time",
            color_discrete_sequence=GREENS,
        )
        fig.update_layout(template="plotly_white", height=440, paper_bgcolor="white")
        st.plotly_chart(fig, width="stretch")

    with c2:
        travel_data = (
            filtered_df.groupby("line")["travel_time_minutes"].mean().reset_index()
        )
        travel_data.columns = ["line", "avg_travel_time"]
        travel_data["line_name"] = travel_data["line"].map(LINE_NAMES)
        fig = px.bar(
            travel_data,
            x="line_name",
            y="avg_travel_time",
            text_auto=".2f",
            title="Average Travel Time by Line",
            color_discrete_sequence=[GREENS[1]],
        )
        fig.update_layout(template="plotly_white", height=440, paper_bgcolor="white")
        st.plotly_chart(fig, width="stretch")

    st.markdown(
        '<div class="section-heading">🐌 Slowest Routes</div>', unsafe_allow_html=True
    )
    slowest = (
        filtered_df.groupby("route")
        .agg(
            avg_travel_time=("travel_time_minutes", "mean"),
            train_count=("train_no", "count"),
        )
        .reset_index()
    )
    slowest = slowest[slowest["train_count"] >= 2]
    slowest = slowest.sort_values("avg_travel_time", ascending=False).head(10)

    fig = px.bar(
        slowest.sort_values("avg_travel_time"),
        x="avg_travel_time",
        y="route",
        orientation="h",
        text_auto=".2f",
        title="Top 10 Slowest Routes",
        color_discrete_sequence=[GREENS[0]],
    )
    fig.update_layout(
        template="plotly_white",
        height=440,
        xaxis_title="Average Travel Time (minutes)",
        paper_bgcolor="white",
    )
    st.plotly_chart(fig, width="stretch")


# ==================================================================
# SQL INSIGHTS
# ==================================================================

elif page == "SQL Insights":
    st.markdown(
        '<div class="section-heading">🗄️ SQL Insights</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="panel">This section is powered by the SQLite database created from the '
        "cleaned Mumbai Local timetable dataset. <b>Database:</b> mumbai_local.db</div>",
        unsafe_allow_html=True,
    )

    st.subheader("🚆 Train Records by Railway Line")
    sql_line = load_sql(
        "SELECT line, COUNT(*) AS train_records FROM train_timetable GROUP BY line ORDER BY train_records DESC;"
    )
    sql_line["line_name"] = sql_line["line"].map(LINE_NAMES)
    st.dataframe(sql_line, width="stretch", hide_index=True)

    st.subheader("📍 Top Destinations")
    sql_dest = load_sql(
        "SELECT destination, COUNT(*) AS train_count FROM train_timetable GROUP BY destination ORDER BY train_count DESC LIMIT 10;"
    )
    st.dataframe(sql_dest, width="stretch", hide_index=True)

    st.subheader("🛤️ Busiest Routes")
    sql_routes = load_sql(
        "SELECT from_station || ' -> ' || to_station AS route, COUNT(*) AS train_count "
        "FROM train_timetable GROUP BY from_station, to_station ORDER BY train_count DESC LIMIT 10;"
    )
    st.dataframe(sql_routes, width="stretch", hide_index=True)

    st.subheader("⏱️ Average Travel Time by Line")
    sql_travel = load_sql(
        "SELECT line, ROUND(AVG(travel_time_minutes), 2) AS avg_travel_time FROM train_timetable GROUP BY line ORDER BY avg_travel_time DESC;"
    )
    sql_travel["line_name"] = sql_travel["line"].map(LINE_NAMES)
    fig = px.bar(
        sql_travel,
        x="line_name",
        y="avg_travel_time",
        text_auto=".2f",
        title="SQL: Average Travel Time by Railway Line",
        color_discrete_sequence=[GREENS[0]],
    )
    fig.update_layout(template="plotly_white", height=400, paper_bgcolor="white")
    st.plotly_chart(fig, width="stretch")

    st.subheader("🚈 Local vs AC")
    sql_types = load_sql(
        "SELECT train_type, COUNT(*) AS train_count FROM train_timetable GROUP BY train_type ORDER BY train_count DESC;"
    )
    c1, c2 = st.columns(2)
    c1.dataframe(sql_types, width="stretch", hide_index=True)
    fig = px.pie(
        sql_types,
        names="train_type",
        values="train_count",
        hole=0.5,
        color_discrete_sequence=GREENS,
    )
    fig.update_layout(template="plotly_white", height=350, paper_bgcolor="white")
    c2.plotly_chart(fig, width="stretch")

    st.subheader("🕐 Train Frequency by Time Period")
    sql_time = load_sql(
        "SELECT time_period, COUNT(*) AS train_count FROM train_timetable GROUP BY time_period ORDER BY train_count DESC;"
    )
    fig = px.bar(
        sql_time,
        x="time_period",
        y="train_count",
        text="train_count",
        title="SQL: Train Frequency by Time Period",
        color_discrete_sequence=[GREENS[1]],
    )
    fig.update_layout(template="plotly_white", height=400, paper_bgcolor="white")
    st.plotly_chart(fig, width="stretch")

    st.subheader("🐌 Slowest Routes")
    sql_slowest = load_sql(
        "SELECT from_station || ' -> ' || to_station AS route, ROUND(AVG(travel_time_minutes), 2) AS avg_travel_time "
        "FROM train_timetable GROUP BY from_station, to_station HAVING COUNT(*) >= 2 ORDER BY avg_travel_time DESC LIMIT 10;"
    )
    st.dataframe(sql_slowest, width="stretch", hide_index=True)

    st.subheader("📏 Longest Routes")
    sql_longest = load_sql(
        "SELECT from_station || ' -> ' || to_station AS route, ROUND(AVG(distance_km), 2) AS avg_distance "
        "FROM train_timetable GROUP BY from_station, to_station ORDER BY avg_distance DESC LIMIT 10;"
    )
    st.dataframe(sql_longest, width="stretch", hide_index=True)


# ==================================================================
# DATA EXPLORER
# ==================================================================

elif page == "Data Explorer":
    st.markdown(
        '<div class="section-heading">📋 Data Explorer</div>', unsafe_allow_html=True
    )

    search_term = st.text_input(
        "🔍 Search station, route or destination",
        placeholder="Example: Panvel, Vashi, Goregaon...",
    )
    explorer_df = filtered_df.copy()

    if search_term:
        search_columns = [
            "route",
            "from_station",
            "to_station",
            "origin",
            "destination",
        ]
        mask = pd.Series(False, index=explorer_df.index)
        for column in search_columns:
            mask |= (
                explorer_df[column]
                .astype(str)
                .str.contains(search_term, case=False, na=False)
            )
        explorer_df = explorer_df[mask]

    st.write(f"Showing **{len(explorer_df):,}** records")
    st.dataframe(explorer_df, width="stretch", height=500, hide_index=True)
    st.download_button(
        "⬇️ Download Filtered Data",
        data=explorer_df.to_csv(index=False).encode("utf-8"),
        file_name="mumbai_local_filtered.csv",
        mime="text/csv",
        width="stretch",
    )


st.markdown(
    '<div class="footer">© 2026 Mumbai Local Train Analytics </div>',
    unsafe_allow_html=True,
)
