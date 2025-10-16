import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# Load each dataset into a unique variable name
df_orders = pd.read_csv(r"olist_orders_dataset.csv")
df_customers = pd.read_csv(r"olist_customers_dataset.csv")
df_geolocation = pd.read_csv(r"olist_geolocation_dataset.csv")
df_items = pd.read_csv(r"olist_order_items_dataset.csv")
df_payments = pd.read_csv(r"olist_order_payments_dataset.csv")
df_reviews = pd.read_csv(r"olist_order_reviews_dataset.csv")
df_products = pd.read_csv(r"olist_products_dataset.csv")
print(" orders\n")
print(df_orders)
print(" customers\n")
print(df_customers)
print(" geolocation\n")
print(df_geolocation)
print(" items\n")
print(df_items)
print(" payments\n")
print(df_payments)
print(" reviews\n")
print(df_reviews)
print(" products\n")
print(df_products)
print("DataFrames loaded successfully.")


# merge dataframes
# 1. Merge Orders + Customers (Key: 'customer_id')
df_core = pd.merge(df_orders, df_customers, on='customer_id', how='left')
# 2. Merge Result + Order Items (Key: 'order_id')
# This brings in the price, freight, and product_id.
df_analysis = pd.merge(df_core, df_items, on='order_id', how='left')
# 3. Merge Result + Payments (Key: 'order_id')
# This brings in the payment type and value.
df_analysis = pd.merge(df_analysis, df_payments, on='order_id', how='left')
# 4. Merge Result + Reviews (Key: 'order_id')
# This brings in the review score.
df_final = pd.merge(df_analysis, df_reviews, on='order_id', how='left')
# Assuming you loaded df_products earlier:

# --- 5. Merge Result + Products ---
# Key: 'product_id' (This brings in the category name needed for aggregation)
df_final = pd.merge(df_final, df_products, on='product_id', how='left')

print(f"✅ FINAL MERGE COMPLETE: Category column added. Final shape: {df_final.shape}")


print("Merging DataFrames...")

# engineering features

# Assuming df_final is your merged DataFrame

# 1. Date Conversion
date_cols = [
    'order_purchase_timestamp',
    'order_delivered_customer_date',
    'order_estimated_delivery_date',
    'shipping_limit_date',
    'review_creation_date'
]

for col in date_cols:
    df_final[col] = pd.to_datetime(df_final[col], errors='coerce')

# 2. Calculate Total Item Revenue (Primary KPI)
# Vectorized addition of price and shipping cost is very fast.
df_final['Total_Item_Revenue'] = df_final['price'] + df_final['freight_value']

# 3. Extract Time Features for Grouping
# Creates a clean 'YYYY-MM' string for chronological analysis.
df_final['Purchase_Month_Year'] = df_final['order_purchase_timestamp'].dt.strftime(
    '%Y-%m')

# 4. Use NumPy for Conditional Logic (Delivery Performance Flag)
df_final['Is_Late_Delivery'] = np.where(
    df_final['order_delivered_customer_date'] > df_final['order_estimated_delivery_date'],
    'Late',
    'On_Time'
)

print("✅ Feature Engineering Complete. New revenue and time features created.")

print("DataFrames merged successfully.")

# Analysis
# --- INSERT THIS BLOCK AFTER Feature Engineering (Phase 2) ---

# 1. Clean Category Names (Prevents GroupBy Errors)
df_final['product_category_name'] = df_final['product_category_name'].fillna('Unknown')

# 2. Monthly Revenue Trend (Tabulation - CREATES monthly_kpis)
monthly_kpis = df_final.groupby('Purchase_Month_Year')['Total_Item_Revenue'].agg(
    ['sum', 'mean', 'count']
).reset_index()
# Rename the columns for clarity
monthly_kpis.columns = ['Purchase_Month_Year', 'Total_Revenue', 'Average_Order_Value', 'Total_Orders']

print("\n✅ Monthly KPIs created.")

# 3. Top Product Categories (Tabulation - CREATES top_categories)
top_categories = df_final.groupby('product_category_name')[
    'Total_Item_Revenue'
].sum().nlargest(10).reset_index(name='Total_Revenue')

print("✅ Top Categories table created.")


# Visualizations

# 1. Monthly Revenue Trend
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_kpis, x='Purchase_Month_Year', y='Total_Revenue', marker='o')
plt.title('Monthly Revenue Trend')
plt.xticks(rotation=45)
plt.grid()
plt.show()

# 2. Top 10 Product Categories
plt.figure(figsize=(12, 6))
sns.barplot(data=top_categories, x='Total_Revenue', y='product_category_name', orient='h')
plt.title('Top 10 Product Categories by Revenue')
plt.grid()
plt.show()

print("✅ Visualizations generated.")
# Reporting Insights
# This block assumes the 'monthly_kpis' DataFrame is correctly defined from your aggregation steps.

# 1. Calculate the overall mean monthly revenue (The baseline)
average_monthly_revenue = monthly_kpis['Total_Revenue'].mean()

# 2. Identify the peak month revenue (The highest value in the Total_Revenue column)
peak_revenue = monthly_kpis['Total_Revenue'].max()

# 3. Identify the Purchase Month/Year of that peak for the report
peak_month_year = monthly_kpis.loc[monthly_kpis['Total_Revenue'].idxmax(), 'Purchase_Month_Year']

# 4. Calculate the percentage increase
# Formula: ((Peak - Average) / Average) * 100
percentage_increase = ((peak_revenue - average_monthly_revenue) / average_monthly_revenue) * 100

# 5. Print the result for your report
print(f"The average monthly revenue across the dataset is: R$ {average_monthly_revenue:,.2f}")
print(f"The peak revenue in {peak_month_year} was: R$ {peak_revenue:,.2f}")
print(f"*** The Peak Revenue was {percentage_increase:,.2f}% higher than the average monthly revenue. ***")
print("Reporting insights generated.")
