🏆 Olist E-commerce Performance Analysis (Python/Pandas/NumPy)
This project provides an end-to-end data analysis of the Brazilian Olist e-commerce dataset (2016-2018), covering sales trends, customer behavior, and logistics performance. The goal is to identify core revenue drivers and operational inefficiencies for strategic business recommendations.

💡 Key Findings and Business Impact
The analysis, derived from over 119,000 merged transactions, revealed critical, quantified insights for stakeholders:

Seasonality (High Impact): Revenue shows a consistent spike of [145.7%] over the monthly average, peaking reliably in November (Q4).

Action: Increase Q4 inventory and budget allocation to capitalize on the holiday demand.

Product Focus (Concentration): The Top 3 product categories (e.g., beleza_saude) account for [22.5 % ]of total gross revenue.

Action: Concentrate marketing and purchasing on these high-performing core categories.

Logistics Risk (Operational KPI): Calculated the delivery lag KPI, showing that [14.5 %] of all orders were delivered past the estimated date.

Action: Initiate a performance audit for high-volume sellers contributing most to the delivery lag.


🛠️  Technical Methodology
This project demonstrates proficiency in the standard data analysis workflow:

Data Wrangling (Pandas): Successfully loaded and merged 7 relational tables (orders, customers, items, products, etc.) using efficient left joins (pd.merge).

Feature Engineering (NumPy): Created the Total_Item_Revenue KPI and used np.where() for high-speed conditional flagging (creating the Is_Late_Delivery metric).

Analysis & Aggregation: Generated summary reports (monthly_kpis, top_categories) using the powerful .groupby().agg() function for time-series analysis.

 📈 Visual Summary

The visualizations in the main notebook confirm the project's primary findings:

* **Monthly Revenue Trend:** Shows the sharp increase confirming seasonality (the November/Q4 spike).
* **Top 10 Product Categories:** Highlights the revenue concentration and identifies the best-selling categories.

🚀 Getting Started
To run and reproduce this analysis locally, ensure you have Python 3.8+ and install the required libraries:

pip install pandas numpy matplotlib seaborn
The full analysis, code, and rendered charts are contained within the olist data project.py file in this repository.

