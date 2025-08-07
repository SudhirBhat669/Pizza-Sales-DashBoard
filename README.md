# 🍕 Pizza Sales Analysis Dashboard

📷 Screenshots

## 📊 Project Overview
This project focuses on analyzing pizza sales data to uncover insights about customer preferences, sales trends, and operational optimizations. The analysis helps answer questions such as:
- What are the top-selling pizza types?
- Which days/times generate the highest sales?
- What category of pizzas brings the most revenue?

The insights are visualized using Python and presented in a dashboard-style report.

## 🧩 Dataset
- The dataset is provided in an Excel file: `Data Model - Pizza Sales.xlsx`, containing the following tables:
- pizza_sales: Includes details like order_id, date/time, pizza name, quantity, price, and category.

## 🛠️ Tools Used
- Python
- pandas, matplotlib, seaborn
- Jupyter Notebook / VSCode
- openpyxl (for reading Excel)
- streamlit (for dashboard interface, optional)

## 📌 Objectives
1. Identify the most popular pizzas.
2. Analyze daily/weekly/monthly sales patterns.
3. Discover peak sales time slots.
4. Track revenue trends by pizza category.
5. Recommend strategies for increasing sales.

## 🧮 Key Metrics Analyzed
- 🏆 Top 5 most sold pizzas
- 💰 Highest earning pizzas
- 📆 Sales per day of the week
- ⏰ Peak sales time slots
- 🧬 Category-wise performance

## 📈 Visualizations
- Bar plots for top-selling pizzas
- Line plots for daily sales trends
- Pie charts for revenue share by category
- Heatmaps for time slot sales

## 🧪 How It Was Done
1. Load Dataset
    - import pandas as pd
    - df = pd.read_excel("Data Model - Pizza Sales.xlsx", sheet_name="pizza_sales")
    
2. Data Cleaning
    - Checked for nulls
    - Converted datetime columns
    - Ensured price/quantity are numeric

3. Analysis Examples
    - Top-selling pizzas:
     - top_pizzas = df.groupby('pizza_name')['quantity'].sum().sort_values(ascending=False).head(5)
      
    - Revenue per day:
      - df['date'] = pd.to_datetime(df['date'])
      - df['day'] = df['date'].dt.day_name()
      - daily_revenue = df.groupby('day')['total_price'].sum()
      

4. Visualizations
  - import matplotlib.pyplot as plt
  -  top_pizzas.plot(kind='bar')
  -  plt.title("Top 5 Pizzas Sold")
    

## 💡 Insights & Recommendations

- Weekend evenings show peak demand – ideal for offers.
- Pepperoni and BBQ Chicken are the most sold – promote combo deals.
- Thin crust and classic style dominate revenue – stock accordingly.

## 🚀 Future Enhancements
- Real-time dashboard using Streamlit
- Customer segmentation with ML
- Forecasting sales using ARIMA models

## 📁 Project Structure
- pizza_sales_analysis.py
- Data Model - Pizza Sales.xlsx
- report.docx
- README.md




