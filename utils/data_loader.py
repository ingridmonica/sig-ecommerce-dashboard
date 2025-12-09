import pandas as pd
from io import StringIO
from utils.data_processor import normalize_columns

def load_csv_robust(uploaded_file):
    """Lê CSV tentando encodings e separadores comuns"""
    try:
        df = pd.read_csv(uploaded_file, sep=None, engine="python", encoding='utf-8-sig')
    except Exception:
        uploaded_file.seek(0)
        df = None
        
        for enc in ['utf-8-sig', 'utf-8', 'latin1', 'iso-8859-1', 'cp1252']:
            for sep in [',', ';', '\t']:
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding=enc, sep=sep)
                    break
                except Exception:
                    continue
            if df is not None:
                break
        
        if df is None:
            uploaded_file.seek(0)
            content = uploaded_file.read()
            if isinstance(content, bytes):
                try:
                    content = content.decode('utf-8-sig')
                except:
                    try:
                        content = content.decode('utf-8')
                    except:
                        content = content.decode('latin1', errors='ignore')
            df = pd.read_csv(StringIO(content), sep=None, engine="python")
    
    df = normalize_columns(df)
    
    return df