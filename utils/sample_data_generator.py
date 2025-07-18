import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_financial_data():
    """Generate sample financial data for testing the BI Agent"""
    
    np.random.seed(42)  # For reproducible results
    
    # Generate date range (3 years of quarterly data)
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2023, 12, 31)
    quarters = pd.date_range(start=start_date, end=end_date, freq='QE')  # QE for quarter end
    
    # Generate sample data
    data = []
    base_revenue = 1000000  # Base revenue of 1M
    
    for i, quarter in enumerate(quarters):
        # Simulate growth and seasonality
        growth_factor = 1 + (i * 0.05)  # 5% growth per quarter
        seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * i / 4)  # Seasonal variation
        
        revenue = base_revenue * growth_factor * seasonal_factor * (1 + np.random.normal(0, 0.1))
        
        # Calculate related metrics
        gross_profit = revenue * (0.6 + np.random.normal(0, 0.05))  # 60% gross margin ± 5%
        operating_expenses = revenue * (0.35 + np.random.normal(0, 0.03))  # 35% opex ± 3%
        net_profit = gross_profit - operating_expenses
        
        # Additional metrics
        total_assets = revenue * (2.5 + np.random.normal(0, 0.2))  # Asset turnover ~0.4
        total_equity = total_assets * (0.6 + np.random.normal(0, 0.1))  # 60% equity ratio
        cash_flow = net_profit * (1.2 + np.random.normal(0, 0.1))  # Cash flow ~ 120% of net profit
        
        # Product/segment data
        products = ['Product A', 'Product B', 'Product C', 'Product D']
        regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America']
        
        for product in products:
            for region in regions:
                product_revenue = revenue * np.random.uniform(0.05, 0.15)  # 5-15% per product-region
                product_margin = np.random.uniform(0.15, 0.25)  # 15-25% margin
                
                data.append({
                    'Date': quarter,
                    'Year': quarter.year,
                    'Quarter': f"Q{quarter.quarter}",
                    'Product': product,
                    'Region': region,
                    'Revenue': product_revenue,
                    'Gross_Profit': product_revenue * product_margin,
                    'Operating_Expenses': product_revenue * np.random.uniform(0.10, 0.20),
                    'Net_Profit': product_revenue * product_margin - (product_revenue * np.random.uniform(0.10, 0.20)),
                    'Total_Assets': product_revenue * np.random.uniform(2.0, 3.0),
                    'Total_Equity': product_revenue * np.random.uniform(1.2, 1.8),
                    'Cash_Flow': product_revenue * np.random.uniform(0.15, 0.30),
                    'Employees': int(product_revenue / 50000),  # Revenue per employee
                    'Customer_Count': int(product_revenue / 1000),  # Revenue per customer
                    'Market_Share': np.random.uniform(0.05, 0.30),  # 5-30% market share
                })
    
    df = pd.DataFrame(data)
    
    # Add some calculated columns
    df['Profit_Margin'] = (df['Net_Profit'] / df['Revenue']) * 100
    df['ROA'] = (df['Net_Profit'] / df['Total_Assets']) * 100
    df['ROE'] = (df['Net_Profit'] / df['Total_Equity']) * 100
    df['Revenue_Per_Employee'] = df['Revenue'] / df['Employees']
    df['Customer_Acquisition_Cost'] = df['Operating_Expenses'] / df['Customer_Count']
    
    return df

def generate_sample_sales_data():
    """Generate sample sales data"""
    
    np.random.seed(42)
    
    # Generate 2 years of daily sales data
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = []
    salespeople = ['Alice Johnson', 'Bob Smith', 'Carol Brown', 'David Wilson', 'Eva Garcia']
    products = ['Widget A', 'Widget B', 'Widget C', 'Gadget X', 'Gadget Y']
    categories = ['Electronics', 'Software', 'Hardware', 'Services']
    
    for date in dates:
        # Simulate weekend effect
        weekend_factor = 0.3 if date.weekday() >= 5 else 1.0
        
        # Simulate seasonal trends
        month_factor = 1 + 0.2 * np.sin(2 * np.pi * date.month / 12)
        
        daily_transactions = int(np.random.poisson(10) * weekend_factor * month_factor)
        
        for _ in range(daily_transactions):
            salesperson = np.random.choice(salespeople)
            product = np.random.choice(products)
            category = np.random.choice(categories)
            
            # Product-specific pricing
            base_prices = {
                'Widget A': 250, 'Widget B': 180, 'Widget C': 320,
                'Gadget X': 450, 'Gadget Y': 600
            }
            
            unit_price = base_prices[product] * (1 + np.random.normal(0, 0.1))
            quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03])
            total_sale = unit_price * quantity
            
            # Commission and costs
            commission_rate = np.random.uniform(0.05, 0.15)
            cost_of_goods = unit_price * 0.6 * quantity  # 60% COGS
            
            data.append({
                'Date': date,
                'Salesperson': salesperson,
                'Product': product,
                'Category': category,
                'Quantity': quantity,
                'Unit_Price': unit_price,
                'Total_Sale': total_sale,
                'Commission': total_sale * commission_rate,
                'Cost_of_Goods': cost_of_goods,
                'Gross_Profit': total_sale - cost_of_goods,
                'Customer_ID': f"CUST_{np.random.randint(1000, 9999)}",
                'Lead_Source': np.random.choice(['Website', 'Referral', 'Cold Call', 'Trade Show', 'Social Media']),
                'Deal_Size': np.random.choice(['Small', 'Medium', 'Large'], p=[0.6, 0.3, 0.1])
            })
    
    df = pd.DataFrame(data)
    
    # Add calculated columns
    df['Profit_Margin'] = (df['Gross_Profit'] / df['Total_Sale']) * 100
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter
    df['Year'] = df['Date'].dt.year
    df['Weekday'] = df['Date'].dt.day_name()
    
    return df

def generate_sample_operational_data():
    """Generate sample operational/manufacturing data"""
    
    np.random.seed(42)
    
    # Generate 1 year of daily operational data
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = []
    facilities = ['Plant A', 'Plant B', 'Plant C', 'Warehouse D']
    departments = ['Production', 'Quality Control', 'Packaging', 'Shipping']
    
    for date in dates:
        for facility in facilities:
            for department in departments:
                # Simulate operational metrics
                efficiency = np.random.normal(0.85, 0.1)  # 85% efficiency ± 10%
                efficiency = max(0.5, min(1.0, efficiency))  # Clamp between 50-100%
                
                target_output = np.random.normal(1000, 200)  # Target units
                actual_output = target_output * efficiency
                
                # Costs and resources
                labor_hours = actual_output / 10  # 10 units per hour
                labor_cost = labor_hours * np.random.uniform(25, 35)  # $25-35/hour
                material_cost = actual_output * np.random.uniform(5, 15)  # $5-15 per unit
                
                # Quality metrics
                defect_rate = np.random.beta(2, 50) * 100  # Low defect rate (typically <5%)
                rework_hours = (actual_output * defect_rate / 100) * 0.5  # 30 min rework per defect
                
                # Energy and utilities
                energy_consumption = actual_output * np.random.uniform(2, 8)  # kWh per unit
                utility_cost = energy_consumption * 0.12  # $0.12 per kWh
                
                data.append({
                    'Date': date,
                    'Facility': facility,
                    'Department': department,
                    'Target_Output': target_output,
                    'Actual_Output': actual_output,
                    'Efficiency_Percent': efficiency * 100,
                    'Labor_Hours': labor_hours,
                    'Labor_Cost': labor_cost,
                    'Material_Cost': material_cost,
                    'Utility_Cost': utility_cost,
                    'Total_Cost': labor_cost + material_cost + utility_cost,
                    'Defect_Rate_Percent': defect_rate,
                    'Rework_Hours': rework_hours,
                    'Energy_Consumption_kWh': energy_consumption,
                    'Downtime_Hours': np.random.exponential(1),  # Exponential distribution for downtime
                    'Safety_Incidents': np.random.poisson(0.1),  # Low rate of safety incidents
                    'Employee_Count': np.random.randint(15, 50)
                })
    
    df = pd.DataFrame(data)
    
    # Add calculated columns
    df['Output_Variance'] = df['Actual_Output'] - df['Target_Output']
    df['Cost_Per_Unit'] = df['Total_Cost'] / df['Actual_Output']
    df['Productivity'] = df['Actual_Output'] / df['Labor_Hours']
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter
    df['Weekday'] = df['Date'].dt.day_name()
    
    return df

def save_sample_datasets():
    """Generate and save sample datasets for testing"""
    
    # Generate datasets
    financial_data = generate_sample_financial_data()
    sales_data = generate_sample_sales_data()
    operational_data = generate_sample_operational_data()
    
    # Save to CSV files
    financial_data.to_csv('sample_financial_data.csv', index=False)
    sales_data.to_csv('sample_sales_data.csv', index=False)
    operational_data.to_csv('sample_operational_data.csv', index=False)
    
    print("Sample datasets generated and saved:")
    print(f"- sample_financial_data.csv: {len(financial_data)} rows, {len(financial_data.columns)} columns")
    print(f"- sample_sales_data.csv: {len(sales_data)} rows, {len(sales_data.columns)} columns")
    print(f"- sample_operational_data.csv: {len(operational_data)} rows, {len(operational_data.columns)} columns")
    
    return financial_data, sales_data, operational_data

if __name__ == "__main__":
    save_sample_datasets()
