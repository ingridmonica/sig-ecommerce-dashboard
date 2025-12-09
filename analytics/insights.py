import pandas as pd
import numpy as np

def generate_smart_insights(kpis: dict, df: pd.DataFrame):
    """
    Gera insights inteligentes baseados em análise de dados
    Retorna lista ordenada por prioridade (alta -> baixa)
    """
    insights = []
    monthly = kpis.get('monthly', pd.DataFrame())
    
    #  1. ANÁLISE DE CRESCIMENTO (PRIORIDADE ALTA)
    if len(monthly) >= 2:
        last_revenue = monthly.iloc[-1]['revenue']
        prev_revenue = monthly.iloc[-2]['revenue']
        
        if prev_revenue > 0:
            growth = ((last_revenue - prev_revenue) / prev_revenue) * 100
            
            if growth > 15:
                insights.append({
                    'priority': 1,
                    'type': 'success',
                    'icon': '🚀',
                    'title': 'Crescimento Acelerado',
                    'text': f'Receita cresceu {growth:.1f}% no último mês! Tendência muito positiva.',
                    'action': 'Manter estratégia atual e considerar expansão.'
                })
            elif growth > 5:
                insights.append({
                    'priority': 2,
                    'type': 'success',
                    'icon': '📈',
                    'title': 'Crescimento Saudável',
                    'text': f'Crescimento de {growth:.1f}% na receita mês-a-mês.',
                    'action': 'Continuar monitorando e otimizando processos.'
                })
            elif growth < -10:
                insights.append({
                    'priority': 1,
                    'type': 'danger',
                    'icon': '⚠️',
                    'title': 'ALERTA: Queda Significativa',
                    'text': f'Receita caiu {abs(growth):.1f}% no último mês.',
                    'action': 'URGENTE: Investigar causas e implementar ações corretivas.'
                })
            elif growth < -5:
                insights.append({
                    'priority': 2,
                    'type': 'warning',
                    'icon': '📉',
                    'title': 'Queda na Receita',
                    'text': f'Redução de {abs(growth):.1f}% na receita.',
                    'action': 'Analisar categorias e estados com queda.'
                })
    
    #  2. ANÁLISE DE TICKET MÉDIO 
    avg_ticket = kpis.get('avg_ticket', 0)
    
    if avg_ticket < 150:
        insights.append({
            'priority': 2,
            'type': 'warning',
            'icon': '💡',
            'title': 'Oportunidade: Ticket Médio Baixo',
            'text': f'Ticket médio de R$ {avg_ticket:.2f} está abaixo do ideal.',
            'action': 'Implementar estratégias de upsell e cross-sell.'
        })
    elif avg_ticket > 500:
        insights.append({
            'priority': 3,
            'type': 'success',
            'icon': '💰',
            'title': 'Excelente Ticket Médio',
            'text': f'Ticket médio alto: R$ {avg_ticket:.2f}.',
            'action': 'Manter foco em produtos premium.'
        })
    
    #  3. CONCENTRAÇÃO GEOGRÁFICA 
    if 'customer_state' in df.columns:
        state_revenue = df.groupby('customer_state')['total_value'].sum().sort_values(ascending=False)
        
        if len(state_revenue) > 0:
            top_state = state_revenue.index[0]
            top_share = (state_revenue.iloc[0] / state_revenue.sum()) * 100
            
            if top_share > 50:
                insights.append({
                    'priority': 1,
                    'type': 'danger',
                    'icon': '🎯',
                    'title': 'RISCO: Alta Concentração Geográfica',
                    'text': f'{top_state} representa {top_share:.1f}% da receita total.',
                    'action': 'URGENTE: Diversificar geograficamente para reduzir risco.'
                })
            elif top_share > 35:
                insights.append({
                    'priority': 2,
                    'type': 'warning',
                    'icon': '🗺️',
                    'title': 'Concentração Geográfica Moderada',
                    'text': f'{top_state} representa {top_share:.1f}% das vendas.',
                    'action': 'Considerar expansão para outros estados.'
                })
    
    #  4. ANÁLISE DE CATEGORIAS 
    if 'product_category' in df.columns:
        cat_revenue = df.groupby('product_category')['total_value'].sum().sort_values(ascending=False)
        
        if len(cat_revenue) > 0:
            top_cat = cat_revenue.index[0]
            top_cat_share = (cat_revenue.iloc[0] / cat_revenue.sum()) * 100
            
            if top_cat_share > 40:
                insights.append({
                    'priority': 2,
                    'type': 'warning',
                    'icon': '📊',
                    'title': 'Dependência de Categoria',
                    'text': f'"{top_cat}" representa {top_cat_share:.1f}% da receita.',
                    'action': 'Diversificar portfólio de produtos.'
                })
            
            # Categoria em crescimento
            if len(cat_revenue) >= 2:
                second_cat = cat_revenue.index[1]
                second_share = (cat_revenue.iloc[1] / cat_revenue.sum()) * 100
                
                if second_share > 20:
                    insights.append({
                        'priority': 3,
                        'type': 'info',
                        'icon': '✨',
                        'title': 'Oportunidade: Categoria Emergente',
                        'text': f'"{second_cat}" já representa {second_share:.1f}% da receita.',
                        'action': 'Avaliar aumento de investimento nesta categoria.'
                    })
    
    #  5. VOLUME DE CLIENTES 
    total_customers = kpis.get('total_customers', 0)
    total_orders = kpis.get('total_orders', 0)
    
    if total_customers > 0 and total_orders > 0:
        orders_per_customer = total_orders / total_customers
        
        if orders_per_customer < 1.2:
            insights.append({
                'priority': 2,
                'type': 'info',
                'icon': '🔄',
                'title': 'Baixa Taxa de Recompra',
                'text': f'Clientes fazem em média {orders_per_customer:.1f} pedidos.',
                'action': 'Implementar programa de fidelidade e remarketing.'
            })
        elif orders_per_customer > 2:
            insights.append({
                'priority': 3,
                'type': 'success',
                'icon': '🎉',
                'title': 'Excelente Taxa de Recompra',
                'text': f'Clientes fazem em média {orders_per_customer:.1f} pedidos.',
                'action': 'Fortalecer relacionamento com clientes fiéis.'
            })
    
    #  6. SAÚDE GERAL DO NEGÓCIO 
    total_revenue = kpis.get('total_revenue', 0)
    
    if total_revenue > 100000:
        insights.append({
            'priority': 3,
            'type': 'success',
            'icon': '💎',
            'title': 'Negócio Saudável',
            'text': f'Receita total de R$ {total_revenue:,.2f} demonstra solidez.',
            'action': 'Foco em escalabilidade e eficiência operacional.'
        })
    elif total_revenue < 10000:
        insights.append({
            'priority': 2,
            'type': 'info',
            'icon': '🌱',
            'title': 'Fase Inicial',
            'text': f'Receita de R$ {total_revenue:,.2f} indica negócio em desenvolvimento.',
            'action': 'Foco em aquisição de clientes e validação de produto.'
        })
    
    # Ordenar por prioridade (1 = alta, 3 = baixa)
    insights.sort(key=lambda x: x['priority'])
    
    # Retornar apenas os 5 mais relevantes
    return insights[:5]