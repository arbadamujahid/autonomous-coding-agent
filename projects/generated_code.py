import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('sales_data.csv')

# Total Sales
total_sales = data['sale_amount'].sum()
print(f"Total Sales: {total_sales}")

# Average Sales
average_sales = total_sales / len(data)
print(f"Average Sales: {average_sales}")

# Highest-Selling Product
highest_selling_product = data[data['sale_amount'] == data['sale_amount'].max()]
print(f"Highest Selling Product: {highest_selling_product['product_name'].values[0]}")

# Sales by Category
sales_by_category = data.groupby('category')['sale_amount'].sum()
print("Sales by Category:")
print(sales_by_category)

# Total Sales Histogram
plt.figure(figsize=(10, 5))
plt.hist(data['sale_amount'], bins=30, color='skyblue', edgecolor='black')
plt.title('Total Sales Distribution')
plt.xlabel('Sales Amount')
plt.ylabel('Frequency')
plt.show()

# Sales by Category Bar Chart
plt.figure(figsize=(10, 5))
sales_by_category.plot(kind='bar', color='green')
plt.title('Sales by Category')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()

# Save the results to a new CSV file
data.to_csv('sales_analysis_results.csv', index=False)
print("Results saved to sales_analysis_results.csv")