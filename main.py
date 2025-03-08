import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import requests

# Step 1: Fetch Real-time Financial Data from API
# Using Alpha Vantage API for real-time stock/bank data
API_KEY = 'demo'  # Replace with your API key
symbol = 'IBM'
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'

response = requests.get(url)
data = response.json()

# Convert the API response to a DataFrame
time_series = data['Time Series (Daily)']
df = pd.DataFrame.from_dict(time_series, orient='index')
df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
df.index = pd.to_datetime(df.index)
df = df.sort_index()

# Step 2: Data Analysis
# Calculate income, expense, and balance
# Simulating income and expenses based on stock price variation
income = float(df['High'].iloc[-1]) * 100
expense = float(df['Low'].iloc[-1]) * 50
balance = income - expense

# Step 3: Visualize the data
plt.figure(figsize=(10, 5))
df['Close'].plot(color='green')
plt.title('Stock Price Trend')
plt.ylabel('Stock Price (USD)')
plt.savefig('stock_trend.png')
plt.close()

# Step 4: Generate a PDF Report
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)
pdf.cell(200, 10, 'Real-time Financial Report', ln=True, align='C')

# Add Income, Expense, and Balance
pdf.set_font('Arial', '', 12)
pdf.cell(200, 10, f'Total Income: ₹{income:.2f}', ln=True)
pdf.cell(200, 10, f'Total Expense: ₹{expense:.2f}', ln=True)
pdf.cell(200, 10, f'Net Balance: ₹{balance:.2f}', ln=True)

# Add the stock price trend chart
pdf.image('stock_trend.png', x=10, y=60, w=180)

# Step 5: Save the PDF
pdf.output('Real_Time_Financial_Report.pdf')

print("Report successfully generated as 'Real_Time_Financial_Report.pdf'")
