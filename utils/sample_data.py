import pandas as pd
import numpy as np

def create_sample_data(n_records=1000):
    """Gera dados de exemplo para o dashboard"""
    np.random.seed(42)
    
    categories = ['Eletrônicos', 'Moda', 'Casa e Decoração', 'Livros', 'Esportes', 'Beleza']
    states = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE']
    cities_by_state = {
        'SP': ['São Paulo', 'Campinas', 'Santos', 'Ribeirão Preto'],
        'RJ': ['Rio de Janeiro', 'Niterói'],
        'MG': ['Belo Horizonte', 'Uberlândia'],
        'RS': ['Porto Alegre', 'Caxias do Sul'],
        'PR': ['Curitiba', 'Londrina'],
        'SC': ['Florianópolis', 'Joinville'],
        'BA': ['Salvador', 'Feira de Santana'],
        'PE': ['Recife', 'Olinda'],
    }
    payment_methods = ['Cartão de Crédito', 'PIX', 'Boleto', 'Cartão de Débito']
    
    state_probs = np.array([0.35, 0.20, 0.12, 0.08, 0.06, 0.05, 0.08, 0.06])
    state_probs = state_probs / state_probs.sum()
    
    dates = pd.date_range(start='2024-01-01', end='2024-10-31').to_pydatetime().tolist()
    rows = []
    
    for i in range(n_records):
        state = np.random.choice(states, p=state_probs)
        city = np.random.choice(cities_by_state[state])
        cat = np.random.choice(categories)
        
        price_ranges = {
            'Eletrônicos': (200, 3500),
            'Moda': (30, 700),
            'Casa e Decoração': (60, 1500),
            'Livros': (15, 120),
            'Esportes': (40, 900),
            'Beleza': (20, 400)
        }
        price = round(np.random.uniform(*price_ranges[cat]), 2)
        
        qty = int(np.random.randint(1, 5))
        total = round(price * qty, 2)
        datec = pd.Timestamp(np.random.choice(dates)).strftime('%Y-%m-%d')
        
        rows.append({
            'order_id': f'ORD_{i+1:06d}',
            'customer_id': f'CUST_{np.random.randint(1,2000):06d}',
            'order_date': datec,
            'product_category': cat,
            'product_price': price,
            'quantity': qty,
            'total_value': total,
            'customer_state': state,
            'customer_city': city,
            'payment_method': np.random.choice(payment_methods, p=[0.45,0.3,0.15,0.10])
        })
    
    df = pd.DataFrame(rows)
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df