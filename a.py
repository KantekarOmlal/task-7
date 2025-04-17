import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: Create and connect to the SQLite database
db_name = "sales_data.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Step 2: Create sales table (only if it doesn't exist)
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
""")

# Step 3: Insert sample data (if the table is empty)
cursor.execute("SELECT COUNT(*) FROM sales")
if cursor.fetchone()[0] == 0:
    sample_data = [
        ("Apple", 10, 2.5),
        ("Banana", 20, 1.0),
        ("Orange", 15, 1.5),
        ("Apple", 5, 2.5),
        ("Banana", 10, 1.0),
        ("Orange", 10, 1.5)
    ]
    cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
    conn.commit()

# Step 4: Run SQL query to get summary
query = """
SELECT 
    product, 
    SUM(quantity) AS total_qty, 
    ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
GROUP BY product
"""
df = pd.read_sql_query(query, conn)

# Step 5: Display results
print("=== Sales Summary ===")
print(df)

# Step 6: Plot revenue bar chart
df.plot(kind='bar', x='product', y='revenue', title="Revenue by Product", legend=False)
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.show()

# Close DB connection
conn.close()
