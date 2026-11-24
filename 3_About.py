import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="🚗",
    layout="wide"
)

# Header
st.title("🚗 About the Automobile Analytics Dashboard")
st.markdown("---")

# About Project
st.header("📖 Project Overview")

st.write("""
The **Automobile Analytics Dashboard** is an interactive data visualization
application developed using **Python** and **Streamlit**. It helps users
analyze automobile data through charts, KPIs, filters, and summary statistics.
The dashboard makes it easy to understand vehicle performance and compare
different automobile features.
""")

# Features
st.header("✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.success("📊 Interactive Charts")
    st.success("📈 Vehicle Performance Analysis")
    st.success("⚙️ Dynamic Filters")

with col2:
    st.success("🚗 Vehicle Information")
    st.success("📋 Dataset Summary")
    st.success("📉 KPI Metrics")

# Technologies
st.header("🛠 Technologies Used")

st.write("""
- Python
- Streamlit
- Pandas
- Plotly
- Matplotlib
""")

# Dataset
st.header("📂 Dataset Information")

st.write("""
The dashboard analyzes an automobile dataset containing information such as:

- Manufacturer
- Vehicle Model
- Engine Size
- Fuel Efficiency
- Mileage
- Fuel Type
- Transmission
- Vehicle Category
""")

# Developer
st.header("👨‍💻 Developer")

st.info("""
**Name:** Priyanshu Tiwari

Developed using **Python** and **Streamlit** to provide an interactive
dashboard for automobile data analysis and visualization.
""")

st.markdown("---")
st.caption("© 2026 Automobile Analytics Dashboard | Built with ❤️ using Streamlit")