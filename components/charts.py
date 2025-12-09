# components/charts.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_temporal_tab(kpis: dict, df_filtered: pd.DataFrame):
    """Renderiza a aba de evolução temporal"""
    st.subheader("Evolução de Receita e Pedidos (Mensal)")
    
    monthly = kpis.get('monthly', pd.DataFrame())
    
    if len(monthly) == 0:
        st.info("Sem dados suficientes para mostrar séries temporais.")
        return
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=monthly['period'], y=monthly['orders'], name='Pedidos', marker_color='#1e3c72'),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=monthly['period'],
            y=monthly['revenue'],
            name='Receita (R$)',
            mode='lines+markers',
            line=dict(color='#ff7f0e', width=3)
        ),
        secondary_y=True
    )
    fig.update_layout(hovermode='x unified', height=420, legend=dict(orientation='h'))
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("#### Pedidos por Dia")
    
    df_to_use = kpis.get('df', df_filtered)
    
    if 'order_date' not in df_to_use.columns:
        st.warning("Coluna 'order_date' não encontrada para gráfico diário.")
        return
    
    if 'order_id' not in df_to_use.columns:
        st.warning("Coluna 'order_id' não encontrada para gráfico diário.")
        return
    
    df_days = df_to_use.groupby(df_to_use['order_date'].dt.date).agg(
        revenue=('total_value','sum'),
        orders=('order_id','nunique')
    ).reset_index()
    
    if len(df_days) == 0:
        st.info("Sem dados para mostrar por dia.")
    else:
        fig2 = px.line(
            df_days,
            x='order_date',
            y='revenue',
            labels={'order_date':'Data','revenue':'Receita (R$)'}
        )
        fig2.update_traces(line_color='#0b6bf7', line_width=2)
        st.plotly_chart(fig2, use_container_width=True)

def render_products_tab(df_filtered: pd.DataFrame):
    """Renderiza a aba de produtos"""
    st.subheader("🏆 Performance por Categoria/Produto")
    
    if 'product_category' not in df_filtered.columns:
        st.info("Coluna 'product_category' não encontrada.")
        return
    
    if 'order_id' not in df_filtered.columns or 'total_value' not in df_filtered.columns:
        st.warning("Colunas necessárias não encontradas.")
        return
    
    prod = df_filtered.groupby('product_category').agg(
        revenue=('total_value','sum'),
        orders=('order_id','nunique'),
        qty=('quantity','sum')
    ).reset_index().sort_values('revenue', ascending=False)
    
    if len(prod) == 0:
        st.info("Sem dados de produtos para mostrar.")
        return
    
    figp = px.bar(
        prod.head(8),
        x='revenue',
        y='product_category',
        orientation='h',
        labels={'revenue':'Receita','product_category':'Categoria'},
        color='revenue',
        color_continuous_scale='Blues'
    )
    figp.update_layout(height=420, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(figp, use_container_width=True)
    
    st.markdown("#### Tabela de categorias")
    prod_display = prod.copy()
    prod_display['revenue'] = prod_display['revenue'].map(lambda x: f"R$ {x:,.2f}")
    st.dataframe(prod_display.reset_index(drop=True), use_container_width=True)

def render_geography_tab(df_filtered: pd.DataFrame):
    """Renderiza a aba de geografia"""
    st.subheader("🗺️ Análise Geográfica")
    
    if 'customer_state' not in df_filtered.columns:
        st.info("Coluna 'customer_state' não encontrada.")
        return
    
    if 'order_id' not in df_filtered.columns or 'total_value' not in df_filtered.columns:
        st.warning("Colunas necessárias não encontradas.")
        return
    
    geo = df_filtered.groupby('customer_state').agg(
        revenue=('total_value','sum'),
        orders=('order_id','nunique')
    ).reset_index().sort_values('revenue', ascending=False)
    
    if len(geo) == 0:
        st.info("Sem dados geográficos para mostrar.")
        return
    
    figg = px.bar(
        geo.head(10),
        x='customer_state',
        y='revenue',
        labels={'customer_state':'Estado','revenue':'Receita (R$)'},
        color='revenue',
        color_continuous_scale='Purples'
    )
    figg.update_layout(height=420)
    st.plotly_chart(figg, use_container_width=True)

def render_payments_tab(df_filtered: pd.DataFrame):
    """Renderiza a aba de pagamentos"""
    st.subheader("💳 Métodos de Pagamento")
    
    if 'payment_method' not in df_filtered.columns:
        st.info("Coluna 'payment_method' não encontrada.")
        return
    
    if 'order_id' not in df_filtered.columns or 'total_value' not in df_filtered.columns:
        st.warning("Colunas necessárias não encontradas.")
        return
    
    pay = df_filtered.groupby('payment_method').agg(
        orders=('order_id','nunique'),
        revenue=('total_value','sum')
    ).reset_index().sort_values('orders', ascending=False)
    
    if len(pay) == 0:
        st.info("Sem dados de pagamento para mostrar.")
        return
    
    figpay = px.pie(pay, names='payment_method', values='orders', hole=0.45)
    figpay.update_traces(
        textposition='outside',
        textinfo='percent+label',
        pull=[0.05 if i==0 else 0 for i in range(len(pay))]
    )
    st.plotly_chart(figpay, use_container_width=True)
    
    st.markdown("#### Receita por método")
    figpay2 = px.bar(
        pay,
        x='payment_method',
        y='revenue',
        labels={'revenue':'Receita (R$)','payment_method':'Método'},
        color='revenue',
        color_continuous_scale='Greens'
    )
    figpay2.update_layout(height=380, xaxis_tickangle=-45)
    st.plotly_chart(figpay2, use_container_width=True)