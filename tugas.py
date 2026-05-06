import pandas as pd
import matplotlib

# Pakai backend non-GUI (biar tidak freeze & pasti bisa save)
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import datetime as dt
import os

print("Program mulai...")
print("Lokasi file:", os.getcwd())

# =========================
# LOAD DATA
# =========================
df = pd.read_csv('data_praktikum.csv')

# =========================
# DATA CLEANING
# =========================
df = df[df['Price_Per_Unit'] > 0]
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

print("Data berhasil dibaca")

# =========================
# 1. UNDERPERFORMER
# =========================
print("\nMembuat grafik underperformer...")

avg_price = df['Price_Per_Unit'].mean()

product_analysis = df.groupby('Product_Category').agg({
    'Price_Per_Unit': 'mean',
    'Quantity': 'sum'
}).reset_index()

# Print hasil analisis
print("\n=== UNDERPERFORMER ===")
print(product_analysis.sort_values(by='Quantity'))

# Plot
plt.figure()
plt.scatter(product_analysis['Price_Per_Unit'], product_analysis['Quantity'])

plt.axvline(avg_price)
plt.axhline(product_analysis['Quantity'].mean())

plt.xlabel('Price Per Unit')
plt.ylabel('Quantity')
plt.title('Underperformer Products')

# Save
plt.savefig('underperformer.png', dpi=300)
plt.close()

print("✅ underperformer.png berhasil dibuat!")

# =========================
# 2. RFM ANALYSIS
# =========================
print("\nLanjut ke RFM...")

snapshot_date = df['Order_Date'].max() + dt.timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'Order_Date': lambda x: (snapshot_date - x.max()).days,
    'Order_ID': 'count',
    'Total_Sales': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

# Pakai cut biar aman
rfm['R_Score'] = pd.cut(rfm['Recency'], bins=5, labels=[5,4,3,2,1])
rfm['F_Score'] = pd.cut(rfm['Frequency'], bins=5, labels=[1,2,3,4,5])
rfm['M_Score'] = pd.cut(rfm['Monetary'], bins=5, labels=[1,2,3,4,5])

rfm['RFM_Group'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

print("\n=== RFM ANALYSIS ===")
print(rfm.head())

# =========================
# 3. EFISIENSI KATEGORI
# =========================
print("\nMembuat grafik efisiensi...")

category_analysis = df.groupby('Product_Category').agg({
    'Total_Sales': 'sum',
    'Ad_Budget': 'sum'
}).reset_index()

category_analysis['Efficiency'] = category_analysis['Total_Sales'] / category_analysis['Ad_Budget']

print("\n=== EFISIENSI KATEGORI ===")
print(category_analysis)

# Plot
plt.figure()
plt.barh(category_analysis['Product_Category'], category_analysis['Efficiency'])

plt.xlabel('Efficiency')
plt.ylabel('Category')
plt.title('Category Efficiency')

# Save
plt.savefig('efisiensi.png', dpi=300)
plt.close()

print("✅ efisiensi.png berhasil dibuat!")

# =========================
# 4. UJI HIPOTESIS
# =========================
print("\nLanjut ke Uji Hipotesis...")

median_ads = df['Ad_Budget'].median()

high_ads = df[df['Ad_Budget'] > median_ads]
low_ads = df[df['Ad_Budget'] <= median_ads]

avg_high = high_ads['Total_Sales'].mean()
avg_low = low_ads['Total_Sales'].mean()

print("\n=== UJI HIPOTESIS ===")
print("Rata-rata Penjualan (Iklan Tinggi):", avg_high)
print("Rata-rata Penjualan (Iklan Rendah):", avg_low)

print("\n🎉 Program selesai!")