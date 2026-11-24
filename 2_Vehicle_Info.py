import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Vehicle Information",
    page_icon="🚗",
    layout="wide"
)

# CUSTOM CSS
# ==========================================================
st.markdown("""
<style>

/* Metric Card */
[data-testid="stMetric"]{
    background:#f8f9fa;
    padding:20px;
    border-radius:15px;
    border:1px solid #dcdcdc;
    box-shadow:0 4px 10px rgba(0,0,0,0.15);
}

/* Metric Label */
[data-testid="stMetricLabel"]{
    color:#1565C0 !important;
    font-size:18px !important;
    font-weight:600 !important;
}

/* Metric Value */
[data-testid="stMetricValue"]{
    color:#000000 !important;
    font-size:32px !important;
    font-weight:bold !important;
}

/* Metric Delta (if any) */
[data-testid="stMetricDelta"]{
    color:#28a745 !important;
}

</style>
""", unsafe_allow_html=True)

# HERO SECTION
# ==========================================================

st.markdown("""
<div class="hero">

<h1>🚗 Vehicle Information Explorer</h1>

<p>
Explore detailed information about every automobile in the dataset.
</p>

</div>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(r"C:\Users\Acer\OneDrive\Documents\Desktop\Minior project\work2\automobile_dataset.csv")

    return df

df = load_data()

# ==========================================================
# CLEAN DATA
# ==========================================================

numeric_columns = [
    "Engine_Size",
    "Mileage",
    "Horsepower",
    "Torque",
    "Fuel_Efficiency",
    "Selling_Price",
    "Owners"
]

for col in numeric_columns:

    if col in df.columns:

        df[col] = pd.to_numeric(df[col], errors="coerce")

text_columns = [
    "Transmission",
    "Fuel_Type",
    "Body_Type",
    "Service_History",
    "Accident_History",
    "Color",
    "Drivetrain",
    "Location"
]

for col in text_columns:

    if col in df.columns:

        df[col] = df[col].fillna("Unknown")

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("🔍 Dashboard Filters")

selected_make = st.sidebar.multiselect(
    "Manufacturer",
    sorted(df["Make"].dropna().unique()),
    default=sorted(df["Make"].dropna().unique())
)

selected_fuel = st.sidebar.multiselect(
    "Fuel Type",
    sorted(df["Fuel_Type"].dropna().unique()),
    default=sorted(df["Fuel_Type"].dropna().unique())
)

selected_transmission = st.sidebar.multiselect(
    "Transmission",
    sorted(df["Transmission"].dropna().unique()),
    default=sorted(df["Transmission"].dropna().unique())
)

filtered_df = df[
    (df["Make"].isin(selected_make)) &
    (df["Fuel_Type"].isin(selected_fuel)) &
    (df["Transmission"].isin(selected_transmission))
]

# ==========================================================
# KPI CARDS
# ==========================================================

st.subheader("📊 Dashboard Overview")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:

    st.metric(
        "🚗 Total Vehicles",
        len(filtered_df)
    )

with kpi2:

    st.metric(
        "🏭 Manufacturers",
        filtered_df["Make"].nunique()
    )

with kpi3:

    avg_price = filtered_df["Selling_Price"].mean()

    st.metric(
        "💰 Avg Price",
        f"${avg_price:,.0f}"
    )

with kpi4:

    avg_hp = filtered_df["Horsepower"].mean()

    st.metric(
        "🏁 Avg Horsepower",
        f"{avg_hp:.0f} HP"
    )

st.markdown("---")
# ==========================================================
# VEHICLE SEARCH
# ==========================================================

st.subheader("🔍 Vehicle Search")

col1, col2 = st.columns(2)

with col1:

    selected_make = st.selectbox(
        "Select Manufacturer",
        sorted(filtered_df["Make"].unique())
    )

models = filtered_df[filtered_df["Make"] == selected_make]["Model"].unique()

with col2:

    selected_model = st.selectbox(
        "Select Model",
        sorted(models)
    )

vehicle = filtered_df[
    (filtered_df["Make"] == selected_make) &
    (filtered_df["Model"] == selected_model)
].iloc[0]

st.markdown("---")

# ==========================================================
# VEHICLE DETAILS
# ==========================================================

st.subheader("🚗 Vehicle Details")

info1, info2, info3 = st.columns(3)

with info1:

    st.info(f"""
### Basic Information

**Manufacturer:** {vehicle['Make']}

**Model:** {vehicle['Model']}

**Year:** {vehicle['Year']}

**Color:** {vehicle['Color']}

**Location:** {vehicle['Location']}
""")

with info2:

    st.success(f"""
### Engine & Performance

**Engine Size:** {vehicle['Engine_Size']} L

**Horsepower:** {vehicle['Horsepower']} HP

**Torque:** {vehicle['Torque']}

**Fuel Efficiency:** {vehicle['Fuel_Efficiency']}

**Transmission:** {vehicle['Transmission']}
""")

with info3:

    st.warning(f"""
### Vehicle History

**Fuel Type:** {vehicle['Fuel_Type']}

**Body Type:** {vehicle['Body_Type']}

**Owners:** {vehicle['Owners']}

**Service History:** {vehicle['Service_History']}

**Accident History:** {vehicle['Accident_History']}
""")

st.metric(
    "💰 Selling Price",
    f"${vehicle['Selling_Price']:,.0f}"
)

st.markdown("---")

# ==========================================================
# GRAPH SECTION
# ==========================================================

st.subheader("📊 Vehicle Statistics")

left, right = st.columns(2)

# ==========================================================
# GRAPH 1
# ==========================================================

with left:

    make_df = (
        filtered_df["Make"]
        .value_counts()
        .reset_index()
    )

    make_df.columns = ["Manufacturer", "Vehicles"]

    fig1 = px.bar(
        make_df,
        x="Manufacturer",
        y="Vehicles",
        color="Vehicles",
        text="Vehicles",
        color_continuous_scale="Blues",
        title="Vehicle Count by Manufacturer"
    )

    fig1.update_layout(
        height=450,
        template="plotly_white"
    )

    st.plotly_chart(fig1, use_container_width=True)

# ==========================================================
# GRAPH 2
# ==========================================================

with right:

    fuel_df = (
        filtered_df["Fuel_Type"]
        .value_counts()
        .reset_index()
    )

    fuel_df.columns = ["Fuel Type", "Count"]

    fig2 = px.pie(
        fuel_df,
        names="Fuel Type",
        values="Count",
        hole=0.45,
        title="Fuel Type Distribution"
    )

    fig2.update_layout(
        height=450
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    # ==========================================================
# GRAPH 6 - TOP 10 MOST EXPENSIVE VEHICLES
# ==========================================================

st.markdown("---")
st.subheader("💰 Top 10 Most Expensive Vehicles")

price_df = filtered_df.dropna(subset=["Selling_Price"])

top10 = price_df.nlargest(10, "Selling_Price")

fig6 = px.bar(
    top10,
    x="Model",
    y="Selling_Price",
    color="Selling_Price",
    text="Selling_Price",
    hover_data=[
        "Make",
        "Year",
        "Fuel_Type"
    ],
    color_continuous_scale="Viridis",
    title="Top 10 Most Expensive Vehicles"
)

fig6.update_layout(
    height=500,
    template="plotly_white",
    xaxis_title="Vehicle Model",
    yaxis_title="Selling Price"
)

st.plotly_chart(fig6, use_container_width=True)

# ==========================================================
# GRAPH 7 - SELLING PRICE DISTRIBUTION
# ==========================================================

st.subheader("📈 Selling Price Distribution")

fig7 = px.histogram(
    filtered_df,
    x="Selling_Price",
    nbins=25,
    color="Fuel_Type",
    title="Distribution of Vehicle Selling Prices"
)

fig7.update_layout(
    height=500,
    template="plotly_white"
)

st.plotly_chart(fig7, use_container_width=True)

# ==========================================================
# DATASET PREVIEW
# ==========================================================

st.markdown("---")
st.subheader("📋 Filtered Vehicle Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# DOWNLOAD DATASET
# ==========================================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_vehicle_data.csv",
    mime="text/csv",
    use_container_width=True
)

# ==========================================================
# DATASET SUMMARY
# ==========================================================

st.markdown("---")
st.subheader("Dataset Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Average Mileage",
        f"{filtered_df['Mileage'].mean():,.0f}"
    )

with c2:
    st.metric(
        "Average Fuel Efficiency",
        f"{filtered_df['Fuel_Efficiency'].mean():.1f}"
    )

with c3:
    st.metric(
        "Average Engine Size",
        f"{filtered_df['Engine_Size'].mean():.1f} L"
    )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
"""
<div style="text-align:center;color:gray;padding:10px;">

### 🚗 Vehicle Information Dashboard

Explore • Compare • Analyze

Built with ❤️ using Python, Streamlit, Pandas & Plotly

</div>
""",
unsafe_allow_html=True
)
