import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from config.settings import APP_CONFIG
from styles.custom_css import get_custom_css
from components.header import render_header
from components.sidebar import render_sidebar
from components.home_page import render_home_page
from components.kpi_cards import render_kpi_cards
from components.charts import (
    render_temporal_tab,
    render_products_tab,
    render_geography_tab,
    render_payments_tab
)
from components.insights_cards import render_insights_section
from analytics.kpis import calculate_kpis
from utils.data_processor import process_dataframe

# Configuração da página
st.set_page_config(**APP_CONFIG)

# CSS customizado
st.markdown(get_custom_css(), unsafe_allow_html=True)

def main():
    # Cabeçalho
    render_header()
    
    # Sidebar e carregamento de dados
    df, company_name = render_sidebar()
    
    # Se não há dados, mostra página inicial
    if df is None:
        render_home_page()
        return
    
    # Verificar se df está vazio
    if len(df) == 0:
        st.error("❌ O arquivo está vazio ou não foi possível processar os dados.")
        return
    
    # Processar dados
    try:
        df = process_dataframe(df)
    except Exception as e:
        st.error(f"❌ Erro ao processar dados: {e}")
        st.info("Verifique se o arquivo CSV está no formato correto.")
        with st.expander("🐛 Debug - Ver estrutura do dataframe"):
            st.write("Colunas encontradas:", df.columns.tolist())
            st.write("Primeiras linhas:", df.head())
        return
    
    if 'order_date' not in df.columns:
        st.error("❌ Coluna obrigatória 'order_date' não encontrada no dataset.")
        st.info("O CSV deve conter as colunas: order_id, customer_id, order_date, product_category, product_price, quantity, total_value")
        with st.expander("🐛 Debug - Colunas disponíveis"):
            st.write(df.columns.tolist())
        return
    
    # Informações do dashboard
    st.markdown(f"""
    <div style="margin-top:10px; margin-bottom:8px;">
        <h3 style="margin:0;">📈 Dashboard Gerencial - <span style="color:#1e3c72;">{company_name}</span></h3>
        <div class="small-muted">
            Período de dados: {df['order_date'].min().strftime('%d/%m/%Y')} a {df['order_date'].max().strftime('%d/%m/%Y')} 
            | Registros: {len(df):,}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtros avançados
    with st.expander("🔍 Filtros Avançados", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            min_date = df['order_date'].min().date()
            max_date = df['order_date'].max().date()
            date_range = st.date_input(
                "Período:",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                format="DD/MM/YYYY"  # ← Formato brasileiro
            )
        with col2:
            states = sorted(df['customer_state'].dropna().unique().tolist()) if 'customer_state' in df.columns else []
            selected_states = st.multiselect("Estados:", options=states, default=states)

    # Validar seleção de datas
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    elif isinstance(date_range, tuple) and len(date_range) == 1:
        # Usuário selecionou apenas uma data
        st.warning("⚠️ Por favor, selecione a data final do período.")
        return
    else:
        # Fallback: usar data única para ambas
        start_date = end_date = date_range

    # Aplicar filtros
    df_filtered = df[
        (df['order_date'] >= pd.to_datetime(start_date)) &
        (df['order_date'] <= pd.to_datetime(end_date))
    ]
    
    if 'customer_state' in df_filtered.columns and selected_states:
        df_filtered = df_filtered[df_filtered['customer_state'].isin(selected_states)]
    
    # Verificar se ainda há dados após filtros
    if len(df_filtered) == 0:
        st.warning("⚠️ Nenhum dado encontrado com os filtros aplicados. Ajuste os filtros.")
        return
    
    # Calcular KPIs
    try:
        kpis = calculate_kpis(df_filtered)
        
        # Verificar se KPIs foi calculado corretamente
        if kpis is None:
            st.error("❌ Erro ao calcular KPIs.")
            st.info("💡 Verifique o console do terminal para mais detalhes do erro.")
            return
            
    except Exception as e:
        st.error(f"❌ Erro ao calcular KPIs: {e}")
        return
    
    # Renderizar KPI cards
    render_kpi_cards(kpis)
    
    st.markdown("---")
    
    # Abas de análise
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Evolução Temporal",
        "🏆 Produtos",
        "🗺️ Geografia",
        "💳 Pagamentos"
    ])
    
    with tab1:
        try:
            render_temporal_tab(kpis, df_filtered)
        except Exception as e:
            st.error(f"Erro ao renderizar aba temporal: {e}")
    
    with tab2:
        try:
            render_products_tab(df_filtered)
        except Exception as e:
            st.error(f"Erro ao renderizar aba de produtos: {e}")
    
    with tab3:
        try:
            render_geography_tab(df_filtered)
        except Exception as e:
            st.error(f"Erro ao renderizar aba de geografia: {e}")
    
    with tab4:
        try:
            render_payments_tab(df_filtered)
        except Exception as e:
            st.error(f"Erro ao renderizar aba de pagamentos: {e}")
    
    # Insights
  
    try:
        render_insights_section(df_filtered, company_name, kpis)  # ← ADICIONAR kpis
    except Exception as e:
        st.error(f"Erro ao renderizar insights: {e}")

if __name__ == "__main__":
    main()