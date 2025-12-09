import pandas as pd
import numpy as np

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove BOM, espaços e padroniza nomes para minúsculo"""
    df = df.copy()
    df.columns = (
        df.columns
        .astype(str)
        .str.replace("\ufeff", "", regex=False)  # Remove BOM
        .str.replace("\u200b", "", regex=False)  # Remove zero-width space
        .str.strip()
        .str.lower()
    )
    return df

def normalize_number_str(s):
    """Normaliza strings numéricas no formato BR/EN para float"""
    if pd.isna(s):
        return np.nan
    s = str(s).strip()
    if s == "":
        return np.nan
    if '.' in s and ',' in s:
        s = s.replace('.', '').replace(',', '.')
    elif ',' in s and '.' not in s:
        s = s.replace(',', '.')
    try:
        return float(s)
    except:
        return np.nan

def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Processa e normaliza todas as colunas do dataframe"""
    df = normalize_columns(df)
    
    if 'total_value' in df.columns:
        df['total_value'] = df['total_value'].apply(
            lambda x: normalize_number_str(x) if not pd.api.types.is_numeric_dtype(type(x)) else x
        )
        df['total_value'] = pd.to_numeric(df['total_value'], errors='coerce').fillna(0.0)
    else:
        df['total_value'] = 0.0
    
    if 'product_price' in df.columns:
        df['product_price'] = df['product_price'].apply(
            lambda x: normalize_number_str(x) if not pd.api.types.is_numeric_dtype(type(x)) else x
        )
        df['product_price'] = pd.to_numeric(df['product_price'], errors='coerce').fillna(0.0)
    
    if 'quantity' in df.columns:
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).astype(int)
    else:
        df['quantity'] = 0
    
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df = df[~df['order_date'].isna()].copy()
    
    return df