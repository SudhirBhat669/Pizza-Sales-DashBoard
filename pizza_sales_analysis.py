# pizza_sales_analysis.py

import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# -----------------------------
# Load and preprocess the Excel file
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Data Model Pizza Sales.xlsx", sheet_name="pizza_sales")
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['order_time'] = pd.to_datetime(df['order_time'], format='%H:%M:%S').dt.time
    df['day_of_week'] = df['order_date'].dt.day_name()
    df['hour'] = pd.to_datetime(df['order_time'], format='%H:%M:%S').apply(lambda x: x.hour)
    return df

df = load_data()

# -----------------------------
# Create SQLite Database
# -----------------------------
conn = sqlite3.connect("pizza_sales.db")
df.to_sql("pizza_sales", conn, if_exists="replace", index=False)

# -----------------------------
# KPI Queries using SQL
# -----------------------------
total_revenue = pd.read_sql("SELECT SUM(total_price) FROM pizza_sales", conn).iloc[0, 0]
avg_order_value = pd.read_sql("SELECT AVG(total_price) FROM pizza_sales", conn).iloc[0, 0]
total_pizzas_sold = pd.read_sql("SELECT SUM(quantity) FROM pizza_sales", conn).iloc[0, 0]
total_orders = pd.read_sql("SELECT COUNT(DISTINCT order_id) FROM pizza_sales", conn).iloc[0, 0]
avg_pizzas_per_order = total_pizzas_sold / total_orders

# -----------------------------
# Streamlit Dashboard Layout
# -----------------------------
st.set_page_config(page_title="Pizza Sales Dashboard", layout="wide")
st.title("🍕 Pizza Sales Report")

# KPI Display
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Avg Order Value", f"${avg_order_value:,.2f}")
col3.metric("Total Pizzas Sold", f"{total_pizzas_sold:,}")
col4.metric("Total Orders", f"{total_orders:,}")
col5.metric("Avg Pizzas / Order", f"{avg_pizzas_per_order:.2f}")

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_category = st.sidebar.multiselect("Pizza Category", df['pizza_category'].unique(), default=df['pizza_category'].unique())
filtered_df = df[df['pizza_category'].isin(selected_category)]

# -----------------------------
# Charts Section
# -----------------------------
st.markdown("### 🔝 Top 5 Pizzas by Revenue")
top_revenue = (
    filtered_df.groupby('pizza_name')['total_price']
    .sum().sort_values(ascending=False).head(5).reset_index()
)
fig1 = px.bar(top_revenue, x='total_price', y='pizza_name', orientation='h', title="Top 5 Pizzas by Revenue")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 🍕 Top 5 Pizzas by Quantity Sold")
top_quantity = (
    filtered_df.groupby('pizza_name')['quantity']
    .sum().sort_values(ascending=False).head(5).reset_index()
)
fig2 = px.bar(top_quantity, x='quantity', y='pizza_name', orientation='h', title="Top 5 Pizzas by Quantity")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 📆 Orders by Day of Week")
orders_by_day = (
    filtered_df.groupby('day_of_week')['order_id']
    .nunique().reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
)
fig3 = px.bar(x=orders_by_day.index, y=orders_by_day.values, labels={'x': 'Day', 'y': 'Orders'}, title="Orders by Day")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("### 🕒 Hourly Sales Distribution")
hourly_sales = filtered_df.groupby('hour')['quantity'].sum()
fig4 = px.line(x=hourly_sales.index, y=hourly_sales.values, labels={'x': 'Hour', 'y': 'Pizzas Sold'}, title="Sales by Hour")
st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# 🧠 ML Forecasting
# -----------------------------
st.markdown("### 📈 ML Forecast: Monthly Revenue Trend")

df['month'] = df['order_date'].dt.to_period("M")
monthly_revenue = df.groupby('month')['total_price'].sum().reset_index()
monthly_revenue['month'] = monthly_revenue['month'].astype(str)

# ML Regression
X = np.arange(len(monthly_revenue)).reshape(-1, 1)
y = monthly_revenue['total_price'].values
poly = PolynomialFeatures(degree=3)
X_poly = poly.fit_transform(X)
model = LinearRegression().fit(X_poly, y)
y_pred = model.predict(X_poly)

fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=monthly_revenue['month'], y=monthly_revenue['total_price'],
                          mode='lines+markers', name='Actual'))
fig5.add_trace(go.Scatter(x=monthly_revenue['month'], y=y_pred,
                          mode='lines', name='Forecast', line=dict(dash='dash')))
fig5.update_layout(title="Monthly Revenue Forecast", xaxis_title="Month", yaxis_title="Revenue")
st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# 🚦 Seating Capacity Utilization
# -----------------------------
st.markdown("### 🚦 Seating Utilization (Assuming 60 Seats, 15 Tables)")
peak_orders = df.groupby(['day_of_week', 'hour'])['order_id'].nunique().reset_index()
peak_orders['seating_capacity'] = 60
peak_orders['utilization'] = peak_orders['order_id'] * 2  # assume 2 pizzas per table
peak_orders['utilization_pct'] = (peak_orders['utilization'] / 60) * 100
max_util = peak_orders['utilization_pct'].max()

st.write(f"**Max Hourly Utilization:** {max_util:.2f}%")

fig6 = px.density_heatmap(
    peak_orders,
    x='hour',
    y='day_of_week',
    z='utilization_pct',
    title="Hourly Seating Utilization (%)",
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.caption("Developed by Sudhir S Bhat | Plato's Pizza")
