# analytics/kpis.py

import pandas as pd
import numpy as np

def calculate_kpis(df: pd.DataFrame):
    """Calcula KPIs principais a partir do dataframe filtrado"""
    try:
        df = df.copy()
        
        if 'total_value' not in df.columns:
            df['total_value'] = 0.0
        
        if 'order_id' not in df.columns:
            df['order_id'] = [f'ORD_{i:06d}' for i in range(1, len(df) + 1)]
        
        if 'customer_id' not in df.columns:
            df['customer_id'] = [f'CUST_{i:06d}' for i in range(1, len(df) + 1)]
        
        if 'quantity' not in df.columns:
            df['quantity'] = 1
        
        total_orders = df['order_id'].nunique()
        total_revenue = float(df['total_value'].fillna(0).sum())
        total_customers = df['customer_id'].nunique()
        total_items = int(df['quantity'].sum())
        
        if total_orders > 0:
            order_totals = df.groupby('order_id')['total_value'].sum()
            avg_ticket = float(order_totals.mean())
        else:
            avg_ticket = 0.0
        
        monthly = pd.DataFrame(columns=['period', 'orders', 'revenue', 'customers', 'items'])
        
        if 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
            df_valid_dates = df[~df['order_date'].isna()].copy()
            
            if len(df_valid_dates) > 0:
                df_valid_dates['period'] = df_valid_dates['order_date'].dt.to_period('M').astype(str)
                
                monthly = df_valid_dates.groupby('period').agg(
                    orders=('order_id', 'nunique'),
                    revenue=('total_value', 'sum'),
                    customers=('customer_id', 'nunique'),
                    items=('quantity', 'sum')
                ).reset_index()
                
                monthly = monthly.sort_values('period')
                
                if len(monthly) >= 2:
                    monthly['revenue_growth'] = monthly['revenue'].pct_change() * 100
                    monthly['orders_growth'] = monthly['orders'].pct_change() * 100
                else:
                    monthly['revenue_growth'] = 0.0
                    monthly['orders_growth'] = 0.0
        
        return {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_customers': total_customers,
            'total_items': total_items,
            'avg_ticket': avg_ticket,
            'monthly': monthly,
            'df': df
        }
    
    except Exception as e:
        print(f"Erro em calculate_kpis: {e}")
        import traceback
        traceback.print_exc()
        return None