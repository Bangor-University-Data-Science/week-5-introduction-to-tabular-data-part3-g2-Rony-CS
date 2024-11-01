import pandas as pd

def import_data(filename: str) -> pd.DataFrame:
    if filename.endswith('.csv'):
        df = pd.read_csv(filename)
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(filename)
    else:
        raise ValueError("File format not supported. Please provide a .csv or .xlsx file.")
    return df

def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=['CustomerID'])
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    return df

def loyalty_customers(df: pd.DataFrame, min_purchases: int) -> pd.DataFrame:
    customer_counts = df.groupby('CustomerID').size().reset_index(name='PurchaseCount')
    loyal_customers = customer_counts[customer_counts['PurchaseCount'] >= min_purchases]
    return loyal_customers

def quarterly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    df['Quarter'] = df['InvoiceDate'].dt.to_period('Q')
    quarterly_revenue = df.groupby('Quarter')['Revenue'].sum().reset_index(name='TotalRevenue')
    return quarterly_revenue

def high_demand_products(df: pd.DataFrame, top_n: int) -> pd.DataFrame:
    product_demand = df.groupby('StockCode')['Quantity'].sum().reset_index(name='TotalQuantitySold')
    high_demand = product_demand.nlargest(top_n, 'TotalQuantitySold')
    return high_demand

def purchase_patterns(df: pd.DataFrame) -> pd.DataFrame:
    purchase_summary = df.groupby('StockCode').agg(
        avg_quantity=('Quantity', 'mean'),
        avg_unit_price=('UnitPrice', 'mean')
    ).reset_index()
    purchase_summary = purchase_summary.rename(columns={'StockCode': 'Product'})
    return purchase_summary

def answer_conceptual_questions() -> dict:
    answers = {
        "Q1": ["A", "D"],
        "Q2": ["B"],
        "Q3": ["C"],
        "Q4": ["A", "B"],
        "Q5": ["A"]
    }
    return answers


if __name__ == "__main__":
    filename = 'Online Retail.xlsx'  
    df = import_data(filename)
    
    print("Original Data:")
    print(df.head())
    
    filtered_df = filter_data(df)
    print("\nFiltered Data:")
    print(filtered_df.head())
    
    loyal_customers_df = loyalty_customers(filtered_df, min_purchases=5)
    print("\nLoyal Customers (at least 5 purchases):")
    print(loyal_customers_df)
    
    quarterly_revenue_df = quarterly_revenue(filtered_df)
    print("\nQuarterly Revenue:")
    print(quarterly_revenue_df)
    
    top_products_df = high_demand_products(filtered_df, top_n=5)
    print("\nTop 5 High Demand Products:")
    print(top_products_df)
    
    purchase_patterns_df = purchase_patterns(filtered_df)
    print("\nPurchase Patterns (Average Quantity and Unit Price):")
    print(purchase_patterns_df)
    
    conceptual_answers = answer_conceptual_questions()
    print("\nConceptual Questions Answers:")
    print(conceptual_answers)
