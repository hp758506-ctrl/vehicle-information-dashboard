import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Automobile Analysis Dashboard",
    page_icon="🚗",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\Acer\OneDrive\Documents\Desktop\Minior project\work2\automobile_dataset.csv")
    return df

df = load_data()

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

/* Navigation menu */
section[data-testid="stSidebarNav"] *{
    color:white !important;
    font-weight:600;
}

/* Selected page */
section[data-testid="stSidebarNav"] a[aria-current="page"]{
    background:#2563EB !important;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.markdown("""

<div class="header">

<h1>🚗 Automobile Analysis Dashboard</h1>

<p>
Explore insights, trends and performance of automobiles using interactive
visualizations.
</p>

</div>

""", unsafe_allow_html=True)

st.write("")

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.title("🔍 Dashboard Filters")

# Manufacturer

make = st.sidebar.multiselect(

    "Select Manufacturer",

    options=sorted(df["Make"].dropna().unique()),

    default=sorted(df["Make"].dropna().unique())

)

# Fuel Type

fuel = st.sidebar.multiselect(

    "Fuel Type",

    options=sorted(df["Fuel_Type"].dropna().unique()),

    default=sorted(df["Fuel_Type"].dropna().unique())

)

# Transmission

transmission = st.sidebar.multiselect(

    "Transmission",

    options=sorted(df["Transmission"].dropna().unique()),

    default=sorted(df["Transmission"].dropna().unique())

)

# Body Type

body = st.sidebar.multiselect(

    "Body Type",

    options=sorted(df["Body_Type"].dropna().unique()),

    default=sorted(df["Body_Type"].dropna().unique())

)

# Year

year = st.sidebar.slider(

    "Manufacturing Year",

    int(df["Year"].min()),

    int(df["Year"].max()),

    (

        int(df["Year"].min()),

        int(df["Year"].max())

    )

)

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_df = df[
    (df["Make"].isin(make)) &
    (df["Fuel_Type"].isin(fuel)) &
    (df["Transmission"].isin(transmission)) &
    (df["Body_Type"].isin(body)) &
    (df["Year"].between(year[0], year[1]))
]

# ==========================================================
# KPI CARDS
# ==========================================================

st.subheader("📊 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "🚗 Total Vehicles",

        len(filtered_df)

    )

with col2:

    st.metric(

        "🏭 Manufacturers",

        filtered_df["Make"].nunique()

    )

with col3:

    st.metric(

        "⛽ Fuel Types",

        filtered_df["Fuel_Type"].nunique()

    )

with col4:

    st.metric(

        "💰 Average Price",

        f"${filtered_df['Selling_Price'].mean():,.0f}"

    )

st.markdown("---")
# ==========================================================
# 📈 ANALYSIS GRAPHS - PART 2
# ==========================================================

st.subheader("📈 Automobile Analysis")

# ==========================================================
# ROW 1
# ==========================================================

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# GRAPH 1 : VEHICLE COUNT BY MANUFACTURER
# ----------------------------------------------------------

with col1:

    manufacturer = (
        filtered_df["Make"]
        .value_counts()
        .reset_index()
    )

    manufacturer.columns = ["Manufacturer", "Count"]

    fig1 = px.bar(
        manufacturer,
        x="Manufacturer",
        y="Count",
        color="Count",
        text="Count",
        title="🚗 Vehicle Count by Manufacturer",
        color_continuous_scale="Blues"
    )

    fig1.update_layout(
        title_x=0.20,
        xaxis_title="Manufacturer",
        yaxis_title="Number of Vehicles",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig1, use_container_width=True)

# ----------------------------------------------------------
# GRAPH 2 : FUEL TYPE DISTRIBUTION
# ----------------------------------------------------------

with col2:

    fig2 = px.pie(
        filtered_df,
        names="Fuel_Type",
        hole=0.50,
        title="⛽ Fuel Type Distribution",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig2.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig2.update_layout(
        title_x=0.25,
        height=450
    )

    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ==========================================================
# ROW 2
# ==========================================================

col3, col4 = st.columns(2)

# ----------------------------------------------------------
# GRAPH 3 : TRANSMISSION DISTRIBUTION
# ----------------------------------------------------------

with col3:

    transmission = (
        filtered_df["Transmission"]
        .value_counts()
        .reset_index()
    )

    transmission.columns = [
        "Transmission",
        "Count"
    ]

    fig3 = px.bar(
        transmission,
        x="Transmission",
        y="Count",
        color="Transmission",
        text="Count",
        title="⚙️ Transmission Distribution"
    )

    fig3.update_layout(
        title_x=0.20,
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ----------------------------------------------------------
# GRAPH 4 PREVIEW CARD
# ----------------------------------------------------------

with col4:

    st.markdown("""
    ### 📊 Dashboard Summary

    #### Current Filter Results

    The selected filters are currently displaying:

    ✔ Manufacturer-wise vehicles

    ✔ Fuel Type distribution

    ✔ Transmission distribution

    ---
    **Next Section Includes:**

    🚘 Body Type Distribution

    🏎 Horsepower vs Engine Size

    💰 Top 10 Most Expensive Vehicles
    """)

st.markdown("---")
# ==========================================================
# 📈 ANALYSIS GRAPHS - PART 3
# ==========================================================

# ----------------------------------------------------------
# GRAPH 4 : BODY TYPE DISTRIBUTION
# ----------------------------------------------------------

st.subheader("🚘 Vehicle Body Type Distribution")

body = (
    filtered_df["Body_Type"]
    .value_counts()
    .reset_index()
)

body.columns = ["Body Type", "Count"]

fig4 = px.bar(
    body,
    x="Body Type",
    y="Count",
    color="Count",
    text="Count",
    title="Vehicle Distribution by Body Type",
    color_continuous_scale="Tealgrn"
)

fig4.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.25,
    xaxis_title="Body Type",
    yaxis_title="Number of Vehicles"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ==========================================================
# GRAPH 5 : HORSEPOWER VS ENGINE SIZE
# ==========================================================


scatter_df = filtered_df.dropna(
    subset=["Engine_Size", "Horsepower"]
)

fig5 = px.scatter(
    filtered_df,
    x="Engine_Size",
    y="Horsepower",
    color="Fuel_Type",
    hover_name="Model",
    hover_data=["Make", "Year", "Selling_Price"],
    title="Horsepower vs Engine Size"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ==========================================================
# GRAPH 6 : TOP 10 MOST EXPENSIVE VEHICLES
# ==========================================================

st.subheader("💰 Top 10 Most Expensive Vehicles")

top10 = (
    filtered_df
    .sort_values(
        "Selling_Price",
        ascending=False
    )
    .head(10)
)

fig6 = px.bar(
    top10,
    x="Selling_Price",
    y="Model",
    orientation="h",
    color="Selling_Price",
    text="Selling_Price",
    hover_data=[
        "Make",
        "Year",
        "Fuel_Type"
    ],
    color_continuous_scale="Turbo",
    title="Top 10 Highest Selling Price Vehicles"
)

fig6.update_layout(
    template="plotly_white",
    height=550,
    title_x=0.22,
    xaxis_title="Selling Price",
    yaxis_title="Vehicle Model"
)

fig6.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")