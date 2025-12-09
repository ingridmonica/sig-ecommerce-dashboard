import pandas as pd

def generate_insights(kpis: dict, df: pd.DataFrame):
    """Gera lista de insights com regras simples"""
    insights = []
    monthly = kpis.get('monthly', pd.DataFrame())
    
    if len(monthly) >= 2:
        last = monthly.iloc[-1]['revenue']
        prev = monthly.iloc[-2]['revenue']
        if prev != 0:
            growth = (last - prev) / prev * 100
            if growth > 5:
                insights.append({
                    'type': 'success',
                    'title': 'Crescimento',
                    'text': f'Crescimento de {growth:.1f}% na receita mês-a-mês.'
                })
            elif growth < -5:
                insights.append({
                    'type': 'danger',
                    'title': 'Queda',
                    'text': f'Queda de {abs(growth):.1f}% na receita mês-a-mês.'
                })
    
    if 'customer_state' in df.columns and 'total_value' in df.columns:
        state_rev = df.groupby('customer_state')['total_value'].sum().sort_values(ascending=False)
        if len(state_rev) > 0:
            top_state = state_rev.index[0]
            share = (state_rev.iloc[0] / state_rev.sum()) * 100 if state_rev.sum() > 0 else 0
            if share > 35:
                insights.append({
                    'type': 'warning',
                    'title': 'Concentração',
                    'text': f'{top_state} representa {share:.1f}% da receita. Alta dependência geográfica.'
                })
    
    if 'product_category' in df.columns:
        cat_rev = df.groupby('product_category')['total_value'].sum().sort_values(ascending=False)
        if len(cat_rev) > 0:
            top_cat = cat_rev.index[0]
            share = (cat_rev.iloc[0] / cat_rev.sum()) * 100 if cat_rev.sum() > 0 else 0
            insights.append({
                'type': 'info',
                'title': 'Categoria Líder',
                'text': f'"{top_cat}" gera {share:.1f}% da receita.'
            })
    
    if kpis.get('avg_ticket', 0) < 200:
        insights.append({
            'type': 'danger',
            'title': 'Ticket Médio Baixo',
            'text': f'Ticket médio R$ {kpis.get("avg_ticket",0):.2f}. Considere upsell.'
        })
    
    return insights