# ==========================================
# PROJECT 3 : DATA VISUALIZATION DASHBOARD
# Internship Project
# ==========================================

import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# ------------------------------------------
# Load Dataset
# ------------------------------------------
df = pd.read_excel("cleaned_dataset.xlsx")

# Convert date column
df['date'] = pd.to_datetime(df['date'])

# ------------------------------------------
# KPI Calculations
# ------------------------------------------
total_revenue = df['totalprice'].sum()
total_orders = len(df)
avg_order_value = df['totalprice'].mean()

print("=" * 50)
print("BUSINESS SUMMARY")
print("=" * 50)
print(f"Total Revenue      : ₹{total_revenue:,.2f}")
print(f"Total Orders       : {total_orders}")
print(f"Average Order Value: ₹{avg_order_value:,.2f}")

# ------------------------------------------
# Data Aggregation
# ------------------------------------------

# Revenue by Product
product_sales = (
    df.groupby('product')['totalprice']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# Monthly Revenue Trend
monthly_sales = (
    df.groupby(df['date'].dt.to_period('M'))['totalprice']
    .sum()
    .reset_index()
)

monthly_sales['date'] = monthly_sales['date'].astype(str)

# Order Status Distribution
status_counts = (
    df['orderstatus']
    .value_counts()
    .reset_index()
)

status_counts.columns = ['Status', 'Count']

# Referral Source Performance
referral_sales = (
    df.groupby('referralsource')['totalprice']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# ------------------------------------------
# Dashboard Layout
# ------------------------------------------

fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "Revenue by Product",
        "Monthly Revenue Trend",
        "Order Status Distribution",
        "Revenue by Referral Source"
    ),
    specs=[
        [{"type": "bar"}, {"type": "scatter"}],
        [{"type": "pie"}, {"type": "bar"}]
    ]
)

# ------------------------------------------
# Chart 1 : Product Revenue
# ------------------------------------------

fig.add_trace(
    go.Bar(
        x=product_sales['product'],
        y=product_sales['totalprice'],
        name="Revenue"
    ),
    row=1,
    col=1
)

# ------------------------------------------
# Chart 2 : Monthly Trend
# ------------------------------------------

fig.add_trace(
    go.Scatter(
        x=monthly_sales['date'],
        y=monthly_sales['totalprice'],
        mode='lines+markers',
        name='Monthly Revenue'
    ),
    row=1,
    col=2
)

# ------------------------------------------
# Chart 3 : Order Status Pie Chart
# ------------------------------------------

fig.add_trace(
    go.Pie(
        labels=status_counts['Status'],
        values=status_counts['Count'],
        hole=0.4
    ),
    row=2,
    col=1
)

# ------------------------------------------
# Chart 4 : Referral Source Revenue
# ------------------------------------------

fig.add_trace(
    go.Bar(
        x=referral_sales['referralsource'],
        y=referral_sales['totalprice'],
        name='Referral Revenue'
    ),
    row=2,
    col=2
)

# ------------------------------------------
# Dashboard Styling
# ------------------------------------------

fig.update_layout(
    title={
        'text': "E-Commerce Sales Analytics Dashboard",
        'x': 0.5,
        'font': {'size': 24}
    },
    height=900,
    width=1400,
    template="plotly_dark",
    showlegend=False
)

fig.show()

# ------------------------------------------
# Automatic Insights
# ------------------------------------------

top_product = product_sales.iloc[0]
top_referral = referral_sales.iloc[0]

print("\n" + "=" * 50)
print("KEY INSIGHTS")
print("=" * 50)

print(
    f"Top Revenue Product: {top_product['product']} "
    f"(₹{top_product['totalprice']:,.2f})"
)

print(
    f"Best Referral Source: {top_referral['referralsource']} "
    f"(₹{top_referral['totalprice']:,.2f})"
)

print(
    f"Average Order Value: ₹{avg_order_value:,.2f}"
)

print(
    "Monthly trend chart helps identify seasonal sales patterns."
)

print(
    "Order status distribution highlights operational performance."
)